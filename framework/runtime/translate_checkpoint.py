"""translate_checkpoint.py — L01: nao perder as linhas JA PAGAS quando os retries esgotam.

`model._api_translate` acumula em `merged` as linhas que passaram nos gates (cobertura/paridade/formatacao).
Se apos `_MAX_TRIES` ainda sobra linha quebrada, ele levanta erro — e antes o `merged` inteiro ia embora: a
proxima rodada re-traduzia a cena toda (pagando de novo as N-k linhas boas). Aqui:
  - `save`  grava as linhas boas em `partial_translations_<id>.json` (so no esgotamento);
  - `load`  na proxima rodada devolve as que AINDA VALEM (mesmo source E mesmo doctrine_hash — glossario/
            decisoes/tom/Carta mudaram => a traducao foi feita sob outra doutrina => descarta) p/ semear o
            `merged`; o modelo so recebe as restantes. As semeadas passam pelos MESMOS gates de novo;
  - `clear` apaga ao concluir;
  - `log_exhausted` anexa 1 linha a `translate_exhausted.jsonl` (cena, custo das tentativas, quantas
            linhas quebradas/salvas) — o numero que mede se o esgotamento e frequente (ver cost_report).
Modulo FOLHA (deps: paths, cost). So o 1o passe usa checkpoint (`enabled=False` no escalonamento de
fitting: la a traducao e mais curta de proposito e nao deve ser semeada nem semear).
Best-effort: falha de I/O aqui avisa e segue — nunca mascara o erro de esgotamento nem derruba a traducao.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import cost
import paths


def load(root, scene, scene_id, doctrine_hash, srcmap, *, enabled=True) -> dict:
    """{offset: linha} das linhas salvas que ainda valem. {} se desligado/ausente/ilegivel/invalido — ou se
    o checkpoint ja cobre TODAS as linhas de `srcmap` (TM/fonte mudaram: nao ha o que retomar, traduz normal)."""
    p = paths.translations_partial(Path(root), scene, scene_id)
    if not enabled or not p.is_file():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        saved = data["lines"]
        same_doctrine = data.get("doctrine_hash") == doctrine_hash
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"[translate_checkpoint] AVISO: checkpoint {p.name} ilegivel ({exc!r}) -- ignorado.")
        return {}
    if not same_doctrine:
        print(f"[translate_checkpoint] {scene}: doutrina mudou desde o checkpoint -- descartado.")
        return {}
    seed = {off: e["v"] for off, e in saved.items()
            if off in srcmap and e.get("source") == srcmap[off] and isinstance(e.get("v"), dict)}
    if not seed or all(o in seed for o in srcmap):
        return {}
    print(f"[translate_checkpoint] {scene}: retomando {len(seed)}/{len(srcmap)} linha(s) ja pagas "
          f"-- o modelo recebe so as {len(srcmap) - len(seed)} restantes.")
    return seed


def save(root, scene, scene_id, doctrine_hash, merged, srcmap, bad, *, enabled=True) -> int:
    """Grava as linhas de `merged` que NAO estao em `bad` (paridade/formatacao ruim). Retorna quantas salvou."""
    good = {o: {"source": srcmap.get(o, ""), "v": v} for o, v in merged.items() if o not in bad}
    if not enabled or not good:
        return 0
    p = paths.translations_partial(Path(root), scene, scene_id)
    try:
        p.write_text(json.dumps({"doctrine_hash": doctrine_hash, "lines": good}, ensure_ascii=False,
                                indent=2), encoding="utf-8")
    except OSError as exc:
        print(f"[translate_checkpoint] AVISO: nao gravei {p.name} ({exc!r}) -- as {len(good)} linha(s) "
              f"pagas serao re-traduzidas na proxima rodada.")
        return 0
    return len(good)


def clear(root, scene, scene_id, *, enabled=True) -> None:
    if not enabled:
        return
    try:
        paths.translations_partial(Path(root), scene, scene_id).unlink(missing_ok=True)
    except OSError as exc:
        print(f"[translate_checkpoint] AVISO: nao removi o checkpoint de {scene} ({exc!r}).")


def log_exhausted(root, scene, model, usage, last, kept, *, stage) -> None:
    """1 linha em translate_exhausted.jsonl: `last` = {"missing","bad_parity","bad_structural",...} da ultima
    rodada; `usage` = tokens ACUMULADOS das tentativas (o custo que a rodada perdeu se nao houver checkpoint)."""
    rec = {"t": round(time.time(), 3), "scene": scene, "model": model, "stage": stage,
           "cost_usd": round(cost.cost_of(model, usage), 5),
           "missing": len(last["missing"]), "bad_parity": len(last["bad_parity"]),
           "bad_structural": len(last["bad_structural"]), "kept": kept}
    try:
        with paths.translate_exhausted(Path(root)).open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError as exc:
        print(f"[translate_checkpoint] AVISO: nao registrei o esgotamento de {scene} ({exc!r}).")
