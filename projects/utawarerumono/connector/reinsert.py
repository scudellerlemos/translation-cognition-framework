#!/usr/bin/env python3
"""
reinsert.py — conector hex_binary para Utawarerumono (versão ENG/Steam)

Reinseridor DETERMINÍSTICO: approved_translations.csv -> output/ScriptEvent.sdat + patch IPS

Contrato (framework/connectors/hex_binary.md):
  entrada : approved_translations.csv (id, text_target) + dialogs.csv (byte_budget) + .sdat original (read-only)
  saída   : output/ScriptEvent.sdat (mesmo nome/extensão do input) + output/<nome>.ips + reinsertion_report.md

Formato do .sdat (engenharia reversa — ver connector/table_schema.md):
- Bloco de texto: strings UTF-8 null-terminated e contíguas.
- Bytecode de script com o opcode de texto `50 00` (LE 0x0050) seguido de um PONTEIRO absoluto
  uint32 LE para a string ("head"). Não há tabela central de ponteiros.
- "Continuações": strings sem ponteiro próprio, lidas em sequência logo após o head. Um "run" =
  head + suas continuações, até o próximo head.

Estratégia de encaixe (cascata determinística, sem LLM):
- CHARSET: a fonte do jogo NÃO tem diacríticos (acento -> '@'). Decisão: TRANSLITERAR na gravação
  (á->a, ç->c, ...). A tradução canônica (approved_translations.csv) permanece com acento; só os
  BYTES gravados no jogo são dobrados para ASCII.
- T1 in_place : len(transliterado) <= byte_budget -> grava no slot original.
- REPOINT     : se algum membro de um run estoura, RELOCA o run inteiro (head + continuações) para o
                fim do arquivo e reescreve o(s) ponteiro(s) `50 00`+ptr do head para o novo endereço.
                Continuações viajam junto -> a leitura sequencial é preservada.
- T4 resíduo  : caso irredutível (sem ponteiro e sem como caber) -> issue para o Passo 06c.

Regras de governança:
- NUNCA escreve no binário-fonte. Lê o original (read-only) e grava em output/ no projeto.
- 100% determinístico. A IA não escreve a tradução à mão — este script aplica o arquivo APROVADO.
- Gate de round-trip: reinserir o text_source (idêntico) reproduz o original byte-a-byte.

Caminho do binário (NUNCA hardcoded): CLI > connector.source_binary do project.json.
"""
import csv
import json
import struct
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # raiz do projeto
ART = ROOT / "artifacts"
REPORT = ART / "reinsertion_report.md"

TEXT_OPCODE = b"\x50\x00"      # opcode de exibição de texto, precede o ponteiro absoluto
MAX_RUN = 32                   # trava de segurança ao caminhar um run


# ----------------------------------------------------------------------------- governança de caminho
def resolve_source() -> Path:
    """Caminho do binário-fonte: CLI > connector.source_binary do project.json. Sem hardcode."""
    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
    else:
        cfg = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
        sb = cfg.get("connector", {}).get("source_binary", "")
        if not sb:
            sys.exit("ERRO: forneça o binário-fonte via argumento "
                     "(`python reinsert.py <caminho>`) ou preencha "
                     "`connector.source_binary` no project.json.")
        p = Path(sb)
        if not p.is_absolute():
            p = ROOT / p
    if not p.is_file():
        sys.exit(f"ERRO: binário não encontrado: {p}\n"
                 "Aponte `connector.source_binary` (no project.json) ou o argumento de CLI "
                 "para o arquivo do jogo a traduzir.")
    return p


# ----------------------------------------------------------------------------- transliteração (charset)
# Acentos pt-BR -> ASCII. Determinístico, sem LLM. Tokens {..} são ASCII e não são afetados.
def transliterate(s: str) -> str:
    """Dobra diacríticos para ASCII (NFKD + descarte de combining marks). Mantém tudo o mais."""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


# ----------------------------------------------------------------------------- leitura do binário
def read_cstr(buf: bytes, off: int) -> bytes:
    """String null-terminated a partir de off (sem o \\0)."""
    end = buf.find(b"\x00", off)
    if end == -1:
        end = len(buf)
    return buf[off:end]


def find_pointers(data: bytes, off: int):
    """Localizações dos ponteiros REAIS para 'off': bytes `50 00` + uint32(off) LE.
    O prefixo do opcode filtra falsos-positivos (4 bytes aleatórios que casam o valor)."""
    needle = TEXT_OPCODE + struct.pack("<I", off)
    locs, s = [], 0
    while True:
        i = data.find(needle, s)
        if i == -1:
            break
        locs.append(i + len(TEXT_OPCODE))   # posição do ponteiro (após o opcode)
        s = i + 1
    return locs


