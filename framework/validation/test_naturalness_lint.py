#!/usr/bin/env python3
"""
test_naturalness_lint.py — gate do linter de naturalidade (pytest).

Prova que o linter (1) pega os smells injetados, (2) NÃO gera falso-positivo em nomes próprios,
gritos puros, ou palavras curtas legítimas, e (3) na instância real só sinaliza candidatos reais.

Rodar:  pytest framework/validation/
"""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import naturalness_lint as N  # noqa: E402

REPO = HERE.parent.parent
REF_PROJECT = REPO / "projects" / "utawarerumono"


def _make_project(tmp: Path, lines, glossary_rows=None):
    art = tmp / "artifacts"; art.mkdir(parents=True)
    (tmp / "project.json").write_text(json.dumps({
        "title": "T", "source_language": "en", "target_language": "pt-BR",
        "source": {"id_column": "offset", "text_column": "text_source"},
        "formatting_tokens": ["{W75}", "{W80}"],
    }), encoding="utf-8")
    plan = {"lines": [{"offset": o, "text_source": s, "base_translation": t,
                       "speaker": "A", "entities_present": [], "tone_register": "dialogo",
                       "intent": "x", "risk_level": "low", "byte_budget": 1,
                       "glossary_flags": [], "spoiler_flags": []} for o, s, t in lines],
            "total_lines": len(lines), "critical_lines": 0, "plan_version": "x"}
    (art / "translation_plan.json").write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    if glossary_rows:
        import csv
        with (art / "glossary.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["term", "category", "target_translation",
                                              "handling_rule", "spoiler_level"])
            w.writeheader(); w.writerows(glossary_rows)
    return tmp


def _checks(findings, offset):
    return {f["check"] for f in findings if f["offset"] == offset}


# ----------------------------------------------------------------- smells injetados
def test_flags_raw_copy(tmp_path):
    p = _make_project(tmp_path, [("0x1", "Hm?", "Hm?")])
    assert "copia_crua" in _checks(N.lint_project(p), "0x1")


def test_flags_residual_stammer(tmp_path):
    p = _make_project(tmp_path, [("0x1", "U... Urgh...", "U... Argh...")])
    assert "fragmento_residual" in _checks(N.lint_project(p), "0x1")


# ----------------------------------------------------------------- NÃO deve flagar
def test_skips_pure_scream(tmp_path):
    p = _make_project(tmp_path, [("0x1", "Aaaah!", "Aaaah!"), ("0x2", "Aaagh--", "Aaagh--")])
    assert N.lint_project(p) == []


def test_skips_proper_name_with_punct(tmp_path):
    p = _make_project(tmp_path, [("0x1", "Kuon...", "Kuon...")],
                      glossary_rows=[{"term": "Kuon", "category": "Personagem",
                                      "target_translation": "Kuon", "handling_rule": "manter_original",
                                      "spoiler_level": "none"}])
    assert N.lint_project(p) == []


def test_skips_numeric_token_line(tmp_path):
    p = _make_project(tmp_path, [("0x1", "5, {W75}4, {W80}1...", "5, {W75}4, {W80}1...")])
    assert N.lint_project(p) == []


def test_no_false_positive_on_short_word(tmp_path):
    # "a short distance away." -> "a pouca distância." : "a" é palavra, não stammer
    p = _make_project(tmp_path, [("0x1", "a short distance away.", "a pouca distancia.")])
    assert N.lint_project(p) == []


# ----------------------------------------------------------------- instância real
@pytest.mark.skipif(not REF_PROJECT.is_dir(), reason="projeto de referência ausente")
def test_reference_only_real_candidates():
    findings = N.lint_project(REF_PROJECT)
    # nenhum nome próprio / grito deve ser flagado (sem copia_crua falsa)
    assert all(f["check"] == "fragmento_residual" for f in findings), \
        f"falso-positivo de copia_crua: {[f for f in findings if f['check'] != 'fragmento_residual'][:5]}"
    # o stammer conhecido 0x3640 está na lista
    assert any(f["offset"] == "0x3640" for f in findings)
