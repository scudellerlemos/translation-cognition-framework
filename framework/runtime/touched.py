"""Reconferencia so do que mudou: impressao digital por fala da traducao, gravada no run_state quando a cena
fecha `verified`. Uma cena verified sem fala nova/alterada (e com o mesmo conector e a mesma doutrina) nao
precisa passar de novo por gate nenhum; `run_scene` a pula, a menos que se peca `--full`.

  fingerprint(root, scene) -> {offset: sha1[:12] do texto traduzido}
  touched(root, scene)     -> offsets novos/alterados desde o ultimo verified (None = sem registro: tudo)
"""
import hashlib
import json

import artifact_io
import context_pack
import paths


def fingerprint(root, scene) -> dict:
    return {off: hashlib.sha1(str(e.get("t", "")).encode(), usedforsecurity=False).hexdigest()[:12]
            for off, e in artifact_io.translations_map(root, scene).items()}


def _state(root, scene) -> dict:
    p = paths.run_state(root)
    return json.loads(p.read_text(encoding="utf-8")).get("scenes", {}).get(scene, {}) if p.is_file() else {}


def touched(root, scene):
    st = _state(root, scene)
    if st.get("status") != "verified" or "t_hashes" not in st:
        return None
    old = st["t_hashes"]
    return sorted(o for o, h in fingerprint(root, scene).items() if old.get(o) != h)


def unchanged(root, scene, connector_hash="") -> bool:
    """verified, nenhuma fala tocada, mesma doutrina e mesmo conector."""
    st = _state(root, scene)
    t = touched(root, scene)
    return (t == [] and bool(fingerprint(root, scene)) and st.get("doctrine_hash") == context_pack._doctrine_hash(root)
            and st.get("connector_hash", "") == connector_hash)
