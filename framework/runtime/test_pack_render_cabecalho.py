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
