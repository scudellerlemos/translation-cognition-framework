"""
amostra_revisao.py — amostra estratificada das cenas ainda sem visto humano (ponto de controle do `hitl.py`).

A amostra antiga eram 15 falas por ordem de hash: sem separar cena nem risco. Esta cobre os dois:
  1. ate `MAX_RISCO` falas `high`/`critical`, espalhadas pelas cenas (a rodada percorre as cenas, grupos intercalados, e tira uma fala por vez);
  2. o resto das `TOTAL` falas, uma por cena por rodada, ate cada cena ter aparecido.
A escolha dentro de cada cena e pelo hash `sha1(cena|offset)`: a mesma lista de cenas sempre da a mesma amostra.
A planilha traz `veredito` (ok/ruim) e `correcao` em branco, para o humano preencher.
"""
from __future__ import annotations

import hashlib

import artifact_io

TOTAL = 40
MAX_RISCO = 20
COLUNAS = ["scene", "offset", "risk", "speaker", "source_en", "target_pt", "veredito", "correcao"]
_ALTO = {"high", "critical"}


def _hash(scene: str, offset) -> str:
    return hashlib.sha1(f"{scene}|{offset}".encode(), usedforsecurity=False).hexdigest()


def _falas(root, scene: str) -> list[dict]:
    final = artifact_io.translations_map(root, scene)
    out = []
    for ln in artifact_io.plan_lines(root, scene):
        off = str(ln.get("offset", ""))
        t = (final.get(off) or {}).get("t") or ln.get("base_translation", "")
        out.append({"scene": scene, "offset": off, "risk": ln.get("risk_level", ""), "speaker": ln.get("speaker", ""),
                    "source_en": ln.get("text_source", ""), "target_pt": t, "veredito": "", "correcao": ""})
    return sorted(out, key=lambda r: _hash(scene, r["offset"]))


def _ordem_das_cenas(cenas) -> list[str]:
    """Intercala os grupos (prefixo do id da cena); dentro de cada grupo a ordem e a do hash, nao a alfabetica."""
    grupos: dict[str, list[str]] = {}
    for c in sorted(cenas, key=lambda c: _hash(c, "")):
        grupos.setdefault(c.split("_")[0], []).append(c)
    return [c for _, _, c in sorted((i, g, c) for g, v in grupos.items() for i, c in enumerate(v))]


def _rodadas(por_cena: dict[str, list[dict]], limite: int) -> list[dict]:
    """Uma fala de cada cena por rodada, com os grupos intercalados, ate `limite`."""
    saida: list[dict] = []
    fila = {c: list(v) for c, v in por_cena.items()}
    ordem = _ordem_das_cenas(fila)
    while len(saida) < limite and any(fila.values()):
        for c in ordem:
            if fila[c] and len(saida) < limite:
                saida.append(fila[c].pop(0))
    return saida


def amostra(root, scenes: list[str], total: int = TOTAL, max_risco: int = MAX_RISCO) -> list[dict]:
    todas = {s: _falas(root, s) for s in sorted(set(scenes))}
    risco = _rodadas({s: [r for r in v if r["risk"] in _ALTO] for s, v in todas.items()}, max_risco)
    vistos = {(r["scene"], r["offset"]) for r in risco}
    resto = _rodadas({s: [r for r in v if (r["scene"], r["offset"]) not in vistos] for s, v in todas.items()},
                     total - len(risco))
    return sorted(risco + resto, key=lambda r: (r["scene"], r["offset"]))
