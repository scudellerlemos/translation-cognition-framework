#!/usr/bin/env python3
"""
hitl.py — HUMANO NO LACO: os pontos do pipeline em que a decisao e do humano, nao da IA.

Liga com `"hitl": true` no project.json (projeto sem a chave segue como antes). Quatro pecas:

  ESCOPO     aceite humano do corpus extraido (cenas/linhas) antes de traduzir. Re-extracao que muda os
             numeros reabre o aceite.                              -> `accept-scope`
  GLOSSARIO  os termos mais frequentes do glossario pedem ratificacao humana (kb_ratified.csv, o mesmo
             arquivo das entidades da KB). AVISO: nao bloqueia.     -> `ratify`
  ONDA       a cada WAVE_SCENES cenas recem-verificadas sai uma amostra para o humano ler.
             AVISO: nao bloqueia.                                   -> `ack`
  FILA       escalonamento: fala em que a forma do glossario nao entrou, ou que o tradutor marcou com
             `escalate`, vai para uma planilha em vez de a IA decidir sozinha. O humano responde com
             `alias` (a forma usada passa a valer: vira regra no glossario) ou `correcao` (texto certo).
             Item aberto bloqueia o quality_gate.                   -> `resolve`

So bloqueia o que e decisao de verdade: escopo, caminho e a fila (ambiguidade). Glossario frequente e onda
sao relatorio — ratificar/dar visto em serie nao achava problema e virava cerimonia.

O gate roda no CLI do run_scene (antes do lote); a fila e o ponto de controle sao alimentados depois dele.
Toda decisao humana fica em artifacts/hitl_log.jsonl (quem, quando, o que — sem o texto da fala).
Decisao dada em conversa e registrada por um assistente leva `--quote "frase literal do humano"`: o log
guarda via=conversa + a frase. Sem frase literal do humano nao ha registro (aviso de sistema ou relatorio
de agente nao e decisao).

Uso:
  python hitl.py status       <projeto>
  python hitl.py accept-scope <projeto> --reviewer NOME
  python hitl.py ratify       <projeto> --reviewer NOME [TERMO ...]     (sem termo = todos os pendentes)
  python hitl.py ack          <projeto> --reviewer NOME
  python hitl.py resolve      <projeto> --reviewer NOME
  (qualquer um, fora o status)          [--quote "frase do humano na conversa"]
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import io
import json
import re
import sys
import time
from datetime import date
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import artifact_io  # noqa: E402
import context_pack  # noqa: E402
import events  # noqa: E402
import glossary_lint  # noqa: E402
import paths  # noqa: E402

RATIFY_TOP = 30     # termos mais frequentes do glossario que exigem ratificacao antes de escalar
WAVE_SCENES = 10    # cenas recem-verificadas que abrem um ponto de controle
WAVE_SAMPLE = 15    # falas da onda mostradas ao humano
QUEUE_COLS = ["scene", "offset", "kind", "term", "expected", "source_en", "target_pt", "reason",
              "alias", "correcao"]


def _cfg(root: Path) -> dict:
    p = paths.project_json(root)
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def enabled(root) -> bool:
    return bool(_cfg(Path(root)).get("hitl"))


_VIA: dict = {}     # {"via": "conversa", "quote": ...} quando a decisao veio da conversa (--quote)


def _log(root: Path, **rec) -> None:
    rec = {**rec, **_VIA}
    with (paths.artifacts(root) / "hitl_log.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"t": round(time.time(), 3), **rec}, ensure_ascii=False) + "\n")


def _state_path(root: Path) -> Path:
    return paths.artifacts(root) / "hitl_state.json"


def _state(root: Path) -> dict:
    p = _state_path(root)
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def _save_state(root: Path, state: dict) -> None:
    _state_path(root).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


# --- escopo -----------------------------------------------------------------------------------------
def corpus(root: Path) -> tuple[int, int, str]:
    """(cenas, linhas, texto-fonte concatenado) do corpus extraido: dialogs.csv unico, ou um por cena."""
    flat = paths.dialogs_flat(root)
    files = [flat] if flat.is_file() else sorted(paths.scenes_dir(root).glob("*/dialogs.csv"))
    scenes, lines, text = set(), 0, []
    for f in files:
        with f.open(encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                scenes.add(r.get("file") or f.parent.name)
                lines += 1
                text.append(" ".join(v for v in r.values() if isinstance(v, str)))
    return len(scenes), lines, "\n".join(text)


def accepted_scope(root: Path) -> dict | None:
    """Ultimo aceite de escopo registrado no hitl_log.jsonl (versionado: o aceite acompanha o projeto)."""
    p = paths.artifacts(root) / "hitl_log.jsonl"
    recs = [json.loads(ln) for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()] if p.is_file() else []
    return next((r for r in reversed(recs) if r.get("kind") == "escopo"), None)


def scope_problems(root: Path, n_scenes: int, n_lines: int) -> list[str]:
    acc = accepted_scope(root)
    if not acc:
        return [f"escopo da extracao sem aceite humano ({n_scenes} cenas, {n_lines} linhas) — confira o que "
                f"entra e o que fica de fora e rode: hitl.py accept-scope <projeto> --reviewer NOME"]
    if (acc.get("scenes"), acc.get("lines")) != (n_scenes, n_lines):
        return [f"o corpus mudou desde o aceite ({acc.get('scenes')} cenas/{acc.get('lines')} linhas -> "
                f"{n_scenes}/{n_lines}) — re-extracao reabre o aceite: hitl.py accept-scope"]
    return []


# --- caminho (sessao ou api) ------------------------------------------------------------------------
def chosen_path(root: Path) -> dict | None:
    p = paths.artifacts(root) / "hitl_log.jsonl"
    recs = [json.loads(ln) for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()] if p.is_file() else []
    return next((r for r in reversed(recs) if r.get("kind") == "caminho"), None)


def path_problems(root: Path, backend: str) -> list[str]:
    """Um projeto, um caminho: tradutor e modelo mudam entre sessao e api, entao misturar muda o estilo.
    Quem escolhe (e quem troca) e um humano; o run_scene so roda no caminho escolhido."""
    ch = chosen_path(root)
    if not ch:
        return ["caminho do projeto (sessao ou api) sem decisao humana — rode: "
                "hitl.py choose-path <projeto> in-session|api --reviewer NOME"]
    if ch.get("backend") != backend:
        return [f"projeto decidido para o caminho '{ch.get('backend')}' por {ch.get('by')}; pedido '{backend}'. "
                f"Trocar e decisao humana: hitl.py choose-path <projeto> {backend} --reviewer NOME"]
    return []


# --- glossario --------------------------------------------------------------------------------------
def pending_glossary(root: Path, text: str, top: int = RATIFY_TOP) -> list[tuple[str, str, int]]:
    """[(termo, forma canonica, ocorrencias)] dos `top` termos mais frequentes ainda sem ratificacao."""
    import kb_reconcile
    ratified = kb_reconcile._ratified_set(root)
    counted = []
    for term, expected, _rule in glossary_lint._load_glossary(root):
        flags = 0 if term != term.lower() else re.I      # mesma regra de caixa do glossary_lint
        n = len(re.findall(r"(?<!\w)" + re.escape(term) + r"(?![\w'’])", text, flags))
        if n:
            counted.append((term, expected[0], n))
    counted.sort(key=lambda x: (-x[2], x[0]))
    return [c for c in counted[:top] if c[0].lower() not in ratified]


# --- ponto de controle por onda ---------------------------------------------------------------------
def note_verified(root: Path, scenes: list[str]) -> bool:
    """Acumula cenas recem-verificadas; ao chegar a WAVE_SCENES grava a amostra. True se ha onda aberta."""
    if not scenes:
        return len(_state(root).get("wave", [])) >= WAVE_SCENES
    p = _state_path(root)
    with paths.locked(p):      # lotes em paralelo terminam juntos
        state = _state(root)
        wave = sorted(set(state.get("wave", [])) | set(scenes))
        state["wave"] = wave
        _save_state(root, state)
    if len(wave) < WAVE_SCENES:
        return False
    rows = []
    for s in wave:
        for ln in artifact_io.plan_lines(root, s):
            h = hashlib.sha1(f"{s}|{ln.get('offset', '')}".encode(), usedforsecurity=False).hexdigest()
            rows.append((h, s, ln.get("offset", ""), ln.get("text_source", ""), ln.get("base_translation", "")))
    out = paths.qa_outbox(root)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "onda_amostra.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["scene", "offset", "source_en", "target_pt"])
        w.writerows(r[1:] for r in sorted(rows)[:WAVE_SAMPLE])   # ordem do hash = amostra estavel
    return True


def wave_problems(root: Path, scenes: list[str]) -> list[str]:
    wave = _state(root).get("wave", [])
    fresh = [s for s in scenes if not paths.pack(root, s).is_file()]
    if len(wave) >= WAVE_SCENES and fresh:
        return [f"ponto de controle aberto: {len(wave)} cenas verificadas sem visto humano — amostra em "
                f"{paths.qa_outbox(root) / 'onda_amostra.csv'}; visto: hitl.py ack <projeto> --reviewer NOME"]
    return []


# --- gate (antes do lote) ---------------------------------------------------------------------------
def gate(root, scenes: list[str], backend: str | None = None) -> list[str]:
    root = Path(root)
    n_scenes, n_lines, text = corpus(root)
    problems = scope_problems(root, n_scenes, n_lines)
    if backend:
        problems += path_problems(root, backend)
    notes = wave_problems(root, scenes)          # glossario e onda: aviso, nao bloqueio
    pend = pending_glossary(root, text)
    if pend:
        notes.append(f"{len(pend)} dos {RATIFY_TOP} termos mais frequentes do glossario sem ratificacao humana "
                     f"({', '.join(p[0] for p in pend[:6])}{' ...' if len(pend) > 6 else ''}) — veja hitl.py status")
    for n in notes:
        print(f"[hitl] aviso (nao bloqueia): {n}")
    events.emit(root, "gate.hitl", "block" if problems else "pass", problems=len(problems))
    return problems


# --- fila de escalonamento --------------------------------------------------------------------------
def queue_path(root: Path) -> Path:
    return paths.qa_outbox(root) / "escalonamento.csv"


def read_queue(root: Path) -> list[dict]:
    p = queue_path(root)
    if not p.is_file():
        return []
    with p.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def _write_queue(root: Path, rows: list[dict]) -> None:
    p = queue_path(root)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=QUEUE_COLS)
        w.writeheader()
        w.writerows({c: r.get(c, "") for c in QUEUE_COLS} for r in rows)


def open_items(root) -> list[dict]:
    return [r for r in read_queue(Path(root)) if not (r.get("alias") or r.get("correcao") or "").strip()]


def enqueue(root: Path, items: list[dict]) -> int:
    """Acrescenta itens novos (chave: cena+offset+termo). Item ja respondido nao e reaberto."""
    if not items:
        return 0
    queue_path(root).parent.mkdir(parents=True, exist_ok=True)
    with paths.locked(queue_path(root)):
        rows = read_queue(root)
        seen = {(r["scene"], r["offset"], r["term"]) for r in rows}
        new = [i for i in items if (i["scene"], i["offset"], i.get("term", "")) not in seen]
        if new:
            _write_queue(root, rows + new)
    return len(new)


def prune(root: Path, findings: list[dict]) -> int:
    """Fecha item `glossario` sem resposta que o lint nao acusa mais (a causa sumiu: nao ha o que decidir)."""
    live = {(context_pack.scene_id_of(f["scene"]), f["offset"], f["term"]) for f in findings}
    if not queue_path(root).is_file():
        return 0
    with paths.locked(queue_path(root)):
        rows = read_queue(root)
        gone = [r for r in rows if r.get("kind") == "glossario" and not (r.get("alias") or r.get("correcao") or "").strip()
                and (context_pack.scene_id_of(r["scene"]), r["offset"], r["term"]) not in live]
        if gone:
            _write_queue(root, [r for r in rows if r not in gone])
    for r in gone:
        _log(root, kind="escalonamento", by="glossary_lint", scene=r["scene"], offset=r["offset"],
             term=r["term"], action="fechado: o lint nao acusa mais")
    return len(gone)


def collect(root: Path, scenes: list[str], findings: list[dict] | None = None) -> list[dict]:
    """Itens de escalonamento das cenas: forma do glossario ausente + pedido do tradutor (`escalate`)."""
    by_id = {context_pack.scene_id_of(s): s for s in scenes}
    items = []
    for f in glossary_lint.lint(root) if findings is None else findings:
        s = by_id.get(context_pack.scene_id_of(f["scene"]))
        if s:
            items.append({"scene": s, "offset": f["offset"], "kind": "glossario", "term": f["term"],
                          "expected": f["expected"], "source_en": f["source"], "target_pt": f["target"],
                          "reason": "a forma do glossario nao esta na traducao"})
    for s in scenes:
        tf = paths.translations(root, s, context_pack.scene_id_of(s))
        lines = json.loads(tf.read_text(encoding="utf-8")).get("lines", {}) if tf.is_file() else {}
        src = {ln.get("offset", ""): ln.get("text_source", "") for ln in artifact_io.plan_lines(root, s)}
        for off, v in lines.items():
            if isinstance(v, dict) and v.get("escalate"):
                items.append({"scene": s, "offset": off, "kind": "tradutor", "term": "", "expected": "",
                              "source_en": src.get(off, ""), "target_pt": v.get("t", ""),
                              "reason": str(v["escalate"])})
    return items


def after_batch(root, verified: list[str], newly: list[str]) -> None:
    """Depois do lote: alimenta a fila com as cenas verificadas e conta as recem-verificadas na onda."""
    root = Path(root)
    findings = glossary_lint.lint(root)
    gone = prune(root, findings)
    if gone:
        print(f"[hitl] {gone} item(ns) de glossario fechado(s): o lint nao acusa mais")
    n = enqueue(root, collect(root, verified, findings))
    if n:
        print(f"[hitl] {n} fala(s) na fila de escalonamento -> {queue_path(root)} (decisao humana; "
              f"bloqueia o quality_gate ate hitl.py resolve)")
    if note_verified(root, newly):
        print(f"[hitl] amostra da onda -> {paths.qa_outbox(root) / 'onda_amostra.csv'} (aviso; nao bloqueia)")


def _add_alias(root: Path, term: str, alias: str) -> bool:
    """A forma aceita pelo humano vira alias do termo no glossary.csv (a regra passa a valer p/ o lint)."""
    p = paths.glossary(root)
    if not p.is_file():
        return False
    raw = p.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    txt = raw.decode("utf-8-sig")
    nl = "\r\n" if "\r\n" in txt else "\n"
    rows = list(csv.DictReader(io.StringIO(txt)))
    hit = False
    for r in rows:
        if r.get("term") == term:
            have = [a for a in re.split(r"[;|]", r.get("aliases") or "") if a.strip()]
            if alias not in have:
                r["aliases"] = ";".join(have + [alias])
                if "updated_date" in r:
                    r["updated_date"] = date.today().isoformat()
            hit = True
    if hit:
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator=nl)
        w.writeheader()
        w.writerows(rows)
        p.write_bytes((b"\xef\xbb\xbf" if bom else b"") + buf.getvalue().encode("utf-8"))
    return hit


def resolve(root, reviewer: str) -> dict:
    """Aplica as respostas da planilha: `alias` vira regra no glossario; `correcao` entra verbatim na cena."""
    root = Path(root)
    import quality_review  # tardio: puxa o model
    rows, left, fixes = read_queue(root), [], {}
    n_alias = 0
    for r in rows:
        alias, fix = (r.get("alias") or "").strip(), (r.get("correcao") or "").strip()
        if fix:
            fixes.setdefault(r["scene"], []).append((r["offset"], fix))
        elif alias and r.get("term") and _add_alias(root, r["term"], alias):
            n_alias += 1
        else:
            left.append(r)
            continue
        _log(root, kind="escalonamento", by=reviewer, scene=r["scene"], offset=r["offset"],
             term=r.get("term", ""), action="correcao" if fix else "alias", alias=alias if not fix else "")
    n_fix = sum(quality_review._apply_verbatim(root, s, pairs) for s, pairs in fixes.items())
    _write_queue(root, left)
    return {"alias": n_alias, "correcao": n_fix, "open": len(left), "scenes": sorted(fixes)}


# --- CLI --------------------------------------------------------------------------------------------
def _sync_ratified(root: Path) -> None:
    """Modo banco: quem le a ratificacao e o SQLite (kb_review._ratified_set); espelha a planilha nele."""
    db_path, db_pid = context_pack._db_path(root, _cfg(root))
    kr = paths.kb_ratified(root)
    if not db_path or not kr.is_file():
        return
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "db"))
    from store import Store
    with kr.open(encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if (r.get("name") or "").strip()]
    with Store(db_path) as db:
        db.upsert_kb_ratified(db_pid, rows)


def _ratify(root: Path, reviewer: str, terms: list[str]) -> int:
    _sync_ratified(root)          # antes: o que ja esta na planilha nao volta como pendente
    n = _ratify_csv(root, reviewer, terms)
    _sync_ratified(root)
    return n


def _ratify_csv(root: Path, reviewer: str, terms: list[str]) -> int:
    if terms:      # termo nomeado: vale qualquer entrada do glossario, nao so as mais frequentes
        import kb_reconcile
        known = {g[0].lower(): g[0] for g in glossary_lint._load_glossary(root)}
        done = kb_reconcile._ratified_set(root)
        for t in terms:
            if t.lower() not in known:
                print(f"[hitl] '{t}' nao esta no glossario — ignorado.", file=sys.stderr)
        todo = list(dict.fromkeys(known[t.lower()] for t in terms if t.lower() in known and t.lower() not in done))
    else:
        todo = [p[0] for p in pending_glossary(root, corpus(root)[2])]
    kr = paths.kb_ratified(root)
    new = not kr.is_file()
    with kr.open("a", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["name", "ratified_by", "date", "note"])
        for t in todo:
            w.writerow([t, reviewer, date.today().isoformat(), "glossario: termo ratificado (hitl)"])
            _log(root, kind="glossario", by=reviewer, term=t, action="ratify")
    return len(todo)


def main():
    with contextlib.suppress(AttributeError, ValueError, OSError):
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    ap = argparse.ArgumentParser(description="Humano no laco: aceite de escopo, ratificacao, onda e fila.")
    ap.add_argument("cmd", choices=["status", "accept-scope", "choose-path", "ratify", "ack", "resolve"])
    ap.add_argument("project")
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--reviewer", default=None, help="quem decide (obrigatorio fora do status)")
    ap.add_argument("--quote", default=None,
                    help="frase literal do humano, quando a decisao veio da conversa e quem registra e um assistente")
    a = ap.parse_args()
    if a.quote is not None:
        if not a.quote.strip():
            ap.error("--quote vazio: sem a frase literal do humano nao ha decisao a registrar")
        _VIA.update(via="conversa", quote=a.quote.strip())
    root = Path(a.project)
    if a.cmd != "status" and not a.reviewer:
        ap.error("--reviewer NOME e obrigatorio: a decisao e de um humano e fica registrada")
    if a.cmd == "status":
        n_scenes, n_lines, text = corpus(root)
        cfg = _cfg(root)
        print(f"hitl {'LIGADO' if cfg.get('hitl') else 'desligado (project.json sem \"hitl\")'}")
        for p in scope_problems(root, n_scenes, n_lines) or [f"escopo aceito ({n_scenes} cenas, {n_lines} linhas)"]:
            print(f"  escopo   : {p}")
        ch = chosen_path(root)
        print(f"  caminho  : {ch['backend'] + ' (por ' + str(ch.get('by')) + ')' if ch else 'sem decisao — hitl.py choose-path'}")
        pend = pending_glossary(root, text)
        print(f"  glossario: {len(pend)} termo(s) frequente(s) sem ratificacao")
        for term, target, n in pend:
            print(f"      {n:5}x  {term} -> {target}")
        wave = _state(root).get("wave", [])
        print(f"  onda     : {len(wave)} cena(s) verificada(s) sem visto"
              + (" — PONTO DE CONTROLE ABERTO" if len(wave) >= WAVE_SCENES else f" (abre com {WAVE_SCENES})"))
        print(f"  fila     : {len(open_items(root))} item(ns) aberto(s) em {queue_path(root)}")
    elif a.cmd == "accept-scope":
        n_scenes, n_lines, _ = corpus(root)
        _log(root, kind="escopo", by=a.reviewer, scenes=n_scenes, lines=n_lines, action="accept")
        print(f"escopo aceito por {a.reviewer}: {n_scenes} cenas, {n_lines} linhas.")
    elif a.cmd == "choose-path":
        if a.terms not in (["in-session"], ["api"]):
            ap.error("choose-path pede o caminho: in-session ou api")
        prev = chosen_path(root)
        _log(root, kind="caminho", by=a.reviewer, backend=a.terms[0], action="choose",
             previous=prev.get("backend") if prev else None)
        print(f"caminho do projeto: {a.terms[0]}, decidido por {a.reviewer}"
              + (f" (antes: {prev.get('backend')})." if prev and prev.get("backend") != a.terms[0] else "."))
    elif a.cmd == "ratify":
        print(f"{_ratify(root, a.reviewer, a.terms)} termo(s) ratificado(s) por {a.reviewer} em {paths.kb_ratified(root)}.")
    elif a.cmd == "ack":
        with paths.locked(_state_path(root)):
            state = _state(root)
            wave = state.pop("wave", [])
            _save_state(root, state)
        _log(root, kind="onda", by=a.reviewer, scenes=len(wave), action="ack")
        print(f"visto de {a.reviewer} em {len(wave)} cena(s); proxima onda liberada.")
    else:
        r = resolve(root, a.reviewer)
        print(f"fila: {r['alias']} alias no glossario, {r['correcao']} correcao(oes) aplicada(s), {r['open']} em aberto.")
        if r["alias"]:
            print("  glossario mudou: rode state_index.py <projeto> (projeto com banco) antes do proximo lint.")
        if r["scenes"]:
            print(f"  re-rode o run_scene destas cenas (round-trip + retrotraducao): {' '.join(r['scenes'])}")


if __name__ == "__main__":
    main()
