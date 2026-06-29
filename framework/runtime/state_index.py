#!/usr/bin/env python3
"""
state_index.py — constroi o ESTADO EXTERNO CONSULTAVEL do projeto (memoria fora da janela da LLM).

Parte do harness `framework/runtime/` (generico, reusavel). Tira da sessao a "memoria de
consistencia" que hoje vive no chat: em vez de recarregar capitulos anteriores na janela, o
context_pack consulta estes indices.

Gera (em `<projeto>/artifacts/state/`):
  - translation_memory.jsonl  : 1 linha por fala ja traduzida -> {scene, offset, speaker,
                                source, target, src_key}. src_key = sha1(source normalizado).
                                Fonte: TODOS os translation_plan*.json (raiz + ch_*/), que ja
                                carregam text_source + speaker + base_translation.
  - voice_cards.json          : {personagem -> {criticality, lines[]}} destilado do tone_analysis.md
                                (<=~300 tok/card). So a voz, sem o resto do contexto narrativo.
  - decision_index.json       : [{title, tags[], universal, summary}] derivado do decision_log.md
                                (## secoes). Permite carregar SO as decisoes relevantes a uma cena.

GOVERNANCA: codigo determinista, sem rede, sem work-text hardcoded. Idempotente: rodar 2x ->
saidas byte-identicas (ordenacao estavel, sem timestamps/random). Reconstruivel a partir dos artefatos.

Uso:  python state_index.py <dir-do-projeto> [--rebuild]
      (--rebuild apenas reescreve; o comportamento e o mesmo, idempotente.)
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import paths  # noqa: E402  (paths.py: fonte unica do contrato de caminhos de artefato)
from config import GLOSSARY_STALENESS_DAYS  # noqa: E402

# --- caracteristicas universais do conector que TODA cena precisa (decisoes sempre incluidas) ---
UNIVERSAL_DECISION_HINTS = (
    "ponteiro", "opcode", "charset", "translit", "token", "cor", "conector",
    "reinser", "byte", "relocac", "pack", "acento",
)
# stopwords pt p/ derivar tags do titulo das decisoes (evita ruido)
_STOP = {
    "de", "do", "da", "dos", "das", "e", "o", "a", "os", "as", "no", "na", "nos", "nas",
    "um", "uma", "por", "para", "pra", "com", "sem", "em", "ao", "aos", "que", "the",
    "of", "+", "-", "medido", "real", "data", "tipo", "passo",
}


def _norm(s: str) -> str:
    """Normaliza p/ chave de TM: minusculo, espacos colapsados, sem pontuacao de borda."""
    s = (s or "").replace("\\n", " ").lower()
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _key(s: str) -> str:
    return hashlib.sha1(_norm(s).encode("utf-8"), usedforsecurity=False).hexdigest()[:16]


def _slug_tags(title: str) -> list[str]:
    words = re.findall(r"[0-9a-zA-ZçáàâãéêíóôõúüÇÁÀÂÃÉÊÍÓÔÕÚÜ_]+", title.lower())
    tags = []
    for w in words:
        if len(w) >= 4 and w not in _STOP and w not in tags:
            tags.append(w)
    return tags


# ----------------------------- Translation Memory -----------------------------

def build_tm(art: Path) -> list[dict]:
    """Le todos os translation_plan*.json (raiz + subdirs) -> entradas de TM, ordenadas e dedup."""
    entries: dict[str, dict] = {}
    plan_files = sorted(art.glob("translation_plan*.json")) + \
        sorted(art.glob("*/translation_plan*.json"))
    for pf in plan_files:
        try:
            data = json.loads(pf.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        lines = data.get("lines", [])
        # 'lines' pode ser lista (translation_plan_*) — schema canonico do build_plan
        if isinstance(lines, dict):
            lines = [{"offset": k, **v} for k, v in lines.items()]
        scene = data.get("scene_group") or pf.stem.replace("translation_plan_", "").replace(
            "translation_plan", "root")
        # V4: tenta ler pack.json da cena para registrar doctrine_version por entrada de TM
        scene_pack = art / pf.parent.name / "pack.json" if pf.parent != art else None
        doctrine_version = ""
        if scene_pack and scene_pack.is_file():
            try:
                doctrine_version = json.loads(
                    scene_pack.read_text(encoding="utf-8")).get("doctrine_hash", "")
            except Exception:
                pass
        for ln in lines:
            src = ln.get("text_source", "")
            tgt = ln.get("base_translation", ln.get("t", ""))
            if not src or not tgt:
                continue
            off = ln.get("offset", "")
            ent = {
                "scene": scene,
                "offset": off,
                "speaker": ln.get("speaker", ""),
                "source": src,
                "target": tgt,
                "src_key": _key(src),
                "doctrine_version": doctrine_version,
            }
            # dedup por (scene, offset); ultimo plano vence (planos de capitulo > raiz)
            entries[f"{scene}|{off}"] = ent
    return [entries[k] for k in sorted(entries)]


# ------------------------------- Voice Cards ----------------------------------

def build_voice_cards(tone_md: str) -> dict:
    """Extrai perfis de voz do tone_analysis.md. Best-effort, tolerante ao formato.

    Captura blocos '### Nome — `voice_criticality: X`' + bullets seguintes, e linhas inline
    '- **Nome** — `voice_criticality: X`. ...' das secoes de atualizacao.
    """
    cards: dict[str, dict] = {}
    crit_re = re.compile(r"voice_criticality:\s*([a-z]+)")
    _ARTICLES = ("a ", "o ", "as ", "os ")

    def parse_name(raw: str):
        """Retorna (primary, aliases[]) limpos e matchaveis a partir do cabecalho de perfil."""
        # remove o sufixo de criticality e tudo apos o traco que o precede
        raw = re.sub(r"[—-]\s*`?voice_criticality.*$", "", raw)
        raw = re.sub(r"\([^)]*\)", " ", raw)          # tira parenteticos (canonico/spoiler)
        raw = raw.split("—")[0]                        # corta em em-dash residual
        cands = [c for c in re.split(r"[/]", raw) if c.strip()]
        clean = []
        for c in cands:
            c = c.replace("*", "").replace('"', "").strip().strip(".").strip()
            low = c.lower()
            for art in _ARTICLES:                      # tira artigo inicial ("A Garota" -> "Garota")
                if low.startswith(art):
                    c = c[len(art):].strip()
                    break
            if c:
                clean.append(c)
        if not clean:
            return None, []
        # primary = candidato mais curto e nao-vazio (rotulo enxuto); aliases = todos distintos
        primary = min(clean, key=len)
        aliases = []
        for c in clean:
            if c != primary and c not in aliases:
                aliases.append(c)
        return primary, aliases

    lines = tone_md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        h = re.match(r"^###\s+(.*)$", line)
        inl = re.match(r"^[-*]\s+\*\*(.+?)\*\*\s*[—-].*?voice_criticality", line)
        if h:
            nm, aliases = parse_name(h.group(1))
            crit = crit_re.search(line)
            i += 1
            if nm is None:
                continue
            card = cards.setdefault(nm, {"criticality": "", "aliases": [], "lines": []})
            if crit:
                card["criticality"] = crit.group(1)
            card["aliases"] = sorted(set(card["aliases"]) | set(aliases))
            while i < len(lines) and not lines[i].startswith("#"):
                b = lines[i].strip()
                if b.startswith(("-", "*")):
                    txt = re.sub(r"\s+", " ", b.lstrip("-* ").strip())
                    if txt:
                        card["lines"].append(txt[:240])
                i += 1
            continue
        if inl:
            nm, aliases = parse_name(inl.group(1))
            crit = crit_re.search(line)
            if nm is not None:
                card = cards.setdefault(nm, {"criticality": "", "aliases": [], "lines": []})
                if crit and not card["criticality"]:
                    card["criticality"] = crit.group(1)
                card["aliases"] = sorted(set(card["aliases"]) | set(aliases))
                txt = re.sub(r"\s+", " ", line.lstrip("-* ").strip())
                card["lines"].append(txt[:240])
        i += 1
    # poda cada card a <= 6 bullets (limite ~300 tok) + limpa marcadores de negrito
    for c in cards.values():
        c["lines"] = [re.sub(r"\*+", "", x).strip() for x in c["lines"]][:6]
    return dict(sorted(cards.items()))


# ----------------------------- Decision Index ---------------------------------

def build_decision_index(log_md: str) -> list[dict]:
    """Quebra o decision_log.md em secoes '## ' -> {title, tags, universal, summary}."""
    out = []
    blocks = re.split(r"\n##\s+", "\n" + log_md)
    for b in blocks:
        b = b.strip()
        if not b or b.startswith("#"):           # pula o titulo/preambulo (linha markdown iniciada por #)
            continue
        title = b.splitlines()[0].strip()
        if not title or title.lower().startswith("decision log"):
            continue
        body = b[len(title):]
        # summary = primeiras linhas uteis (ignora metadados **Data/Passo/Tipo**)
        summary_lines = []
        for ln in body.splitlines():
            t = ln.strip()
            if not t or t.startswith(("**Data", "**Passo", "**Tipo", "---")):
                continue
            t = re.sub(r"\s+", " ", t)
            summary_lines.append(t)
            if len(" ".join(summary_lines)) > 260:
                break
        summary = " ".join(summary_lines)[:300]
        tl = title.lower()
        universal = any(h in tl for h in UNIVERSAL_DECISION_HINTS)
        out.append({"title": title, "tags": _slug_tags(title),
                    "universal": universal, "summary": summary})
    return out


# --------------------------------- driver -------------------------------------

def build(root: Path) -> dict:
    root = Path(root)
    art = paths.artifacts(root)
    state = paths.state_dir(root)
    state.mkdir(parents=True, exist_ok=True)

    tm = build_tm(art)
    cards = build_voice_cards(_read(paths.tone_analysis(root)))
    decisions = build_decision_index(_read(paths.decision_log(root)))

    # TM como JSONL ordenado e estavel
    tm_txt = "\n".join(json.dumps(e, ensure_ascii=False, sort_keys=True) for e in tm)
    (paths.translation_memory(root)).write_text(tm_txt + ("\n" if tm else ""), encoding="utf-8")
    (paths.voice_cards(root)).write_text(
        json.dumps(cards, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    (paths.decision_index(root)).write_text(
        json.dumps(decisions, ensure_ascii=False, indent=2), encoding="utf-8")
    warnings = []

    # Voice cards completeness: falantes com falas na TM mas sem card de voz
    tm_speakers = {e["speaker"] for e in tm if e.get("speaker")}
    def _has_card(sp):
        if sp in cards:
            return True
        return any(sp in c.get("aliases", []) for c in cards.values())
    missing = sorted(s for s in tm_speakers if not _has_card(s))
    if missing:
        warnings.append(f"{len(missing)} falante(s) sem voice card: {missing[:5]}"
                        + (" ..." if len(missing) > 5 else ""))

    # Governanca do glossario: verifica coluna updated_date e detecta termos com revisao atrasada.
    import csv as _csv
    gp = paths.glossary(root)
    if gp.is_file():
        try:
            with gp.open(encoding="utf-8-sig", newline="") as fh:
                hdr = next(_csv.reader(fh), [])
            hdr_clean = [h.strip() for h in hdr]
            if "updated_date" not in hdr_clean:
                warnings.append("glossary.csv sem coluna 'updated_date' — adicione p/ rastrear "
                                 "quando cada termo foi revisado pela ultima vez.")
            else:
                import datetime as _dt
                threshold = (
                    _dt.date.today() - _dt.timedelta(days=GLOSSARY_STALENESS_DAYS)
                ).isoformat()
                ud_idx = hdr_clean.index("updated_date")
                stale = 0
                with gp.open(encoding="utf-8-sig", newline="") as fh2:
                    rdr = _csv.reader(fh2)
                    next(rdr, None)         # pula cabecalho
                    for row in rdr:
                        val = row[ud_idx].strip() if ud_idx < len(row) else ""
                        if val and val < threshold:
                            stale += 1
                if stale:
                    warnings.append(f"{stale} termo(s) do glossario com updated_date "
                                    f"> {GLOSSARY_STALENESS_DAYS} dias — considere revisar.")
        except Exception:
            pass

    # persiste avisos em warnings.jsonl (agregado permanente — nao so stdout)
    if warnings:
        import time as _time
        rec = {"t": round(_time.time(), 3), "source": "state_index", "warnings": warnings}
        wlog = paths.warnings_log(root)
        try:
            with wlog.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        except OSError:
            pass

    return {"tm": len(tm), "cards": len(cards), "decisions": len(decisions),
            "dir": state, "warnings": warnings}


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def _check_sync(root: Path) -> None:
    """V4: lista cenas com doctrine_version diferente da doutrina atual."""
    import importlib
    rt_dir = str(Path(__file__).resolve().parent)
    if rt_dir not in sys.path:
        sys.path.insert(0, rt_dir)
    cp = importlib.import_module("context_pack")
    current = cp._doctrine_hash(root)
    tm_path = paths.translation_memory(root)
    if not tm_path.is_file():
        print("TM vazia — nenhuma cena traduzida.")
        return
    entries = [json.loads(ln) for ln in tm_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    stale = {e["scene"] for e in entries
             if e.get("doctrine_version") and e["doctrine_version"] != current}
    no_ver = {e["scene"] for e in entries if not e.get("doctrine_version")}
    print(f"Doutrina atual: {current}")
    if stale:
        print(f"{len(stale)} cena(s) com doutrina desatualizada:")
        for s in sorted(stale):
            print(f"  {s}")
    if no_ver:
        print(f"{len(no_ver)} cena(s) sem doctrine_version (traduzidas antes do versionamento):")
        for s in sorted(no_ver):
            print(f"  {s}")
    if not stale and not no_ver:
        print("OK: todas as cenas sincronizadas com a doutrina atual.")


def main():
    if "--check-sync" in sys.argv:
        flags = [a for a in sys.argv[1:] if not a.startswith("--")]
        root = Path(flags[0]) if flags else Path(".")
        if not (root / "project.json").is_file():
            sys.exit(f"ERRO: project.json nao encontrado em {root}")
        _check_sync(root)
        sys.exit(0)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = Path(args[0]) if args else Path(".")
    if not (root / "project.json").is_file():
        sys.exit(f"ERRO: project.json nao encontrado em {root}")
    r = build(root)
    print(f"OK state_index -> {r['dir']}")
    print(f"  translation_memory: {r['tm']} entradas")
    print(f"  voice_cards: {r['cards']} personagens")
    print(f"  decision_index: {r['decisions']} decisoes")


if __name__ == "__main__":
    main()
