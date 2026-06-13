"""artifact_io.py — camada de LEITURA compartilhada dos artefatos por-cena.

Os scripts de qualidade/governanca (quality_gate, quality_fix, quality_review, tm_correct,
spoiler_check, ...) repetiam as MESMAS operacoes: iterar as cenas de um capitulo (glob `ch_*`),
derivar o capitulo de uma cena, ler `translation_plan`/`translations`/`back_translation`. Cada copia
era uma chance de divergir. Aqui ficam os UNICOS leitores; os scripts importam estes helpers.

E uma camada de LEITURA (sem mutacao, sem rede, sem IA) sobre `paths.py`. Acima de `paths` (que so
resolve caminhos) e abaixo dos scripts. `model._plan_lines` delega aqui (fonte unica do parse de plano).
Tolerante a arquivo ausente/ilegivel: retorna vazio em vez de estourar.
"""
from __future__ import annotations
import json
from pathlib import Path

import context_pack  # noqa: E402  (scene_id_of — fonte unica da derivacao do id de cena)
import paths          # noqa: E402


def scene_chapter(scene: str) -> str:
    """'ch_19_03' -> '19'; '' se nao casar o padrao ch_<cap>_<resto>."""
    parts = scene.split("_")
    return parts[1] if scene.startswith("ch_") and len(parts) >= 3 else ""


def scenes(root, chapter=None) -> list[str]:
    """Nomes das cenas (dirs `ch_*` em artifacts/), ordenados. chapter=None varre tudo; senao filtra
    pelo capitulo (ex.: '19')."""
    chap = str(chapter) if chapter is not None else None
    out = []
    for sc_dir in sorted(paths.artifacts(Path(root)).glob("ch_*")):
        if not sc_dir.is_dir():
            continue
        name = sc_dir.name
        if chap is None or scene_chapter(name) == chap:
            out.append(name)
    return out


def _read_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def plan_lines(root, scene) -> list:
    """Lista de linhas do translation_plan_<id>.json (ou [] se nao houver). Fonte unica do parse."""
    sid = context_pack.scene_id_of(scene)
    data = _read_json(paths.translation_plan(Path(root), scene, sid))
    return (data or {}).get("lines", []) if isinstance(data, dict) else []


def translations_map(root, scene) -> dict:
    """Mapa {offset: {t,...}} do translations_<id>.json (ou {} se nao houver/ilegivel)."""
    sid = context_pack.scene_id_of(scene)
    data = _read_json(paths.translations(Path(root), scene, sid))
    return (data or {}).get("lines", {}) if isinstance(data, dict) else {}


def back_entries(root, scene) -> dict:
    """Mapa {offset: entry} do back_translation_<id>.json (ou {} se nao houver/ilegivel)."""
    sid = context_pack.scene_id_of(scene)
    data = _read_json(paths.back_translation(Path(root), scene, sid))
    if not isinstance(data, dict):
        return {}
    return {e.get("offset", ""): e for e in data.get("entries", [])}
