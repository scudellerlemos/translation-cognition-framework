"""test_connector_io.py — cobre os utilitarios compartilhados entre conectores (#86):
resolucao de caminho (CLI > env var > project.json) e escrita de dialogs.csv/extraction_log.md."""
import csv
import json
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import connector_io as cio  # noqa: E402


def _approved(tmp_path, header, rows):
    p = tmp_path / "approved_translations.csv"
    p.write_text("\n".join([header, *rows]) + "\n", encoding="utf-8")
    return p


def test_load_approved_reads_text_target_and_legacy_text_pt(tmp_path):
    p = _approved(tmp_path, "offset,text_target", ["0x1,Ola", "0x2,  ", ",sem-id"])
    assert cio.load_approved(p, "x") == {"0x1": "Ola"}          # espaco-so e id vazio ignorados
    p = _approved(tmp_path, "offset,text_pt", ["0x1,Legado"])
    assert cio.load_approved(p, "x") == {"0x1": "Legado"}


def test_load_approved_raises_when_rows_but_none_filled(tmp_path):
    p = _approved(tmp_path, "offset,text_en", ["0x1,coluna errada"])      # coluna nao reconhecida
    with pytest.raises(ValueError, match="nenhuma com coluna text_target/text_pt.*consequencia-x"):
        cio.load_approved(p, "consequencia-x")


def test_load_approved_empty_csv_is_not_an_error(tmp_path):
    assert cio.load_approved(_approved(tmp_path, "offset,text_target", []), "x") == {}


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


def _db_project(root):
    """project.json declarando db + o DB ja criado (o mirror do inicio do run cria)."""
    from store import Store  # noqa: E402
    root.mkdir(parents=True, exist_ok=True)
    (root / "project.json").write_text(
        json.dumps({"title": "x", "db": {"path": "p.db", "project_id": "proj"}}), encoding="utf-8")
    Store(root / "p.db").close()


def test_sync_translations_db_noop_without_db_config(tmp_path):
    (tmp_path / "project.json").write_text(json.dumps({"title": "x"}), encoding="utf-8")
    scene_dir = _scene(tmp_path)
    assert cio.sync_translations_db(tmp_path, "s1", "a", _APPROVED, _PLAN_LINES) is False
    assert not (scene_dir / "approved_a.csv").exists()


def test_sync_translations_db_does_not_create_missing_db(tmp_path):
    """DB declarado mas ainda nao criado: sync criava um DB so com traducoes e o context_pack
    trocava p/ modo DB com KB/linhas vazias. Quem cria e o mirror; aqui o caller segue flat."""
    (tmp_path / "project.json").write_text(
        json.dumps({"title": "x", "db": {"path": "p.db", "project_id": "proj"}}), encoding="utf-8")
    _scene(tmp_path)
    assert cio.sync_translations_db(tmp_path, "s1", "a", _APPROVED, _PLAN_LINES) is False
    assert not (tmp_path / "p.db").exists()


def test_sync_translations_db_writes_db_and_derives_csv(tmp_path):
    _db_project(tmp_path)
    scene_dir = _scene(tmp_path)

    assert cio.sync_translations_db(tmp_path, "s1", "a", _APPROVED, _PLAN_LINES) is True

    from store import Store  # noqa: E402
    with Store(tmp_path / "p.db") as db:
        # #216: build_plan roda antes do verify -> nada aprovado (nao vira TM) ate a cena fechar verified
        assert db.get_translations("proj") == []
        rows = {r["offset"]: r for r in db.get_translations("proj", approved_only=False)}
        db.approve_scene("proj", "s1")
        assert len(db.get_translations("proj")) == 2
    assert rows["0x1"]["target"] == "O heroi pega a Bugiganga."
    assert rows["0x1"]["speaker"] == "Hero"
    assert rows["0x2"]["target"] == "[14]Ola[01]tudo bem?"

    csv_text = (scene_dir / "approved_a.csv").read_text(encoding="utf-8").splitlines()
    assert csv_text == ["offset,text_target", "0x1,O heroi pega a Bugiganga.", "0x2,[14]Ola[01]tudo bem?"]


def test_sync_translations_db_keys_db_by_canonical_scene_id(tmp_path):
    """Cena "ch_01_02": sync gravava o nome do dir cru no DB e o migrate grava scene_id_of ("01_02")
    -> mesma cena duplicada no DB. Chave do DB = canonica; CSV continua no dir cru."""
    from migrate_from_flat import migrate  # noqa: E402
    from store import Store  # noqa: E402
    _db_project(tmp_path)
    scene_dir = _scene(tmp_path, "ch_01_02")
    assert cio.sync_translations_db(tmp_path, "ch_01_02", "a", _APPROVED, _PLAN_LINES) is True
    assert (scene_dir / "approved_a.csv").is_file()
    migrate(tmp_path, tmp_path / "p.db", project_id="proj")
    with Store(tmp_path / "p.db") as db:
        rows = db.get_translations("proj", approved_only=False)
    assert sorted({r["scene_id"] for r in rows}) == ["01_02"] and len(rows) == 2


