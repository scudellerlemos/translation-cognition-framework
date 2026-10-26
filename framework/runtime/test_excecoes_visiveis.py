"""Auditoria F5: falha engolida em caminho de batch pago deixa rastro no log (antes: so o status, sem a causa)."""
import model


def test_resposta_de_batch_ilegivel_avisa_em_vez_de_calar(capsys):
    assert model._parse_batch_lines({"lines": [], "project_constraints": {}}, "isto nao e json") == {}
    assert "ilegivel" in capsys.readouterr().out
