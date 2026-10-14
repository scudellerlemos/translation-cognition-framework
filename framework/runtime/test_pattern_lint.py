

def test_ptpt_tem_de_only_before_infinitive():
    import quality_review
    assert quality_review._PTPT.search("Ele tem de ir embora")
    assert not quality_review._PTPT.search("Tem de sobra por aqui")
