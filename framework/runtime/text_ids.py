"""text_ids.py — primitivos de IDENTIDADE compartilhados pelo runtime E pelo db.

Módulo-FOLHA (deps só `re`/`hashlib`, nenhum import de framework). Existe para que a
canonicalização de `scene_id` e a chave de TM por source normalizado tenham UMA definição —
antes viviam duplicadas em `context_pack.scene_id_of`, `state_index._key/_norm`,
`migrate_from_flat._sid` e `export_to_flat._src_key`. Por ser folha sem dependências, `db/`
pode importá-lo sem acoplar a migração ao pack-builder pesado (`context_pack`).

Os nomes antigos viram delegação (re-export), então nenhum caller precisou mudar.
"""
from __future__ import annotations

import hashlib
import re


def scene_id_of(name: str) -> str:
    """scene_id canônico: tira o prefixo 'ch_' ('ch_19_03' -> '19_03'). Consistente entre
    flat e DB — é o que chaveia as tabelas por cena."""
    return name[3:] if name.startswith("ch_") else name


def norm_source(s: str) -> str:
    """Normaliza um source p/ chave de TM: minúsculo, '\\n' -> espaço, espaços colapsados, sem borda."""
    return re.sub(r"\s+", " ", (s or "").replace("\\n", " ").lower()).strip()


def tm_key(s: str) -> str:
    """sha1[:16] do source normalizado — chave ESTÁVEL de TM (flat e DB produzem a mesma)."""
    return hashlib.sha1(norm_source(s).encode("utf-8"), usedforsecurity=False).hexdigest()[:16]
