#!/usr/bin/env python3
"""
reinsert.py — conector hex_binary para Utawarerumono (versão ENG/Steam)

Reinseridor DETERMINÍSTICO: approved_translations.csv -> output/ScriptEvent.sdat + patch IPS

Contrato (framework/connectors/hex_binary.md):
  entrada : approved_translations.csv (id, text_target) + dialogs.csv (byte_budget) + .sdat original (read-only)
  saída   : output/ScriptEvent.sdat (mesmo nome/extensão do input) + output/<nome>.ips + reinsertion_report.md

Formato do .sdat (engenharia reversa — ver connector/table_schema.md):
- Bloco de texto: strings UTF-8 null-terminated e contíguas.
- Bytecode de script com o opcode de texto `50 00` (LE 0x0050) seguido de um ponteiro uint32 LE
  RELATIVO ao início do arquivo (alvo_abs = file_start + u32). Não há tabela central de ponteiros.
- "Continuações": strings sem ponteiro próprio, lidas em sequência logo após o head. Um "run" =
  head + suas continuações, até o próximo head.

Estratégia de encaixe (cascata determinística, sem LLM):
- CHARSET: a fonte do jogo NÃO tem diacríticos (acento -> '@'). Decisão: TRANSLITERAR na gravação
  (á->a, ç->c, ...). A tradução canônica (approved_translations.csv) permanece com acento; só os
  BYTES gravados no jogo são dobrados para ASCII.
- T1 in_place : len(transliterado) <= byte_budget -> grava no slot original.
- RELOC intra-arquivo : se algum membro de um run estoura, anexa o run inteiro (head + continuações)
                ao FIM da região do PRÓPRIO arquivo, faz o arquivo crescer (size do Pack é reescrito
                via sdat_format.rebuild_container) e reescreve o(s) ponteiro(s) `50 00`+u32 do head
                com o valor FILE-RELATIVO = posição local no arquivo. Continuações viajam junto.
                (O gate in-game REPROVOU anexar ao fim do CONTAINER — o engine carrega cada arquivo
                num buffer próprio dimensionado pelo `size` do Pack; ver artifacts/decision_log.md.)
- T4 resíduo  : caso irredutível (overflow sem head identificável) -> issue para o Passo 06c.

Regras de governança:
- NUNCA escreve no binário-fonte. Lê o original (read-only) e grava em output/ no projeto.
- 100% determinístico. A IA não escreve a tradução à mão — este script aplica o arquivo APROVADO.
- Gate de round-trip: reinserir o text_source (idêntico) reproduz o original byte-a-byte.

Uso: python reinsert.py [<caminho-binário>] [--validate-one <offset_hex>]
- --validate-one : modo gate — reloca SÓ o run que contém <offset>, deixando todo o resto do
  container idêntico ao original (blast radius mínimo para um teste in-game isolado).
Caminho do binário (NUNCA hardcoded): CLI > connector.source_binary do project.json.
"""
import csv
import json
import struct
import sys
import unicodedata
from pathlib import Path

import sdat_format as S
from sdat_format import read_cstr, find_pointers, is_head, read_run

ROOT = Path(__file__).resolve().parent.parent          # raiz do projeto
ART = ROOT / "artifacts"
REPORT = ART / "reinsertion_report.md"


# ----------------------------------------------------------------------------- governança de caminho
def parse_args():
    """Retorna (path|None, only_offset|None). Suporta `--validate-one <offset>` + caminho posicional."""
    args = sys.argv[1:]
    path, only = None, None
    i = 0
    while i < len(args):
        if args[i] == "--validate-one":
            only = args[i + 1] if i + 1 < len(args) else sys.exit("ERRO: --validate-one exige <offset_hex>.")
            i += 2
        else:
            path = args[i]
            i += 1
    return path, only


def resolve_source(path: str | None = None) -> Path:
    """Caminho do binário-fonte: CLI > connector.source_binary do project.json. Sem hardcode."""
    if path is not None:
        p = Path(path)
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


