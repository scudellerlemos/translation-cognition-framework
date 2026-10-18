"""Onda 3 (performance): o baseline cobre toda operacao medida e a regressao de mais de 2x e detectada."""
import json

import perf_bench as pb
import pytest


def test_baseline_cobre_todas_as_operacoes_e_so_elas():
    base = json.loads(pb.BASELINE.read_text(encoding="utf-8"))
    assert set(base) == set(pb.OPS)
    assert all(isinstance(v, float | int) and v > 0 for v in base.values())


def test_regressao_acima_de_2x_avisa_e_abaixo_nao():
    base = {"a": 1.0, "b": 2.0}
    assert pb.regressoes({"a": 1.9, "b": 3.9}, base) == []
    r = pb.regressoes({"a": 2.1, "b": 2.0}, base)
    assert len(r) == 1 and r[0].startswith("a:")


def test_operacao_sem_baseline_conta_como_problema():
    assert pb.regressoes({"nova": 1.0}, {}) == ["nova: sem baseline (rode --update-baseline)"]


@pytest.mark.parametrize("nome", sorted(pb.OPS))
def test_cada_operacao_roda_sobre_dados_sinteticos(nome, tmp_path):
    pb.OPS[nome](tmp_path)          # nao levanta; a medicao em si fica fora da suite (variancia de maquina)


def test_main_strict_sai_1_quando_regride(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(pb, "BASELINE", tmp_path / "b.json")
    (tmp_path / "b.json").write_text(json.dumps({n: 0.001 for n in pb.OPS}), encoding="utf-8")
    monkeypatch.setattr(pb, "medir", lambda: {n: 5.0 for n in pb.OPS})
    monkeypatch.setattr("sys.argv", ["perf_bench.py", "--strict"])
    with pytest.raises(SystemExit) as e:
        pb.main()
    assert e.value.code == 1
    assert "::warning::performance" in capsys.readouterr().out
