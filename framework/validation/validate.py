#!/usr/bin/env python3
"""
validate.py — Validation leve: valida os artefatos de um projeto contra os schemas
(framework/schemas/artifacts_schema.md) e os invariantes, de forma EXECUTÁVEL.

Genérico e sem dados de obra: descobre tudo lendo `project.json` (id_column, formatting_tokens) e os
artefatos em `<projeto>/artifacts/`. Valida só o que existe (o pipeline é incremental). Severidades:
- ERROR: viola schema/invariante → bloqueia (exit 1).
- WARN : suspeita não-bloqueante (ex.: enum fora da lista, contagem divergente).

Uso:  python validate.py <dir-do-projeto>     (default: diretório atual)
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

_FRAMEWORK_CONNECTORS = Path(__file__).resolve().parent.parent / "connectors"
if str(_FRAMEWORK_CONNECTORS) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK_CONNECTORS))
import connector_io  # noqa: E402  (RISK_LEVELS compartilhado entre conectores)

RISK = connector_io.RISK_LEVELS
HANDLING = {"manter_original", "traduzir", "traduzir_parcial"}
SPOILER = {"none", "moderate", "major", "critical"}
CATEGORY = {"Personagem", "Local", "Facção", "Item", "Conceito", "Título", "Criatura",
            "Alimento", "Cultural", "Mecânica", "UI"}
IMPORTANCE = {"main", "secondary", "background"}
CONFIDENCE = {"high", "medium", "low"}

Issue = tuple[str, str, str]


def _csv(p: Path) -> list[dict]:
    with p.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def _E(art: str, msg: str) -> Issue:
    return ("ERROR", art, msg)


def _W(art: str, msg: str) -> Issue:
    return ("WARN", art, msg)


def _text_col(rows: list[dict], src: dict) -> str:
    return "text_source" if (rows and "text_source" in rows[0]) else src.get("text_column", "")


def _check_risk(label: str, lines: list[dict]) -> list[Issue]:
    out: list[Issue] = []
    for l in lines:
        off = l.get("offset", "?")
        if l.get("risk_level") not in RISK:
            out.append(_E(label, f"{off}: risk_level inválido '{l.get('risk_level')}'"))
        if l.get("risk_level") in ("medium", "high", "critical") and not (l.get("risk_notes") or "").strip():
            out.append(_E(label, f"{off}: risk_notes obrigatório para risk_level ≥ medium"))
    return out


def _check_manifest(cfg: dict) -> tuple[list[Issue], list[re.Pattern]]:
    """Campos obrigatórios do project.json + compila formatting_token_patterns (regex, nao literais:
    tokens parametrizados de indice variavel, ex.: cor {c<N>}/{c-1}/{c-})."""
    out = [_E("project.json", f"campo obrigatório ausente: {k}")
           for k in ("title", "source_language", "target_language", "source", "formatting_tokens")
           if not cfg.get(k)]
    rx_tokens: list[re.Pattern] = []
    for p in (cfg.get("formatting_token_patterns", []) or []):
        try:
            rx_tokens.append(re.compile(p))
        except re.error as e:
            out.append(_E("project.json", f"formatting_token_patterns: regex inválida {p!r} ({e})"))
    return out, rx_tokens


def _check_glossary(art: Path) -> list[Issue]:
    out: list[Issue] = []
    for r in _csv(art / "glossary.csv"):
        term = r.get("term", "?")
        hr = (r.get("handling_rule") or "").strip()
        if not hr:
            out.append(_E("glossary.csv", f"{term}: handling_rule vazio"))
        elif hr not in HANDLING:
            out.append(_E("glossary.csv", f"{term}: handling_rule inválido '{hr}'"))
        if hr in ("traduzir", "traduzir_parcial") and not (r.get("target_translation") or "").strip():
            out.append(_E("glossary.csv", f"{term}: target_translation obrigatório para handling_rule '{hr}'"))
        sl = (r.get("spoiler_level") or "").strip()
        if sl and sl not in SPOILER:
            out.append(_W("glossary.csv", f"{term}: spoiler_level fora do enum '{sl}'"))
    return out


def _check_dialogs(art: Path, idc: str, src: dict) -> tuple[list[Issue], set[str], dict[str, str]]:
    """dialogs.csv (source, somente leitura a partir do Passo 01) -> (issues, ids, texto-fonte por id)."""
    out: list[Issue] = []
    dialog_ids: set[str] = set()
    src_text: dict[str, str] = {}
    rows = _csv(art / "dialogs.csv")
    tcol = _text_col(rows, src)
    for r in rows:
        i = r.get(idc)
        if not i:
            out.append(_E("dialogs.csv", "linha sem id"))
            continue
        if i in dialog_ids:
            out.append(_E("dialogs.csv", f"id duplicado: {i}"))
        dialog_ids.add(i)
        src_text[i] = r.get(tcol, "") or ""
        if "byte_budget" in r:
            try:
                if int(r["byte_budget"]) < 0:
                    out.append(_E("dialogs.csv", f"{i}: byte_budget < 0"))
            except ValueError:
                out.append(_E("dialogs.csv", f"{i}: byte_budget não-inteiro"))
    return out, dialog_ids, src_text


def _check_target(label: str, i, s: str, tgt: str, tokens: list, rx_tokens: list) -> list[Issue]:
    out: list[Issue] = []
    for tk in tokens:
        if s.count(tk) != tgt.count(tk):
            out.append(_E(label, f"{i}: token {tk} {s.count(tk)}→{tgt.count(tk)}"))
    # tokens parametrizados: o multiset de ocorrências deve ser idêntico (pega drop,
    # troca de índice {c5}→{c6} e desbalanceamento que a contagem literal não veria)
    for rx in rx_tokens:
        ms, mt = sorted(rx.findall(s)), sorted(rx.findall(tgt))
        if ms != mt:
            out.append(_E(label, f"{i}: token de padrão /{rx.pattern}/ não preservado verbatim {ms}→{mt}"))
    if s.count("\\n") != tgt.count("\\n"):
        out.append(_W(label, f"{i}: nº de quebras '\\n' difere do source"))
    return out


def _check_approved_flat(art: Path, idc: str, dialog_ids: set[str], src_text: dict[str, str],
                         tokens: list, rx_tokens: list) -> list[Issue]:
    """approved_translations.csv: casa com dialogs + preserva tokens."""
    out: list[Issue] = []
    for r in _csv(art / "approved_translations.csv"):
        i = r.get(idc)
        tgt = r.get("text_target", "") or ""
        if dialog_ids and i not in dialog_ids:
            out.append(_E("approved_translations.csv", f"id '{i}' não existe em dialogs.csv"))
        s = src_text.get(i) if i is not None else None
        if s is not None:
            out += _check_target("approved_translations.csv", i, s, tgt, tokens, rx_tokens)
    return out


def _check_scene_approved(art: Path, idc: str, src: dict, tokens: list, rx_tokens: list) -> list[Issue]:
    """Layout por cena: scenes/<cena>/dialogs.csv + approved_*.csv (o flat acima nao existe mais nos
    projetos atuais -> sem isto a preservacao de tokens NUNCA era conferida)."""
    out: list[Issue] = []
    for sd in sorted(p for p in (art / "scenes").glob("*") if p.is_dir()):
        if not (sd / "dialogs.csv").is_file():
            continue
        drows = _csv(sd / "dialogs.csv")
        tcol = _text_col(drows, src)
        scene_src = {r.get(idc): (r.get(tcol) or "") for r in drows}
        for ap in sorted(sd.glob("approved_*.csv")):
            label = f"scenes/{sd.name}/{ap.name}"
            for r in _csv(ap):
                i = r.get(idc)
                if i not in scene_src:
                    out.append(_E(label, f"id '{i}' não existe em dialogs.csv da cena"))
                else:
                    out += _check_target(label, i, scene_src[i], r.get("text_target", "") or "",
                                         tokens, rx_tokens)
    return out


def _check_plan_lines(label: str, plan: dict, required: tuple) -> list[Issue]:
    """Campos obrigatorios + risk_level/risk_notes por linha + total_lines coerente com as linhas."""
    lines = plan.get("lines", [])
    out = [_E(label, f"{l.get('offset', '?')}: campo obrigatório ausente '{k}'")
           for l in lines for k in required if k not in l]
    out += _check_risk(label, lines)
    if plan.get("total_lines") != len(lines):
        out.append(_E(label, f"total_lines {plan.get('total_lines')} != nº de linhas {len(lines)}"))
    return out


def _check_plan_legacy(art: Path, dialog_ids: set[str]) -> list[Issue]:
    """translation_plan.json (legado sem sufixo — poc_pipeline antigo)."""
    plan = _json(art / "translation_plan.json")
    lines = plan.get("lines", [])
    lab = "translation_plan.json"
    out = _check_plan_lines(lab, plan, (
        "offset", "text_source", "speaker", "entities_present", "tone_register",
        "intent", "risk_level", "base_translation", "glossary_flags", "spoiler_flags"))
    if dialog_ids and len(lines) != len(dialog_ids):
        out.append(_W(lab, f"plano cobre {len(lines)} linhas != {len(dialog_ids)} do dialogs.csv"))
    cc = sum(1 for l in lines if l.get("risk_level") == "critical")
    if plan.get("critical_lines") != cc:
        out.append(_E(lab, f"critical_lines {plan.get('critical_lines')} != contagem real {cc}"))
    return out


def _check_plans_per_scene(art: Path) -> list[Issue]:
    """translation_plan_<scene_id>.json por cena (schema real de produção; ver paths.py).
    Campos obrigatórios reduzidos ao subconjunto universal entre conectores (o resto varia:
    nem todo conector emite tone_register/intent/glossary_flags/entities_present)."""
    out: list[Issue] = []
    for pf in sorted((art / "scenes").glob("*/translation_plan_*.json")):
        out += _check_plan_lines(f"scenes/{pf.parent.name}/{pf.name}", _json(pf), (
            "offset", "text_source", "speaker", "risk_level", "base_translation"))
    return out


def _check_entities(art: Path) -> list[Issue]:
    out: list[Issue] = []
    seen: set[str] = set()
    for r in _csv(art / "entities.csv"):
        cn = r.get("canonical_name", "?")
        if cn in seen:
            out.append(_E("entities.csv", f"canonical_name duplicado: {cn}"))
        seen.add(cn)
        for col, allowed in (("category", CATEGORY), ("importance", IMPORTANCE), ("confidence", CONFIDENCE)):
            if r.get(col) not in allowed:
                out.append(_W("entities.csv", f"{cn}: {col} fora do enum '{r.get(col)}'"))
    return out


def _check_aliases(art: Path) -> list[Issue]:
    out: list[Issue] = []
    for a in _json(art / "aliases_map.json").get("aliases", []):
        for k in ("alias", "canonical_name", "spoiler_level"):
            if not a.get(k):
                out.append(_E("aliases_map.json", f"alias '{a.get('alias', '?')}': campo obrigatório ausente '{k}'"))
        sl = a.get("spoiler_level", "none")
        if sl not in SPOILER:
            out.append(_W("aliases_map.json", f"alias '{a.get('alias')}': spoiler_level fora do enum '{sl}'"))
        if sl != "none" and not a.get("reveal_timing"):
            out.append(_E("aliases_map.json",
                          f"alias '{a.get('alias')}': reveal_timing obrigatório quando spoiler_level ≠ none"))
    return out


def validate_project(root: Path) -> list[Issue]:
    """Retorna lista de (severidade, artefato, mensagem). Vazia = tudo ok."""
    root = Path(root)
    pj = root / "project.json"
    if not pj.is_file():
        return [_E("project.json", f"manifesto não encontrado em {root}")]
    cfg = _json(pj)
    issues, rx_tokens = _check_manifest(cfg)
    src = cfg.get("source", {}) or {}
    idc = src.get("id_column", "offset")
    tokens = cfg.get("formatting_tokens", []) or []
    art = root / "artifacts"

    def has(name): return (art / name).is_file()

    if has("glossary.csv"):
        issues += _check_glossary(art)
    dialog_ids: set[str] = set()
    src_text: dict[str, str] = {}
    if has("dialogs.csv"):
        d_issues, dialog_ids, src_text = _check_dialogs(art, idc, src)
        issues += d_issues
    if has("approved_translations.csv"):
        issues += _check_approved_flat(art, idc, dialog_ids, src_text, tokens, rx_tokens)
    issues += _check_scene_approved(art, idc, src, tokens, rx_tokens)
    if has("translation_plan.json"):
        issues += _check_plan_legacy(art, dialog_ids)
    issues += _check_plans_per_scene(art)
    if has("entities.csv"):
        issues += _check_entities(art)
    if has("aliases_map.json"):
        issues += _check_aliases(art)
    return issues


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    issues = validate_project(root)
    for sev, a, msg in issues:
        print(f"{sev:5} [{a}] {msg}")
    errs = sum(1 for i in issues if i[0] == "ERROR")
    print(f"\n{errs} ERRO(s), {len(issues) - errs} aviso(s).")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
