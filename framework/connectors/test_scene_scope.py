import scene_scope as ss


def _proj(tmp_path, units, ordem=None):
    for name, budgets in units.items():
        d = tmp_path / "artifacts" / "scenes" / name
        d.mkdir(parents=True)
        (d / "dialogs.csv").write_text("offset,scene,text_en,byte_budget\n" + "".join(
            f"{name}:{i},{name},t,{b}\n" for i, b in enumerate(budgets)), encoding="utf-8")
    if ordem is not None:
        (tmp_path / "artifacts" / "ordem_cenas.txt").write_text("\n".join(ordem) + "\n", encoding="utf-8")
    return tmp_path


def test_tables_are_split_from_story_scenes_by_id_shape(tmp_path):
    res = ss.scan(_proj(tmp_path, {"10_01_00": [20, 30], "10_02_00": [40], "NameTextData": [5, 6, 30]}, ["10_01_00"]))
    assert res["ordem_confirmada"]
    seq, tab = res["cats"]["(sequencia)"], res["cats"]["NameTextData"]
    assert (seq["kind"], seq["units"], seq["strings"]) == ("sequencia", 2, 3)    # 10_02_00 fora da lista: continua cena
    assert (tab["kind"], tab["strings"], sum(b <= 16 for b in tab["budgets"])) == ("tabela", 3, 2)


def test_without_order_file_the_commonest_shape_is_the_story_and_order_is_unconfirmed(tmp_path):
    res = ss.scan(_proj(tmp_path, {"1_a": [9], "2_a": [9], "UnitTextData": [4]}))
    assert not res["ordem_confirmada"] and res["cats"]["UnitTextData"]["kind"] == "tabela"
    txt = ss.report(res)
    assert "NAO confirmada" in txt and "TABELAS DE SISTEMA: UnitTextData" in txt


def test_empty_project(tmp_path):
    assert ss.scan(tmp_path)["cats"] == {}


def test_report_conta_falas_com_falante_extraido(tmp_path):
    d = tmp_path / "artifacts" / "scenes" / "1_a"
    d.mkdir(parents=True)
    (d / "dialogs.csv").write_text("offset,speaker,text_en,byte_budget\n1,Ana,oi,5\n2,,tchau,5\n", encoding="utf-8")
    res = ss.scan(tmp_path)
    assert (res["falas"], res["com_falante"]) == (2, 1)
    assert "FALANTE: 1 de 2 falas" in ss.report(res)
    (d / "dialogs.csv").write_text("offset,text_en,byte_budget\n1,oi,5\n", encoding="utf-8")
    assert "nenhuma" in ss.report(ss.scan(tmp_path))
