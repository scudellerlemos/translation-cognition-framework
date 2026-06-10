#!/usr/bin/env python3
"""
test_runtime.py — gates do harness `framework/runtime/` (pytest).

Prova as 3 propriedades que sustentam a arquitetura-alvo:
  - context_pack e DETERMINISTA (rodar 2x -> pack.json byte-identico) e LIMITADO (O(cena): subconjunto
    do glossario/vozes, nao o estado inteiro).
  - state_index e IDEMPOTENTE (rodar 2x -> indices byte-identicos) e a TM e reconstruivel.
  - GOVERNANCA: nenhum work-text (dialogo/traducao) hardcoded nos .py do runtime.

Roda na instancia de referencia (utawarerumono) — unica disponivel, como o test_cost_model.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack          # noqa: E402
import state_index           # noqa: E402
import run_chapter           # noqa: E402
import kb_gate               # noqa: E402

REPO = _HERE.parents[1]
PROJECT = REPO / "projects" / "utawarerumono"
SCENE = "ch_12_01"           # cena leve, sem dependencia de traducao


def _norm_accents(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


@pytest.fixture(scope="module")
def built():
    state_index.build(PROJECT)
    return True


# ------------------------------- state_index ----------------------------------

def test_state_index_idempotent(built):
    state = PROJECT / "artifacts" / "state"
    first = {p.name: p.read_bytes() for p in state.glob("*")}
    state_index.build(PROJECT)
    second = {p.name: p.read_bytes() for p in state.glob("*")}
    assert first.keys() == second.keys()
    for name in first:
        assert first[name] == second[name], f"{name} mudou entre rebuilds (nao idempotente)"


def test_tm_reconstructible_and_keyed(built):
    tm = [json.loads(l) for l in
          (PROJECT / "artifacts" / "state" / "translation_memory.jsonl")
          .read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(tm) > 1000, "TM deveria conter o capitulo 11 inteiro (~2129 linhas)"
    e = tm[0]
    assert set(e) >= {"scene", "offset", "speaker", "source", "target", "src_key"}
    # a chave e funcao determinista do source normalizado
    assert e["src_key"] == state_index._key(e["source"])


def test_voice_cards_present(built):
    cards = json.loads((PROJECT / "artifacts" / "state" / "voice_cards.json")
                       .read_text(encoding="utf-8"))
    assert cards, "esperava perfis de voz destilados do tone_analysis.md"
    for c in cards.values():
        assert "criticality" in c and "lines" in c


# ------------------------------- context_pack ---------------------------------

def test_context_pack_deterministic(built):
    context_pack.write_pack(PROJECT, SCENE)
    p = PROJECT / "artifacts" / SCENE / "pack.json"
    first = p.read_bytes()
    context_pack.write_pack(PROJECT, SCENE)
    assert p.read_bytes() == first, "pack.json mudou entre execucoes (nao determinista)"


def test_context_pack_bounded(built):
    pack = context_pack.build_pack(PROJECT, SCENE)
    full = context_pack.load_glossary(PROJECT / "artifacts" / "glossary.csv")
    full_terms = {g["term"] for g in full}
    sub_terms = {g["term"] for g in pack["glossary_subset"]}
    assert sub_terms <= full_terms, "subconjunto do glossario deve estar contido no glossario completo"
    assert len(sub_terms) < len(full_terms), "cena pequena nao deveria puxar o glossario inteiro"
    all_cards = json.loads((PROJECT / "artifacts" / "state" / "voice_cards.json")
                           .read_text(encoding="utf-8"))
    assert set(pack["voice_cards"]) <= set(all_cards)
    # cobre exatamente as linhas da cena
    dialogs = context_pack.load_dialogs(PROJECT / "artifacts" / SCENE / "dialogs.csv")
    assert pack["n_lines"] == len(dialogs) == len(pack["lines"])


def test_scene_prompt_self_contained(built):
    context_pack.write_pack(PROJECT, SCENE)
    txt = (PROJECT / "artifacts" / SCENE / "scene_prompt.md").read_text(encoding="utf-8")
    # contem a doutrina (Carta), as linhas e o formato de saida exigido
    assert "CARTA DE GOVERNANCA" in txt
    assert "Linhas a traduzir" in txt
    assert f"translations_{context_pack.sfx_of(SCENE)}.json" in txt


# ------------------------------- kb_gate --------------------------------------
# Gate de cobertura: research reconciliado + KB presente; fronteira bloqueia cena alem do pesquisado.

def _kb_project(tmp_path, *, reconciled=True, frontier=None, with_kb=True):
    art = tmp_path / "artifacts"
    (art / "state").mkdir(parents=True)
    status = "**Status:** reconciled" if reconciled else "**Status:** in_progress"
    (art / "research_log.md").write_text(
        f"# Research\n{status}\n**Fronteira de spoiler:** Cap. 11\n", encoding="utf-8")
    if with_kb:
        (art / "glossary.csv").write_text("term,target_translation\nHaku,Haku\n", encoding="utf-8")
        (art / "universe_knowledge_base.md").write_text("# KB\n## Haku\n", encoding="utf-8")
        (art / "state" / "voice_cards.json").write_text('{"Haku": {}}', encoding="utf-8")
    cfg = {"source": {"file": "x"}}
    if frontier:
        cfg["kb_frontier"] = frontier
    (tmp_path / "project.json").write_text(json.dumps(cfg), encoding="utf-8")
    return tmp_path


def test_kb_gate_passes_when_reconciled_and_present(tmp_path):
    root = _kb_project(tmp_path)
    assert kb_gate.check(root, "ch_12_03")["problems"] == []


def test_kb_gate_blocks_unreconciled(tmp_path):
    root = _kb_project(tmp_path, reconciled=False)
    probs = kb_gate.check(root, "ch_12_03")["problems"]
    assert any("reconcil" in p.lower() for p in probs)


def test_kb_gate_blocks_missing_artifacts(tmp_path):
    root = _kb_project(tmp_path, with_kb=False)
    assert kb_gate.check(root, "ch_12_03")["problems"], "KB ausente deve bloquear"


def test_kb_gate_frontier_blocks_beyond(tmp_path):
    root = _kb_project(tmp_path, frontier="12_05")
    assert kb_gate.check(root, "ch_12_03")["problems"] == [], "cena dentro da fronteira passa"
    beyond = kb_gate.check(root, "ch_12_09")["problems"]
    assert any("fronteira" in p.lower() for p in beyond), "cena alem da fronteira deve bloquear"
    assert kb_gate.check(root, "ch_13_01")["problems"], "capitulo seguinte deve bloquear"


# ------------------------------- run_chapter ----------------------------------
# Driver de capitulo: ordem das cenas, resume (skip de verified) e para-na-falha.
# Sem rede — run_scene e mockado (a unica parte de IA fica isolada em model.py).

def _fake_chapter(tmp_path, scenes):
    art = tmp_path / "artifacts"
    for s in scenes:
        d = art / f"ch_{s}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "dialogs.csv").write_text("offset,text_source,byte_budget\n0x1,Hi,5\n", encoding="utf-8")
    return tmp_path


def test_run_chapter_orders_and_resumes(monkeypatch, tmp_path):
    root = _fake_chapter(tmp_path, ("99_02", "99_01", "99_03"))   # fora de ordem de proposito
    (root / "artifacts" / "run_state.json").write_text(
        json.dumps({"scenes": {"ch_99_01": {"status": "verified", "verified": True}}}),
        encoding="utf-8")
    calls = []
    monkeypatch.setattr(run_chapter.RS, "run_scene",
                        lambda r, scene, **kw: calls.append(scene) or
                        {"status": "verified", "scene": scene, "verified": True})
    r = run_chapter.run_chapter(root, "99", backend="api")
    assert r["status"] == "complete"
    assert calls == ["ch_99_02", "ch_99_03"], "ch_99_01 ja verified deve ser pulado; resto em ordem"


def test_run_chapter_stops_on_failure(monkeypatch, tmp_path):
    root = _fake_chapter(tmp_path, ("99_01", "99_02"))
    monkeypatch.setattr(run_chapter.RS, "run_scene",
                        lambda r, scene, **kw:
                        {"status": "verify_failed" if scene == "ch_99_01" else "verified",
                         "scene": scene})
    r = run_chapter.run_chapter(root, "99", backend="api")
    assert r["status"] == "stopped" and r["stopped_at"] == "ch_99_01"


# ------------------------------- governanca -----------------------------------

def test_no_work_text_in_runtime_scripts():
    """Nenhuma fala/traducao do corpus pode estar hardcoded nos .py do runtime."""
    phrases = set()
    art = PROJECT / "artifacts"
    csvs = list(art.glob("approved_*.csv")) + list(art.glob("*/approved_*.csv"))
    import csv as _csv
    for f in csvs:
        with f.open(encoding="utf-8") as fh:
            for r in _csv.DictReader(fh):
                t = (r.get("text_target") or "").replace("\\n", " ")
                n = _norm_accents(t)
                if len(n) >= 22:                 # so frases longas (evita falso-positivo de palavras comuns)
                    phrases.add(n)
    assert phrases, "esperava frases do corpus p/ o guard"
    for py in _HERE.glob("*.py"):
        src = _norm_accents(py.read_text(encoding="utf-8"))
        hit = next((p for p in phrases if p in src), None)
        assert hit is None, f"work-text hardcoded em {py.name}: '{hit[:40]}...'"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