def test_verified_scene_is_semantically_searchable_end_to_end(tmp_path):
    """#182 critério de pronto, versão forte: com Embedder/sqlite-vec REAIS (só roda se a
    stack ML estiver instalada; skip limpo em test.yml (push/PR), roda de verdade semanalmente
    em ml-coverage-optional.yml (#181)), a cena tem que aparecer em Embedder.search() assim
    que fecha verified -- pelo write-path REAL (sync_translations_db -> approve_scene_db), sem
    NENHUM passo manual (nem db index, nem migrate), e sem esperar a cena seguinte. Antes da
    aprovação (approved=0, #216) ela NÃO pode aparecer."""
    pytest.importorskip("sentence_transformers")
    pytest.importorskip("sqlite_vec")
    sys.path.insert(0, str(_HERE.parent / "runtime"))
    import state_index  # noqa: E402

    _db_project(tmp_path)
    _scene(tmp_path)
    assert cio.sync_translations_db(tmp_path, "s1", "a", _APPROVED, _PLAN_LINES) is True

    from embedder import Embedder  # noqa: E402
    from store import Store  # noqa: E402
    emb, q = Embedder(), "Hero picks up the Widget."
    with Store(tmp_path / "p.db") as db:
        assert emb.search(db._con, q, project_id="proj", k=2) == []     # ainda nao verificada
    state_index.approve_scene_db(tmp_path, "s1")    # cena fechou verified (run_scene, #216)
    with Store(tmp_path / "p.db") as db:
        hits = emb.search(db._con, q, project_id="proj", k=2)
    assert any(h["offset"] == "0x1" for h in hits), hits


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
    _db_project(dbfirst_root)
    assert cio.sync_translations_db(dbfirst_root, "s1", "a", _APPROVED, _PLAN_LINES) is True

    from store import Store  # noqa: E402
    with Store(legacy_db) as db:
        legacy_rows = {r["offset"]: (r["target"], r["speaker"], r["source"])
                       for r in db.get_translations("proj")}
    with Store(dbfirst_root / "p.db") as db:
        db.approve_scene("proj", "s1")          # cena fechou verified (run_scene, #216)
        dbfirst_rows = {r["offset"]: (r["target"], r["speaker"], r["source"])
                        for r in db.get_translations("proj")}
    assert dbfirst_rows == legacy_rows


def test_structural_match_with_capturing_group_still_compares_literals():
    """Padrao com grupo de captura nao pode cegar a checagem dos tokens literais (<C1> -> <C2>)."""
    rx = cio.structural_token_rx(["<C1>", "<C2>"], [r"\{c(\d+)\}"])
    assert not cio.structural_tokens_match(rx, "<C1>Oi {c5}", "<C2>Oi {c5}")
    assert cio.structural_tokens_match(rx, "<C1>Oi {c5}", "Ola <C1> {c5}")
    assert cio.structural_token_rx(None, None).pattern == "(?!)"   # JSON null == []


def test_structural_rx_longest_literal_first_and_rejects_empty_match():
    """Literal prefixo ("<C") nao pode engolir <C1>/<C2>; padrao que casa vazio e recusado."""
    rx = cio.structural_token_rx(["<C", "<C1>", "<C2>"], [])
    assert not cio.structural_tokens_match(rx, "<C1>x", "<C2>x")
    with pytest.raises(ValueError):
        cio.structural_token_rx([], [r"\d*"])


@pytest.mark.parametrize("tokens,patterns", [
    ("<C1>", None),            # string viraria 4 tokens de 1 char
    ([5], None),               # item nao-string
    (None, {}),                # falsy nao-lista nao pode virar [] calado
    (0, None),
    (None, [5]),               # (?:5) passaria como padrao
    (None, [r"(?P<a>x)", r"(?P<a>y)"]),   # so quebra combinado
])
def test_structural_token_rx_fails_fast_on_bad_config(tokens, patterns):
    with pytest.raises(ValueError):
        cio.structural_token_rx(tokens, patterns)


def test_structural_token_rx_wrapped_only_pattern_ok():
    rx = cio.structural_token_rx(None, [r"<c)|(\d>"])
    assert rx.search("<c") and rx.search("5>")
    problems, _, patterns = cio.structural_token_config(None, [r"<c)|(\d>"])
    assert problems == [] and patterns == [r"<c)|(\d>"]


def test_structural_token_config_combined_conflict_keeps_valid_patterns():
    problems, _, patterns = cio.structural_token_config(None, [r"(?P<a>x)", r"(?P<a>y)", "<b>"])
    assert len(problems) == 1 and "<b>" in patterns   # validate segue auditando <b> por linha


def test_transliterate_folds_accents_but_keeps_compat_glyphs_and_tokens():
    # NFD (não NFKD): ①②③ têm de sobreviver (round-trip do Utawarerumono, ch_30_09).
    assert cio.transliterate("Ação, coração é ótimo") == "Acao, coracao e otimo"
    assert cio.transliterate("①②③") == "①②③"
    assert cio.transliterate("{c5}Ação{c-1} [14][0A]") == "{c5}Acao{c-1} [14][0A]"


def test_structural_tokens_match_capture_group_pattern_distinguishes_tokens():
    """Pattern com grupo de captura (BoF4 `\\[([0-9A-Fa-f]{2})\\]`): findall devolvia so o grupo e
    trocar [01] por [02] passava. Comparacao por match inteiro tem que reprovar."""
    rx = cio.structural_token_rx([], [r"\[([0-9A-Fa-f]{2})\]"])
    assert cio.structural_tokens_match(rx, "a [01] b", "x [01] y")
    assert not cio.structural_tokens_match(rx, "a [01] b", "x [02] y")
    assert not cio.structural_tokens_match(rx, "a [01] b", "x y")
