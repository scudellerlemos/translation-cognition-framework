#!/usr/bin/env python3
"""
quality_review.py — REVISAO HUMANA por capitulo, sem IA-julga-IA (piso de qualidade de verdade).

A back-translation (Opus julgando Sonnet/Haiku) custa e nao substitui um humano lendo o pt-BR. Aqui o
humano E o juiz: o `export` gera UM CSV com o CAPITULO INTEIRO (todas as linhas, p/ leitura integral),
mas cada linha vem MARCADA de forma 100% DETERMINISTICA (sem IA) com uma tag dizendo ONDE avaliar —
risco alto, amostra do tier barato, ou flags baratas (identico-a-fonte=provavel nao-traduzido, outlier
de tamanho, `largura`=segmento estoura o balao no jogo, marcador pt-PT). Linha sem tag = passa o olho;
tag preenchida = "avalie aqui".

O humano devolve o MESMO arquivo. A DECISAO e dele, numa coluna propria: escreve **CORRIGIR** (ou
corrigir) na coluna `marcar` da linha que quer mudar. O `apply` le SO as linhas marcadas CORRIGIR.
Na linha marcada, preenche UMA:
  - coluna `correcao` = o texto certo  -> aplico VERBATIM (zero IA: so gate de charset/round-trip + merge);
  - coluna `nota` (sem correcao) = instrucao (ex.: "encurtar", "tom formal") -> IA re-traduz SO aquela
    linha seguindo a nota (cirurgico, nunca a cena inteira).
Linha SEM CORRIGIR = aprovada, nao toco. A coluna `revisar` e so DICA de onde olhar (deterministica +
o micro-QA da IA JA pago — verdict 'revise' da back-translation); NAO decide nada, $0, sem nova API.

O `apply` processa EXATAMENTE o que foi marcado e re-verifica round-trip dos capitulos tocados. Governanca:
HUMANO propoe -> gate (charset/paridade/round-trip) aprova -> script aplica. Sem work-text no .py.

Uso:
  python quality_review.py export <projeto> [<cap>] [--csv]   # XLSX amigavel (default); omita cap = JOGO TODO
  python quality_review.py apply  <projeto> <arquivo-devolvido>   # le XLSX ou CSV
"""
from __future__ import annotations
import argparse
import csv
import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import artifact_io   # noqa: E402  (leitura compartilhada: scenes/translations_map)
import context_pack  # noqa: E402
import model          # noqa: E402
import paths          # noqa: E402

# 'marcar' = a COLUNA DE DECISÃO do humano: ele escreve CORRIGIR (ou corrigir) na linha que quer mudar.
# O apply lê SÓ as linhas marcadas. 'revisar' é só DICA ($0, micro-QA da IA) de onde olhar — não decide nada.
COLS = ["scene", "offset", "speaker", "risk", "revisar", "source_en", "target_pt",
        "marcar", "correcao", "nota"]

# Marcadores pt-PT de ALTA precisao (raros no pt-BR falado) — heuristica, por isso a tag leva '?'.
_PTPT = re.compile(r"\b(tens|estás|fazes|podes|queres|deves|vês|hás)\b|\btem de\b|\bhás de\b", re.IGNORECASE)

# Largura do BALAO: o byte_budget garante que cabe no ARQUIVO (reinsercao), NAO que cabe na largura
# VISUAL do balao. Cada segmento entre tokens de quebra (`\n`) e UMA linha exibida; o pt-BR (~+25% vs
# EN) estoura linhas que no EN estavam no limite. Calibrado por QA in-game: o maior segmento EN que
# COUBE no corpus tem 62 chars transliterados -> usamos 60 (margem). Segmento pt-BR > isso = risco de
# sair do balao (o round-trip de bytes NAO pega isto).
WIDTH_MAX = 60


