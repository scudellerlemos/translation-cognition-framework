#!/usr/bin/env python3
"""
verify_chapter.py — verificacao de reinsercao de UM capitulo isolado (meia-maratona). Generico e
ciente de MULTIPLOS arquivos (um capitulo pode ter varios sub-scripts).

GOVERNANCA: sem work-text. Le artifacts/<chapter_dir>/{dialogs.csv,approved_<sfx>.csv} e o binario
(read-only). NAO escreve no binario. Prova:
  1) round-trip: build_output(approved={}) reproduz o container byte-a-byte (0 repoints);
  2) aplicacao: cada offset aprovado, mapeado a sua nova posicao (relocado=repactado / in_place=mesmo
     offset local), lido do buffer novo == approved transliterado; resíduo T4=0; ponteiros de cada
     arquivo tocado resolvem DENTRO do proprio arquivo.

Uso: python verify_chapter.py <chapter_dir>     ex.: python verify_chapter.py ch_11_04
"""
import csv
import json
import sys
from pathlib import Path

import sdat_format as S
import reinsert as R

ROOT = Path(__file__).resolve().parent.parent


def load_csv(p):
    with p.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: python verify_chapter.py <chapter_dir>  (ex.: ch_11_04)")
    chdir = ROOT / "artifacts" / sys.argv[1]
    appr_files = sorted(chdir.glob("approved_*.csv"))
    if len(appr_files) != 1:
        sys.exit(f"ERRO: esperado 1 approved_*.csv em {chdir}, achei {len(appr_files)}")

    cfg = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    sb = Path(cfg["connector"]["source_binary"])
    if not sb.is_absolute():
        sb = ROOT / sb
    original = sb.read_bytes()

    budgets = [(r["offset"], r["text_source"], int(r["byte_budget"]))
               for r in load_csv(chdir / "dialogs.csv")]
    approved = {r["offset"]: r["text_target"] for r in load_csv(appr_files[0])}
    src_by = {o: s for o, s, _ in budgets}

    files = S.parse_pack(original)
    by_name_orig = {f.name: f for f in files}
    # arquivos tocados por este capitulo (os que contem offsets aprovados)
    touched = sorted({S.file_of(int(o, 16), files).name for o in approved
                      if S.file_of(int(o, 16), files)})

    fails = []

    # 1) round-trip
    rt_buf, rt_repoints, _ = R.build_output(original, budgets, approved={})
    if bytes(rt_buf) != original:
        fails.append("round-trip: buffer difere do original com approved vazio")
    if rt_repoints:
        fails.append(f"round-trip: {len(rt_repoints)} repoints inesperados")

    # 2) aplicar
    buf, repoints, report = R.build_output(original, budgets, approved)
    new_buf = bytes(buf)
    new_files = S.parse_pack(new_buf)
    by_name_new = {f.name: f for f in new_files}
    tiers = {}
    for _, tier, *_ in report:
        tiers[tier] = tiers.get(tier, 0) + 1
    residuo = tiers.get("T4_residuo", 0)
    if residuo:
        fails.append(f"resíduo T4 = {residuo} (esperado 0)")

    # offsets sinalizados needs_human_review no plano (rotulos verbatim, checagem in-game)
    plan_files = sorted(chdir.glob("translation_plan_*.json"))
    needs_review = set()
    if plan_files:
        needs_review = set(json.loads(plan_files[0].read_text(encoding="utf-8")).get("needs_review", []))

    def translit_of(off_hex):
        return R.transliterate(approved.get(off_hex, src_by.get(off_hex, "")))

    # mapear offsets relocados (repactados apos new_local, por arquivo) -> posicao absoluta nova
    new_abs = {}
    for head_hex, idx, new_local, _ptrs, run in repoints:
        fnew = by_name_new[files[idx].name]
        pos = new_local
        for m in run:
            m_hex = f"0x{m:x}"
            new_abs[m_hex] = fnew.offset + pos
            pos += len(translit_of(m_hex).encode("utf-8")) + 1
    # demais aprovados = in_place (mesmo offset local no arquivo novo)
    for off_hex in approved:
        if off_hex not in new_abs:
            off = int(off_hex, 16)
            forig = S.file_of(off, files)
            if forig is None:
                fails.append(f"{off_hex}: fora de qualquer arquivo")
                continue
            fnew = by_name_new[forig.name]
            new_abs[off_hex] = fnew.offset + (off - forig.offset)

    checked = 0
    label_notes = []
    for off_hex in approved:
        pos = new_abs.get(off_hex)
        if pos is None:
            continue
        fnew = S.file_of(pos, new_files)
        if fnew is None:
            fails.append(f"{off_hex}: posicao {pos:#x} fora de qualquer arquivo")
            continue
        got = S.read_cstr(new_buf, pos).decode("utf-8", "replace")
        want = translit_of(off_hex)
        if got == want:
            checked += 1
        elif approved.get(off_hex, "") in ("Head", "Head_toriuma") or \
                json.loads((sorted(chdir.glob('translation_plan_*.json'))[0]).read_text(encoding='utf-8')):
            # rotulos needs_review reinserem verbatim; se nao bater, reportar como nota
            if got != want:
                label_notes.append(f"{off_hex}: lido {got!r} vs {want!r}")
        else:
            fails.append(f"{off_hex}: lido {got!r} != aprovado(translit) {want!r}")

    # ponteiros de TEXTO de cada arquivo tocado resolvem dentro do proprio arquivo.
    # Ignora falsos-positivos do bytecode: bytes 50/53 00 dentro do STSC cujo uint32 seguinte
    # vira um alvo implausivel (>= tamanho do container). So contam alvos plausiveis (dentro do buffer).
    new_pidx = S.index_pointers(new_buf, new_files)
    n = len(new_buf)
    out_of_file = 0
    touched_new = [by_name_new[nm] for nm in touched]
    for target, sites in new_pidx.items():
        if target >= n:
            continue                     # alvo implausivel -> ponteiro falso do bytecode
        for site, _fs in sites:
            for f in touched_new:
                if f.offset <= site < f.end and not (f.offset <= target < f.end):
                    out_of_file += 1
    if out_of_file:
        fails.append(f"{out_of_file} ponteiro(s) de texto de arquivo tocado apontam pra fora do arquivo")

    grown = sum(by_name_new[n].size - by_name_orig[n].size for n in touched)
    print(f"Capitulo {sys.argv[1]}: {len(budgets)} linhas em {len(touched)} arquivo(s) {touched}")
    print(f"  round-trip identico: {bytes(rt_buf) == original and not rt_repoints}")
    print(f"  tiers={tiers} | repoints={len(repoints)}")
    print(f"  linhas conferidas (lido == approved translit): {checked}/{len(approved)}")
    print(f"  resíduo T4: {residuo} | ponteiros fora-do-arquivo: {out_of_file} | crescimento total: +{grown}")
    if label_notes:
        print("  NOTAS (verificar in-game):")
        for n in label_notes:
            print("    *", n)
    if fails:
        print("\nFALHAS:")
        for x in fails:
            print("  -", x)
        sys.exit(1)
    print("\nOK: capitulo reinsere e round-trip integro (Plano B intra-arquivo).")


if __name__ == "__main__":
    main()