def is_head(data: bytes, off: int) -> bool:
    return len(find_pointers(data, off)) >= 1


def read_run(data: bytes, head_off: int):
    """Run = head + continuações (strings com 0 ponteiros) até o próximo head.
    Lê direto do binário (robusto mesmo para continuações fora das 20 da POC)."""
    members = [head_off]
    nxt = head_off + len(read_cstr(data, head_off)) + 1
    while len(members) < MAX_RUN and nxt < len(data):
        if data[nxt] == 0x00:           # padding/fim de bloco
            break
        if is_head(data, nxt):          # próximo head -> fim do run
            break
        members.append(nxt)
        nxt += len(read_cstr(data, nxt)) + 1
    return members


# ----------------------------------------------------------------------------- carga de artefatos
def load_budgets():
    """offset(hex str) -> (text_source, byte_budget). Preserva ordem do dialogs.csv."""
    rows = list(csv.DictReader((ART / "dialogs.csv").open(encoding="utf-8")))
    return [(r["offset"], r["text_source"], int(r["byte_budget"])) for r in rows]


def load_approved():
    return {r["offset"]: r["text_target"]
            for r in csv.DictReader((ART / "approved_translations.csv").open(encoding="utf-8"))}


# ----------------------------------------------------------------------------- núcleo do encaixe
def final_text_bytes(off_hex: str, source: str, approved: dict) -> bytes:
    """Bytes a gravar: transliteração da tradução aprovada (ou do source se não houver aprovação)."""
    text = approved.get(off_hex, source)
    return transliterate(text).encode("utf-8")


def build_output(original: bytes, budgets, approved):
    """Aplica in_place + repoint. Retorna (buf, repoints, report_rows).
    repoints: lista de (head_hex, new_off, [ptr_locs]). report_rows: (off,tier,nbytes,budget,text)."""
    buf = bytearray(original)
    sorted_items = budgets  # já em ordem de offset
    off_to_idx = {o: i for i, (o, _, _) in enumerate(sorted_items)}

    # 1) classificar cada string conhecida e achar overflows
    encoded = {}
    overflow = []
    for off_hex, source, budget in sorted_items:
        enc = final_text_bytes(off_hex, source, approved)
        encoded[off_hex] = (enc, budget)
        if len(enc) > budget:
            overflow.append(off_hex)

    # 2) para cada overflow, achar o HEAD do seu run e ler o run completo do binário
    relocated_runs = {}   # head_off(int) -> [member_off(int)]
    member_to_head = {}   # qualquer membro(int) -> head_off(int)
    for off_hex in overflow:
        off = int(off_hex, 16)
        if is_head(original, off):
            head = off
        else:
            # continuação: head = maior offset conhecido < off que seja head, sem head no meio
            head = None
            idx = off_to_idx[off_hex]
            for j in range(idx - 1, -1, -1):
                cand = int(sorted_items[j][0], 16)
                if is_head(original, cand):
                    head = cand
                    break
            if head is None:
                # sem head identificável -> não dá para repointar: T4 resíduo
                continue
        if head not in relocated_runs:
            run = read_run(original, head)
            relocated_runs[head] = run
            for m in run:
                member_to_head[m] = head

    relocated_offsets = set(member_to_head.keys())

    # 3) PASS in_place — grava as aprovadas que cabem e NÃO estão em run relocado
    report = []
    for off_hex, source, budget in sorted_items:
        off = int(off_hex, 16)
        enc, _ = encoded[off_hex]
        if off in relocated_offsets:
            continue  # será gravada na relocação
        if len(enc) <= budget:
            buf[off:off + len(enc)] = enc
            for k in range(off + len(enc), off + budget + 1):
                buf[k] = 0x00
            report.append((off_hex, "T1_in_place", len(enc), budget, enc.decode("utf-8", "replace")))
        else:
            # overflow sem run relocável (ex.: continuação sem head conhecido) -> resíduo
            report.append((off_hex, "T4_residuo", len(enc), budget, enc.decode("utf-8", "replace")))

    # 4) PASS relocação — anexa cada run no fim do arquivo e repointa o head
    repoints = []
    for head in sorted(relocated_runs):
        run = relocated_runs[head]
        new_head_off = len(buf)
        # grava membros do run (transliterados) contíguos e null-terminated
        for m in run:
            m_hex = f"0x{m:x}"
            if m_hex in encoded:
                enc = encoded[m_hex][0]
            else:
                # continuação fora das 20 -> mantém original (transliterado, no-op se ASCII)
                enc = transliterate(read_cstr(original, m).decode("utf-8", "replace")).encode("utf-8")
            buf += enc + b"\x00"
        # reescreve todos os ponteiros do head para o novo endereço
        ptr_locs = find_pointers(original, head)
        for loc in ptr_locs:
            buf[loc:loc + 4] = struct.pack("<I", new_head_off)
        repoints.append((f"0x{head:x}", new_head_off, [f"0x{l:x}" for l in ptr_locs], run))
        # marca tiers no relatório
        for m in run:
            m_hex = f"0x{m:x}"
            if m_hex in encoded:
                enc, budget = encoded[m_hex]
                tier = "REPOINT_head" if m == head else "REPOINT_cont"
                report.append((m_hex, tier, len(enc), budget, enc.decode("utf-8", "replace")))

    return buf, repoints, report