def _norm_cmp(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").replace("\\n", " ")).strip().lower()


def _flags(source: str, target: str, risk: str, sampled: bool, bt_revise: bool = False) -> str:
    """Tags de 'onde avaliar' — DICA p/ o humano, NUNCA decisao (a decisao e a coluna CORRIGIR).
    Tudo $0: deterministico OU reusa o micro-QA da IA JA pago (verdict 'revise' da back-translation).
    '' = linha sem sinal (passa o olho)."""
    fl = []
    if bt_revise:
        fl.append("micro-qa:revise")                      # a back-translation (IA, ja paga) achou divergencia
    if risk in ("high", "critical"):
        fl.append(f"risco:{risk}")
    if sampled:
        fl.append("amostra")
    if target and _norm_cmp(source) == _norm_cmp(target):
        fl.append("identico-fonte")                       # provavel nao-traduzido
    slen, tlen = model._translit_len(source), model._translit_len(target)
    if slen and (tlen > slen * 3 or (slen > 8 and tlen < slen * 0.4)):
        fl.append("tamanho")                              # outlier de comprimento
    if any(model._translit_len(seg) > WIDTH_MAX for seg in (target or "").split(context_pack.TOKEN)):
        fl.append("largura")                              # segmento estoura a largura do balao (in-game)
    if _PTPT.search(target or ""):
        fl.append("pt-PT?")
    return ";".join(fl)


def export(root, chapter) -> list[dict]:
    """CSV-rows do capitulo inteiro, cada linha marcada. Determinista (sem rede)."""
    root = Path(root)
    rows = []
    for scene in artifact_io.scenes(root, chapter):
        plan_lines = model._plan_lines(root, scene)
        if not plan_lines:
            continue
        tmap = artifact_io.translations_map(root, scene)
        sampled = {x["offset"] for x in model.sample_low_risk_lines(root, scene)}
        revise = _bt_revise_offsets(root, scene)          # micro-QA da IA JA pago ($0 ler)
        for ln in plan_lines:
            off = ln.get("offset", "")
            src = ln.get("text_source", "")
            tgt = (tmap.get(off) or {}).get("t", "") if isinstance(tmap.get(off), dict) \
                else ln.get("base_translation", "")
            risk = ln.get("risk_level", "")
            rows.append({"scene": scene, "offset": off, "speaker": ln.get("speaker", ""),
                         "risk": risk,
                         "revisar": _flags(src, tgt, risk, off in sampled, off in revise),
                         "source_en": src, "target_pt": tgt,
                         "marcar": "", "correcao": "", "nota": ""})
    return rows


def _bt_revise_offsets(root, scene) -> set:
    """Offsets que a back-translation (micro-QA da IA, JA paga) marcou 'revise'. So leitura ($0)."""
    sid = context_pack.scene_id_of(scene)
    btf = paths.back_translation(root, scene, sid)
    if not btf.is_file():
        return set()
    try:
        data = json.loads(btf.read_text(encoding="utf-8"))
    except Exception:
        return set()
    return {e.get("offset") for e in data.get("entries", []) if e.get("verdict") == "revise"}


def write_csv(rows, out_path):
    with Path(out_path).open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLS})


# rotulos amigaveis (PT) p/ o XLSX, na MESMA ordem de COLS (a leitura mapeia por posicao)
_XLSX_HEAD = ["Cena", "Offset", "Falante", "Risco", "Revisar (onde olhar)", "Ingles (fonte)",
              "Portugues (atual)", "Corrigir? (escreva CORRIGIR)", "Correcao (texto certo)",
              "Nota (instrucao p/ IA)"]
# severidade -> cor da linha (a 1a tag presente vence; ordem = mais grave primeiro)
_XLSX_SEV = [("micro-qa", "F4CCCC"), ("critical", "FFC7CE"), ("high", "FFE2C7"), ("largura", "CFE2FF"),
             ("identico-fonte", "E8E8E8"), ("tamanho", "FFF0C7"), ("pt-PT", "EAD9F2")]
_XLSX_INPUT = "FFF7CC"   # amarelo claro nas colunas de input do humano (Corrigir?/Correcao/Nota)


