#!/usr/bin/env python3
"""
estimar_lote.py — quanto tempo leva um lote de ondas (usado pelo rodar_ondas.ps1 e pelo vigia).

Ritmo = mediana de minutos por fala das ondas ja feitas (cada `logs/onda_<n>_<AAAAMMDD_HHMMSS>.log` com a linha
final `ONDA_OK: <c> cenas, <f> falas`; o fim e a data do arquivo). A mediana segura o outlier de uma onda que
esperou o reset da cota. Falas das proximas ondas = o plano do `panorama.py` (linhas `onda +N: ... = X falas`).
Sem onda feita: ritmo padrao. A estimativa nao conta espera de reset da cota (soma-se por fora).

Uso:  python panorama.py projects/<nome> | python estimar_lote.py <pasta de logs> <n ondas>
      python estimar_lote.py --estado projects/<nome>      (cenas verified e idade do ultimo evento: batimento do lote)
"""
from __future__ import annotations

import json
import re
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path

RITMO_PADRAO = 0.04          # min/fala, medido nas ondas 30 e 31 do utawarerumono_prelude (2026-10-20)
_ONDA_OK = re.compile(r"ONDA_OK:\s*(\d+)\s+cenas?,\s*(\d+)\s+falas")
_STAMP = re.compile(r"onda_\d+_(\d{8}_\d{6})\.log$")
_PLANO = re.compile(r"onda \+(\d+):.*?=\s*(\d+)\s+falas")


def ritmos(logs: Path) -> list[float]:
    """Minutos por fala de cada onda concluida (do log mais antigo ao mais novo)."""
    out = []
    for f in sorted(logs.glob("onda_*.log"), key=lambda p: p.stat().st_mtime):
        m = _STAMP.search(f.name)
        ok = _ONDA_OK.findall(f.read_text(encoding="utf-8", errors="replace"))
        if not m or not ok or int(ok[-1][1]) <= 0:
            continue
        minutos = (f.stat().st_mtime - datetime.strptime(m.group(1), "%Y%m%d_%H%M%S").timestamp()) / 60
        if minutos > 0:
            out.append(minutos / int(ok[-1][1]))
    return out


def ritmo(logs: Path) -> float:
    r = ritmos(logs)
    return statistics.median(r) if r else RITMO_PADRAO


def plano(panorama: str, n: int) -> list[int]:
    """Falas das proximas `n` ondas pelo plano do panorama."""
    return [int(f) for _, f in _PLANO.findall(panorama)][:n]


def estimativa(falas: list[int], min_por_fala: float) -> dict:
    por_onda = [round(f * min_por_fala, 1) for f in falas]
    return {"ondas": len(falas), "falas": sum(falas), "min_por_onda": por_onda,
            "min_total": round(sum(por_onda), 1), "min_por_fala": round(min_por_fala, 3)}


def resumo(e: dict, agora: datetime | None = None) -> str:
    agora = agora or datetime.now()
    fim = agora.timestamp() + e["min_total"] * 60
    return (f"estimativa: {e['ondas']} onda(s), {e['falas']} falas, ~{e['min_total']:.0f} min "
            f"(ritmo {e['min_por_fala']} min/fala; termina por volta das {datetime.fromtimestamp(fim):%H:%M}, "
            f"sem contar espera de reset da cota)")


def estado(projeto: Path, agora: float | None = None) -> str:
    """Uma linha com as cenas `verified` do projeto e ha quantos minutos foi o ultimo evento."""
    ev = projeto / "artifacts" / "events.jsonl"
    if not ev.is_file():
        return "sem events.jsonl"
    verified, ultimo = set(), None
    for ln in ev.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            e = json.loads(ln)
        except json.JSONDecodeError:
            continue
        ultimo = e
        if e.get("stage") == "scene" and e.get("result") == "verified":
            verified.add(e.get("scene"))
    if ultimo is None:
        return "events.jsonl vazio"
    idade = int(((agora or time.time()) - float(ultimo.get("t", 0))) / 60)
    return f"{len(verified)} cenas verified | ultimo evento ha {idade} min ({ultimo.get('scene')} {ultimo.get('stage')})"


def main() -> None:
    if len(sys.argv) == 3 and sys.argv[1] == "--estado":
        print(estado(Path(sys.argv[2])))
        return
    if len(sys.argv) < 3:
        sys.exit("uso: python estimar_lote.py <pasta de logs> <n ondas>   (panorama no stdin)")
    falas = plano(sys.stdin.read(), int(sys.argv[2]))
    if not falas:
        sys.exit("sem plano no panorama")
    print(resumo(estimativa(falas, ritmo(Path(sys.argv[1])))))


if __name__ == "__main__":
    main()
