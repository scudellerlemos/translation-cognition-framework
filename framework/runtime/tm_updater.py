#!/usr/bin/env python3
"""
tm_updater.py — atualiza a TM da SERIE com traducoes ja APROVADAS pelo QA (nao toda traducao
que sai do modelo -- so as que passaram pelo crivo humano de quality_review.py).

sync_scenes() e chamado ao fim de quality_review.apply() com as cenas TOCADAS pelo ciclo de QA
daquela rodada (verbatim aplicado ou nota resolvida). Cena 100% limpa (nada marcado CORRIGIR)
nunca e "tocada" por apply() -- por isso ha tambem um comando manual (`sync-tm`) pra forcar sync
de capitulos ja verified sem nenhuma correcao.

Retradução de um jogo: `reset_game()` remove SO as entradas daquele jogo (source_game) da TM da
serie -- avisa explicitamente antes (acao rara e deliberada, nunca automatica).

Puro/deterministico: nenhuma funcao chama datetime.now() -- `approved_at` e passado pelo caller.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import paths  # noqa: E402
from text_ids import tm_key  # noqa: E402
from tm_lookup import series_tm_path  # noqa: E402


def _game_id_of(root) -> str:
    """Identifica o jogo-fonte de uma entrada de TM (pra reset_game/retraducao saber o que remover).
    Usa o nome do diretorio do projeto -- estavel, nao depende de titulo (que pode mudar)."""
    return Path(root).resolve().name


def _read_plan_entries(root, scene, scene_id) -> dict[str, dict]:
    """{offset: {source, target, speaker}} do translation_plan_<sid>.json -- fonte UNICA (nao
    approved_<sid>.csv: esse e uma projecao do CONECTOR, gerada no build_plan, e _apply_verbatim
    (correcao humana do QA) so atualiza translations_*.json + translation_plan_*.json — o approved
    so seria regerado rodando build_plan de novo, o que o ciclo de QA nao faz)."""
    p = paths.translation_plan(root, scene, scene_id)
    if not p.is_file():
        return {}
    try:
        lines = json.loads(p.read_text(encoding="utf-8")).get("lines", [])
    except (json.JSONDecodeError, OSError):
        return {}
    return {ln.get("offset", ""): {"source": ln.get("text_source", ""),
                                   "target": ln.get("base_translation", ""),
                                   "speaker": ln.get("speaker", "")}
            for ln in lines}


def sync_scenes(root, cfg: dict, scenes: list, *, approved_at: str) -> int:
    """Le translation_plan_<sid>.json das cenas passadas (so as JA VERIFIED em run_state.json) e
    faz UPSERT na TM da serie por (source_game, src_key). Retorna nº de entradas gravadas/atualizadas."""
    from tm_lookup import series_of
    root = Path(root)
    series = series_of(cfg, root)
    game_id = _game_id_of(root)
    tm_path = series_tm_path(series)
    tm_path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict] = []
    if tm_path.is_file():
        try:
            existing = json.loads(tm_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            existing = []
    by_key = {(e["source_game"], e["src_key"]): i for i, e in enumerate(existing)}

    rs = paths.run_state(root)
    verified = set()
    if rs.is_file():
        try:
            st = json.loads(rs.read_text(encoding="utf-8")).get("scenes", {})
            verified = {s for s, v in st.items() if v.get("status") == "verified" and v.get("verified")}
        except (json.JSONDecodeError, OSError):
            pass

    n = 0
    for scene in scenes:
        if scene not in verified:
            continue
        scene_id = context_pack.scene_id_of(scene)
        entries = _read_plan_entries(root, scene, scene_id)
        for off, info in entries.items():
            source, target = info.get("source", ""), info.get("target", "")
            if not source or not target:
                continue
            key = tm_key(source)
            entry = {"source_game": game_id, "scene": scene, "offset": off,
                     "speaker": info.get("speaker", ""), "source": source, "target": target,
                     "src_key": key, "approved_at": approved_at}
            idx = by_key.get((game_id, key))
            if idx is not None:
                existing[idx] = entry
            else:
                by_key[(game_id, key)] = len(existing)
                existing.append(entry)
            n += 1
    if n:
        tm_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    return n


def reset_game(series: str, source_game: str) -> int:
    """Remove SO as entradas de `source_game` da TM da serie. Avisa explicitamente (acao rara e
    deliberada -- retraducao de um jogo inteiro, nunca automatica). Retorna nº removido."""
    tm_path = series_tm_path(series)
    if not tm_path.is_file():
        return 0
    try:
        existing = json.loads(tm_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return 0
    kept = [e for e in existing if e.get("source_game") != source_game]
    removed = len(existing) - len(kept)
    if removed:
        print(f"[tm_updater] AVISO: removendo {removed} entrada(s) de '{source_game}' da TM da "
              f"serie '{series}' (retraducao) — acao IRREVERSIVEL sem backup manual.")
        tm_path.write_text(json.dumps(kept, ensure_ascii=False, indent=2), encoding="utf-8")
    return removed


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Reset de TM da serie por retraducao de um jogo.")
    ap.add_argument("series")
    ap.add_argument("source_game")
    ap.add_argument("--confirm", action="store_true", help="obrigatorio -- sem isso, so simula")
    a = ap.parse_args()
    if not a.confirm:
        print("[tm_updater] dry-run (sem --confirm, nada e removido).")
        from tm_lookup import load_series_tm
        n = sum(1 for e in load_series_tm(a.series) if e.get("source_game") == a.source_game)
        print(f"  {n} entrada(s) de '{a.source_game}' SERIAM removidas da serie '{a.series}'.")
        return
    reset_game(a.series, a.source_game)


if __name__ == "__main__":
    main()