def write_xlsx(rows, out_path):
    """Relatorio AMIGAVEL p/ o revisor humano (Excel/LibreOffice): aba 'Leia-me' (instrucoes+legenda+
    contagem) + aba 'Revisao' com cabecalho congelado, autofiltro, cor por tipo de erro, colunas de
    input em amarelo e EN/PT com quebra de linha. O `apply` le este xlsx de volta (mapeado por posicao)."""
    from collections import Counter
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment
    except ImportError as e:
        raise RuntimeError("o relatorio XLSX amigavel requer 'openpyxl' (pip install openpyxl). "
                           "Ou use --csv p/ o CSV cru.") from e

    cnt = Counter(t for r in rows if r.get("revisar") for t in r["revisar"].split(";"))
    marked = sum(1 for r in rows if r.get("revisar"))
    wb = Workbook()

    intro = wb.active
    intro.title = "Leia-me"
    intro.column_dimensions["A"].width = 26
    intro.column_dimensions["B"].width = 60
    L = [("COMO REVISAR", ""), ("", ""),
         ("1.", "Va para a aba 'Revisao'."),
         ("2.", "A coluna 'Revisar (onde olhar)' e so DICA (do micro-QA da IA, ja pago) — NAO decide nada. "
                "Filtre por NAO-vazias p/ priorizar onde olhar."),
         ("3.", "VOCE decide: na coluna 'Corrigir? (escreva CORRIGIR)' escreva CORRIGIR (ou corrigir) "
                "na linha que quer mudar. So as linhas marcadas CORRIGIR serao processadas."),
         ("4.", "Na MESMA linha, preencha UMA: 'Correcao' = o texto CERTO (aplicado verbatim, $0); "
                "OU 'Nota' = instrucao p/ a IA reescrever so aquela linha (ex.: 'encurtar', 'mais formal')."),
         ("5.", "Linha boa = NAO escreva CORRIGIR (deixe em branco). Salve e devolva no inbox (devolvido/)."),
         ("", ""), ("LEGENDA DAS CORES (dica 'Revisar')", ""),
         ("micro-qa:revise", "a back-translation da IA (ja paga) achou divergencia de sentido — olhe"),
         ("critical / high", "linha de alto risco (voz/sentido/spoiler) — leia com atencao"),
         ("largura", "o texto pode SAIR do balao no jogo — encurte se preciso"),
         ("identico-fonte", "igual ao ingles — provavel nao-traduzido (confira; SFX/rotulo pode ficar)"),
         ("tamanho", "traducao muito mais longa/curta que o original"),
         ("pt-PT", "marcador de portugues de Portugal — adaptar p/ pt-BR"),
         ("", ""), ("RESUMO", ""),
         ("Total de linhas", len(rows)), ("Com dica p/ olhar", marked)]
    for tag, c in cnt.most_common():
        L.append((f"  {tag}", c))
    for a, b in L:
        intro.append([a, b])
    intro["A1"].font = Font(name="Arial", bold=True, size=14)
    for row in intro.iter_rows():
        for cell in row:
            if cell.column == 1 and cell.value in ("COMO REVISAR", "LEGENDA DAS CORES (coluna Revisar)", "RESUMO"):
                cell.font = Font(name="Arial", bold=True, size=12)
            elif not cell.font or cell.font.name != "Arial":
                cell.font = Font(name="Arial", size=10)

    ws = wb.create_sheet("Revisao")
    ws.append(_XLSX_HEAD)
    hfill = PatternFill("solid", fgColor="2F5496")
    hfont = Font(name="Arial", bold=True, color="FFFFFF", size=10)
    for cell in ws[1]:
        cell.fill = hfill
        cell.font = hfont
        cell.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)
    wrap = Alignment(vertical="top", wrap_text=True)
    top = Alignment(vertical="top")
    inputfill = PatternFill("solid", fgColor=_XLSX_INPUT)
    for r in rows:
        ws.append([r.get(c, "") for c in COLS])
        i = ws.max_row
        rev = r.get("revisar", "")
        fill = next((PatternFill("solid", fgColor=clr) for tag, clr in _XLSX_SEV if tag in rev), None)
        for col in range(1, len(COLS) + 1):
            cell = ws.cell(row=i, column=col)
            cell.font = Font(name="Arial", size=10)
            cell.alignment = wrap if col in (6, 7, 9, 10) else top
            if col in (8, 9, 10):                          # Corrigir?/Correcao/Nota = input do humano (amarelo)
                cell.fill = inputfill
            elif fill is not None:
                cell.fill = fill
    widths = {1: 10, 2: 11, 3: 14, 4: 9, 5: 22, 6: 52, 7: 52, 8: 16, 9: 42, 10: 28}
    for col, w in widths.items():
        ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = w
    ws.freeze_panes = "A2"                                 # cabecalho fixo ao rolar
    ws.auto_filter.ref = f"A1:{ws.cell(row=1, column=len(COLS)).column_letter}{ws.max_row}"
    wb.save(out_path)


def _read_xlsx_rows(path):
    """Le a aba 'Revisao' do xlsx devolvido -> lista de dicts {COLS: valor} (mapeado por POSICAO)."""
    try:
        from openpyxl import load_workbook
    except ImportError as e:
        raise RuntimeError("ler XLSX devolvido requer 'openpyxl' (pip install openpyxl).") from e
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb["Revisao"] if "Revisao" in wb.sheetnames else wb[wb.sheetnames[-1]]
    out, first = [], True
    for row in ws.iter_rows(values_only=True):
        if first:                                          # pula cabecalho
            first = False
            continue
        out.append({COLS[i]: ("" if i >= len(row) or row[i] is None else str(row[i]))
                    for i in range(len(COLS))})
    return out


