import os
from datetime import datetime

import estimar_lote as E


def _log(pasta, n, stamp, falas, minutos):
    f = pasta / f"onda_{n}_{stamp}.log"
    f.write_text(f"texto\nONDA_OK: 2 cenas, {falas} falas\n", encoding="utf-8")
    t0 = datetime.strptime(stamp, "%Y%m%d_%H%M%S").timestamp()
    os.utime(f, (t0 + minutos * 60, t0 + minutos * 60))
    return f


def test_ritmo_e_a_mediana_e_ignora_log_sem_onda_ok(tmp_path):
    _log(tmp_path, 1, "20261019_100000", 100, 4)          # 0,04
    _log(tmp_path, 2, "20261019_110000", 100, 6)          # 0,06
    _log(tmp_path, 3, "20261019_120000", 100, 120)        # 1,2: onda que esperou o reset (outlier)
    (tmp_path / "onda_4_20261019_130000.log").write_text("PARADA: teste\n", encoding="utf-8")
    assert E.ritmo(tmp_path) == 0.06


def test_ritmo_padrao_sem_onda_feita(tmp_path):
    assert E.ritmo(tmp_path) == E.RITMO_PADRAO


def test_plano_pega_as_n_primeiras_ondas_do_panorama():
    pan = "PLANO: 3 ondas\n onda +1: a b c = 447 falas\n onda +2: d e = 606 falas\n onda +3: f = 480 falas\n"
    assert E.plano(pan, 2) == [447, 606]


def test_estimativa_e_resumo():
    e = E.estimativa([100, 200], 0.05)
    assert e["min_por_onda"] == [5.0, 10.0] and e["min_total"] == 15.0 and e["falas"] == 300
    agora = datetime(2026, 10, 20, 1, 0, 0)
    assert "~15 min" in E.resumo(e, agora) and "01:15" in E.resumo(e, agora)


def test_estado_conta_cenas_verified_e_idade_do_ultimo_evento(tmp_path):
    arts = tmp_path / "artifacts"
    arts.mkdir()
    linhas = ['{"t": 100, "scene": "a", "stage": "scene", "result": "verified"}',
              '{"t": 160, "scene": "a", "stage": "scene", "result": "verified"}',
              "lixo",
              '{"t": 220, "scene": "b", "stage": "quality", "result": "ok"}']
    (arts / "events.jsonl").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    assert E.estado(tmp_path, agora=340) == "1 cenas verified | ultimo evento ha 2 min (b quality)"
    assert E.estado(tmp_path / "nada") == "sem events.jsonl"
