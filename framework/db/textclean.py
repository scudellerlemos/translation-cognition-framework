"""textclean.py — forma LIMPA do texto, compartilhada por `store` e `embedder`.

Módulo-FOLHA (deps só `re`). Existe p/ quebrar o ciclo store <-> embedder: `store` instancia o
`Embedder` e o `Embedder` precisava de `strip_codes`, que morava em `store`. `store.strip_codes`
continua importável (re-export) — `context_pack` usa `from store import Store, strip_codes`.
"""
from __future__ import annotations

import re

_CODE_RX = re.compile(r"\[[0-9A-Fa-f]{2}\]")


def strip_codes(text: str) -> str:
    """Forma LIMPA do texto: remove os códigos de controle do jogo (`[XX]`) e normaliza
    espaços. Para LEITURA e EMBEDDING semântico — o `target` FIEL (com códigos) continua
    intacto no banco (round-trip/conector dependem dele). Genérico (multi-game)."""
    if not text:
        return text or ""
    return re.sub(r"\s+", " ", _CODE_RX.sub(" ", text)).strip()
