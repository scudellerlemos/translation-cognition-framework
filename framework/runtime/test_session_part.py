"""session_part: divide um prompt de lote por secao do offset e junta os .tsv de volta (sem texto de jogo real)."""
import pytest
import session_part

LOT = "\n".join([
    "# prompt",
    "## 7. Falas",
    "cabecalho da secao",
    "| 00_01:10:1 | speaker | texto a |",
    "| 00_01:10:2 | speaker | texto b com Alpha |",
    "| 00_01:20:1 | speaker | texto c |",
    "## 8. Saida",
    "grave em lot_9.tsv",
]) + "\n"


def test_split_cria_um_arquivo_por_secao_com_so_as_suas_falas(tmp_path, capsys):
    (tmp_path / "lot_9.md").write_text(LOT, encoding="utf-8")
    (tmp_path / "keep_names.txt").write_text("Alpha\nBeta\n", encoding="utf-8")
    session_part.split(tmp_path, "9")
    s10 = (tmp_path / "lot_9_10.md").read_text(encoding="utf-8")
    s20 = (tmp_path / "lot_9_20.md").read_text(encoding="utf-8")
    assert "texto a" in s10 and "texto b" in s10 and "texto c" not in s10
    assert "texto c" in s20 and "texto a" not in s20
    assert "Nomes que aparecem neste lote: Alpha" in s10        # so o nome presente nas falas da secao
    assert "(nenhum)" in s20
    assert "lot_9_10.tsv" in s10 and "lot_9.tsv" not in s10     # saida redirecionada para o .tsv da secao
    assert "lot_9_10.md: 2 falas, 1 nomes" in capsys.readouterr().out


def test_split_sem_keep_names_usa_lista_vazia(tmp_path):
    (tmp_path / "lot_9.md").write_text(LOT, encoding="utf-8")
    session_part.split(tmp_path, "9")
    assert "(nenhum)" in (tmp_path / "lot_9_10.md").read_text(encoding="utf-8")


def test_split_sem_secoes_7_e_8_da_erro_claro(tmp_path):
    (tmp_path / "lot_9.md").write_text("# so isto\n", encoding="utf-8")
    with pytest.raises(ValueError, match="sem as secoes"):
        session_part.split(tmp_path, "9")


def test_join_junta_as_partes_em_ordem_e_ignora_linha_vazia(tmp_path, capsys):
    (tmp_path / "lot_9_10.tsv").write_text("a\tx\n\nb\ty\n", encoding="utf-8")
    (tmp_path / "lot_9_20.tsv").write_text("c\tz\n", encoding="utf-8")
    session_part.join(tmp_path, "9")
    assert (tmp_path / "lot_9.tsv").read_text(encoding="utf-8") == "a\tx\nb\ty\nc\tz\n"
    assert "lot_9.tsv: 3 falas de 2 parte(s)" in capsys.readouterr().out
