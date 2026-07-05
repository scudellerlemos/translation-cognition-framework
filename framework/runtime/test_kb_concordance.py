"""test_kb_concordance.py — triagem de concordancia rascunho x pesquisa humana (#67).

Usa kb_build_ollama.build() (com chat_fn fake) pra gerar os artefatos reais no formato de
verdade, mesma convencao de test_kb_reconcile.py. A logica de concordance() e testada com
embed_fn injetado (fake, bag-of-words) -- mesmo padrao de chat_fn injetavel em
kb_build_ollama.build(), evita depender de sentence-transformers instalado pros testes de
comportamento. Um teste separado (skip se ML ausente) valida a fiacao real do Embedder.
"""
import csv
import math
from pathlib import Path

import kb_build_ollama as kbo
import kb_concordance as kbc
import pytest

_VOCAB = ["oshtor", "guerreiro", "woren", "companheiro", "leal", "nina", "infancia",
          "kuon", "financas", "reino", "castelo", "nunca", "sai", "do",
          "dragao", "ancestral", "montanhas", "fogo", "vive", "nas", "cospe"]


def _fake_embed(texts: list[str]) -> list[list[float]]:
    """Embedding fake deterministico: bag-of-words unit-norm sobre _VOCAB. Textos com o mesmo
    vocabulario -> cosine alto; textos sem palavra em comum -> cosine 0.0. Suficiente pra testar
    o LIMIAR e a logica de concordance() sem depender de sentence-transformers."""
    vecs = []
    for t in texts:
        words = set(t.lower().replace(",", "").replace(".", "").split())
        v = [1.0 if w in words else 0.0 for w in _VOCAB]
        norm = math.sqrt(sum(x * x for x in v)) or 1.0
        vecs.append([x / norm for x in v])
    return vecs


def _write_entities(root: Path, names_importance):
    import paths
    paths.entities(root).parent.mkdir(parents=True, exist_ok=True)
    with paths.entities(root).open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["canonical_name", "category", "aliases", "importance",
                                           "confidence", "notes"])
        w.writeheader()
        for name, importance in names_importance:
            w.writerow({"canonical_name": name, "category": "Personagem", "aliases": "",
                        "importance": importance, "confidence": "", "notes": ""})


def _cache_one(root: Path, texto: str, fonte: str, encontrada_por: str):
    import kb_fetch
    import paths
    h = kb_fetch._hash_of(fonte)
    out = paths.research_cache(root, h)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"---\nfonte: {fonte}\ntipo: url\nfetched_em: t\ntruncado: false\n"
        f"encontrada_por: {encontrada_por}\n---\n" + texto,
        encoding="utf-8",
    )


def _chat_with(definicao: str):
    def _chat(model, messages, fmt):
        return {"found": True, "definicao": definicao, "fontes": ["h1"], "confianca": "medium"}
    return _chat


def test_concordance_empty_when_no_draft(tmp_path):
    assert kbc.concordance(tmp_path) == []


def test_concordance_flags_high_agreement_on_paraphrase(tmp_path):
    # draft e fonte humana com REDACAO DIFERENTE (nao a mesma string) mas o mesmo conteudo --
    # prova que a comparacao tolera parafrase, nao so string identica (cosine=1.0 trivial).
    _write_entities(tmp_path, [("Oshtor", "main")])
    texto_humano = ("Consta nos registros que Oshtor, guerreiro do povo Woren, e companheiro "
                    "leal de Nina desde a infancia dos dois.")
    _cache_one(tmp_path, texto_humano, "https://wiki.test/oshtor", "usuario")
    kbo.build(tmp_path, chat_fn=_chat_with(
        "Oshtor e um guerreiro Woren, companheiro leal de Nina desde a infancia."
    ))

    items = kbc.concordance(tmp_path, embed_fn=_fake_embed)
    assert len(items) == 1
    assert items[0]["name"] == "Oshtor"
    assert items[0]["level"] == "alta"
    assert items[0]["score"] >= 0.85
    assert items[0]["human_sources"] == 1


def test_concordance_flags_low_agreement_on_real_divergence(tmp_path):
    _write_entities(tmp_path, [("Kuon", "main")])
    _cache_one(tmp_path, "Kuon administra as financas do reino e nunca sai do castelo.",
               "https://wiki.test/kuon", "usuario")
    kbo.build(tmp_path, chat_fn=_chat_with(
        "Kuon e um dragao ancestral que vive nas montanhas e cospe fogo."
    ))

    items = kbc.concordance(tmp_path, embed_fn=_fake_embed)
    assert len(items) == 1
    assert items[0]["name"] == "Kuon"
    assert items[0]["level"] == "baixa"
    assert items[0]["score"] < 0.85


def test_concordance_marks_missing_human_research_explicitly(tmp_path):
    _write_entities(tmp_path, [("Semfonte", "main")])
    _cache_one(tmp_path, "texto irrelevante", "https://x.test", "ia")   # so IA, nenhum humano
    kbo.build(tmp_path, chat_fn=_chat_with("Definicao qualquer vinda so da IA."))

    items = kbc.concordance(tmp_path, embed_fn=_fake_embed)
    assert len(items) == 1
    assert items[0]["level"] == "sem_pesquisa_humana"
    assert items[0]["score"] is None
    assert items[0]["human_sources"] == 0


def test_concordance_ignores_unsourced_entities(tmp_path):
    _write_entities(tmp_path, [("Ninguem", "main")])
    # sem cache nenhum -> kb_build_ollama gera UNSOURCED direto (nao chama o modelo)
    kbo.build(tmp_path, chat_fn=_chat_with("nao deveria ser chamado"))

    assert kbc.concordance(tmp_path, embed_fn=_fake_embed) == []


def test_concordance_name_matching_respects_word_boundary(tmp_path):
    # "Ana" nao pode casar dentro de "banana" (substring); so como palavra solta.
    _write_entities(tmp_path, [("Ana", "main")])
    _cache_one(tmp_path, "A plantacao de banana cresceu bastante este ano.",
               "https://x.test/banana", "usuario")
    kbo.build(tmp_path, chat_fn=_chat_with("Definicao qualquer sobre Ana."))

    items = kbc.concordance(tmp_path, embed_fn=_fake_embed)
    assert len(items) == 1
    assert items[0]["level"] == "sem_pesquisa_humana"   # "banana" nao deve contar como fonte
    assert items[0]["human_sources"] == 0


def test_concordance_real_embedder_wiring(tmp_path):
    """Smoke test com o Embedder REAL (sentence-transformers) -- so roda se a stack ML estiver
    instalada localmente (requirements-ml.txt); skip limpo em CI, que nao instala essa stack."""
    pytest.importorskip("sentence_transformers")
    _write_entities(tmp_path, [("Oshtor", "main")])
    texto = "Oshtor e um guerreiro Woren, companheiro leal de Nina desde a infancia."
    _cache_one(tmp_path, texto, "https://wiki.test/oshtor", "usuario")
    kbo.build(tmp_path, chat_fn=_chat_with(texto))

    items = kbc.concordance(tmp_path)   # sem embed_fn -- usa o Embedder real
    assert len(items) == 1
    assert items[0]["level"] == "alta"
