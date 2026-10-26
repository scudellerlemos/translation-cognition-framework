"""Auditoria F6: o CI compara com o baseline do proprio runner (--baseline), nao com o medido na maquina local."""
import json
import sys

import perf_bench as pb


def test_baseline_alternativo_e_o_usado_na_comparacao(tmp_path, monkeypatch):
    monkeypatch.setattr(pb, "medir", lambda *a, **k: {"append_line": 10.0})
    ci = tmp_path / "ci.json"
    ci.write_text(json.dumps({"append_line": 1.0}), encoding="utf-8")
    out = tmp_path / "out.json"
    monkeypatch.setattr(sys, "argv", ["perf_bench", "--baseline", str(ci), "--out", str(out)])
    pb.main()
    res = json.loads(out.read_text(encoding="utf-8"))
    assert res["baseline"] == {"append_line": 1.0} and len(res["regressoes"]) == 1


def test_update_baseline_grava_no_arquivo_pedido_e_nao_no_padrao(tmp_path, monkeypatch):
    monkeypatch.setattr(pb, "medir", lambda *a, **k: {"append_line": 2.0})
    ci = tmp_path / "ci.json"
    monkeypatch.setattr(sys, "argv", ["perf_bench", "--baseline", str(ci), "--update-baseline"])
    antes = pb.BASELINE.read_bytes()
    pb.main()
    assert json.loads(ci.read_text(encoding="utf-8")) == {"append_line": 2.0}
    assert pb.BASELINE.read_bytes() == antes