# ----------------------------------------------------------------------------- IPS patch
def make_ips(original: bytes, modified: bytes) -> bytes:
    """Gera um patch IPS (original -> modified). Cobre também o crescimento no fim do arquivo.
    Limite IPS: offset de 3 bytes (< 16 MiB) — ok para este arquivo."""
    patch = bytearray(b"PATCH")
    i, n = 0, max(len(original), len(modified))
    while i < n:
        ob = original[i] if i < len(original) else None
        mb = modified[i] if i < len(modified) else None
        if ob == mb:
            i += 1
            continue
        start = i
        chunk = bytearray()
        while i < n and (original[i] if i < len(original) else None) != (modified[i] if i < len(modified) else None):
            chunk.append(modified[i] if i < len(modified) else 0x00)
            i += 1
            if len(chunk) >= 0xFFFF:
                break
        if start > 0xFFFFFF:
            raise ValueError("offset excede o limite de 3 bytes do IPS")
        patch += struct.pack(">I", start)[1:]      # 3 bytes big-endian
        patch += struct.pack(">H", len(chunk))     # tamanho 2 bytes
        patch += bytes(chunk)
    patch += b"EOF"
    return bytes(patch)


# ----------------------------------------------------------------------------- main
def main():
    src = resolve_source()
    OUT = ROOT / "output" / src.name
    original = src.read_bytes()
    budgets = load_budgets()
    approved = load_approved()

    # 1) GATE DE ROUND-TRIP: reinserir o source (transliterado = idêntico p/ ASCII) reproduz o original
    rt_buf, rt_repoints, _ = build_output(original, budgets, approved={})
    round_trip_ok = bytes(rt_buf) == original and not rt_repoints
    print(f"Round-trip self-test: {'OK (byte-identico)' if round_trip_ok else 'FALHOU'}")

    # 2) aplicar o APROVADO (in_place + repoint)
    buf, repoints, report = build_output(original, budgets, approved)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(buf)
    ips = make_ips(original, bytes(buf))
    IPS = OUT.with_suffix(OUT.suffix + ".ips")
    IPS.write_bytes(ips)

    # 3) métricas
    tiers = {}
    for _, tier, *_ in report:
        tiers[tier] = tiers.get(tier, 0) + 1
    residuo = tiers.get("T4_residuo", 0)

    # 4) relatório
    order = {o: i for i, (o, _, _) in enumerate(budgets)}
    report.sort(key=lambda r: order.get(r[0], 1 << 30))
    lines = [
        "# Reinsertion Report — Utawarerumono (POC 20 linhas)", "",
        f"- Round-trip self-test: {'OK' if round_trip_ok else 'FALHOU'}",
        f"- Saída: output/{OUT.name} (mesmo nome/extensão do input)",
        f"- Patch: output/{IPS.name}",
        f"- Charset: TRANSLITERAÇÃO na gravação (fonte sem diacríticos — evidência char1/char2.png)",
        f"- Distribuição por tier: " + ", ".join(f"{k}={v}" for k, v in sorted(tiers.items())),
        f"- Overflows não resolvidos (T4): {residuo}",
        "",
        "## Repoints (head -> novo offset)", "",
    ]
    if repoints:
        lines += ["| head | novo offset | ponteiros reescritos | membros do run |",
                  "|---|---|---|---|"]
        for head, new_off, ptrs, run in repoints:
            run_s = ", ".join(f"0x{m:x}" for m in run)
            lines.append(f"| {head} | 0x{new_off:x} | {', '.join(ptrs)} | {run_s} |")
    else:
        lines.append("_nenhum_")
    lines += ["", "## Strings", "", "| offset | tier | bytes | budget | texto |", "|---|---|---|---|---|"]
    for off, tier, nb, budget, txt in report:
        safe = txt.replace("|", "\\|")
        lines.append(f"| {off} | {tier} | {nb} | {budget} | {safe} |")
    REPORT.write_text("\n".join(lines), encoding="utf-8")

    print(f"Tiers: {tiers}")
    print(f"Repoints: {len(repoints)}  |  Resíduo T4: {residuo}")
    print(f"SAÍDA  -> {OUT}")
    print(f"PATCH  -> {IPS}")
    print(f"Relatório -> {REPORT}")


if __name__ == "__main__":
    main()
