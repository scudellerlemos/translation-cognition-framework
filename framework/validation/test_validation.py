#!/usr/bin/env python3
"""
test_validation.py — gate de regressão do validador B1 (pytest).

Prova que o validador (1) PASSA na instância de referência real e (2) PEGA violações injetadas
(não-circular). Genérico: a instância real é localizada por caminho relativo ao repo.

Rodar:  pytest framework/validation/
"""
import csv
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import validate as V  # noqa: E402

REPO = HERE.parent.parent
REF_PROJECT = REPO / "projects" / "utawarerumono"


def _errors(issues):
    return [i for i in issues if i[0] == "ERROR"]


# --------------------------------------------------------------- instância real passa
@pytest.mark.skipif(not REF_PROJECT.is_dir(), reason="projeto de referência ausente")
def test_reference_project_has_no_errors():
    issues = V.validate_project(REF_PROJECT)
    errs = _errors(issues)
    assert not errs, "validador acusou ERRO na instância de referência:\n" + \
        "\n".join(f"  [{a}] {m}" for _, a, m in errs[:15])


# --------------------------------------------------------------- helper p/ projeto mínimo sintético
def _make_project(tmp: Path, *, glossary_rows=None, plan=None, approved=None, dialogs=None):
    art = tmp / "artifacts"
    art.mkdir(parents=True)
    (tmp / "project.json").write_text(json.dumps({
        "title": "T", "source_language": "en", "target_language": "pt-BR",
        "source": {"file": "artifacts/dialogs.csv", "id_column": "offset", "text_column": "text_source"},
        "formatting_tokens": ["{W75}", "{END}"],
    }, ensure_ascii=False), encoding="utf-8")

    def wcsv(name, rows, cols):
        with (art / name).open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

    if dialogs is not None:
        wcsv("dialogs.csv", dialogs, ["offset", "text_source", "byte_budget"])
    if glossary_rows is not None:
        wcsv("glossary.csv", glossary_rows,
             ["term", "category", "target_translation", "handling_rule", "spoiler_level"])
    if approved is not None:
        wcsv("approved_translations.csv", approved, ["offset", "text_target"])
    if plan is not None:
        (art / "translation_plan.json").write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    return tmp


def _plan_line(**kw):
    base = {"offset": "0x1", "text_source": "Hi", "speaker": "A", "entities_present": [],
            "tone_register": "dialogo", "intent": "x", "risk_level": "low",
            "base_translation": "Oi", "byte_budget": 2, "glossary_flags": [], "spoiler_flags": []}
    base.update(kw)
    return base


# --------------------------------------------------------------- violações injetadas → ERRO
def test_catches_empty_handling_rule(tmp_path):
    p = _make_project(tmp_path, glossary_rows=[
        {"term": "Foo", "category": "Personagem", "target_translation": "",
         "handling_rule": "", "spoiler_level": "none"}])
    assert any("handling_rule vazio" in m for _, _, m in _errors(V.validate_project(p)))


def test_catches_missing_target_for_traduzir(tmp_path):
    p = _make_project(tmp_path, glossary_rows=[
        {"term": "Bar", "category": "Conceito", "target_translation": "",
         "handling_rule": "traduzir", "spoiler_level": "none"}])
    assert any("target_translation obrigatório" in m for _, _, m in _errors(V.validate_project(p)))


def test_catches_risk_medium_without_notes(tmp_path):
    plan = {"lines": [_plan_line(risk_level="high")], "total_lines": 1,
            "critical_lines": 0, "plan_version": "2026-01-01"}
    p = _make_project(tmp_path, plan=plan)
    assert any("risk_notes obrigatório" in m for _, _, m in _errors(V.validate_project(p)))


def test_catches_total_lines_mismatch(tmp_path):
    plan = {"lines": [_plan_line()], "total_lines": 99, "critical_lines": 0, "plan_version": "x"}
    p = _make_project(tmp_path, plan=plan)
    assert any("total_lines" in m for _, _, m in _errors(V.validate_project(p)))


def test_catches_token_drop_in_approved(tmp_path):
    p = _make_project(
        tmp_path,
        dialogs=[{"offset": "0x1", "text_source": "Wait{W75}", "byte_budget": "9"}],
        approved=[{"offset": "0x1", "text_target": "Espere"}])  # perdeu {W75}
    assert any("token {W75}" in m for _, _, m in _errors(V.validate_project(p)))


def test_clean_synthetic_project_passes(tmp_path):
    plan = {"lines": [_plan_line()], "total_lines": 1, "critical_lines": 0, "plan_version": "x"}
    p = _make_project(
        tmp_path, plan=plan,
        dialogs=[{"offset": "0x1", "text_source": "Hi", "byte_budget": "2"}],
        approved=[{"offset": "0x1", "text_target": "Oi"}],
        glossary_rows=[{"term": "Foo", "category": "Personagem", "target_translation": "Foo",
                        "handling_rule": "manter_original", "spoiler_level": "none"}])
    assert not _errors(V.validate_project(p))
