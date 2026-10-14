import review_page


def test_render_embeds_sheet_and_save_is_whitelisted(tmp_path):
    (tmp_path / "amostra_qualidade.csv").write_text("id,source_en,target_pt,veredito,nota\n1,Hi[01],Oi,,\n",
                                                   encoding="utf-8-sig")
    html = review_page.render(tmp_path)
    assert '"amostra_qualidade.csv"' in html and "Hi[01]" in html and "__DATA__" not in html
    assert review_page.save(tmp_path, "amostra_qualidade.csv", b"x")
    assert not review_page.save(tmp_path, "../evil.csv", b"x")          # fora da lista: recusa
    assert not review_page.save(tmp_path, "onda_amostra.csv", b"x")     # so leitura
