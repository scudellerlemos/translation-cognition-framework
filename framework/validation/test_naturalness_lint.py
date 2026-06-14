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


def _make_project(tmp: Path, lines, glossary_rows=None, token_patterns=None):
    art = tmp / "artifacts"; art.mkdir(parents=True)
    manifest = {
        "title": "T", "source_language": "en", "target_language": "pt-BR",
        "source": {"id_column": "offset", "text_column": "text_source"},
        "formatting_tokens": ["{W75}", "{W80}"],
    }
    if token_patterns is not None:
        manifest["formatting_token_patterns"] = token_patterns
    (tmp / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
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


def test_skips_localized_stammer(tmp_path):
    # inicial localizada (letra diferente do source) NÃO é resíduo — é o fix correto.
    p = _make_project(tmp_path, [("0x1", "U... Urgh...", "Nnh... Argh...")])
    assert "fragmento_residual" not in _checks(N.lint_project(p), "0x1")


def test_skips_ptbr_word_initial_stammer(tmp_path):
    # "E.../A.../O..." são palavra/artigo pt-BR — copiar a inicial não é resíduo.
    p = _make_project(tmp_path, [("0x1", "E... well...", "E... bem..."),
                                 ("0x2", "A... shop?", "A... loja?"),
                                 ("0x3", "O... milk?", "O... leite?")])
    found = N.lint_project(p)
    assert not [f for f in found if f["check"] == "fragmento_residual"]


def test_scans_per_scene_plans(tmp_path):
    # o linter varre os planos POR CENA do harness (ch_*/translation_plan_*.json), não só o legado.
    art = tmp_path / "artifacts"
    (art / "ch_11_01").mkdir(parents=True)
    (tmp_path / "project.json").write_text(json.dumps({
        "title": "T", "source_language": "en", "target_language": "pt-BR",
        "source": {"id_column": "offset", "text_column": "text_source"},
        "formatting_tokens": [],
    }), encoding="utf-8")
    plan = {"scene_group": "11_01", "lines": [
        {"offset": "0x9", "text_source": "U... Urgh...", "base_translation": "U... Argh...",
         "speaker": "A", "entities_present": [], "tone_register": "", "intent": "x",
         "risk_level": "low", "byte_budget": 1, "glossary_flags": [], "spoiler_flags": []}]}
    (art / "ch_11_01" / "translation_plan_11_01.json").write_text(
        json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    assert "fragmento_residual" in _checks(N.lint_project(tmp_path), "0x9")


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


# ----------------------------------------------------------------- onomatopeia / SFX / labels
def test_skips_consonant_grunt_but_flags_hm(tmp_path):
    # grunhido real ("Ngh","Grr","Mmf") = onomatopeia (fica); familia "hm/mm" (som de pensar) = candidato.
    p = _make_project(tmp_path, [("0x1", "Ngh...", "Ngh..."), ("0x2", "Grr...", "Grr..."),
                                 ("0x3", "Mmf!", "Mmf!"), ("0x4", "Hm?", "Hm?")])
    found = N.lint_project(p)
    assert _checks(found, "0x1") == set() and _checks(found, "0x2") == set() and _checks(found, "0x3") == set()
    assert "copia_crua" in _checks(found, "0x4")            # "Hm?" localizavel -> sinaliza


def test_skips_laugh_and_consonant_soup(tmp_path):
    p = _make_project(tmp_path, [("0x1", "Bwahahaha!", "Bwahahaha!"),
                                 ("0x2", "GLRGBBLBRLRGGLE!!!", "GLRGBBLBRLRGGLE!!!")])
    assert N.lint_project(p) == []


def test_skips_sfx_in_asterisks(tmp_path):
    p = _make_project(tmp_path, [("0x1", "*CRASH*", "*CRASH*"),
                                 ("0x2", "*Tap, tap*...", "*Tap, tap*...")])
    assert N.lint_project(p) == []


def test_skips_camelcase_and_alnum_labels(tmp_path):
    p = _make_project(tmp_path, [("0x1", "RightFoot", "RightFoot"), ("0x2", "lightA02", "lightA02")])
    assert N.lint_project(p) == []


# ----------------------------------------------------------------- tokens de cor reconhecidos
def test_strips_color_tokens(tmp_path):
    # linha só com tokens de cor (sem conteúdo alfabético real): strip_tokens via padrão deixa
    # alpha vazio -> NÃO é copia_crua. Sem o padrão, "{c5}{c-1}" viraria alpha "cc" e seria flagrado.
    p = _make_project(tmp_path, [("0x1", "{c5}{c-1}", "{c5}{c-1}")],
                      token_patterns=[r"\{c-?\d*\}"])
    assert N.lint_project(p) == []


# ----------------------------------------------------------------- instância real
@pytest.mark.skipif(not REF_PROJECT.is_dir(), reason="projeto de referência ausente")
def test_reference_no_residual_stammers():
    """Na instância real (caps 11–19, varrida pelos planos por cena), NÃO sobra stammer inicial
    copiado cru (`fragmento_residual`): os `U... Urgh...` viraram `Nnh... Argh...`. Este é o gate do
    item de stammers — a localização inicial foi aplicada e não regride."""
    findings = N.lint_project(REF_PROJECT)
    residual = [f for f in findings if f["check"] == "fragmento_residual"]
    assert not residual, f"stammer residual na instância real: {residual[:5]}"


@pytest.mark.skipif(not REF_PROJECT.is_dir(), reason="projeto de referência ausente")
def test_reference_skips_asset_identifiers():
    """Identificadores de rig/asset (`Leg_2_B_L`, `gake_parts`, `Head_toriuma`) não viram achados —
    não são diálogo."""
    import re as _re
    findings = N.lint_project(REF_PROJECT)
    leaked = [f for f in findings if _re.match(r"^[A-Za-z]\w*_\w+$", (f["target"] or "").strip())]
    assert not leaked, f"identificador de asset vazou no linter: {leaked[:5]}"
