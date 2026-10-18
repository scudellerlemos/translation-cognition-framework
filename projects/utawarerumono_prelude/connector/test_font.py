"""Testes sinteticos do font.py (sem arquivo de jogo)."""
import os

import font as F
import pytest


def test_lz_literal_roundtrip():
    raw = os.urandom(1000) + bytes(300)
    assert F.lz_decode(F.lz_encode(raw)) == raw


def test_fit():
    assert F.fit("“Olá…” — ‘sim’") == '"Olá..." ― \'sim\''


def test_targets_and_slots():
    assert len(F.TARGETS) == len(F.SACRIFICE) == len(set(F.SACRIFICE))


def test_build_real():
    base = os.environ.get("UTAP_BACKUP")
    if not base:
        pytest.skip("defina UTAP_BACKUP=<backup_original> para testar com o exe/font.tex reais")
    e, t = open(f"{base}/game.exe", "rb").read(), open(f"{base}/font.tex", "rb").read()
    ne, nt, used = F.build(e, t)
    assert len(ne) == len(e) and len(used) == 24
    _, ents = F.read_table(ne)
    assert [x[0] for x in ents] == sorted(x[0] for x in ents) and ord("é") in {x[0] for x in ents} and ord("~") in {x[0] for x in ents}
    assert F.read_tex(nt)[0] == F.read_tex(t)[0]


def test_tilde_nao_sacrificado():
    # o EN desenha `~` (cantigas ♪~♪~~): sem a entrada o jogo mostra `@`
    assert "~" not in F.SACRIFICE


def test_glyph_fails():
    from verify_chapter import glyph_fails
    allowed = {ord(c) for c in "abc ♪~"}
    assert glyph_fails({"x:1": "ab\\nc {W1} ♪~"}, allowed) == []
    assert glyph_fails({"x:2": "a<b"}, allowed) == ["x:2: caractere sem glifo na fonte do jogo (vira '@'): '<'"]
