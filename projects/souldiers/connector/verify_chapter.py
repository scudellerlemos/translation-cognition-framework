#!/usr/bin/env python3
"""
verify_chapter.py — Souldiers

Verifica a reinserção de UMA cena pelo protocolo do harness:
  1. Round-trip: rebuild_table(translations={}) reproduz o bundle byte-a-byte (fast-path de
     identidade em reinsert.rebuild_table — não passa pelo UnityPy quando nada muda).
  2. Apply: rebuild_table(translations) → ler a tabela de volta == approved_<sfx>.csv.

GOVERNANÇA: sem work-text. Lê os bundles somente-leitura; escreve só em memória (rebuild_table),
nunca no jogo. data_dir: project.json connector.data_dir_env (SOULDIERS_DATA_DIR) OU arg CLI.

Sem resíduo/fitting (project.json length_constraints.mode="none" — engine faz wrap automático,
diferente do BoF4). exit 3 fica reservado pelo protocolo mas não é alcançável aqui hoje.

Protocolo de exit code (consumido por run_scene.py):
  exit 0 = OK
  exit 3 = falha SOMENTE de fitting (não aplicável a este projeto — reservado)
  exit 1 = falha dura (round-trip, leitura ou readback — sempre bloqueante aqui)

Uso: python verify_chapter.py <scene>   ex.: python verify_chapter.py EUDER_PRESENTATION
"""
import csv
import json
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import reinsert as R  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

_DIALOGUE_TABLES = R._DIALOGUE_TABLES


def _load_offset_table_map(root: Path) -> dict[str, str]:
    """offset -> table, do dialogs.csv GLOBAL (extract.py escreve a coluna 'table' real).
    NÃO usar pack.json (context_pack.write_pack() o SOBRESCREVE, perde 'source_rows') nem
    adivinhar pelo prefixo do ID (texts_SIDE_DIALOGS tem IDs sem o prefixo 'SIDE_DIALOG_', ex.:
    'CH1_CREW_TEXT_01' — achado real rodando o jogo inteiro, 2026-07-02)."""
    out: dict[str, str] = {}
    with (root / "artifacts" / "dialogs.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["offset"]] = row["table"]
    return out


def _data_dir(root: Path) -> Path:
    env = os.environ.get("SOULDIERS_DATA_DIR")
    if env:
        return Path(env)
    cfg = json.loads((root / "project.json").read_text(encoding="utf-8"))
    d = cfg.get("connector", {}).get("data_dir", "")
    if not d:
        sys.exit(
            "ERRO: SOULDIERS_DATA_DIR não definido e connector.data_dir ausente em project.json.\n"
            "      set SOULDIERS_DATA_DIR=<caminho para Souldiers_Data\\StreamingAssets\\aa\\StandaloneWindows64>"
        )
    return Path(d)


def main() -> None:
    try:                                              # Windows cp1252: permitir setas/acentos no stdout
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) < 2:
        sys.exit("uso: python verify_chapter.py <scene>  (ex.: EUDER_PRESENTATION)")

    scene = sys.argv[1]
    chdir = ROOT / "artifacts" / "scenes" / scene
    if not chdir.is_dir():
        sys.exit(f"ERRO: diretório não encontrado: {chdir}")

    appr_files = sorted(chdir.glob("approved_*.csv"))
    if len(appr_files) != 1:
        sys.exit(
            f"ERRO: esperado 1 approved_*.csv em {chdir}, achei {len(appr_files)}"
        )

    data_dir = _data_dir(ROOT)

    dialogs: dict[str, str] = {}
    with (chdir / "dialogs.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            dialogs[row["offset"]] = row["text_en"]

    global_table_map = _load_offset_table_map(ROOT)
    offset_table: dict[str, str] = {off: global_table_map.get(off, "") for off in dialogs}
    unknown = [off for off, t in offset_table.items() if not t]
    if unknown:
        sys.exit(f"ERRO: {len(unknown)} offset(s) sem tabela reconhecida (nao estao no "
                 f"dialogs.csv global): {unknown[:5]}")

    approved: dict[str, str] = {}
    with appr_files[0].open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            approved[row["offset"]] = row["text_target"]

    touched_tables = sorted({offset_table[o] for o in dialogs if o in offset_table})

    fails: list[str] = []
    checked = 0

    for table_name in touched_tables:
        bundle_file = _DIALOGUE_TABLES.get(table_name)
        if not bundle_file:
            fails.append(f"{table_name}: tabela sem bundle mapeado em reinsert._DIALOGUE_TABLES")
            continue
        bundle_path = data_dir / bundle_file
        if not bundle_path.is_file():
            fails.append(f"{table_name}: bundle não encontrado em {data_dir} ({bundle_file})")
            continue

        original_bytes = bundle_path.read_bytes()

        # --- 1) Round-trip: sem traduções, bytes tem que ser identicos ao original ---
        try:
            rt_bytes, rt_changed = R.rebuild_table(table_name, bundle_path, {})
        except Exception as exc:
            fails.append(f"{table_name}: round-trip — rebuild_table falhou: {exc}")
            continue
        if rt_bytes != original_bytes or rt_changed != 0:
            fails.append(f"{table_name}: round-trip falhou (bundle difere com translations vazio)")

        # --- 2) Apply: so as linhas desta cena, resto fica no EN original ---
        file_translations: dict[str, str] = {
            off: approved[off] for off, tbl in offset_table.items()
            if tbl == table_name and off in approved
        }
        try:
            new_bytes, n_applied = R.rebuild_table(table_name, bundle_path, file_translations)
        except Exception as exc:
            fails.append(f"{table_name}: apply — rebuild_table falhou: {exc}")
            continue
        if n_applied != len(file_translations):
            fails.append(
                f"{table_name}: {n_applied}/{len(file_translations)} linhas aplicadas "
                f"(algum offset não bateu com ::ID:: da tabela)"
            )

        # --- 3) Leitura de volta ---
        try:
            new_rows = R.read_table(table_name, new_bytes)
        except Exception as exc:
            fails.append(f"{table_name}: readback — read_table falhou: {exc}")
            continue
        for off, want in file_translations.items():
            got = new_rows.get(off, "")
            if got == want:
                checked += 1
            else:
                fails.append(f"{off}: lido {got!r} != aprovado {want!r}")

    print(f"Cena {scene}: {len(dialogs)} strings em {len(touched_tables)} tabela(s) {touched_tables}")
    rt_ok = not any("round-trip" in f for f in fails)
    print(f"  round-trip: {'OK' if rt_ok else 'FALHOU'}")
    print(f"  strings conferidas (lido == approved): {checked}/{len(approved)}")

    print("VERIFY_STATUS: " + json.dumps({
        "ok": not fails,
        "fitting_failure": False,
        "n_fails": len(fails),
    }, ensure_ascii=False))

    if fails:
        print("\nFALHAS:")
        for x in fails:
            print("  -", x)
        sys.exit(1)

    print(f"\nOK: cena {scene} reinsere e round-trip íntegro.")


if __name__ == "__main__":
    main()