def read_returned(path) -> dict:
    """Le o CSV ou XLSX devolvido -> {scene: {'verbatim': [(offset, texto)], 'nota': [(offset, instrucao)]}}.
    So entram as linhas que o HUMANO marcou explicitamente com CORRIGIR (coluna 'marcar', case-insensitive)
    E que tenham correcao OU nota. Linha sem CORRIGIR = aprovada, ignorada (le-se so o que o humano marcou)."""
    p = Path(path)
    if p.suffix.lower() == ".xlsx":
        records = _read_xlsx_rows(p)
    else:
        with p.open(encoding="utf-8-sig", newline="") as fh:
            records = list(csv.DictReader(fh))
    by_scene = {}
    for r in records:
        scene, off = (r.get("scene") or "").strip(), (r.get("offset") or "").strip()
        marcar = (r.get("marcar") or "").strip().lower()
        cor, nota = (r.get("correcao") or "").strip(), (r.get("nota") or "").strip()
        if not scene or not off or marcar != "corrigir":
            continue                                       # so processa o que foi MARCADO 'corrigir'
        if not cor and not nota:
            continue                                       # marcada mas sem texto/instrucao -> nada a aplicar
        slot = by_scene.setdefault(scene, {"verbatim": [], "nota": []})
        if cor:
            slot["verbatim"].append((off, cor))           # correcao verbatim vence a nota
        else:
            slot["nota"].append((off, nota))
    return by_scene


def _apply_verbatim(root, scene, pairs) -> int:
    """Grava o texto do humano em translations + plan (parity-fit; SEM IA). Retorna nº de linhas."""
    import json
    sid = context_pack.scene_id_of(scene)
    tf, pf = paths.translations(root, scene, sid), paths.translation_plan(root, scene, sid)
    if not tf.is_file() or not pf.is_file():
        return 0
    tdata = json.loads(tf.read_text(encoding="utf-8"))
    pdata = json.loads(pf.read_text(encoding="utf-8"))
    srcmap = {ln.get("offset", ""): ln.get("text_source", "") for ln in pdata.get("lines", [])}
    n = 0
    for off, txt in pairs:
        fitted = model._parity_fit(srcmap.get(off, ""), model._norm_t(txt))
        tdata.setdefault("lines", {}).setdefault(off, {})["t"] = fitted
        for ln in pdata.get("lines", []):
            if ln.get("offset") == off:
                ln["base_translation"] = fitted
        n += 1
    tf.write_text(json.dumps(tdata, ensure_ascii=False, indent=2), encoding="utf-8")
    pf.write_text(json.dumps(pdata, ensure_ascii=False, indent=2), encoding="utf-8")
    model.invalidate_back_translation(root, scene, [o for o, _ in pairs])  # crivo antigo nao vale mais
    return n


def returned_files(root, arg) -> list[Path]:
    """Resolve de ONDE ler a revisao devolvida: arquivo explicito, ou uma PASTA (todos os .xlsx/.csv
    dentro), ou — se nada for passado — o INBOX padrao (artifacts/qa_revisao/devolvido/). Ignora
    arquivos temporarios do Excel (~$...). Devolve [] se nao houver nada (apply vira no-op seguro)."""
    if arg:
        p = Path(arg)
        if p.is_file():
            return [p]
        if p.is_dir():
            base = p
        else:
            return []                                       # caminho dado mas inexistente
    else:
        base = paths.qa_inbox(root)
    if not base.is_dir():
        return []
    return sorted(f for f in base.iterdir()
                  if f.suffix.lower() in (".xlsx", ".csv") and not f.name.startswith("~$"))


def apply(root, csv_path, *, model_name=None, max_usd=None) -> dict:
    """Processa EXATAMENTE o devolvido: verbatim (0 IA) + nota (IA cirurgica por linha). `max_usd` so
    limita o caminho de IA (verbatim e sempre $0). Retorna {verbatim, ai, scenes, cost_usd,
    scenes_touched[], stopped_budget}."""
    root = Path(root)
    returned = read_returned(csv_path)
    m = model_name or model.MODEL_TRANSLATE
    verbatim_n, ai_n, cost = 0, 0, 0.0
    touched, stopped = [], False
    for scene in sorted(returned):
        slot = returned[scene]
        touched.append(scene)
        if slot["verbatim"]:
            verbatim_n += _apply_verbatim(root, scene, slot["verbatim"])   # sempre $0
        if slot["nota"]:
            if max_usd is not None and cost >= max_usd:
                stopped = True
                continue                                  # teto: pula o caminho PAGO (verbatim ja entrou)
            note = "\n\n## REVISAO DO HUMANO (reescreva SO estes offsets seguindo a instrucao)\n" + \
                   "\n".join(f"- {off}: {ins}" for off, ins in slot["nota"])
            res = model.retranslate_offsets(root, scene, [o for o, _ in slot["nota"]],
                                            model=m, budget_tolerance=1.0, quality_note=note)
            if res.get("usage"):
                cost += model.cost_of(m, res["usage"])
            ai_n += len(slot["nota"])
    return {"verbatim": verbatim_n, "ai": ai_n, "scenes": len(touched),
            "cost_usd": round(cost, 4), "scenes_touched": touched, "stopped_budget": stopped}


