"""test_kb_reconcile.py — cobre a promocao draft_ollama -> reconciled (kb_reconcile.py).

Usa kb_build_ollama.build() (com chat_fn fake) pra gerar os artefatos reais no formato de
verdade, em vez de forjar markdown a mao -- evita o teste divergir do formato real produzido.
"""
import csv
import re
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import kb_build_ollama as kbo  # noqa: E402
import kb_fetch  # noqa: E402
import kb_reconcile as kbr  # noqa: E402
import paths  # noqa: E402


def _write_entities(root: Path, names_importance):
    paths.entities(root).parent.mkdir(parents=True, exist_ok=True)
    with paths.entities(root).open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["canonical_name", "category", "aliases", "importance",
                                           "confidence", "notes"])
        w.writeheader()
        for name, importance in names_importance:
            w.writerow({"canonical_name": name, "category": "Personagem", "aliases": "",
                        "importance": importance, "confidence": "", "notes": ""})


def _cache_one(root: Path, texto: str, fonte: str):
    h = kb_fetch._hash_of(fonte)
    out = paths.research_cache(root, h)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"---\nfonte: {fonte}\ntipo: url\nfetched_em: t\ntruncado: false\n"
                   "encontrada_por: ia\n---\n" + texto, encoding="utf-8")


def _ratify(root: Path, *names):
    paths.kb_ratified(root).parent.mkdir(parents=True, exist_ok=True)
    with paths.kb_ratified(root).open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["name"])
        for n in names:
            w.writerow([n])


def _mark_conflicts_resolved(root: Path):
    rl = paths.research_log(root)
    txt = rl.read_text(encoding="utf-8")
    txt = txt.replace(kbr._CONFLICTS_PLACEHOLDER, "Nenhum conflito -- fontes concordam (revisado).")
    rl.write_text(txt, encoding="utf-8")


def _found_chat(model, messages, fmt):
    return {"found": True, "definicao": "Descricao encontrada.", "fontes": ["h1"], "confianca": "medium"}


def _unsourced_chat(model, messages, fmt):
    return {"found": False, "definicao": "", "fontes": [], "confianca": "low"}


def test_check_noop_when_not_draft(tmp_path):
    r = kbr.check(tmp_path)   # nem research_log.md existe ainda
    assert r["status"] == "" and r["ready"] is False and "note" in r


def test_check_lists_unratified_entities(tmp_path):
    _write_entities(tmp_path, [("Oshtor", "main"), ("Kuon", "main")])
    _cache_one(tmp_path, "texto com Oshtor e Kuon", "https://x.test")
    kbo.build(tmp_path, chat_fn=_found_chat)

    r = kbr.check(tmp_path)
    assert r["status"] == "draft_ollama"
    assert sorted(r["pending_ratification"]) == ["Kuon", "Oshtor"]
    assert r["ready"] is False


def test_check_ignores_unsourced_entities(tmp_path):
    _write_entities(tmp_path, [("Semfonte", "main")])
    _cache_one(tmp_path, "texto que nao menciona ninguem", "https://x.test")
    kbo.build(tmp_path, chat_fn=_unsourced_chat)

    r = kbr.check(tmp_path)
    assert r["pending_ratification"] == []   # UNSOURCED nao entra na lista de pendencia


def test_check_blocks_on_untouched_conflicts_placeholder(tmp_path):
    _write_entities(tmp_path, [("Oshtor", "main")])
    _cache_one(tmp_path, "texto com Oshtor", "https://x.test")
    kbo.build(tmp_path, chat_fn=_found_chat)
    _ratify(tmp_path, "Oshtor")   # ratificado, mas ninguem tocou na secao de conflitos

    r = kbr.check(tmp_path)
    assert r["pending_ratification"] == []
    assert r["conflicts_untouched"] is True
    assert r["ready"] is False


def test_promote_refuses_when_not_ready(tmp_path):
    _write_entities(tmp_path, [("Oshtor", "main")])
    _cache_one(tmp_path, "texto com Oshtor", "https://x.test")
    kbo.build(tmp_path, chat_fn=_found_chat)

    r = kbr.promote(tmp_path)
    assert r["promoted"] is False
    assert "Oshtor" in r["pending_ratification"]
    # nada foi alterado -- ainda draft_ollama
    assert kbr._current_status(tmp_path) == "draft_ollama"


