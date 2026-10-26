import amostra_revisao as A


def _fake(monkeypatch, cenas):
    """cenas = {cena: [(offset, risk), ...]}"""
    monkeypatch.setattr(A.artifact_io, "plan_lines", lambda root, s: [
        {"offset": o, "risk_level": r, "speaker": "x", "text_source": "en", "base_translation": "pt"} for o, r in cenas[s]])
    monkeypatch.setattr(A.artifact_io, "translations_map", lambda root, s: {})


def test_amostra_cobre_todas_as_cenas_e_limita_o_risco(monkeypatch):
    cenas = {f"70_{i:02d}_00": [(str(k), "high" if k < 10 else "low") for k in range(30)] for i in range(5)}
    cenas.update({f"80_{i:02d}_00": [(str(k), "low") for k in range(30)] for i in range(5)})
    _fake(monkeypatch, cenas)
    a = A.amostra("r", list(cenas), total=20, max_risco=6)
    assert len(a) == 20
    assert {r["scene"] for r in a} == set(cenas)                       # 10 cenas, 20 falas: todas aparecem
    assert sum(r["risk"] == "high" for r in a) >= 6                     # cota de risco (+ as que cairam no resto)
    assert sum(r["risk"] == "high" for r in a if r["scene"].startswith("80")) == 0


def test_amostra_e_estavel_e_sem_repeticao(monkeypatch):
    cenas = {"a": [(str(k), "high") for k in range(8)], "b": [(str(k), "low") for k in range(8)]}
    _fake(monkeypatch, cenas)
    a1, a2 = A.amostra("r", ["b", "a"], total=6, max_risco=3), A.amostra("r", ["a", "b"], total=6, max_risco=3)
    assert a1 == a2
    assert len({(r["scene"], r["offset"]) for r in a1}) == len(a1) == 6


def test_cena_pequena_nao_estoura_o_total(monkeypatch):
    _fake(monkeypatch, {"a": [("1", "low")], "b": [("1", "high")]})
    assert len(A.amostra("r", ["a", "b"], total=40, max_risco=20)) == 2


def test_grupos_intercalados_nao_deixam_um_grupo_levar_tudo(monkeypatch):
    cenas = {f"20_{i:02d}_00": [("1", "low")] for i in range(20)}
    cenas.update({f"70_{i:02d}_00": [("1", "low")] for i in range(20)})
    _fake(monkeypatch, cenas)
    a = A.amostra("r", list(cenas), total=10, max_risco=0)
    assert sum(r["scene"].startswith("20") for r in a) == 5
