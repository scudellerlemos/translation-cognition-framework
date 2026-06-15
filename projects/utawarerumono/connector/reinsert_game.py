#!/usr/bin/env python3
"""
reinsert_game.py — FASE 3: reinserção GLOBAL (jogo inteiro num passe).

Agrega TODOS os `artifacts/ch_*/dialogs.csv` (budgets) + `approved_*.csv` (traduções aprovadas) e
aplica no binário num ÚNICO `build_output` → `output/<bin>` + patch `.ips`. É o passe que fecha o jogo:
até aqui o conector provava por capítulo; aqui o jogo inteiro vai junto.

GOVERNANÇA: lê DADOS (nunca texto hardcoded), binário-fonte é read-only (grava só em `output/`),
caminho do binário vem de CLI > `project.json` (nunca hardcoded). Determinístico. **Reusa**
`build_output`/`make_ips`/`transliterate` do `reinsert.py` (testados) — zero lógica nova de formato.

Verifica ANTES de escrever:
  1) round-trip global — `build_output(approved={})` reproduz o original byte-a-byte (0 repoints);
  2) aplicação — cada offset aprovado, mapeado à sua nova posição, lê de volta == aprovado transliterado;
  3) resíduo T4 = 0.
Falha em qualquer um → NÃO escreve output e sai com código 1.

Uso:  python connector/reinsert_game.py [<binario>]   (default: connector.source_binary do project.json)
"""
import argparse
import csv
import json
import sys
from pathlib import Path

import sdat_format as S
import reinsert as R


def load_game():
    """Agrega budgets (offset, source, byte_budget) e approved {offset: target} de TODAS as cenas
    `artifacts/ch_*` que tenham dialogs.csv + approved_*.csv. Ordem estável (scene_id, depois dialogs)."""
    budgets, approved, scenes = [], {}, 0
    for sd in sorted(R.ART.glob("ch_*"), key=lambda p: p.name):
        dlg = sd / "dialogs.csv"
        aps = sorted(sd.glob("approved_*.csv"))
        if not dlg.is_file() or not aps:
            continue
        scenes += 1
        for r in csv.DictReader(dlg.open(encoding="utf-8")):
            budgets.append((r["offset"], r["text_source"], int(r["byte_budget"])))
        for ap in aps:
            for r in csv.DictReader(ap.open(encoding="utf-8")):
                approved[r["offset"]] = r["text_target"]
    return budgets, approved, scenes


def _qa_review_present() -> bool:
    """GATE DE QA: o relatorio de revisao humana do JOGO INTEIRO existe no outbox? (checagem de path,
    sem importar o runtime — mantem o conector isolado da camada de cognicao)."""
    outbox = R.ART / "qa_revisao" / "para_revisar"
    return any((outbox / f"review_all.{ext}").is_file() for ext in ("xlsx", "csv"))


