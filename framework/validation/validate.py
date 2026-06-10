#!/usr/bin/env python3
"""
validate.py — Validation leve (B1): valida os artefatos de um projeto contra os schemas
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

RISK = {"low", "medium", "high", "critical"}
HANDLING = {"manter_original", "traduzir", "traduzir_parcial"}
SPOILER = {"none", "moderate", "major", "critical"}
CATEGORY = {"Personagem", "Local", "Facção", "Item", "Conceito", "Título", "Criatura",
            "Alimento", "Cultural", "Mecânica", "UI"}
IMPORTANCE = {"main", "secondary", "background"}
CONFIDENCE = {"high", "medium", "low"}


def _csv(p: Path) -> list[dict]:
    with p.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def validate_project(root: Path) -> list[tuple[str, str, str]]:
    """Retorna lista de (severidade, artefato, mensagem). Vazia = tudo ok."""
    root = Path(root)
    issues: list[tuple[str, str, str]] = []
    def E(art, msg): issues.append(("ERROR", art, msg))
    def W(art, msg): issues.append(("WARN", art, msg))

    pj = root / "project.json"
    if not pj.is_file():
        return [("ERROR", "project.json", f"manifesto não encontrado em {root}")]
    cfg = _json(pj)
    for k in ("title", "source_language", "target_language", "source", "formatting_tokens"):
        if not cfg.get(k):
            E("project.json", f"campo obrigatório ausente: {k}")
    src = cfg.get("source", {}) or {}
    idc = src.get("id_column", "offset")
    tokens = cfg.get("formatting_tokens", []) or []
    # Tokens parametrizados (índice variável, ex.: cor {c<N>}/{c-1}/{c-}): regex, não literais.
    rx_tokens = [re.compile(p) for p in (cfg.get("formatting_token_patterns", []) or [])]
    art = root / "artifacts"

    def has(name): return (art / name).is_file()

    # --- glossary.csv
    if has("glossary.csv"):
        for r in _csv(art / "glossary.csv"):
            term = r.get("term", "?")
            hr = (r.get("handling_rule") or "").strip()
            if not hr:
                E("glossary.csv", f"{term}: handling_rule vazio")
            elif hr not in HANDLING:
                E("glossary.csv", f"{term}: handling_rule inválido '{hr}'")
            if hr in ("traduzir", "traduzir_parcial") and not (r.get("target_translation") or "").strip():
                E("glossary.csv", f"{term}: target_translation obrigatório para handling_rule '{hr}'")
            sl = (r.get("spoiler_level") or "").strip()
            if sl and sl not in SPOILER:
                W("glossary.csv", f"{term}: spoiler_level fora do enum '{sl}'")

    # --- dialogs.csv (source, somente leitura a partir do Passo 01)
    dialog_ids: set[str] = set()
    src_text: dict[str, str] = {}
    if has("dialogs.csv"):
        rows = _csv(art / "dialogs.csv")
        tcol = "text_source" if (rows and "text_source" in rows[0]) else src.get("text_column", "")
        for r in rows:
            i = r.get(idc)
            if not i:
                E("dialogs.csv", "linha sem id"); continue
            if i in dialog_ids:
                E("dialogs.csv", f"id duplicado: {i}")
            dialog_ids.add(i)
            src_text[i] = r.get(tcol, "") or ""
            if "byte_budget" in r:
                try:
                    if int(r["byte_budget"]) < 0:
                        E("dialogs.csv", f"{i}: byte_budget < 0")
                except ValueError:
                    E("dialogs.csv", f"{i}: byte_budget não-inteiro")

    # --- approved_translations.csv (casa com dialogs + preserva tokens)
    if has("approved_translations.csv"):
        for r in _csv(art / "approved_translations.csv"):
            i = r.get(idc)
            tgt = r.get("text_target", "") or ""
            if dialog_ids and i not in dialog_ids:
                E("approved_translations.csv", f"id '{i}' não existe em dialogs.csv")
            s = src_text.get(i)
            if s is not None:
                for tk in tokens:
                    if s.count(tk) != tgt.count(tk):
                        E("approved_translations.csv", f"{i}: token {tk} {s.count(tk)}→{tgt.count(tk)}")
                # tokens parametrizados: o multiset de ocorrências deve ser idêntico (pega drop,
                # troca de índice {c5}→{c6} e desbalanceamento que a contagem literal não veria)
                for rx in rx_tokens:
                    ms, mt = sorted(rx.findall(s)), sorted(rx.findall(tgt))
                    if ms != mt:
                        E("approved_translations.csv",
                          f"{i}: token de padrão /{rx.pattern}/ não preservado verbatim {ms}→{mt}")
                if s.count("\\n") != tgt.count("\\n"):
                    W("approved_translations.csv", f"{i}: nº de quebras '\\n' difere do source")

    # --- translation_plan.json
    if has("translation_plan.json"):
        plan = _json(art / "translation_plan.json")
        lines = plan.get("lines", [])
        req = ("offset", "text_source", "speaker", "entities_present", "tone_register",
               "intent", "risk_level", "base_translation", "glossary_flags", "spoiler_flags")
        for l in lines:
            off = l.get("offset", "?")
            for k in req:
                if k not in l:
                    E("translation_plan.json", f"{off}: campo obrigatório ausente '{k}'")
            if l.get("risk_level") not in RISK:
                E("translation_plan.json", f"{off}: risk_level inválido '{l.get('risk_level')}'")
            if l.get("risk_level") in ("medium", "high", "critical") and not (l.get("risk_notes") or "").strip():
                E("translation_plan.json", f"{off}: risk_notes obrigatório para risk_level ≥ medium")
        if plan.get("total_lines") != len(lines):
            E("translation_plan.json", f"total_lines {plan.get('total_lines')} != nº de linhas {len(lines)}")
        if dialog_ids and len(lines) != len(dialog_ids):
            W("translation_plan.json", f"plano cobre {len(lines)} linhas != {len(dialog_ids)} do dialogs.csv")
        cc = sum(1 for l in lines if l.get("risk_level") == "critical")
        if plan.get("critical_lines") != cc:
            E("translation_plan.json", f"critical_lines {plan.get('critical_lines')} != contagem real {cc}")

    # --- entities.csv
    if has("entities.csv"):
        seen: set[str] = set()
        for r in _csv(art / "entities.csv"):
            cn = r.get("canonical_name", "?")
            if cn in seen:
                E("entities.csv", f"canonical_name duplicado: {cn}")
            seen.add(cn)
            if r.get("category") not in CATEGORY:
                W("entities.csv", f"{cn}: category fora do enum '{r.get('category')}'")
            if r.get("importance") not in IMPORTANCE:
                W("entities.csv", f"{cn}: importance fora do enum '{r.get('importance')}'")
            if r.get("confidence") not in CONFIDENCE:
                W("entities.csv", f"{cn}: confidence fora do enum '{r.get('confidence')}'")

    # --- aliases_map.json
    if has("aliases_map.json"):
        am = _json(art / "aliases_map.json")
        for a in am.get("aliases", []):
            for k in ("alias", "canonical_name", "spoiler_level"):
                if not a.get(k):
                    E("aliases_map.json", f"alias '{a.get('alias', '?')}': campo obrigatório ausente '{k}'")
            sl = a.get("spoiler_level", "none")
            if sl not in SPOILER:
                W("aliases_map.json", f"alias '{a.get('alias')}': spoiler_level fora do enum '{sl}'")
            if sl != "none" and not a.get("reveal_timing"):
                E("aliases_map.json", f"alias '{a.get('alias')}': reveal_timing obrigatório quando spoiler_level ≠ none")

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
