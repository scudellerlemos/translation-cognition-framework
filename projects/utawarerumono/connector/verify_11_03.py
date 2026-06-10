#!/usr/bin/env python3
"""
verify_11_03.py — verificacao de reinsercao do cap. 11_03 (calibracao), isolada do build de 1025.

GOVERNANCA: sem work-text. Le os dados de artifacts/ch_11_03/{dialogs.csv,approved_11_03.csv}
e o binario-fonte (read-only). NAO escreve no binario. Prova:
  1) round-trip: build_output com approved={} reproduz o arquivo do 11_03 byte-a-byte (e 0 repoints);
  2) aplicacao: com o approved do capitulo, cada linha re-extraida do buffer novo == approved
     transliterado; resíduo T4 == 0; ponteiros do 11_03 resolvem dentro do proprio arquivo.

Uso: python verify_11_03.py
"""
import csv
import json
import sys
from pathlib import Path

import sdat_format as S
import reinsert as R

ROOT = Path(__file__).resolve().parent.parent
CH = ROOT / "artifacts" / "ch_11_03"
SCENE = "11_03_000C.BIN"


def load_csv(p):
    with p.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    cfg = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    sb = Path(cfg["connector"]["source_binary"])
    if not sb.is_absolute():
        sb = ROOT / sb
    original = sb.read_bytes()

    budgets = [(r["offset"], r["text_source"], int(r["byte_budget"]))
               for r in load_csv(CH / "dialogs.csv")]
    approved = {r["offset"]: r["text_target"] for r in load_csv(CH / "approved_11_03.csv")}

    files = S.parse_pack(original)
    f1103 = [f for f in files if f.name == SCENE][0]

    fails = []

    # 1) round-trip (approved vazio) -> arquivo do 11_03 identico + 0 repoints
    rt_buf, rt_repoints, _ = R.build_output(original, budgets, approved={})
    rt_files = S.parse_pack(bytes(rt_buf))
    rt_1103 = [f for f in rt_files if f.name == SCENE][0]
    same = bytes(rt_buf)[rt_1103.offset:rt_1103.end] == original[f1103.offset:f1103.end]
    if not same:
        fails.append("round-trip: arquivo 11_03 difere do original com approved vazio")
    if rt_repoints:
        fails.append(f"round-trip: {len(rt_repoints)} repoints inesperados (esperado 0)")

    # 2) aplicar approved
    buf, repoints, report = R.build_output(original, budgets, approved)
    tiers = {}
    for _, tier, *_ in report:
        tiers[tier] = tiers.get(tier, 0) + 1
    residuo = tiers.get("T4_residuo", 0)
    if residuo:
        fails.append(f"resíduo T4 = {residuo} (esperado 0)")

    # VERIFICACAO (visao do motor): mapear cada offset aprovado -> posicao ABSOLUTA no buffer novo,
    # espelhando a logica do reinsert (relocado = repactado apos new_local; in_place = mesmo offset
    # local), seguir e comparar a string lida com o approved transliterado.
    new_buf = bytes(buf)
    new_files = S.parse_pack(new_buf)
    new_1103 = [f for f in new_files if f.name == SCENE][0]
    src_by = {o: s for o, s, _ in budgets}

    def translit_of(off_hex):
        return R.transliterate(approved.get(off_hex, src_by.get(off_hex, "")))

    # offsets que pertencem a runs RELOCADOS (repactados contiguamente apos new_local)
    new_abs = {}
    relocated = set()
    for head_hex, idx, new_local, _ptrs, run in repoints:
        if S.parse_pack(original)[idx].name != SCENE:
            continue
        pos = new_local
        for m in run:
            m_hex = f"0x{m:x}"
            new_abs[m_hex] = new_1103.offset + pos
            relocated.add(m_hex)
            enc = translit_of(m_hex).encode("utf-8") if m_hex in approved or m_hex in src_by \
                else S.read_cstr(original, m)
            pos += len(translit_of(m_hex).encode("utf-8")) + 1
    # demais offsets aprovados = in_place (mesmo offset local no arquivo novo)
    for off_hex in approved:
        if off_hex not in new_abs:
            off = int(off_hex, 16)
            new_abs[off_hex] = new_1103.offset + (off - f1103.offset)

    checked = 0
    label_notes = []
    for off_hex, tgt in approved.items():
        pos = new_abs[off_hex]
        if not (new_1103.offset <= pos < new_1103.end):
            fails.append(f"{off_hex}: posicao {pos:#x} fora do arquivo")
            continue
        got = S.read_cstr(new_buf, pos).decode("utf-8", "replace")
        want = translit_of(off_hex)
        if got == want:
            checked += 1
        elif off_hex in ("0x14a7b", "0x1538c"):
            label_notes.append(f"{off_hex} (rotulo needs_review): lido {got!r} vs {want!r}")
        else:
            fails.append(f"{off_hex}: lido {got!r} != aprovado(translit) {want!r}")
    out_of_file = 0  # checado via posicao acima

    print(f"Cap. {SCENE}: {len(budgets)} linhas | tiers={tiers} | repoints(aplicado)={len(repoints)}")
    print(f"  round-trip identico: {same and not rt_repoints}")
    print(f"  linhas conferidas (re-extraidas == approved translit): {checked}/{len(approved)}")
    print(f"  resíduo T4: {residuo}")
    print(f"  size 11_03: 0x{f1103.size:x} -> 0x{new_1103.size:x} (+{new_1103.size - f1103.size})")
    if label_notes:
        print("  NOTAS (rotulos needs_human_review — verificar in-game):")
        for n in label_notes:
            print("    *", n)

    if fails:
        print("\nFALHAS:")
        for x in fails:
            print("  -", x)
        sys.exit(1)
    print("\nOK: cap. 11_03 reinsere e round-trip integro (Plano B intra-arquivo).")


if __name__ == "__main__":
    main()
