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
