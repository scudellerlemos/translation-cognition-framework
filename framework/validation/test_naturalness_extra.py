"""test_naturalness_extra.py — exercita os checks do linter de naturalidade + as exceções."""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import naturalness_lint as nl  # noqa: E402


def _proj(root: Path, plan_lines):
    (root / "project.json").write_text(json.dumps(
        {"title": "T", "source": {"id_column": "offset"}, "formatting_tokens": ["[01]"]}),
        encoding="utf-8")
    art = root / "artifacts"
    art.mkdir()
    (art / "glossary.csv").write_text(
        "term,handling_rule,category\nMenu,traduzir,UI\nKuon,manter_original,Personagem\n",
        encoding="utf-8")
    (art / "translation_plan.json").write_text(
        json.dumps({"lines": plan_lines}), encoding="utf-8")


def _P(off, s, t):
    return {"offset": off, "text_source": s, "base_translation": t, "speaker": ""}


def test_all_checks_and_exceptions(tmp_path):
    _proj(tmp_path, [
        _P("o1", "Hello", "Hello"),                 # copia_crua
        _P("o6", "Menu", "Menu"),                   # rotulo_cru (UI em labels)
        _P("o3", "U... Argh...", "U... Caramba..."),  # fragmento_residual (U copiado)
        _P("o7", "K... Kuon?", "K... Kuon!"),       # gagueira de NOME PROPRIO -> ok
        _P("o4", "RightFoot", "RightFoot"),         # asset CamelCase -> ok
        _P("o5", "*CRASH*", "*CRASH*"),             # SFX entre asteriscos -> ok
        _P("o8", "Aaaah!", "Aaaah!"),               # onomatopeia pura -> ok
        _P("o9", "Ngh", "Ngh"),                     # grunhido sem vogal -> ok
    ])
    found = nl.lint_project(tmp_path)
    by = {f["offset"]: f["check"] for f in found}
    assert by.get("o1") == "copia_crua"
    assert by.get("o6") == "rotulo_cru"
    assert by.get("o3") == "fragmento_residual"
    for ok in ("o4", "o5", "o7", "o8", "o9"):        # exceções: nada reportado
        assert ok not in by


def test_dialogs_approved_path(tmp_path):
    """Sem plano: usa dialogs.csv + approved_translations.csv."""
    (tmp_path / "project.json").write_text(json.dumps(
        {"title": "T", "source": {"id_column": "offset"}, "formatting_tokens": []}), encoding="utf-8")
    art = tmp_path / "artifacts"
    art.mkdir()
    (art / "dialogs.csv").write_text("offset,text_source\nX:0:1,Hello\n", encoding="utf-8")
    (art / "approved_translations.csv").write_text("offset,text_target\nX:0:1,Hello\n", encoding="utf-8")
    found = nl.lint_project(tmp_path)
    assert any(f["offset"] == "X:0:1" and f["check"] == "copia_crua" for f in found)


def test_is_pure_onomatopoeia():
    assert nl._is_pure_onomatopoeia("Aaaah!") is True       # vogal repetida
    assert nl._is_pure_onomatopoeia("hahaha") is True       # risada
    assert nl._is_pure_onomatopoeia("Grr") is True          # sem vogal
    assert nl._is_pure_onomatopoeia("Hello") is False       # palavra real
