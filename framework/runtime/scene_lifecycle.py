"""scene_lifecycle.py — housekeeping/diagnostico de cena, extraido de run_scene.py (reforco de coesao de codigo).

Extraido quando run_scene.py cruzou o limiar de leitura documentado no ROADMAP (ganhou 3 funcoes
aditivas de housekeeping/diagnostico -- clean_failed_scene, prune_discontinued, _check_stale --
todas POS-orquestracao, sem relacao com o fluxo de traducao em si). run_scene.py reimporta estes
nomes (`from scene_lifecycle import ...`) para manter `rs.clean_failed_scene(...)` etc. funcionando
sem mudar nenhum caller (mesmo padrao ja usado em model.py/back_translate.py).

Funcoes:
  clean_failed_scene   — move artefatos de cena falha p/ artifacts/discontinued/ (retry limpo)
  prune_discontinued   — G4: remove discontinued/ mais antigo que N dias
  _check_stale         — V3: lista cenas com doctrine_hash diferente do atual
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import paths  # noqa: E402  (paths.py: fonte unica do contrato de caminhos de artefato)


def clean_failed_scene(root, scene) -> list[str]:
    """Move artefatos de uma cena em estado de falha para artifacts/discontinued/<scene>/.

    Move (nao apaga) artefatos DERIVADOS: translations, plan, approved, back_translation,
    back_prompt, pack, scene_prompt. Preserva dialogs.csv (entrada) e api_ledger.jsonl
    (auditoria — os tokens cobrados nao voltam). Remove o checkpoint da cena em run_state.json.
    artifacts/discontinued/<scene>/ serve como historico de runs anteriores (nao e re-ingerido
    pelo pipeline). Retorna lista de destinos (strs). Idempotente: rodar 2x nao levanta excecao."""
    root = Path(root)
    scene_id = context_pack.scene_id_of(scene)
    to_move = [
        paths.translations(root, scene, scene_id),
        paths.translation_plan(root, scene, scene_id),
        paths.approved(root, scene, scene_id),
        paths.back_translation(root, scene, scene_id),
        paths.back_prompt(root, scene, scene_id),
        paths.pack(root, scene),
        paths.scene_prompt(root, scene),
    ]
    disc = paths.discontinued_scene_dir(root, scene)
    moved = []
    for p in to_move:
        if p.is_file():
            disc.mkdir(parents=True, exist_ok=True)
            dest = disc / p.name
            p.rename(dest)
            moved.append(str(dest))
    # remove o checkpoint da cena do run_state.json (nao apaga o arquivo, so a chave)
    rs = paths.run_state(root)
    if rs.is_file():
        try:
            state = json.loads(rs.read_text(encoding="utf-8"))
            if scene in state.get("scenes", {}):
                del state["scenes"][scene]
                rs.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        except (json.JSONDecodeError, OSError):
            pass
    return moved


def prune_discontinued(root: Path, older_than_days: int = 30) -> list:
    """G4: remove cenas de artifacts/discontinued/ mais antigas que older_than_days dias.
    Retorna lista de paths removidos. Idempotente — rodar 2x não levanta exceção."""
    import shutil
    import time as _time
    disc = paths.discontinued_dir(root)
    if not disc.is_dir():
        return []
    cutoff = _time.time() - older_than_days * 86400
    removed = []
    for scene_dir in sorted(disc.iterdir()):
        if scene_dir.is_dir() and scene_dir.stat().st_mtime < cutoff:
            shutil.rmtree(scene_dir)
            removed.append(str(scene_dir))
    return removed


def _check_stale(project: str) -> None:
    """V3: compara doctrine_hash atual vs o salvo em run_state.json por cena."""
    root = Path(project)
    current = context_pack._doctrine_hash(root)
    rs = paths.run_state(root)
    if not rs.is_file():
        print("run_state.json nao encontrado — nenhuma cena traduzida.")
        return
    state = json.loads(rs.read_text(encoding="utf-8"))
    scenes = state.get("scenes", {})
    stale, fresh, no_data = [], [], []
    for scene_name, data in scenes.items():
        saved = data.get("doctrine_hash")
        if not saved:
            no_data.append(scene_name)
        elif saved != current:
            stale.append(scene_name)
        else:
            fresh.append(scene_name)
    print(f"Doutrina atual:     {current}")
    if stale:
        print(f"Desatualizadas ({len(stale)}):")
        for s in sorted(stale):
            print(f"  {s}")
    if no_data:
        print(f"Sem doctrine_hash ({len(no_data)}) — rodadas antes do versionamento:")
        for s in sorted(no_data):
            print(f"  {s}")
    if fresh:
        print(f"OK sincronizadas: {len(fresh)} cena(s).")