def test_promote_flips_status_when_ready(tmp_path):
    _write_entities(tmp_path, [("Oshtor", "main")])
    _cache_one(tmp_path, "texto com Oshtor", "https://x.test")
    kbo.build(tmp_path, chat_fn=_found_chat)
    _ratify(tmp_path, "Oshtor")
    _mark_conflicts_resolved(tmp_path)

    r = kbr.promote(tmp_path)
    assert r["promoted"] is True
    rl = paths.research_log(tmp_path).read_text(encoding="utf-8")
    # mesma regex que kb_gate.py usa p/ liberar a KB -- agora DEVE casar
    assert re.search(r"status[:*\s]+reconciled", rl, re.I)
    assert "human_input:** confirmed" in rl


def test_promote_second_call_is_noop_not_destructive(tmp_path):
    _write_entities(tmp_path, [("Oshtor", "main")])
    _cache_one(tmp_path, "texto com Oshtor", "https://x.test")
    kbo.build(tmp_path, chat_fn=_found_chat)
    _ratify(tmp_path, "Oshtor")
    _mark_conflicts_resolved(tmp_path)

    r1 = kbr.promote(tmp_path)
    assert r1["promoted"] is True
    rl_after_1st = paths.research_log(tmp_path).read_text(encoding="utf-8")

    r2 = kbr.promote(tmp_path)   # ja reconciled -- nao deve fazer nada
    assert r2["promoted"] is False
    assert r2["status"] == "reconciled"
    rl_after_2nd = paths.research_log(tmp_path).read_text(encoding="utf-8")
    assert rl_after_1st == rl_after_2nd   # arquivo intocado na 2a chamada


def test_conflicts_tripwire_rejects_trivial_replacement(tmp_path):
    # so remover o placeholder nao basta -- "xxx" e curto demais pra contar como revisado de verdade
    _write_entities(tmp_path, [("Oshtor", "main")])
    _cache_one(tmp_path, "texto com Oshtor", "https://x.test")
    kbo.build(tmp_path, chat_fn=_found_chat)
    _ratify(tmp_path, "Oshtor")
    rl = paths.research_log(tmp_path)
    rl.write_text(rl.read_text(encoding="utf-8").replace(kbr._CONFLICTS_PLACEHOLDER, "xxx"),
                  encoding="utf-8")

    r = kbr.check(tmp_path)
    assert r["conflicts_untouched"] is True
    assert r["ready"] is False
    assert kbr.promote(tmp_path)["promoted"] is False


def test_status_regex_ignores_incidental_mention_elsewhere(tmp_path):
    # decoy: uma mencao a "status" solta no meio do texto, fora do formato '**Status:**' real,
    # nao pode confundir _current_status (regex ancorada em inicio de linha + negrito exato)
    _write_entities(tmp_path, [("Oshtor", "main")])
    _cache_one(tmp_path, "texto com Oshtor", "https://x.test")
    kbo.build(tmp_path, chat_fn=_found_chat)
    rl = paths.research_log(tmp_path)
    decoy = "Nota: o status social do personagem e alto.\n\n"
    rl.write_text(decoy + rl.read_text(encoding="utf-8"), encoding="utf-8")

    assert kbr._current_status(tmp_path) == "draft_ollama"


def test_kb_fetch_records_found_by(tmp_path):
    f = tmp_path / "nota.txt"
    f.write_text("x", encoding="utf-8")
    out = kb_fetch.fetch_and_cache(tmp_path, str(f), fetched_em="t", found_by="usuario")
    assert "encontrada_por: usuario" in out.read_text(encoding="utf-8")
    out2 = kb_fetch.fetch_and_cache(tmp_path, str(f), fetched_em="t")   # default
    assert "encontrada_por: ia" in out2.read_text(encoding="utf-8")


def test_kb_build_ollama_uses_found_by_in_research_log(tmp_path):
    _write_entities(tmp_path, [("Oshtor", "main")])
    f = tmp_path / "nota.txt"
    f.write_text("Oshtor aparece aqui.", encoding="utf-8")
    kb_fetch.fetch_and_cache(tmp_path, str(f), fetched_em="t", found_by="usuario")
    kbo.build(tmp_path, chat_fn=_found_chat)
    rl = paths.research_log(tmp_path).read_text(encoding="utf-8")
    assert "Usuario (rascunho Ollama)" in rl


def test_main_rejects_concordance_and_promote_together(tmp_path, monkeypatch):
    # --concordance e --promote juntos nao pode silenciosamente escolher um -- erro explicito.
    monkeypatch.setattr(sys, "argv", ["kb_reconcile.py", str(tmp_path), "--concordance", "--promote"])
    with pytest.raises(SystemExit) as exc:
        kbr.main()
    assert exc.value.code == 2
