"""text_ids.py — primitivos de IDENTIDADE compartilhados pelo runtime E pelo db.

Módulo-FOLHA (deps só stdlib, nenhum import de framework). Existe para que a
canonicalização de `scene_id` e a chave de TM por source normalizado tenham UMA definição —
antes viviam duplicadas em `context_pack.scene_id_of`, `state_index._key/_norm`,
`migrate_from_flat._sid` e `export_to_flat._src_key`.

Mora na RAIZ de `framework/` (não em `runtime/` nem em `db/`) de propósito: `db/` importava
daqui via manipulação de `sys.path` apontando para dentro de `runtime/`, criando uma dependência
circular (`db` -> `runtime` -> `db`, via `context_pack.py` importando `store.Store`). Um módulo
neutro que nenhum dos dois pacotes "possui" quebra o ciclo — `db/` e `runtime/` importam daqui,
nunca um do outro por causa deste módulo.

Os nomes antigos viram delegação (re-export), então nenhum caller precisou mudar.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


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


def verified_scenes(run_state: Path) -> set[str] | None:
    """Cenas `verified` no run_state.json (mesmo criterio do run_chapter._verified). None = sem
    run_state legivel (legado). Aqui (e nao no runtime) porque TM flat (state_index) e TM do DB
    (migrate_from_flat) filtram pelo MESMO criterio."""
    if not run_state.is_file():
        return None
    try:
        scenes = json.loads(run_state.read_text(encoding="utf-8")).get("scenes", {})
    except (json.JSONDecodeError, OSError):
        return None
    return {k for k, v in scenes.items() if v.get("status") == "verified" and v.get("verified") is True}