def main():
    ap = argparse.ArgumentParser(description="Revisao humana por capitulo (export CSV marcado / apply do devolvido).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pe = sub.add_parser("export", help="gera o CSV marcado p/ revisao (capitulo, ou JOGO TODO se omitir)")
    pe.add_argument("project")
    pe.add_argument("chapter", nargs="?", default=None, help="capitulo (ex.: 11); OMITA p/ o jogo INTEIRO")
    pe.add_argument("--out", default=None)
    pe.add_argument("--csv", action="store_true", help="gera CSV cru (default: XLSX amigavel p/ o revisor)")
    pa = sub.add_parser("apply", help="aplica a revisao devolvida (verbatim + notas); le do INBOX por padrao")
    pa.add_argument("project")
    pa.add_argument("returned", nargs="?", default=None,
                    help="arquivo OU pasta devolvida; OMITA p/ ler do inbox (artifacts/qa_revisao/devolvido/)")
    pa.add_argument("--model", default=None)
    pa.add_argument("--max-usd", type=float, default=None, help="teto p/ o caminho de IA (notas); verbatim e $0")
    a = ap.parse_args()
    if a.cmd == "export":
        rows = export(a.project, a.chapter)
        scope = f"cap_{a.chapter}" if a.chapter else "all"
        ext = "csv" if a.csv else "xlsx"
        if a.out:
            out = a.out
        else:
            outbox = paths.qa_outbox(Path(a.project))      # OUTBOX: disponibiliza p/ o humano ler
            outbox.mkdir(parents=True, exist_ok=True)
            out = str(outbox / f"review_{scope}.{ext}")
        (write_csv if a.csv else write_xlsx)(rows, out)
        marked = sum(1 for r in rows if r["revisar"])
        label = f"cap.{a.chapter}" if a.chapter else "JOGO INTEIRO"
        print(f"[export] {label}: {len(rows)} linha(s) -> {out}")
        print(f"         {marked} marcada(s) p/ avaliar; abra no Excel/LibreOffice, filtre a coluna "
              f"'Revisar', preencha 'Correcao' (texto certo) ou 'Nota' (instrucao) e devolva no inbox "
              f"({paths.qa_inbox(Path(a.project))}).")
        sys.exit(0)
    files = returned_files(Path(a.project), a.returned)
    if not files:
        print(f"[apply] nada a aplicar — nenhum .xlsx/.csv devolvido em "
              f"{a.returned or paths.qa_inbox(Path(a.project))}.")
        sys.exit(0)
    tot = {"verbatim": 0, "ai": 0, "cost": 0.0, "scenes": set(), "stopped": False}
    for f in files:
        print(f"[apply] processando revisao devolvida: {f}")
        r = apply(a.project, f, model_name=a.model, max_usd=a.max_usd)
        tot["verbatim"] += r["verbatim"]; tot["ai"] += r["ai"]; tot["cost"] += r["cost_usd"]
        tot["scenes"].update(r["scenes_touched"]); tot["stopped"] = tot["stopped"] or r.get("stopped_budget")
    print(f"[apply] TOTAL: verbatim={tot['verbatim']} (0 IA) | nota+IA={tot['ai']} (~${tot['cost']:.4f}) "
          f"| cenas tocadas={len(tot['scenes'])}")
    if tot["stopped"]:
        print(f"[apply] teto de ${a.max_usd:.2f} atingido — algumas notas (IA) nao foram processadas; "
              "verbatim entrou tudo. Re-rode com mais orcamento p/ as notas restantes.")
    print("Proximos passos: verify_chapter de cada cap. tocado (round-trip/charset) + state_index --rebuild.")
    print(f"  cenas: {', '.join(sorted(tot['scenes']))}")
    sys.exit(0)


if __name__ == "__main__":
    main()
