#!/usr/bin/env python3
"""
verify_chapter.py — ESQUELETO (copiar para projects/<projeto>/connector/verify_chapter.py e
adaptar os pontos marcados # ADAPTAR).

Protocolo de SAIDA comum a TODOS os conectores (confirmado comparando BoF4/Utawarerumono/
Souldiers) — NAO muda entre projetos, so o `_rebuild(...)` (# ADAPTAR) e especifico do formato:
  exit 0 = OK (round-trip + apply + readback bateram)
  exit 3 = falha SOMENTE de fitting (escalavel — run_scene reaperta o budget e re-tenta)
  exit 1 = falha dura (round-trip, leitura, ou qualquer coisa fora de fitting)
  + linha "VERIFY_STATUS: {json}" com {ok, fitting_failure, n_fails} — run_scene.py le essa
    linha (fallback do exit-code) via connector_mgr._verify_status.

A reconstrucao byte-a-byte do formato NAO da pra generalizar (isso e a parte que exige
julgamento humano/LLM por engine) — so o SHELL (CLI, validacao de cobertura, protocolo de
saida) e reusavel.

Uso: python verify_chapter.py <scene>
"""
import csv
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
# ADAPTAR: importe o modulo de reconstrucao do PROPRIO conector (ex.: "import reinsert as R").
# import reinsert as R

ROOT = Path(__file__).resolve().parent.parent


def _rebuild(scene: str, dialogs: dict, approved: dict) -> tuple[bool, bool, list[str]]:
    """ADAPTAR: chama a reconstrucao especifica do formato (o `reinsert`/`rebuild_table`/
    equivalente do conector real). Retorna (round_trip_ok, fitting_failure, fails).

    round_trip_ok: reconstruir com approved={} (sem traducao nenhuma) reproduz o arquivo
      original byte a byte -- o oraculo inegociavel do projeto.
    fitting_failure: True SO se a UNICA razao de falha foi estouro de espaco/budget (formatos
      sem constraint de tamanho, ex.: length_constraints.mode="none", nunca setam isso -- deixe
      sempre False).
    fails: lista de strings descrevendo cada falha encontrada (round-trip, apply, ou readback).
    """
    raise NotImplementedError(
        "ADAPTAR: implemente a reconstrucao do formato aqui (ver o conector real do projeto "
        "mais parecido em projects/*/connector/verify_chapter.py como referencia)."
    )


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("uso: python verify_chapter.py <scene>")
    scene = sys.argv[1]
    scene_dir = ROOT / "artifacts" / "scenes" / scene
    if not scene_dir.is_dir():
        sys.exit(f"ERRO: diretorio nao encontrado: {scene_dir}")

    appr_files = sorted(scene_dir.glob("approved_*.csv"))
    if len(appr_files) != 1:
        sys.exit(f"ERRO: esperado 1 approved_*.csv em {scene_dir}, achei {len(appr_files)}")

    dialogs: dict[str, str] = {}
    with (scene_dir / "dialogs.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            dialogs[row["offset"]] = row["text_en"]

    approved: dict[str, str] = {}
    with appr_files[0].open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            approved[row["offset"]] = row["text_target"]

    round_trip_ok, fitting_failure, fails = _rebuild(scene, dialogs, approved)

    print(f"Cena {scene}: {len(dialogs)} string(s)")
    print(f"  round-trip: {'OK' if round_trip_ok else 'FALHOU'}")

    print("VERIFY_STATUS: " + json.dumps(
        {"ok": not fails, "fitting_failure": fitting_failure, "n_fails": len(fails)},
        ensure_ascii=False))

    if fails:
        print("\nFALHAS:")
        for x in fails:
            print("  -", x)
        sys.exit(3 if fitting_failure else 1)

    print(f"\nOK: cena {scene} reinsere e round-trip integro.")


if __name__ == "__main__":
    main()