# Leitura do binário (read_cstr/find_pointers/is_head/read_run): vêm de sdat_format (módulo único
# compartilhado com extract.py — garante o mesmo entendimento de formato dos dois lados do round-trip).


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


def _head_of(original: bytes, off: int, pidx) -> int | None:
    """Head do run que contém `off`: o próprio off se for head; senão caminha PELO BINÁRIO para trás
    (strings reais) até achar um head. None se não houver (resíduo)."""
    if is_head(original, off, pidx):
        return off
    cur = off
    for _ in range(S.MAX_RUN):
        prev = original.rfind(b"\x00", 0, cur - 1)
        if prev < 0:
            return None
        cur = prev + 1                      # início da string anterior
        if original[cur] == 0x00:           # padding/fim de bloco -> sem head
            return None
        if is_head(original, cur, pidx):
            return cur
    return None


def build_output(original: bytes, budgets, approved, only_offset=None):
    """Aplica in_place + RELOCAÇÃO INTRA-ARQUIVO e reconstrói o container (Pack reescrito).
    Retorna (buf, repoints, report_rows).
    - repoints: lista de (head_hex, file_index, new_local_off, [ptr_sites_hex], run).
    - report_rows: (off_hex, tier, nbytes, budget, text).
    - only_offset (hex str|int): modo gate — reloca SÓ o run que contém esse offset; sem in_place;
      todos os demais arquivos ficam idênticos ao original."""
    files = S.parse_pack(original)
    by_index = {f.index: f for f in files}
    pidx = S.index_pointers(original, files)   # ponteiros FILE-RELATIVOS (target_abs=file_start+u32)

    # 1) classificar cada string conhecida e achar overflows
    encoded = {}
    overflow = []
    for off_hex, source, budget in budgets:
        enc = final_text_bytes(off_hex, source, approved)
        encoded[off_hex] = (enc, budget)
        if len(enc) > budget:
            overflow.append(off_hex)

    # 2) descobrir o head + run completo de cada overflow (head pode não estar no dialogs)
    relocated_runs = {}   # head_off(int) -> [member_off(int)]
    member_to_head = {}
    for off_hex in overflow:
        head = _head_of(original, int(off_hex, 16), pidx)
        if head is None:
            continue
        if head not in relocated_runs:
            run = read_run(original, head, pidx)
            relocated_runs[head] = run
            for m in run:
                member_to_head[m] = head

    # 2b) modo gate: manter só o run do offset pedido (relocando-o mesmo que não seja overflow)
    if only_offset is not None:
        tgt = int(only_offset, 16) if isinstance(only_offset, str) else only_offset
        head = member_to_head.get(tgt) or _head_of(original, tgt, pidx)
        if head is None:
            relocated_runs, member_to_head = {}, {}
        else:
            run = relocated_runs.get(head) or read_run(original, head, pidx)
            relocated_runs, member_to_head = {head: run}, {m: head for m in run}

    relocated_offsets = set(member_to_head.keys())
    do_inplace = only_offset is None

    # 3) agrupar edições por arquivo (coordenadas LOCAIS ao arquivo)
    report = []
    file_inplace = {}   # idx -> [(local_off, enc, budget, off_hex)]
    if do_inplace:
        for off_hex, source, budget in budgets:
            off = int(off_hex, 16)
            enc, _ = encoded[off_hex]
            if off in relocated_offsets:
                continue                        # será gravada na relocação
            f = S.file_of(off, files)
            if f is not None and len(enc) <= budget:
                file_inplace.setdefault(f.index, []).append((off - f.offset, enc, budget, off_hex))
                report.append((off_hex, "T1_in_place", len(enc), budget, enc.decode("utf-8", "replace")))
            else:
                report.append((off_hex, "T4_residuo", len(enc), budget, enc.decode("utf-8", "replace")))

    file_reloc = {}     # idx -> [(head, run, [ptr_sites])]
    for head in sorted(relocated_runs):
        f = S.file_of(head, files)
        if f is None:
            continue
        file_reloc.setdefault(f.index, []).append(
            (head, relocated_runs[head], find_pointers(original, head, pidx)))

    # 4) construir os bytes novos de cada arquivo alterado (in_place + append do run no fim do arquivo)
    repoints = []
    new_file_bytes = {}
    for idx in sorted(set(file_inplace) | set(file_reloc)):
        f = by_index[idx]
        nd = bytearray(original[f.offset:f.end])
        # 4a) in_place: grava no slot local e zera a sobra (até o terminador do slot original)
        for local_off, enc, budget, off_hex in file_inplace.get(idx, []):
            nd[local_off:local_off + len(enc)] = enc
            for k in range(local_off + len(enc), local_off + budget + 1):
                nd[k] = 0x00
        # 4b) relocação: anexa o run ao fim do arquivo; o ponteiro file-relativo = offset local novo
        for head, run, sites in file_reloc.get(idx, []):
            new_local = len(nd)
            for m in run:
                m_hex = f"0x{m:x}"
                if m_hex in encoded:
                    enc = encoded[m_hex][0]
                else:                            # continuação fora do corpus -> mantém original (translit.)
                    enc = transliterate(read_cstr(original, m).decode("utf-8", "replace")).encode("utf-8")
                nd += enc + b"\x00"
            for site, fs in sites:               # site é absoluto e está NESTE arquivo (ponteiros não cruzam)
                nd[site - f.offset: site - f.offset + 4] = struct.pack("<I", new_local)
            repoints.append((f"0x{head:x}", idx, new_local, [f"0x{s:x}" for s, _ in sites], run))
            for m in run:
                m_hex = f"0x{m:x}"
                if m_hex in encoded:
                    enc, budget = encoded[m_hex]
                    tier = "RELOC_head" if m == head else "RELOC_cont"
                    report.append((m_hex, tier, len(enc), budget, enc.decode("utf-8", "replace")))
        new_file_bytes[idx] = bytes(nd)          # rebuild_container faz o padding a 16 bytes

    buf = bytearray(S.rebuild_container(original, files, new_file_bytes))
    return buf, repoints, report


