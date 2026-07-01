import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import context_pack
import model
import pytest


@pytest.fixture
def fake_pack_ctx(monkeypatch):
    """E6: elimina 3 monkeypatches repetidos em testes de batch.

    Patches: context_pack.write_pack, context_pack.render_prompt, model._carta_text.
    Retorna o dict `packs` para o teste popular:
        fake_pack_ctx["ch_99_01"] = {"scene_id": "99_01", ...}

    Se render_prompt precisar de comportamento específico (ex: embeder offsets),
    sobrescreva com monkeypatch após declarar o fixture — o último setattr vence."""
    packs: dict = {}
    monkeypatch.setattr(context_pack, "write_pack", lambda _r, s: packs[s])
    monkeypatch.setattr(context_pack, "render_prompt", lambda pack, carta="": "PROMPT")
    monkeypatch.setattr(model, "_carta_text", lambda: "CARTA")
    return packs
