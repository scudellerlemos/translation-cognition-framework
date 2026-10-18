import json

import paths
import session_lot as sl


def test_rebreak_matches_break_count_without_dangling_words():
    assert sl.rebreak('a[01]b c', 'um dois tres quatro') == 'um dois[01]tres quatro'
    assert sl.rebreak('a b', 'um[01]dois') == 'um dois'
    assert sl.rebreak('a[01]b', 'um[01]dois') == 'um[01]dois'
    assert sl.rebreak('a[01]b', 'ele foi para a casa dela') == 'ele foi[01]para a casa dela'
    assert sl.rebreak('a[01]b', 'ele veio, mas nao quis ficar') == 'ele veio,[01]mas nao quis ficar'


def test_plan_groups_scenes_and_leaves_duplicates_out(tmp_path):
    (tmp_path / "project.json").write_text(json.dumps({}), encoding="utf-8")
    for sc, txt in (("ch_1_01", "Hi"), ("ch_1_02", "Hi"), ("ch_1_03", "Bye")):
        d = paths.scene_dir(tmp_path, sc)
        d.mkdir(parents=True)
        (d / "dialogs.csv").write_text(f"offset,text_source\nX:{sc}:1,{txt}\n", encoding="utf-8")
    sl._init(tmp_path)
    out = tmp_path / "plan.json"
    sl.cmd_plan(out)
    plan = json.loads(out.read_text(encoding="utf-8"))
    assert plan["lots"] == [{"scenes": ["ch_1_01", "ch_1_03"], "lines": 2}]
    assert plan["dups"] == {"ch_1_01": ["ch_1_02"]}


def test_install_only_changed_files_and_keeps_backup(tmp_path):
    out, src, game = (tmp_path / n for n in ("out", "src", "game"))
    for d in (out, src, game):
        d.mkdir()
    (src / "A.DAT").write_bytes(b"orig")
    (game / "A.DAT").write_bytes(b"orig")
    (out / "A.DAT").write_bytes(b"new")
    (src / "B.DAT").write_bytes(b"same")
    (out / "B.DAT").write_bytes(b"same")
    sl.cmd_install(out, src, game, go=True)
    assert (game / "A.DAT").read_bytes() == b"new" and (game / "A.DAT.bak").read_bytes() == b"orig"
    assert not (game / "B.DAT").exists()


def _lote(tmp_path, source="Oi[01]mundo", budget=None):
    """Projeto minimo com 1 cena e 1 lote: pack.json, meta e (opcional) traducao ja gravada."""
    (tmp_path / "project.json").write_text(json.dumps({}), encoding="utf-8")
    sc, off = "ch_1_01", "ch_1_01.DAT:1:1"
    d = paths.scene_dir(tmp_path, sc)
    d.mkdir(parents=True)
    row = {"offset": off, "source": source, **({"byte_budget": budget} if budget else {})}
    paths.pack(tmp_path, sc).write_text(json.dumps({"lines": [row]}), encoding="utf-8")
    sl._init(tmp_path)
    (sl.TMP / "lot_1.meta.json").write_text(json.dumps({"dup": {}, "offsets": [off]}), encoding="utf-8")
    return sc, off


def _grava(sc, off, t, **extra):
    import context_pack
    p = paths.translations(sl.ROOT, sc, context_pack.scene_id_of(sc))
    p.write_text(json.dumps({"lines": {off: {"t": t, **extra}}}), encoding="utf-8")


def test_check_ok_quando_tokens_e_orcamento_batem(tmp_path, capsys):
    sc, off = _lote(tmp_path, budget=20)
    _grava(sc, off, "Ola[01]mundo")
    sl.cmd_check("1", [sc], run=False)
    assert "CONFERENCIA: ok (1 falas)" in capsys.readouterr().out


def test_check_aponta_traducao_ausente_token_errado_e_estouro(tmp_path, capsys):
    import pytest
    sc, off = _lote(tmp_path, budget=5)
    with pytest.raises(SystemExit):                       # sem traducao nenhuma
        sl.cmd_check("1", [sc], run=False)
    assert f"{off}: sem traducao" in capsys.readouterr().out
    _grava(sc, off, "Ola mundo grande demais", risk_level="urgente")
    with pytest.raises(SystemExit):
        sl.cmd_check("1", [sc], run=False)
    out = capsys.readouterr().out
    assert "tokens [] != original ['[01]']" in out
    assert "bytes >" in out and "risk_level invalido" in out


def test_check_run_le_tsv_curto_e_repoe_quebra(tmp_path, capsys, monkeypatch):
    sc, off = _lote(tmp_path)
    (sl.TMP / "lot_1.tsv").write_text(f"{off}\tnpc\tlow\tOla grande mundo\n\n", encoding="utf-8")
    monkeypatch.setattr(sl.subprocess, "run", lambda *a, **k: type("P", (), {"stdout": "status final ok", "stderr": ""})())
    sl.cmd_check("1", [sc], run=True)
    out = capsys.readouterr().out
    assert "1 quebra(s) [01] reposta(s)" in out and "CONFERENCIA: ok" in out and "status final ok" in out


def test_check_run_tsv_com_linha_malformada_reprova(tmp_path, capsys):
    import pytest
    sc, off = _lote(tmp_path)
    (sl.TMP / "lot_1.tsv").write_text(f"{off}\tnpc\tlow\tOla[01]mundo\nlinha com 2 campos\tx\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        sl.cmd_check("1", [sc], run=True)
    assert "tsv linha 2: 2 campos" in capsys.readouterr().out
