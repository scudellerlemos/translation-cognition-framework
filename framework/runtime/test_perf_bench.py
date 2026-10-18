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


# ---- guardrail do ADR 0019 (A/B: nenhum caminho favorecido a custa do outro) -------------------------------------
def _m(**kw):
    base = {n: 1.0 for n in pb.OPS}
    base.update(kw)
    return base


def test_guardrail_sem_mudanca_ou_dentro_do_limite_passa():
    assert pb.guardrail(_m(), _m()) == []
    assert pb.guardrail(_m(), _m(session_translate=1.09, api_overhead=1.09)) == []


def test_guardrail_reprova_piora_acima_de_10_por_cento():
    probs = pb.guardrail(_m(), _m(render_prompt=1.11))
    assert len(probs) == 1 and probs[0].startswith("render_prompt")


def test_guardrail_reprova_desequilibrio_mesmo_dentro_do_limite():
    """Sessao melhora 8% e a API piora 8%: cada um esta dentro dos 10%, mas um caminho ganhou a custa do outro."""
    probs = pb.guardrail(_m(), _m(session_translate=0.92, api_overhead=1.08))
    assert len(probs) == 1 and probs[0].startswith("desequilibrio")
    assert pb.guardrail(_m(), _m(session_translate=1.08, api_overhead=0.92))[0].startswith("desequilibrio")


def test_guardrail_ganho_nos_dois_ou_ruido_pequeno_nao_e_desequilibrio():
    assert pb.guardrail(_m(), _m(session_translate=0.9, api_overhead=0.9)) == []
    assert pb.guardrail(_m(), _m(session_translate=0.98, api_overhead=1.02)) == []     # dentro do ruido (3%)


def test_grupos_cobrem_so_operacoes_que_existem_e_ambos_os_caminhos():
    ops = {n for g in pb.GRUPOS.values() for n in g}
    assert ops <= set(pb.OPS)
    assert pb.GRUPOS["sessao"] and pb.GRUPOS["api"]
