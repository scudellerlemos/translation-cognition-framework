"""test_connector_io.py — cobre os utilitarios compartilhados entre conectores (#86):
resolucao de caminho (CLI > env var > project.json) e escrita de dialogs.csv/extraction_log.md."""
import csv
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import connector_io as cio  # noqa: E402


def test_resolve_source_path_prefers_cli_arg(tmp_path, monkeypatch):
    monkeypatch.setenv("FAKE_ENV_VAR", str(tmp_path / "from_env"))
    p = cio.resolve_source_path(cli_arg=str(tmp_path / "from_cli"), env_var="FAKE_ENV_VAR")
    assert p == tmp_path / "from_cli"


def test_resolve_source_path_falls_back_to_env_var(tmp_path, monkeypatch):
    monkeypatch.setenv("FAKE_ENV_VAR", str(tmp_path / "from_env"))
    p = cio.resolve_source_path(cli_arg=None, env_var="FAKE_ENV_VAR")
    assert p == tmp_path / "from_env"


def test_resolve_source_path_falls_back_to_project_json(tmp_path, monkeypatch):
    monkeypatch.delenv("FAKE_ENV_VAR", raising=False)
    pj = tmp_path / "project.json"
    pj.write_text(json.dumps({"connector": {"data_dir": "declared/path"}}), encoding="utf-8")
    p = cio.resolve_source_path(cli_arg=None, env_var="FAKE_ENV_VAR",
                                project_json=pj, cfg_key="data_dir")
    assert p == Path("declared/path")


def test_resolve_source_path_relative_base_applies_only_to_project_json(tmp_path, monkeypatch):
    monkeypatch.delenv("FAKE_ENV_VAR", raising=False)
    pj = tmp_path / "project.json"
    pj.write_text(json.dumps({"connector": {"source_binary": "rel/bin.dat"}}), encoding="utf-8")
    p = cio.resolve_source_path(cli_arg=None, project_json=pj, cfg_key="source_binary",
                                relative_base=tmp_path)
    assert p == tmp_path / "rel/bin.dat"

    # CLI arg NAO recebe o ajuste de relative_base (comportamento original do Utawarerumono)
    p2 = cio.resolve_source_path(cli_arg="rel/bin.dat", project_json=pj, cfg_key="source_binary",
                                 relative_base=tmp_path)
    assert p2 == Path("rel/bin.dat")


def test_resolve_source_path_raises_when_nothing_resolves(tmp_path):
    pj = tmp_path / "project.json"
    pj.write_text(json.dumps({"connector": {}}), encoding="utf-8")
    try:
        cio.resolve_source_path(project_json=pj, cfg_key="data_dir",
                                error_hint="caminho nao configurado", exc=RuntimeError)
        assert False, "deveria levantar RuntimeError"
    except RuntimeError as e:
        assert "caminho nao configurado" in str(e)


def test_resolve_source_path_allow_missing_returns_none(tmp_path):
    assert cio.resolve_source_path(allow_missing=True) is None


def test_write_dialogs_csv_creates_parent_and_writes_rows(tmp_path):
    out = tmp_path / "artifacts" / "dialogs.csv"
    cio.write_dialogs_csv(out, ["offset", "text_en"], [{"offset": "0x1", "text_en": "Hi"}])
    assert out.is_file()
    assert out.read_text(encoding="utf-8").splitlines() == ["offset,text_en", "0x1,Hi"]


def test_write_extraction_log_creates_parent_and_writes_text(tmp_path):
    out = tmp_path / "artifacts" / "extraction_log.md"
    cio.write_extraction_log(out, "# Log\n\nOK\n")
    assert out.read_text(encoding="utf-8") == "# Log\n\nOK\n"


def test_normalize_speaker_matches_canonical_case_insensitive():
    assert cio.normalize_speaker("Ryu", frozenset({"Ryu", "Nina"})) == "Ryu"
    assert cio.normalize_speaker("ryu", frozenset({"Ryu", "Nina"})) == "Ryu"


def test_normalize_speaker_maps_system_words_as_whole_tokens():
    assert cio.normalize_speaker("System", frozenset()) == "system"
    assert cio.normalize_speaker("Narrator", frozenset()) == "system"
    assert cio.normalize_speaker("Instructor", frozenset()) == "system"


def test_normalize_speaker_does_not_match_system_words_as_substring():
    # achado do code review: regex sem word-boundary classificava qualquer nome que
    # CONTIVESSE "system"/"narrator"/etc. como falante de sistema (ex.: "Ecosystem Guardian").
    assert cio.normalize_speaker("Ecosystem Guardian", frozenset()) == "npc"
    assert cio.normalize_speaker("Narratorial Kin", frozenset()) == "npc"


def test_normalize_speaker_unknown_for_empty():
    assert cio.normalize_speaker("", frozenset()) == "unknown"


# ── sync_translations_db (#109, Fase 6b: produtores DB-first) ──────────────────────────────

_DB_DIR = str(Path(__file__).resolve().parents[1] / "db")
if _DB_DIR not in sys.path:
    sys.path.insert(0, _DB_DIR)


def _scene(tmp_path, scene_id="s1"):
    d = tmp_path / "artifacts" / "scenes" / scene_id
    d.mkdir(parents=True)
    return d


