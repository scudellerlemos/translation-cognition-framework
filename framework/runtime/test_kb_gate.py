"""test_kb_gate.py — cobre o gate de cobertura de KB (hard/soft/fronteira/decisões/ratified).

kb_gate.check é determinístico (sem rede): dado o estado dos artefatos, decide bloqueio hard
(KB ausente), soft (research_log/glossary/voice/fronteira) e extrai decisões pendentes. Cada
teste parte de um projeto "bom" e perturba um artefato.
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import kb_gate  # noqa: E402
import paths  # noqa: E402


def _good(root: Path):
    art = paths.artifacts(root)
    (art / "state").mkdir(parents=True, exist_ok=True)
    (art / "universe_knowledge_base.md").write_text("# KB\nlore do mundo", encoding="utf-8")
    (art / "research_log.md").write_text("# Pesquisa\n**Status:** reconciled\n", encoding="utf-8")
    paths.glossary(root).write_text(
        "term,translation,updated_date\nDragon,Dragão,2026-01-01\n", encoding="utf-8")
    paths.voice_cards(root).parent.mkdir(parents=True, exist_ok=True)
    paths.voice_cards(root).write_text('{"Ryu": {"lines": ["x"]}}', encoding="utf-8")
    (root / "project.json").write_text(json.dumps(
        {"title": "T", "media_type": "game", "kb_frontier": "12_17"}), encoding="utf-8")


def test_good_project_passes(tmp_path):
    _good(tmp_path)
    r = kb_gate.check(tmp_path, "12_01")
    assert r["hard_problems"] == [] and r["problems"] == []


def test_reconciled_with_unratified_entity_blocks(tmp_path):
    # 'reconciled' sozinho nao basta -- entidade com conteudo afirmado precisa de
    # ratificacao humana (kb_ratified.csv), generalizado do kb_reconcile.py pro caminho MANUAL.
    _good(tmp_path)
    (paths.artifacts(tmp_path) / "universe_knowledge_base.md").write_text(
        "## Ryu\n\n**Definicao:**\nProtagonista.\n\n**Status de confianca:**\nhigh\n", encoding="utf-8")
    r = kb_gate.check(tmp_path, "12_01")
    assert any("ratificacao humana" in p and "Ryu" in p for p in r["problems"])


def test_reconciled_with_ratified_entity_passes(tmp_path):
    _good(tmp_path)
    (paths.artifacts(tmp_path) / "universe_knowledge_base.md").write_text(
        "## Ryu\n\n**Definicao:**\nProtagonista.\n\n**Status de confianca:**\nhigh\n", encoding="utf-8")
    paths.kb_ratified(tmp_path).write_text("name\nRyu\n", encoding="utf-8")
    r = kb_gate.check(tmp_path, "12_01")
    assert r["hard_problems"] == [] and r["problems"] == []


def test_unsourced_entity_never_needs_ratification(tmp_path):
    _good(tmp_path)
    (paths.artifacts(tmp_path) / "universe_knowledge_base.md").write_text(
        "## Fantasma\n\n**Definicao:**\nUNSOURCED -- nenhuma fonte menciona.\n\n"
        "**Status de confianca:**\nUNSOURCED\n", encoding="utf-8")
    r = kb_gate.check(tmp_path, "12_01")
    assert r["hard_problems"] == [] and r["problems"] == []


def test_missing_kb_is_hard(tmp_path):
    _good(tmp_path)
    (paths.artifacts(tmp_path) / "universe_knowledge_base.md").write_text("", encoding="utf-8")
    r = kb_gate.check(tmp_path, "12_01")
    assert any("universe_knowledge_base" in p for p in r["hard_problems"])


def test_research_log_not_reconciled_blocks(tmp_path):
    _good(tmp_path)
    (paths.artifacts(tmp_path) / "research_log.md").write_text("# Pesquisa\nsem status\n", encoding="utf-8")
    r = kb_gate.check(tmp_path, "12_01")
    assert any("reconciled" in p for p in r["problems"])


def test_missing_research_log_blocks(tmp_path):
    _good(tmp_path)
    (paths.artifacts(tmp_path) / "research_log.md").unlink()
    r = kb_gate.check(tmp_path, "12_01")
    assert any("research_log" in p for p in r["problems"])


def test_pending_decisions_extracted(tmp_path):
    _good(tmp_path)
    (paths.artifacts(tmp_path) / "research_log.md").write_text(
        "# Pesquisa\n**Status:** reconciled\n\n## Decisões pendentes\n"
        "1. **Alias de Fou-lu** antes do reveal\n2. Tom da Nina no prólogo\n", encoding="utf-8")
    r = kb_gate.check(tmp_path, "12_01")
    assert len(r["pending_decisions"]) == 2
    assert "Alias de Fou-lu" in r["pending_decisions"][0]


def test_human_input_pending_warns(tmp_path):
    _good(tmp_path)
    (paths.artifacts(tmp_path) / "research_log.md").write_text(
        "# Pesquisa\n**Status:** reconciled\nhuman_input: pending\n", encoding="utf-8")
    r = kb_gate.check(tmp_path, "12_01")
    assert any("human_input" in w for w in r["warnings"])


def test_voice_cards_empty_blocks(tmp_path):
    _good(tmp_path)
    paths.voice_cards(tmp_path).write_text("{}", encoding="utf-8")
    r = kb_gate.check(tmp_path, "12_01")
    assert any("voice_cards.json vazio" in p for p in r["problems"])


def test_glossary_without_updated_date_blocks(tmp_path):
    _good(tmp_path)
    paths.glossary(tmp_path).write_text("term,translation\nDragon,Dragão\n", encoding="utf-8")
    r = kb_gate.check(tmp_path, "12_01")
    assert any("updated_date" in p for p in r["problems"])


def test_kb_frontier_missing_blocks(tmp_path):
    _good(tmp_path)
    (tmp_path / "project.json").write_text('{"title":"T","media_type":"game"}', encoding="utf-8")
    r = kb_gate.check(tmp_path, "12_01")
    assert any("kb_frontier" in p for p in r["problems"])


def test_scene_beyond_frontier_blocks(tmp_path):
    _good(tmp_path)
    r = kb_gate.check(tmp_path, "13_01")   # 13 > fronteira 12_17
    assert any("ALEM da fronteira" in p for p in r["problems"])


def test_path_style_frontier_never_blocks_numeric_scene(tmp_path):
    """Regressao real (Souldiers, 2026-07-02): kb_frontier como path de projeto flat (convencao
    ja usada no BoF4: "artifacts/kb_phase_worklist.md") nao e um scene_id parseavel — _pos()
    retorna tupla vazia. Cena com segmento puramente numerico no nome (ex.: "CAVE_00" -> (0,))
    tinha `_pos(scene) > _pos(frontier vazio)` = True e era bloqueada por engano — travou 500+
    cenas do Souldiers antes do fix."""
    _good(tmp_path)
    (tmp_path / "project.json").write_text(json.dumps({
        "title": "T", "media_type": "game", "kb_frontier": "artifacts/kb_phase_worklist.md",
    }), encoding="utf-8")
    for scene in ("CAVE_00", "1_5", "CRYSTAL_1_SLIDE1_NARRATOR"):
        r = kb_gate.check(tmp_path, scene)
        assert not any("ALEM da fronteira" in p for p in r["problems"]), (scene, r["problems"])


def test_kb_ratified_without_date_col_warns(tmp_path):
    _good(tmp_path)
    paths.kb_ratified(tmp_path).write_text("entity,note\nFou-lu,vilao\n", encoding="utf-8")
    r = kb_gate.check(tmp_path, "12_01")
    assert any("kb_ratified" in w for w in r["warnings"])