# ----------------------------------------------------------------------------- T4: resíduo em lote
def collect_t4_residue(report, src_by):
    """Linhas que NEM in_place NEM relocação resolveram (tier T4_residuo) — overflow irredutível.
    Vira um LOTE para a IA reescrever mais curto numa ÚNICA passada (princípio 'LLM só no resíduo').
    Retorna lista de dicts (offset, text_source, current_target, byte_budget, target_bytes, over_by)."""
    out = []
    for off_hex, tier, nbytes, budget, txt in report:
        if tier == "T4_residuo":
            out.append({
                "offset": off_hex,
                "text_source": src_by.get(off_hex, ""),
                "current_target": txt,
                "byte_budget": budget,
                "target_bytes": nbytes,
                "over_by": nbytes - budget,
                "reason": "overflow sem head relocável (sem ponteiro 50 00) — encurtar para caber in_place",
            })
    return out


def write_t4_batch(path, src_name, residue):
    """Grava artifacts/t4_residue.json: o LOTE a reescrever (vazio = nada a fazer).
    A IA reescreve cada `current_target` para caber em `byte_budget`, devolve no translation_plan.json
    (base_translation), e o fluxo normal (poc_pipeline -> approved -> reinsert) reaplica. Governança:
    a IA PROPÕE no plano; o usuário aprova. Nenhuma escrita de bytes à mão."""
    payload = {
        "generated_for": src_name,
        "count": len(residue),
        "instruction": ("Reescreva cada 'current_target' para caber em 'byte_budget' bytes (UTF-8, já "
                        "transliterado p/ ASCII na gravação), preservando tom, tokens e entidades. "
                        "Devolva as versões curtas no translation_plan.json (base_translation)."),
        "lines": residue,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


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
    path, only = parse_args()
    src = resolve_source(path)
    OUT = ROOT / "output" / src.name
    original = src.read_bytes()
    budgets = load_budgets()
    approved = load_approved()

    # 1) GATE DE ROUND-TRIP: reinserir o source (transliterado = idêntico p/ ASCII) reproduz o original
    rt_buf, rt_repoints, _ = build_output(original, budgets, approved={})
    round_trip_ok = bytes(rt_buf) == original and not rt_repoints
    print(f"Round-trip self-test: {'OK (byte-identico)' if round_trip_ok else 'FALHOU'}")

    # 2) aplicar o APROVADO (in_place + relocação intra-arquivo). Modo gate: só 1 run.
    buf, repoints, report = build_output(original, budgets, approved, only_offset=only)

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

    # T4 — exporta o LOTE de resíduo irredutível (vazio hoje: Plano B reloca tudo)
    src_by = {o: s for o, s, _ in budgets}
    t4 = collect_t4_residue(report, src_by)
    write_t4_batch(ART / "t4_residue.json", OUT.name, t4)

    files = S.parse_pack(original)
    by_index = {f.index: f for f in files}
    grown = {idx for _, idx, *_ in repoints}

    # 4) relatório
    order = {o: i for i, (o, _, _) in enumerate(budgets)}
    report.sort(key=lambda r: order.get(r[0], 1 << 30))
    title = "# Reinsertion Report — Utawarerumono"
    if only:
        title += f" (modo gate --validate-one {only})"
    lines = [
        title, "",
        f"- Round-trip self-test: {'OK' if round_trip_ok else 'FALHOU'}",
        f"- Saída: output/{OUT.name} (mesmo nome/extensão do input) — {len(buf)} bytes "
        f"(original {len(original)}; +{len(buf) - len(original)})",
        f"- Patch: output/{IPS.name}",
        "- Charset: TRANSLITERAÇÃO na gravação (fonte sem diacríticos — evidência char1/char2.png)",
        "- Estratégia: in_place + relocação INTRA-ARQUIVO (run anexado ao fim do próprio arquivo; "
        "Pack reescrito). EOF-append (fim do container) foi REPROVADO in-game — ver decision_log.md.",
        "- Distribuição por tier: " + ", ".join(f"{k}={v}" for k, v in sorted(tiers.items())),
        f"- Overflows não resolvidos (T4): {residuo}",
        "",
        "## Relocações (head -> offset local no arquivo crescido)", "",
    ]
    if repoints:
        lines += ["| head (abs) | arquivo | offset local novo | ponteiros reescritos | membros do run |",
                  "|---|---|---|---|---|"]
        for head, idx, new_local, ptrs, run in repoints:
            f = by_index[idx]
            run_s = ", ".join(f"0x{m:x}" for m in run)
            lines.append(f"| {head} | {f.name} | 0x{new_local:x} | {', '.join(ptrs)} | {run_s} |")
    else:
        lines.append("_nenhuma_")
    if grown:
        new_by_name = {f.name: f.size for f in S.parse_pack(bytes(buf))}
        lines += ["", "## Arquivos crescidos (Pack reescrito)", "",
                  "| arquivo | size original | size novo (pad 16) |", "|---|---|---|"]
        for idx in sorted(grown):
            f = by_index[idx]
            lines.append(f"| {f.name} | 0x{f.size:x} | 0x{new_by_name.get(f.name, f.size):x} |")
    lines += ["", "## Strings", "", "| offset | tier | bytes | budget | texto |", "|---|---|---|---|---|"]
    for off, tier, nb, budget, txt in report:
        safe = txt.replace("|", "\\|")
        lines.append(f"| {off} | {tier} | {nb} | {budget} | {safe} |")
    REPORT.write_text("\n".join(lines), encoding="utf-8")

    print(f"Tiers: {tiers}")
    print(f"Relocações: {len(repoints)}  |  Arquivos crescidos: {len(grown)}  |  Resíduo T4: {residuo}")
    if residuo:
        print(f"T4 LOTE -> {ART / 't4_residue.json'}  ({residuo} linha(s) p/ reescrita LLM em lote)")
    print(f"Tamanho: {len(original)} -> {len(buf)} (+{len(buf) - len(original)})")
    print(f"SAÍDA  -> {OUT}")
    print(f"PATCH  -> {IPS}")
    print(f"Relatório -> {REPORT}")


if __name__ == "__main__":
    main()