_PLAN_LINES = [
    {"offset": "0x1", "text_source": "Hero picks up the Widget.", "speaker": "Hero",
     "risk_level": "low", "base_translation": "O heroi pega a Bugiganga."},
    {"offset": "0x2", "text_source": "Hero says hello.", "speaker": "Hero",
     "risk_level": "medium", "risk_notes": "tom informal", "base_translation": "[14]Ola[01]tudo bem?"},
]
_APPROVED = [(ln["offset"], ln["base_translation"]) for ln in _PLAN_LINES]


def test_sync_translations_db_noop_without_db_config(tmp_path):
    (tmp_path / "project.json").write_text(json.dumps({"title": "x"}), encoding="utf-8")
    scene_dir = _scene(tmp_path)
    assert cio.sync_translations_db(tmp_path, "s1", "a", _APPROVED, _PLAN_LINES) is False
    assert not (scene_dir / "approved_a.csv").exists()


def test_sync_translations_db_writes_db_and_derives_csv(tmp_path):
    (tmp_path / "project.json").write_text(
        json.dumps({"title": "x", "db": {"path": "p.db", "project_id": "proj"}}), encoding="utf-8")
    scene_dir = _scene(tmp_path)

    assert cio.sync_translations_db(tmp_path, "s1", "a", _APPROVED, _PLAN_LINES) is True

    from store import Store  # noqa: E402
    with Store(tmp_path / "p.db") as db:
        rows = {r["offset"]: r for r in db.get_translations("proj")}
    assert rows["0x1"]["target"] == "O heroi pega a Bugiganga."
    assert rows["0x1"]["speaker"] == "Hero"
    assert rows["0x2"]["target"] == "[14]Ola[01]tudo bem?"

    csv_text = (scene_dir / "approved_a.csv").read_text(encoding="utf-8").splitlines()
    assert csv_text == ["offset,text_target", "0x1,O heroi pega a Bugiganga.", "0x2,[14]Ola[01]tudo bem?"]


def test_sync_translations_db_reindexes_embeddings_no_ml_deps(tmp_path):
    """#182: sync_translations_db (write-path real de run_scene/run_chapter) chama
    reindex_pending_embeddings automaticamente, igual ao #171 já fazia em migrate(). Sem
    sentence-transformers/sqlite-vec (CI), a chamada é silenciosa (None) — não quebra a
    escrita da TM. Verificamos via Store.reindex_pending_embeddings diretamente (mesma
    conexão/arquivo que sync_translations_db acabou de escrever) que ela não levanta."""
    (tmp_path / "project.json").write_text(
        json.dumps({"title": "x", "db": {"path": "p.db", "project_id": "proj"}}), encoding="utf-8")
    _scene(tmp_path)
    assert cio.sync_translations_db(tmp_path, "s1", "a", _APPROVED, _PLAN_LINES) is True

    from store import Store  # noqa: E402
    with Store(tmp_path / "p.db") as db:
        result = db.reindex_pending_embeddings("proj")
    assert result is None or result >= 0, result


def test_sync_translations_db_matches_legacy_flat_then_migrate_oracle(tmp_path):
    """Inverso do oráculo de round-trip do #109 (mesma ideia de test_export_roundtrip_lossless,
    invertida): produtor DB-first (sync_translations_db) direto no Store DEVE bater com o
    caminho legado (produtor grava flat -> migrate_from_flat.migrate() espelha pro Store) para
    os MESMOS dados de entrada — nenhuma regressão de paridade na virada de fonte de verdade."""
    from migrate_from_flat import migrate  # noqa: E402

    # caminho legado: producer escreve flat (dialogs.csv + translation_plan + approved.csv),
    # depois migrate() espelha flat -> DB.
    legacy_root = tmp_path / "legacy"
    legacy_scene = _scene(legacy_root)
    (legacy_root / "project.json").write_text(json.dumps({"title": "x"}), encoding="utf-8")
    with (legacy_scene / "dialogs.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["offset", "text_source"])
        for ln in _PLAN_LINES:
            w.writerow([ln["offset"], ln["text_source"]])
    (legacy_scene / "translation_plan_a.json").write_text(
        json.dumps({"lines": _PLAN_LINES}, ensure_ascii=False), encoding="utf-8")
    with (legacy_scene / "approved_a.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["offset", "text_target"])
        w.writerows(_APPROVED)
    legacy_db = tmp_path / "legacy.db"
    migrate(legacy_root, legacy_db, project_id="proj")

    # caminho DB-first: producer grava direto no Store via sync_translations_db.
    dbfirst_root = tmp_path / "dbfirst"
    _scene(dbfirst_root)
    (dbfirst_root / "project.json").write_text(
        json.dumps({"title": "x", "db": {"path": "p.db", "project_id": "proj"}}), encoding="utf-8")
    assert cio.sync_translations_db(dbfirst_root, "s1", "a", _APPROVED, _PLAN_LINES) is True

    from store import Store  # noqa: E402
    with Store(legacy_db) as db:
        legacy_rows = {r["offset"]: (r["target"], r["speaker"], r["source"])
                       for r in db.get_translations("proj")}
    with Store(dbfirst_root / "p.db") as db:
        dbfirst_rows = {r["offset"]: (r["target"], r["speaker"], r["source"])
                        for r in db.get_translations("proj")}
    assert dbfirst_rows == legacy_rows
