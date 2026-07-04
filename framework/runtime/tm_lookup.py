#!/usr/bin/env python3
"""
tm_lookup.py — TM por SERIE (franquia), consultada na ENTRADA do context_pack.

Hoje a TM vive isolada por PROJETO (`artifacts/state/translation_memory.jsonl`, construida por
state_index.build_tm()). Esta TM por serie generaliza pra permitir que jogos da MESMA serie compartilhem termos
recorrentes (ex.: nome de personagem que aparece em 2 jogos da mesma franquia) -- sem nunca
misturar series diferentes.

Isolamento e ESTRUTURAL, nao runtime: cada serie tem seu PROPRIO arquivo `tm/<serie>.json` (raiz
do repo, nao dentro de artifacts/<projeto>/ -- e conhecimento CROSS-PROJETO, nao artefato de 1
projeto so). Impossivel misturar por construcao (leria o arquivo errado, nao "vazaria" dados).

Serie e declarada via campo OPCIONAL `"series"` em project.json. Projeto sem o campo -> serie =
slug do proprio titulo (isolado de si mesmo, ZERO mudanca de comportamento pros projetos
existentes ate um humano declarar o mesmo `"series"` em 2+ project.json).

`tm/<serie>.json` fica COMMITADO (diferente do cache-por-projeto, que e regeneravel e fica fora
do git) -- acumula conhecimento de verdade entre jogo 1 -> jogo 2, nao e so cache.

Uso: from tm_lookup import series_of, load_series_tm, lookup
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
if str(_HERE.parent) not in sys.path:
    sys.path.insert(0, str(_HERE.parent))
from text_ids import tm_key  # noqa: E402  (mesma normalizacao de chave que a TM por-projeto usa)

_REPO_ROOT = _HERE.parent.parent   # framework/runtime -> framework -> raiz do repo


def _slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    return s or "sem_titulo"


def series_of(cfg: dict, root) -> str:
    """Serie declarada em project.json['series'], ou slug do titulo (fallback -- projeto isolado
    de si mesmo, nao quebra nenhum projeto existente que nao declarar isso)."""
    declared = (cfg.get("series") or "").strip()
    if declared:
        return _slugify(declared)
    title = cfg.get("title") or Path(root).name
    return _slugify(title)


def series_tm_path(series: str) -> Path:
    return _REPO_ROOT / "tm" / f"{series}.json"


def load_series_tm(series: str) -> list[dict]:
    """[] se o arquivo nao existir ainda ou estiver corrompido -- nunca levanta."""
    p = series_tm_path(series)
    if not p.is_file():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def lookup(series: str, src_key: str) -> dict | None:
    """Match EXATO por src_key (mesma normalizacao tm_key da TM por-projeto). Primeira entrada
    encontrada vence (a TM da serie e append-only, entradas mais recentes ficam no fim)."""
    for e in load_series_tm(series):
        if e.get("src_key") == src_key:
            return e
    return None


def lookup_by_source(series: str, source_text: str) -> dict | None:
    """Conveniencia: normaliza `source_text` com o mesmo tm_key() antes de consultar."""
    return lookup(series, tm_key(source_text))


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Consulta a TM por serie.")
    ap.add_argument("series")
    ap.add_argument("--source", help="texto fonte a consultar (normalizado via tm_key)")
    a = ap.parse_args()
    if a.source:
        hit = lookup_by_source(a.series, a.source)
        print(json.dumps(hit, ensure_ascii=False, indent=2) if hit else "sem match")
        return
    tm = load_series_tm(a.series)
    print(f"TM da serie '{a.series}': {len(tm)} entrada(s) em {series_tm_path(a.series)}")


if __name__ == "__main__":
    main()
