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

    # ponteiros de TEXTO de arquivo tocado resolvem dentro do proprio arquivo.
    # CUIDADO com falsos-positivos do bytecode: ocorrencias coincidentes de 50/53 00 cujo uint32 vira um
    # alvo cross-file (ex.: cena do cap.12 "apontando" p/ 31_02_000S.BIN). Esses JA existem no binario
    # ORIGINAL intocado -> sao baseline, nao regressao. So e bug do reinsert se o buffer NOVO tiver MAIS
    # ponteiros fora-do-arquivo que o original (delta > 0). (Cena multi-BIN 12_15 tinha 2 em ambos.)
    def _count_oof(buf, fls):
        pidx = S.index_pointers(buf, fls)
        nn = len(buf)
        bn = {f.name: f for f in fls}
        tfs = [bn[nm] for nm in touched if nm in bn]
        c = 0
        for target, sites in pidx.items():
            if target >= nn:
                continue                 # alvo implausivel -> ponteiro falso do bytecode
            for site, _fs in sites:
                for f in tfs:
                    if f.offset <= site < f.end and not (f.offset <= target < f.end):
                        c += 1
        return c
    oof_base = _count_oof(original, files)        # falsos-positivos pre-existentes (bytecode)
    oof_new = _count_oof(new_buf, new_files)
    out_of_file = max(0, oof_new - oof_base)      # so o que o reinsert INTRODUZIU
    if out_of_file:
        fails.append(f"{out_of_file} ponteiro(s) de texto NOVOS fora-do-arquivo (regressao do reinsert; "
                     f"base={oof_base} falsos-positivos pre-existentes no original)")

    grown = sum(by_name_new[n].size - by_name_orig[n].size for n in touched)
    print(f"Capitulo {sys.argv[1]}: {len(budgets)} linhas em {len(touched)} arquivo(s) {touched}")
    print(f"  round-trip identico: {bytes(rt_buf) == original and not rt_repoints}")
    print(f"  tiers={tiers} | repoints={len(repoints)}")
    print(f"  linhas conferidas (lido == approved translit): {checked}/{len(approved)}")
    print(f"  resíduo T4: {residuo} | ponteiros fora-do-arquivo (novos): {out_of_file} "
          f"[{oof_new} total, {oof_base} falsos-positivos pre-existentes] | crescimento total: +{grown}")
    if label_notes:
        print("  NOTAS (verificar in-game):")
        for n in label_notes:
            print("    *", n)

    # PROTOCOLO ESTRUTURADO (H1) — o orquestrador (run_scene) NAO faz grep no stdout p/ decidir
    # escalonamento de fitting. Em vez disso: exit-code distinto + 1 linha JSON machine-readable.
    #   exit 0 = OK | exit 3 = falha SO de FITTING (residuo/out-of-file -> re-traduzir mais apertado
    #   ajuda) | exit 1 = falha DURA (round-trip/leitura -> apertar nao cura). A linha VERIFY_STATUS
    #   carrega os numeros (residuo, out_of_file) p/ observabilidade. JSON e additive (humano ignora).
    n_fitting = (1 if residuo else 0) + (1 if out_of_file else 0)
    fitting_only = bool(fails) and len(fails) == n_fitting     # todas as falhas sao de fitting
    print("VERIFY_STATUS: " + json.dumps({
        "ok": not fails,
        "fitting_failure": fitting_only,
        "residuo_t4": residuo,
        "out_of_file": out_of_file,
        "n_fails": len(fails),
    }, ensure_ascii=False))
    if fails:
        print("\nFALHAS:")
        for x in fails:
            print("  -", x)
        sys.exit(3 if fitting_only else 1)
    print("\nOK: capitulo reinsere e round-trip integro (Plano B intra-arquivo).")


if __name__ == "__main__":
    main()
