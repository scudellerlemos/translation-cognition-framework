"""test_validate_extra.py — exercita os ramos de validate_project (schema/invariantes por artefato)."""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import validate  # noqa: E402


def test_missing_project_json(tmp_path):
    issues = validate.validate_project(tmp_path)
    assert issues[0][0] == "ERROR" and "project.json" in issues[0][1]


def test_clean_minimal_no_artifacts(tmp_path):
    (tmp_path / "project.json").write_text(json.dumps(
        {"title": "T", "source_language": "en", "target_language": "pt-BR",
         "source": {"id_column": "offset"}, "formatting_tokens": ["[01]"]}), encoding="utf-8")
    (tmp_path / "artifacts").mkdir()
    assert validate.validate_project(tmp_path) == []          # nada a validar (incremental)


def test_all_artifacts_with_issues(tmp_path):
    root = tmp_path
    (root / "project.json").write_text(json.dumps({
        "title": "T", "source_language": "en", "target_language": "pt-BR",
        "source": {"id_column": "offset", "text_column": "text_en"},
        "formatting_tokens": ["[01]"], "formatting_token_patterns": [r"\{c\d+\}"]}), encoding="utf-8")
    art = root / "artifacts"
    art.mkdir()
    (art / "glossary.csv").write_text(
        "term,handling_rule,target_translation,spoiler_level\n"
        "Dragon,traduzir,,major\n"           # traduzir sem target_translation -> E
        "Bad,xpto,,none\n"                    # handling_rule inválido -> E
        "Empty,,,badenum\n", encoding="utf-8")   # handling vazio -> E; spoiler fora do enum -> W
    (art / "dialogs.csv").write_text(
        "offset,text_en,byte_budget\n"
        "X:0:1,Hi [01] {c5},10\n"
        "X:0:2,dup,10\n"
        "X:0:2,dup again,10\n"                # id duplicado -> E
        "X:0:3,neg,-5\n"                      # byte_budget < 0 -> E
        "X:0:4,bad,abc\n", encoding="utf-8")     # byte_budget não-int -> E
    (art / "approved_translations.csv").write_text(
        "offset,text_target\n"
        "X:0:1,Oi\n"                          # perde [01] e {c5} -> E (token + padrão)
        "X:0:9,Orfao\n", encoding="utf-8")       # id fora do dialogs -> E
    (art / "translation_plan.json").write_text(json.dumps({
        "lines": [{"offset": "X:0:1", "risk_level": "high"}],   # faltam campos + risk_notes -> E
        "total_lines": 5, "critical_lines": 3}), encoding="utf-8")
    (art / "entities.csv").write_text(
        "canonical_name,category,importance,confidence\n"
        "Ryu,BadCat,main,high\n"             # category fora do enum -> W
        "Ryu,Personagem,main,high\n", encoding="utf-8")   # canonical duplicado -> E
    (art / "aliases_map.json").write_text(json.dumps(
        {"aliases": [{"alias": "X", "canonical_name": "", "spoiler_level": "major"}]}), encoding="utf-8")

    issues = validate.validate_project(root)
    sevs = {i[0] for i in issues}
    msgs = " ".join(i[2] for i in issues)
    assert "ERROR" in sevs and "WARN" in sevs
    for needle in ("handling_rule", "byte_budget", "token [01]", "critical_lines",
                   "canonical_name duplicado", "reveal_timing"):
        assert needle in msgs, needle


def test_inline_flag_pattern_flagged_like_runtime(tmp_path):
    """Flag inline "(?i)..." compila solta mas quebra na forma (?:...) do runtime -> ERROR aqui."""
    (tmp_path / "project.json").write_text(json.dumps(
        {"title": "T", "source_language": "en", "target_language": "pt-BR",
         "source": {"id_column": "offset"}, "formatting_token_patterns": [r"(?i)<c\d>"]}),
        encoding="utf-8")
    (tmp_path / "artifacts").mkdir()
    assert any("formatting_token_patterns" in i[2] for i in validate.validate_project(tmp_path))


def test_capture_group_pattern_compares_whole_token_and_empty_match_flagged(tmp_path):
    """validate compara o token inteiro (group(0)), nao so o grupo; padrao que casa vazio -> ERROR."""
    (tmp_path / "project.json").write_text(json.dumps(
        {"title": "T", "source_language": "en", "target_language": "pt-BR",
         "source": {"id_column": "offset"}, "formatting_token_patterns": [r"<(C)\d+>"]}),
        encoding="utf-8")
    art = tmp_path / "artifacts"
    art.mkdir()
    (art / "dialogs.csv").write_text("offset,text_en\nX:1,<C1>Hi\n", encoding="utf-8")
    (art / "approved_translations.csv").write_text("offset,text_target\nX:1,<C2>Oi\n", encoding="utf-8")
    assert any("X:1" in i[2] for i in validate.validate_project(tmp_path) if i[0] == "ERROR")
    (tmp_path / "project.json").write_text(json.dumps(
        {"title": "T", "source_language": "en", "target_language": "pt-BR",
         "source": {"id_column": "offset"}, "formatting_token_patterns": [r"\d*", 5]}),
        encoding="utf-8")
    errs = [i[2] for i in validate.validate_project(tmp_path) if i[0] == "ERROR"]
    assert any("nao-string" in m for m in errs)
    assert any("casa string vazia" in m for m in errs)   # item ruim nao esconde o erro de vazio


def test_non_string_formatting_token_reported_not_crash(tmp_path):
    (tmp_path / "project.json").write_text(json.dumps(
        {"title": "T", "source_language": "en", "target_language": "pt-BR",
         "source": {"id_column": "offset"}, "formatting_tokens": ["<C1>", 5]}), encoding="utf-8")
    (tmp_path / "artifacts").mkdir()
    errs = [i[2] for i in validate.validate_project(tmp_path) if i[0] == "ERROR"]
    assert any("item invalido 5" in m for m in errs)
    (tmp_path / "project.json").write_text(json.dumps(
        {"title": "T", "source_language": "en", "target_language": "pt-BR",
         "source": {"id_column": "offset"}, "formatting_tokens": "<C1>"}), encoding="utf-8")
    errs = [i[2] for i in validate.validate_project(tmp_path) if i[0] == "ERROR"]
    assert any("deve ser lista" in m for m in errs)   # string nao vira 4 tokens de 1 char
