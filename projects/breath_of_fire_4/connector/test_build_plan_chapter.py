"""
test_build_plan_chapter.py — Breath of Fire IV

Cobre #64: speaker_code (determinístico, extraído do binário) deve ter
precedência sobre o guess do LLM ao resolver o falante de cada linha.

Rodar: pytest connector/test_build_plan_chapter.py -v
"""
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "connector"))
sys.path.insert(0, str(PROJECT_ROOT.parent.parent / "framework" / "connectors"))
from build_plan_chapter import _load_portrait_codes, _resolve_speaker  # noqa: E402
from connector_io import normalize_speaker as _normalize_speaker  # noqa: E402

CANONICAL = frozenset({"Ryu", "Nina", "npc", "system", "unknown"})


def test_resolve_speaker_prefers_mapped_code_over_llm_guess():
    """Caminho principal: código mapeado resolve determinístico, mesmo se o LLM discordar."""
    portrait_codes = {"[14][05]": "Nina"}
    resolved = _resolve_speaker("[14][05]", "npc", portrait_codes, CANONICAL)
    assert resolved == "Nina"


def test_resolve_speaker_falls_back_to_llm_when_code_unmapped():
    """Código presente mas ausente de portrait_codes -> cai no guess do LLM normalizado."""
    portrait_codes = {"[14][05]": "Nina"}
    resolved = _resolve_speaker("[14][C6]", "Ryu", portrait_codes, CANONICAL)
    assert resolved == "Ryu"


def test_resolve_speaker_without_code_keeps_previous_behavior():
    """Sem speaker_code (ex.: narração) -> comportamento inalterado (guess do LLM ou unknown)."""
    portrait_codes = {"[14][05]": "Nina"}
    assert _resolve_speaker("", "npc", portrait_codes, CANONICAL) == "npc"
    assert _resolve_speaker("", "", portrait_codes, CANONICAL) == "unknown"


def test_resolve_speaker_matches_normalize_speaker_when_no_mapping_exists():
    """Tabela vazia (estado atual real) -> idêntico a _normalize_speaker direto."""
    for guess in ("Ryu", "narrator", "algum npc qualquer", ""):
        assert _resolve_speaker("[14][01]", guess, {}, CANONICAL) == _normalize_speaker(guess, CANONICAL)


def test_load_portrait_codes_missing_file_returns_empty(tmp_path):
    assert _load_portrait_codes(tmp_path) == {}


def test_load_portrait_codes_skips_meta_key(tmp_path):
    state_dir = tmp_path / "artifacts" / "state"
    state_dir.mkdir(parents=True)
    (state_dir / "portrait_codes.json").write_text(
        json.dumps({"_meta": {"status": "vazio"}, "[14][05]": "Nina"}),
        encoding="utf-8",
    )
    codes = _load_portrait_codes(tmp_path)
    assert codes == {"[14][05]": "Nina"}
    assert "_meta" not in codes


def test_load_portrait_codes_real_file_has_no_code_entries_yet():
    """A tabela real do projeto ainda não tem nenhum código confirmado (#64 continuação)."""
    codes = _load_portrait_codes(PROJECT_ROOT)
    assert codes == {}
