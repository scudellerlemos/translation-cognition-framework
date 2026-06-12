#!/usr/bin/env python3
"""
batch_smoke.py — SMOKE VIVO do caminho de batch contra a API REAL (~$0.02, ~minutos).

Por que existe: o caminho mais critico de CUSTO (batch -50% + tiering) e validado por MOCKS no pytest,
e os mocks REPETIDAMENTE divergiram da API real — 3 bugs nesta familia (custom_id '@@' invalido,
fragmento na re-rodada, e o 400 do Haiku por `effort`) PASSAVAM no fake e so apareciam queimando
dinheiro num capitulo pago. Este smoke roda UMA cena minima (2 linhas: 1 single-line -> Haiku, 1
multi-linha -> Sonnet) pela API REAL e afirma os invariantes que o mock NAO garante:

  (a) o batch SUBMETE sem 400 (custom_id valido + effort-por-modelo valido);
  (b) CONVERGE (status 'written') — sem cair pro interativo full-price;
  (c) AMBOS os tiers funcionam ao vivo (ha chamada batch=True de Haiku E de Sonnet no ledger);
  (d) ZERO chamada interativa (batch=False) — o -50% se realizou.

Rode antes de um capitulo pago (ou semanalmente). exit 0 = saudavel; 1 = DIVERGENCIA (nao rode capitulo
ate investigar). A funcao `evaluate()` (pura) e testada offline no pytest; `main()` toca a API real.

GOVERNANCA: cena descartavel em tempdir (NAO polui o projeto); requer ANTHROPIC_API_KEY.
Uso:  python batch_smoke.py
"""
from __future__ import annotations
import json
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import model          # noqa: E402
import paths          # noqa: E402


def evaluate(status: dict, ledger_rows: list, scene: str) -> tuple[bool, list]:
    """PURA (testavel offline): dado o status do batch_translate e as linhas do ledger, retorna
    (ok, problemas). Afirma os 4 invariantes (a)-(d) do smoke."""
    problems = []
    tr = [r for r in ledger_rows if r.get("kind") == "translate"]
    batch_models = {r.get("model", "") for r in tr if r.get("batch")}
    n_interactive = sum(1 for r in tr if not r.get("batch"))
    if status.get(scene) != "written":
        problems.append(f"(b) NAO convergiu: status={status.get(scene)!r} (esperado 'written'). "
                        "Cobertura/tiering quebrou — investigar ANTES de pagar capitulo.")
    if not any("haiku" in m for m in batch_models):
        problems.append("(c) tier CHEAP (Haiku) NAO produziu chamada batch — regressao tipo 400-do-effort? "
                        "(as single-line nao voltaram)")
    if not any("sonnet" in m for m in batch_models):
        problems.append("(c) tier MAIN (Sonnet) NAO produziu chamada batch — multi-linha nao voltou?")
    if n_interactive:
        problems.append(f"(d) {n_interactive} chamada(s) INTERATIVA(s) full-price — o batch caiu pro "
                        "fallback (o -50% nao se realizou).")
    return (not problems), problems


def _build_pack(scene_id):
    tok = context_pack.TOKEN
    return {"scene_id": scene_id, "tm_exact": [], "lines": [
        {"offset": "0x1", "source": "Yes, of course."},          # single-line -> tier cheap (Haiku)
        {"offset": "0x2", "source": f"Hello there,{tok}old friend."}]}  # multi-linha -> tier main (Sonnet)


def main():
    scene, scene_id = "ch_00_00", "00_00"
    pack = _build_pack(scene_id)
    # stub do pack/prompt (o smoke nao precisa da KB real — testa a PLUMBING, nao a qualidade);
    # _client() NAO e stubado -> as chamadas vao pra API REAL.
    context_pack.write_pack = lambda r, s: pack
    context_pack.render_prompt = lambda p, carta="": (
        "Traduza CADA linha abaixo para pt-BR natural. Devolva uma entrada por offset, no schema pedido.\n"
        + "\n".join(f"{l['offset']}: {l['source']}" for l in p["lines"]))
    model._carta_text = lambda: "Voce e um tradutor EN->pt-BR de jogos. Responda apenas o JSON do schema."

    tmp = Path(tempfile.mkdtemp(prefix="batch_smoke_"))
    (tmp / "artifacts" / scene).mkdir(parents=True)
    print(f"[smoke] cena minima (2 linhas: 1 Haiku + 1 Sonnet) -> API REAL de batch (~$0.02, minutos)...")
    try:
        status = model.batch_translate(tmp, [scene], poll_seconds=15, max_rounds=2)
    except Exception as e:
        print(f"[smoke] FALHA DURA na submissao/execucao do batch: {e!r}")
        print("        (ex.: 400 de custom_id/effort = regressao de contrato da API). NAO rode capitulo.")
        sys.exit(1)
    ledger = paths.ledger(tmp)
    rows = [json.loads(l) for l in ledger.read_text(encoding="utf-8").splitlines()] if ledger.is_file() else []
    ok, problems = evaluate(status, rows, scene)
    cost = sum(r.get("cost_usd", 0.0) for r in rows)
    by_model = {}
    for r in rows:
        by_model[r.get("model", "?")] = round(by_model.get(r.get("model", "?"), 0.0) + r.get("cost_usd", 0), 5)
    print(f"[smoke] status={status} | custo=${cost:.4f} | por modelo={by_model}")
    if ok:
        print("[smoke] OK ✓ — batch submete, converge, AMBOS os tiers ao vivo, zero fallback. Pode rodar capitulo.")
        sys.exit(0)
    print("[smoke] DIVERGENCIA mock↔API — NAO rode capitulo pago ate investigar:")
    for p in problems:
        print(f"  - {p}")
    sys.exit(1)


if __name__ == "__main__":
    main()
