"""test_scaffold_kb_gate.py — trava de regressao pro gap real do onboarding do Souldiers:
scaffold_project.py e kb_gate.py sao mantidos por skills/codigo separados e ja
divergiram silenciosamente 2x (glossary.csv sem 'updated_date'; universe_knowledge_base.md nunca
scaffoldado). Este teste roda o par ponta-a-ponta pra qualquer divergencia futura quebrar aqui,
nao num piloto pago de outro jogo.
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import connector_gate  # noqa: E402
import kb_gate  # noqa: E402
import paths  # noqa: E402
import scaffold_project  # noqa: E402
import state_index  # noqa: E402


def _write_project_json(root: Path, title: str) -> None:
    (root / "project.json").write_text(json.dumps({
        "title": title, "media_type": "game", "kb_frontier": "00_00",
    }), encoding="utf-8")


def test_scaffold_glossary_has_updated_date_column():
    assert "updated_date" in scaffold_project._GLOSSARY_HEADERS


def test_fresh_scaffold_alone_still_fails_kb_gate(tmp_path):
    """scaffold() NAO deve, sozinho, satisfazer o gate — senao o hard-block de pesquisa
    reconciliada (governanca anti-fabricacao) estaria sendo furado por um placeholder."""
    scaffold_project.scaffold(tmp_path, title="T")
    _write_project_json(tmp_path, "T")
    r = kb_gate.check(tmp_path, "00_00")
    assert r["hard_problems"], "scaffold sozinho nao pode passar o hard-gate (sem pesquisa real)"


def test_scaffold_plus_real_kb_content_passes_gate(tmp_path):
    """Reproduz o fluxo completo: scaffold -> preencher como a skill 03/04 preencheria ->
    state_index.build() deriva voice_cards -> kb_gate.check() deve passar limpo."""
    scaffold_project.scaffold(tmp_path, title="T")
    _write_project_json(tmp_path, "T")
    art = paths.artifacts(tmp_path)

    (art / "universe_knowledge_base.md").write_text(
        "## PersonagemA\n\n**Definicao:**\nlore real, com fonte.\n\n**Fontes:**\n- SRC-001\n",
        encoding="utf-8")
    (art / "research_log.md").write_text(
        "# Research Log — T\n\n**Status:** reconciled\n\n## Fontes Avaliadas\n"
        "| ID | Fonte | Tier |\n|----|-------|------|\n| SRC-001 | Wiki | 2 |\n",
        encoding="utf-8")

    import csv
    glossary_path = art / "glossary.csv"
    with glossary_path.open("a", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerow(
            ["Dragon", "creature", "Dragao", "verbatim", "none", "", "", "2026-01-01"])

    # tone_analysis.md ja sai do scaffold com o marcador certo (### Nome — `voice_criticality: X`)
    # para PersonagemA/B/C — nao precisa editar para o gate/build_voice_cards reconhecerem.

    state_index.build(tmp_path, sync_db=False)

    r = kb_gate.check(tmp_path, "00_00")
    assert r["hard_problems"] == [], r["hard_problems"]
    assert r["problems"] == [], r["problems"]


def test_scaffold_reports_missing_connector_without_creating_fake_stub(tmp_path):
    """scaffold() NAO deve criar stub fake de build_plan_chapter.py/verify_chapter.py --
    so reportar o que falta (mesma governanca do KB: nunca engana o gate com placeholder)."""
    scaffold_project.scaffold(tmp_path, title="T")
    _write_project_json(tmp_path, "T")
    assert not (tmp_path / "connector" / "build_plan_chapter.py").is_file()
    assert not (tmp_path / "connector" / "verify_chapter.py").is_file()
    r = connector_gate.check(tmp_path)
    assert r["hard_problems"], "scaffold sozinho nao deve satisfazer o connector_gate"


def test_scaffold_plus_real_connector_scripts_passes_gate(tmp_path):
    scaffold_project.scaffold(tmp_path, title="T")
    _write_project_json(tmp_path, "T")
    conn = tmp_path / "connector"
    conn.mkdir()
    (conn / "build_plan_chapter.py").write_text("# real", encoding="utf-8")
    (conn / "verify_chapter.py").write_text("# real", encoding="utf-8")
    (conn / "test_roundtrip.py").write_text("# real", encoding="utf-8")
    paths.run_state(tmp_path).parent.mkdir(parents=True, exist_ok=True)
    paths.run_state(tmp_path).write_text(
        json.dumps({"scenes": {"s1": {"status": "verified", "verified": True}}}), encoding="utf-8")
    r = connector_gate.check(tmp_path)
    assert r == {"hard_problems": [], "problems": [], "warnings": []}
