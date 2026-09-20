"""test_kb_build_ollama.py — cobre a sintese de rascunho de KB via Ollama (kb_build_ollama.py).

chat_fn e injetavel (fake determinista, sem servidor Ollama vivo). Cobre: status sempre
draft_ollama (nunca reconciled), UNSOURCED quando nao encontrado/sem cache, confianca nunca 'high',
filtro por importance, e teto de contexto por chamada.
"""
import csv
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import kb_build_ollama as kbo  # noqa: E402
import kb_fetch  # noqa: E402
import paths  # noqa: E402


def _write_entities(root: Path, rows: list[dict]):
    paths.entities(root).parent.mkdir(parents=True, exist_ok=True)
    with paths.entities(root).open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["canonical_name", "category", "aliases", "importance",
                                           "confidence", "notes"])
        w.writeheader()
        w.writerows(rows)


def _cache_one(root: Path, texto: str, fonte: str = "https://x.test/wiki", tipo: str = "url"):
    # grava o cache DIRETO no formato que kb_fetch.py produz (front-matter + texto), sem rede real
    # -- a busca/normalizacao em si ja e coberta isoladamente em test_kb_fetch.py.
    h = kb_fetch._hash_of(fonte)
    out = paths.research_cache(root, h)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"---\nfonte: {fonte}\ntipo: {tipo}\nfetched_em: t\ntruncado: false\n---\n{texto}",
                   encoding="utf-8")
    return h


def test_build_writes_draft_status_never_reconciled(tmp_path):
    _write_entities(tmp_path, [{"canonical_name": "Oshtor", "category": "Personagem", "aliases": "",
                                "importance": "main", "confidence": "", "notes": ""}])
    _cache_one(tmp_path, "Oshtor e o protagonista disfarçado.")

    def fake_chat(model, messages, fmt):
        return {"found": True, "definicao": "Oshtor e o protagonista.", "fontes": ["abc"],
                "confianca": "medium"}

    r = kbo.build(tmp_path, chat_fn=fake_chat)
    assert r == {"entities_covered": 1, "entities_unsourced": 0, "sources_read": 1}
    rl = paths.research_log(tmp_path).read_text(encoding="utf-8")
    # mesma regex que kb_gate.py usa p/ decidir se a KB esta reconciliada -- NAO pode casar aqui
    # (senao o rascunho do Ollama passaria pelo gate sem reconciliacao humana de verdade)
    assert not re.search(r"status[:*\s]+reconciled", rl, re.I)
    assert re.search(r"status[:*\s]+draft_ollama", rl, re.I)
    kb = (paths.artifacts(tmp_path) / "universe_knowledge_base.md").read_text(encoding="utf-8")
    assert "## Oshtor" in kb and "Oshtor e o protagonista." in kb


def test_build_marks_unsourced_when_not_found(tmp_path):
    _write_entities(tmp_path, [{"canonical_name": "Kuon", "category": "Personagem", "aliases": "",
                                "importance": "secondary", "confidence": "", "notes": ""}])
    _cache_one(tmp_path, "texto que nao menciona a entidade")

    def fake_chat(model, messages, fmt):
        return {"found": False, "definicao": "", "fontes": [], "confianca": "low"}

    r = kbo.build(tmp_path, chat_fn=fake_chat)
    assert r["entities_unsourced"] == 1 and r["entities_covered"] == 0
    kb = (paths.artifacts(tmp_path) / "universe_knowledge_base.md").read_text(encoding="utf-8")
    assert "UNSOURCED" in kb


def test_build_no_cache_skips_chat_and_marks_unsourced(tmp_path):
    _write_entities(tmp_path, [{"canonical_name": "Semfonte", "category": "Personagem", "aliases": "",
                                "importance": "main", "confidence": "", "notes": ""}])
    calls = []

    def fake_chat(model, messages, fmt):
        calls.append(1)
        return {"found": True, "definicao": "nunca deveria chamar", "fontes": [], "confianca": "medium"}

    r = kbo.build(tmp_path, chat_fn=fake_chat)   # sem kb_fetch rodado -- cache vazio
    assert calls == [], "sem cache, nao deve chamar o modelo (nao ha o que extrair)"
    assert r == {"entities_covered": 0, "entities_unsourced": 1, "sources_read": 0}


def test_clamp_confidence_never_high():
    assert kbo._clamp_confidence("high") == "low"
    assert kbo._clamp_confidence("medium") == "medium"
    assert kbo._clamp_confidence("") == "low"
    assert kbo._clamp_confidence(None) == "low"


