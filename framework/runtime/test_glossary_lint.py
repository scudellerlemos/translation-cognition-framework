"""glossary_lint: formas validas do glossario (target, aliases, forma_curta)."""
import glossary_lint


def test_forma_curta_conta_como_forma_valida(tmp_path):
    import paths
    (tmp_path / "project.json").write_text("{}", encoding="utf-8")
    g = paths.glossary(tmp_path)
    g.parent.mkdir(parents=True, exist_ok=True)
    g.write_text("term,handling_rule,target_translation,aliases,forma_curta\nRing Longo,traduzir,Anel Comprido,,Anel\n",
                 encoding="utf-8")
    exp = glossary_lint._load_glossary(tmp_path)
    assert exp == [("Ring Longo", ["Anel Comprido", "Anel"], "traduzir")]