def main():
    ap = argparse.ArgumentParser(description="Fase 3 — reinserção global (jogo inteiro num passe).")
    ap.add_argument("binary", nargs="?", default=None, help="binário-fonte (default: project.json)")
    ap.add_argument("--skip-qa-gate", action="store_true",
                    help="pula o gate de QA obrigatorio (NAO recomendado; use so com revisao ja feita por fora)")
    a = ap.parse_args()
    src = R.resolve_source(a.binary)
    original = src.read_bytes()
    budgets, approved, n_scenes = load_game()
    print(f"jogo: {n_scenes} cena(s) · {len(budgets)} linha(s) · {len(approved)} aprovada(s)")
    if not budgets:
        sys.exit("ERRO: nenhuma cena com dialogs.csv + approved_*.csv em artifacts/ch_*/")

    # GATE DE QA OBRIGATORIO (cobre o usuario): nao gera o .sdat de ENTREGA sem o relatorio de revisao
    # humana do jogo inteiro ter sido disponibilizado. Garante que o piso de qualidade (humano ler) nao
    # e pulado por esquecimento. Escape consciente: --skip-qa-gate (logado em alto e bom som).
    if a.skip_qa_gate:
        print("[QA gate] PULADO via --skip-qa-gate (revisao humana assumida feita por fora).")
    elif not _qa_review_present():
        sys.exit("BLOQUEADO (QA obrigatorio): o relatorio de revisao humana do JOGO INTEIRO nao existe.\n"
                 "  Gere antes do output final:  python quality_review.py export <projeto>\n"
                 "  (esperado: artifacts/qa_revisao/para_revisar/review_all.xlsx)\n"
                 "  Pular conscientemente (NAO recomendado): reinsert_game.py --skip-qa-gate")
    else:
        print("[QA gate] OK — relatorio de revisao humana disponibilizado (artifacts/qa_revisao/para_revisar/).")

    fails = []

    # 1) round-trip global (approved vazio == original byte-a-byte)
    rt_buf, rt_repoints, _ = R.build_output(original, budgets, approved={})
    rt_ok = bytes(rt_buf) == original and not rt_repoints
    print(f"round-trip global: {'OK (byte-identico)' if rt_ok else 'FALHOU'}")
    if not rt_ok:
        fails.append("round-trip global difere do original com approved vazio")

    # 2) aplicar TODAS as traduções num passe
    buf, repoints, report = R.build_output(original, budgets, approved)
    new_buf = bytes(buf)
    tiers = {}
    for _, tier, *_ in report:
        tiers[tier] = tiers.get(tier, 0) + 1
    residuo = tiers.get("T4_residuo", 0)
    if residuo:
        fails.append(f"resíduo T4 = {residuo} (esperado 0)")

    # 3) read-back: lido (do buffer novo) == aprovado transliterado. Mapeia relocados (head-reloc por
    #    arquivo) à posição absoluta nova; o resto é in_place (mesmo offset local no arquivo novo).
    files = S.parse_pack(original)
    new_files = S.parse_pack(new_buf)
    by_name_new = {f.name: f for f in new_files}
    src_by = {o: s for o, s, _ in budgets}

    def translit_of(off_hex):
        return R.transliterate(approved.get(off_hex, src_by.get(off_hex, "")))

    new_abs = {}
    for _head_hex, idx, new_local, _ptrs, run in repoints:
        fnew = by_name_new[files[idx].name]
        pos = new_local
        for m in run:
            m_hex = f"0x{m:x}"
            new_abs[m_hex] = fnew.offset + pos
            pos += len(translit_of(m_hex).encode("utf-8")) + 1
    for off_hex in approved:
        if off_hex not in new_abs:
            off = int(off_hex, 16)
            forig = S.file_of(off, files)
            if forig is None:
                fails.append(f"{off_hex}: fora de qualquer arquivo")
                continue
            new_abs[off_hex] = by_name_new[forig.name].offset + (off - forig.offset)

    checked = 0
    for off_hex in approved:
        pos = new_abs.get(off_hex)
        if pos is None:
            continue
        got = S.read_cstr(new_buf, pos).decode("utf-8", "replace")
        if got == translit_of(off_hex):
            checked += 1
        else:
            fails.append(f"{off_hex}: lido {got!r} != aprovado(translit) {translit_of(off_hex)!r}")
    print(f"read-back: {checked}/{len(approved)} linha(s) conferem (lido == aprovado translit)")

    status = {"ok": not fails, "scenes": n_scenes, "lines": len(budgets), "approved": len(approved),
              "residuo_t4": residuo, "checked": checked, "n_fails": len(fails)}
    print("VERIFY_STATUS: " + json.dumps(status, ensure_ascii=False))

    if fails:
        print("\nFALHAS (output NÃO escrito):")
        for x in fails[:30]:
            print("  -", x)
        if len(fails) > 30:
            print(f"  ... +{len(fails) - 30} mais")
        sys.exit(1)

    # 4) escrever output + IPS (só com tudo verde)
    out = R.ROOT / "output" / src.name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(new_buf)
    ips_path = out.with_suffix(out.suffix + ".ips")
    ips_path.write_bytes(R.make_ips(original, new_buf))
    print(f"\nOK: jogo inteiro reinserido (round-trip + apply verdes). crescimento +{len(new_buf) - len(original)} bytes")
    print(f"  -> {out}")
    print(f"  -> {ips_path}  (patch p/ aplicar sobre o ScriptEvent.sdat original da Steam)")


if __name__ == "__main__":
    main()
