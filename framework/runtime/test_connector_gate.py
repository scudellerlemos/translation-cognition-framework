"""test_connector_gate.py — cobre o gate de completude de conector (D6, espelha kb_gate.py).

check(root) e independente de cena (completude de conector e propriedade do PROJETO). Cobre:
scripts ausentes (hard), nenhum round-trip verde ainda (soft), test_roundtrip.py ausente (warning),
e o caminho limpo (tudo presente).
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import connector_gate as cg  # noqa: E402
import paths  # noqa: E402


def _project(root: Path, connector_cfg=None):
    (root / "project.json").write_text(
        json.dumps({"title": "T", "media_type": "game", "connector": connector_cfg or {}}),
        encoding="utf-8")


def test_hard_block_when_scripts_missing(tmp_path):
    _project(tmp_path)
    r = cg.check(tmp_path)
    assert len(r["hard_problems"]) == 2   # build_plan_script + verify_script ausentes
    assert r["problems"] == []            # nao chega a checar round-trip -- scripts nem existem


def test_soft_block_when_no_green_roundtrip_yet(tmp_path):
    _project(tmp_path)
    conn = tmp_path / "connector"
    conn.mkdir()
    (conn / "build_plan_chapter.py").write_text("# stub", encoding="utf-8")
    (conn / "verify_chapter.py").write_text("# stub", encoding="utf-8")
    r = cg.check(tmp_path)
    assert r["hard_problems"] == []
    assert len(r["problems"]) == 1
    assert "round-trip verde" in r["problems"][0]


def test_clean_when_scripts_present_and_verified_scene_exists(tmp_path):
    _project(tmp_path)
    conn = tmp_path / "connector"
    conn.mkdir()
    (conn / "build_plan_chapter.py").write_text("# stub", encoding="utf-8")
    (conn / "verify_chapter.py").write_text("# stub", encoding="utf-8")
    (conn / "test_roundtrip.py").write_text("# stub", encoding="utf-8")
    paths.run_state(tmp_path).parent.mkdir(parents=True, exist_ok=True)
    paths.run_state(tmp_path).write_text(
        json.dumps({"scenes": {"ch_12_01": {"status": "verified", "verified": True}}}), encoding="utf-8")
    r = cg.check(tmp_path)
    assert r == {"hard_problems": [], "problems": [], "warnings": []}


def test_warns_when_test_roundtrip_missing(tmp_path):
    _project(tmp_path)
    conn = tmp_path / "connector"
    conn.mkdir()
    (conn / "build_plan_chapter.py").write_text("# stub", encoding="utf-8")
    (conn / "verify_chapter.py").write_text("# stub", encoding="utf-8")
    paths.run_state(tmp_path).parent.mkdir(parents=True, exist_ok=True)
    paths.run_state(tmp_path).write_text(
        json.dumps({"scenes": {"s1": {"status": "verified", "verified": True}}}), encoding="utf-8")
    r = cg.check(tmp_path)
    assert r["hard_problems"] == [] and r["problems"] == []
    assert len(r["warnings"]) == 1 and "test_roundtrip.py" in r["warnings"][0]


def test_respects_connector_config_overrides(tmp_path):
    # project.json aponta os scripts p/ um caminho custom -- o gate deve resolver via connector_mgr,
    # nao assumir sempre connector/build_plan_chapter.py.
    _project(tmp_path, connector_cfg={"build_plan_script": "custom/bp.py", "verify_script": "custom/v.py"})
    custom = tmp_path / "custom"
    custom.mkdir()
    (custom / "bp.py").write_text("# stub", encoding="utf-8")
    (custom / "v.py").write_text("# stub", encoding="utf-8")
    r = cg.check(tmp_path)
    assert r["hard_problems"] == []   # achou nos paths customizados, nao no default


def test_no_project_json_still_reports_missing_scripts(tmp_path):
    # sem project.json -- cfg vira {} (default), ainda reporta os scripts default ausentes
    r = cg.check(tmp_path)
    assert len(r["hard_problems"]) == 2


def test_assert_fresh_read_passes_when_content_matches(tmp_path):
    p = tmp_path / "verify_chapter.py"
    p.write_text("conteudo real", encoding="utf-8")
    cg.assert_fresh_read(p, "conteudo real")   # nao levanta


def test_assert_fresh_read_raises_when_stale(tmp_path):
    p = tmp_path / "verify_chapter.py"
    p.write_text("conteudo NOVO no disco", encoding="utf-8")
    try:
        cg.assert_fresh_read(p, "conteudo antigo de memoria")
        raise AssertionError("deveria ter levantado StaleReadError")
    except cg.StaleReadError as e:
        assert "releia" in str(e)


def test_assert_fresh_read_raises_when_file_missing(tmp_path):
    try:
        cg.assert_fresh_read(tmp_path / "nao_existe.py", "qualquer coisa")
        raise AssertionError("deveria ter levantado StaleReadError")
    except cg.StaleReadError as e:
        assert "nao existe" in str(e)
