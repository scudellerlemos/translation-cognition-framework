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
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
# ADAPTAR: importe o modulo de reconstrucao do PROPRIO conector (ex.: "import reinsert as R").
import font as F
import reinsert as R
from extract import resolve_sdat

ROOT = Path(__file__).resolve().parent.parent


TOKENS = re.compile(r"\\[nR]|\{[A-Za-z]+-?\d+\}")


def glyph_fails(approved: dict, allowed: set) -> list[str]:
    """Caractere da traducao (apos `fit`, sem tokens de controle) que a tabela de glifos nao tem vira `@` no jogo."""
    fails = []
    for k, text in approved.items():
        bad = sorted({c for c in TOKENS.sub("", F.fit(text)) if ord(c) > 31 and ord(c) not in allowed})
        if bad:
            fails.append(f"{k}: caractere sem glifo na fonte do jogo (vira '@'): {''.join(bad)!r}")
    return fails


def _allowed_glyphs() -> set:
    """Tabela do exe original, menos os glifos sacrificados, mais as letras acentuadas que `font.py` cria."""
    exe = ROOT / "backup_original" / "game.exe"
    if not exe.is_file():
        sys.exit(f"ERRO: {exe} nao existe; o gate de glifos precisa do exe original")
    codes = {e[0] for e in F.read_table(exe.read_bytes())[1]}
    return (codes - {ord(c) for c in F.SACRIFICE}) | {ord(c) for c in F.TARGETS}


def _rebuild(scene: str, dialogs: dict, approved: dict) -> tuple[bool, bool, list[str]]:
    """Round-trip (approved vazio == original) + aplicacao da cena + readback da coluna EN."""
    cfg = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    data = resolve_sdat(cfg["connector"], None).read_bytes()
    fails = []
    if R.rebuild(data, {})[0] != data:
        return False, False, ["round-trip: rebuild sem traducao difere do original"]
    translit = cfg["connector"].get("diacritic_strategy") == "transliterate"
    if not translit:
        fails += glyph_fails(approved, _allowed_glyphs())
    out, orphans = R.rebuild(data, approved, translit)
    if orphans:
        fails.append(f"{len(orphans)} id(s) sem destino: {orphans[:5]}")
    sd = R.read_sdat(out)
    got = {f"{sc}:{k}": s[k * len(R.LANGS) + R.EN_COL].decode("utf-8")
           for sc, _, n, _, s, why in R.text_members(sd) if not why and sc == scene for k in range(n)}
    for k, want in approved.items():
        want = R.connector_io.transliterate(want) if translit else want
        if got.get(k) != want:
            fails.append(f"{k}: readback difere do aprovado")
    return True, False, fails


def main() -> None:
    if {"-h", "--help"} & set(sys.argv[1:]):
        print(__doc__)
        return
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
    with (scene_dir / "dialogs.csv").open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            dialogs[row["offset"]] = row["text_en"]

    approved: dict[str, str] = {}
    with appr_files[0].open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            approved[row["offset"]] = row["text_target"]

    round_trip_ok, fitting_failure, fails = _rebuild(scene, dialogs, approved)
    if not round_trip_ok and not fails:
        fails = ["round-trip falhou (reinsert com approved vazio nao reproduz o original)"]

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
