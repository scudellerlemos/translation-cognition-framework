"""ADR 0019 (guardrail, check 6): camadas entre os caminhos de traducao.

Tres camadas: NUCLEO (regras e pacote, usados pelos DOIS caminhos), SESSAO e API. O nucleo nao depende de nenhum dos
dois caminhos; a sessao nao importa nada especifico da API (cliente, SDK, lote) e a API nao importa o codigo de sessao.
O teste le os `import` por AST (inclusive os preguicosos, dentro de funcao) e compara com a tabela abaixo. Modulo da
tabela que ainda nao existe e ignorado: a tabela cresce a cada passo da divisao de model.py e context_pack.py.
"""
import ast
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent

# Especifico da API: cliente do provedor, SDK, lote, retry/backoff.
API = {"llm_client", "anthropic", "model_api"}
# Especifico da sessao: caminho sem rede (agente da sessao escreve o translations_<cena>.json).
SESSAO = {"model_session"}
# Fachada que ainda mistura os dois (re-exporta); nenhuma camada de baixo pode depender dela.
FACHADA = {"model"}

NUCLEO = {
    "context_pack", "pack_select", "pack_load", "pack_render", "translation_rules",
    "budget", "text_ids", "state_index", "artifact_io", "paths", "events",
}

# modulo -> o que ele NAO pode importar
PROIBIDO: dict[str, set[str]] = {
    **{m: API | SESSAO | FACHADA for m in NUCLEO},          # o nucleo nao conhece os caminhos
    "llm_client": SESSAO | FACHADA,                          # plumbing de API pode usar o nucleo, nao a sessao
    "model_session": API | FACHADA,                          # a sessao nao toca na API
    "model_api": SESSAO | FACHADA,                           # a API nao toca na sessao
}


def _importados(arq: Path) -> set[str]:
    out: set[str] = set()
    for n in ast.walk(ast.parse(arq.read_text(encoding="utf-8"))):
        if isinstance(n, ast.Import):
            out |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            out.add(n.module.split(".")[0])
    return out


def violacoes() -> list[str]:
    out = []
    for mod, proibidos in sorted(PROIBIDO.items()):
        arq = RUNTIME / f"{mod}.py"
        if arq.is_file():
            out += [f"{mod} importa {i}" for i in sorted(_importados(arq) & proibidos)]
    return out


def test_camadas_dos_caminhos_de_traducao_nao_se_misturam():
    assert not violacoes()


def test_o_scanner_enxerga_import_preguicoso_e_o_que_existe(tmp_path):
    f = tmp_path / "x.py"
    f.write_text("import os\n\ndef f():\n    from anthropic.types import X\n    import llm_client.sub\n", encoding="utf-8")
    assert _importados(f) == {"os", "anthropic", "llm_client"}
    # os modulos que a tabela ja cobre existem (nao e uma tabela de fantasia); os futuros sao opcionais
    assert {m for m in PROIBIDO if (RUNTIME / f"{m}.py").is_file()} >= {"context_pack", "llm_client", "paths"}


def test_fachada_e_o_unico_ponto_que_conhece_os_dois_caminhos():
    """So `model` (fachada) e os orquestradores de cima podem importar API e sessao juntos."""
    for arq in sorted(RUNTIME.glob("*.py")):
        if arq.name.startswith("test_") or arq.stem in FACHADA:
            continue
        imp = _importados(arq)
        if arq.stem in NUCLEO | API | SESSAO:
            assert not (imp & API and imp & SESSAO), f"{arq.name} mistura API e sessao"