def test_build_downgrades_hallucinated_high_confidence(tmp_path):
    _write_entities(tmp_path, [{"canonical_name": "Balof", "category": "Personagem", "aliases": "",
                                "importance": "main", "confidence": "", "notes": ""}])
    _cache_one(tmp_path, "Balof e um mercador javali.")

    def fake_chat(model, messages, fmt):
        return {"found": True, "definicao": "Balof e mercador.", "fontes": [], "confianca": "high"}

    kbo.build(tmp_path, chat_fn=fake_chat)
    kb = (paths.artifacts(tmp_path) / "universe_knowledge_base.md").read_text(encoding="utf-8")
    section = kb.split("## Balof", 1)[1]
    conf_line = section.split("**Status de confianca:**\n", 1)[1].splitlines()[0]
    assert conf_line.startswith("low"), f"confianca alucinada 'high' deveria ser rebaixada, veio: {conf_line!r}"


def test_build_skips_entities_below_importance_threshold(tmp_path):
    _write_entities(tmp_path, [
        {"canonical_name": "Fundo", "category": "UI", "aliases": "", "importance": "background",
         "confidence": "", "notes": ""},
    ])
    _cache_one(tmp_path, "qualquer texto")
    calls = []

    def fake_chat(model, messages, fmt):
        calls.append(1)
        return {"found": True, "definicao": "x", "fontes": [], "confianca": "low"}

    r = kbo.build(tmp_path, chat_fn=fake_chat)
    assert calls == [], "importance=background nao deve ser processada"
    assert r == {"entities_covered": 0, "entities_unsourced": 0, "sources_read": 1}


def test_build_respects_max_context_chars(tmp_path, monkeypatch):
    monkeypatch.setattr(kbo, "_MAX_CONTEXT_CHARS", 100)
    _write_entities(tmp_path, [{"canonical_name": "Grande", "category": "Personagem", "aliases": "",
                                "importance": "main", "confidence": "", "notes": ""}])
    _cache_one(tmp_path, "x" * 1000)   # bem maior que o teto de 100
    seen = {}

    def fake_chat(model, messages, fmt):
        seen["content"] = messages[0]["content"]
        return {"found": False, "definicao": "", "fontes": [], "confianca": "low"}

    kbo.build(tmp_path, chat_fn=fake_chat)
    # o bloco de contexto embutido no prompt nao deve carregar as 1000 letras inteiras
    assert seen["content"].count("x") <= 100 + 20   # folga p/ o marcador [FONTE:hash]


def test_parse_cache_file_reads_frontmatter(tmp_path):
    h = _cache_one(tmp_path, "corpo do texto", fonte="local.txt", tipo="txt")
    parsed = kbo._parse_cache_file(paths.research_cache(tmp_path, h))
    assert parsed["fonte"] == "local.txt" and parsed["tipo"] == "txt" and parsed["texto"] == "corpo do texto"


def test_context_for_reports_dropped_sources_when_over_budget():
    # "[FONTE:h1]\n" (11) + 60 x's + "\n" (1) = 72 chars -- com budget=70, a 1a fonte ja consome o
    # teto inteiro (truncada); a 2a nao ganha NENHUM espaco -> vai pra `dropped`, nao some em silencio.
    cache = [{"hash": "h1", "fonte": "a", "tipo": "url", "texto": "x" * 60},
              {"hash": "h2", "fonte": "b", "tipo": "url", "texto": "y" * 60}]
    context, dropped = kbo._context_for(cache, budget=70)
    assert "h1" in context                            # 1a fonte coube (truncada, mas presente)
    assert dropped == ["h2"]                          # 2a fonte nao coube em NADA -- reportada, nao sumida


def test_build_aborts_without_writing_when_chat_fails(tmp_path):
    """Ollama fora do ar em 1 entidade nao pode virar 'UNSOURCED' silencioso nem sobrescrever a KB."""
    import pytest
    _write_entities(tmp_path, [{"canonical_name": "Oshtor", "category": "Personagem", "aliases": "",
                                "importance": "main", "confidence": "", "notes": ""}])
    _cache_one(tmp_path, "Oshtor e o protagonista.")

    def boom(model, messages, fmt):
        raise ConnectionError("ollama down")

    with pytest.raises(RuntimeError):
        kbo.build(tmp_path, chat_fn=boom)
    assert not paths.research_log(tmp_path).exists()


def test_build_refuses_reconciled_kb_without_force(tmp_path):
    import pytest
    _write_entities(tmp_path, [])
    rl = paths.research_log(tmp_path)
    rl.parent.mkdir(parents=True, exist_ok=True)
    rl.write_text("**Status:** reconciled\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="(?i)reconcil"):
        kbo.build(tmp_path, chat_fn=lambda *a: {})
    assert rl.read_text(encoding="utf-8") == "**Status:** reconciled\n"


def test_build_refuses_reconciled_kb_lowercase_status_format(tmp_path):
    """O kb_gate aceita 'status: reconciled' (sem negrito); a guarda de sobrescrita tem que ver o MESMO formato."""
    import pytest
    _write_entities(tmp_path, [])
    rl = paths.research_log(tmp_path)
    rl.parent.mkdir(parents=True, exist_ok=True)
    rl.write_text("status: reconciled\nhuman_input: done\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="(?i)reconcil"):
        kbo.build(tmp_path, chat_fn=lambda *a: {})
