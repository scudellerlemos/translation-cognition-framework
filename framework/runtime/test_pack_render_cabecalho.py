"""O cabecalho do prompt conta linhas do pacote com traducao exata na TM, nunca mais que o numero de linhas."""
import pack_render


def _pack(tm_sources, line_sources):
    return {
        "scene": "S1", "scene_id": "S1", "n_lines": len(line_sources),
        "tm_exact": [{"source": s, "target": "t", "speaker": "A", "from_scene": "S0"} for s in tm_sources],
        "lines": [{"offset": f"S1:{i}", "source": s, "byte_budget": 10} for i, s in enumerate(line_sources)],
    }


def test_tm_com_fala_de_fora_do_pacote_nao_infla_a_contagem():
    linha = pack_render._cabecalho(_pack(["a", "b", "c", "d"], ["a", "b", "x"]))[4]
    assert "2 de 3 linhas" in linha


def test_fala_repetida_no_pacote_conta_cada_linha():
    linha = pack_render._cabecalho(_pack(["a"], ["a", "a", "z"]))[4]
    assert "2 de 3 linhas" in linha


def test_sem_tm_conta_zero():
    assert "0 de 2 linhas" in pack_render._cabecalho(_pack([], ["a", "b"]))[4]


NL = chr(92) + "n"          # token literal de quebra: barra invertida + n (nao uma quebra de linha real)


def test_tabela_traz_nl_com_as_quebras_do_source():
    pc = {"newline_token": NL, "target_charset_supported": True}
    pack = _pack([], ["um", f"dois{NL}tres", f"a{NL}b{NL}c"])
    linhas = pack_render._linhas(pack, pc)
    assert "| offset | byte_budget | nl | source |" in linhas
    assert [x for x in linhas if x.startswith("| S1:")] == [
        "| S1:0 | 10 | 0 | um |", f"| S1:1 | 10 | 1 | dois{NL}tres |", f"| S1:2 | 10 | 2 | a{NL}b{NL}c |"]


def test_sem_token_de_quebra_nl_fica_zero():
    linhas = pack_render._linhas(_pack([], ["x[01]y"]), {"newline_token": ""})
    assert "| S1:0 | 10 | 0 | x[01]y |" in linhas


def _gloss(**extra):
    return {"term": "Ring", "category": "item", "target_translation": "Anel Longo", "handling_rule": "traduzir",
            "spoiler_level": "none", **extra}


def test_glossario_so_ganha_coluna_forma_curta_se_algum_termo_a_usa():
    sem = pack_render._glossario({"glossary_subset": [_gloss()]})
    assert "forma curta" not in "\n".join(sem)
    com = pack_render._glossario({"glossary_subset": [_gloss(forma_curta="Anel")]})
    assert "forma curta" in com[1] and "| Anel |" in com[3]
