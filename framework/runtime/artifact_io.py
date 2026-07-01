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
import paths  # noqa: E402


def scene_chapter(scene: str) -> str:
    """'ch_19_03' -> '19'; '' se nao casar o padrao ch_<cap>_<resto>."""
    parts = scene.split("_")
    return parts[1] if scene.startswith("ch_") and len(parts) >= 3 else ""


def scenes(root, chapter=None) -> list[str]:
    """Nomes das cenas (dirs `ch_*` em artifacts/scenes/) que tenham dialogs.csv, ordenados.
    chapter=None varre tudo; senao filtra pelo capitulo (ex.: '19').
    Dirs sem dialogs.csv (experimentos, cenas deletadas a metade) sao silenciosamente ignorados
    — evita metricas erradas e linhas fantasma no XLSX de revisao."""
    chap = str(chapter).strip() if chapter is not None and str(chapter).strip().lower() not in ("none", "") else None
    out = []
    for sc_dir in sorted(paths.scenes_dir(Path(root)).glob("*")):
        if not sc_dir.is_dir():
            continue
        if not (sc_dir / "dialogs.csv").is_file():   # exige dialogs.csv — sem ele a cena e incompleta
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
