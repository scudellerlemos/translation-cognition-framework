#!/usr/bin/env python3
"""
connector_smoke.py — smoke test de round-trip para conectores em desenvolvimento.

Análogo ao batch_smoke.py (que valida a API batch), mas para o conector local:
verifica 4 invariantes antes de qualquer tradução ou iteração de conector T2.

  1. extract.py roda sem erro (exit 0)
  2. dialogs.csv tem as colunas obrigatórias (offset/id_col, text_*, byte_budget)
  3. extrai ≥ 1 linha não vazia
  4. round-trip byte-idêntico: extract → identity reinsert → compare com original
     (--roundtrip; requer reinsert.py implementado)

Uso:
  python framework/connectors/connector_smoke.py <project_root> [game_data_dir]
  python framework/connectors/connector_smoke.py <project_root> [game_data_dir] --roundtrip

Exit 0 = todos os invariantes testados passaram.
Exit 1 = algum falhou (diagnóstico no stdout).

Por que isso importa para T2:
  Sem smoke test, cada iteração de "implementar → rodar → ler output → diagnosticar" é
  feita manualmente ou via tokens de LLM. O smoke test comprime esse loop a segundos.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_REQUIRED_COLS = {"byte_budget"}  # offset ou id_col checado dinamicamente; text_* pelo prefixo


def smoke(project_root: Path, game_data_dir: Path | None = None, *, roundtrip: bool = False) -> bool:
    """Executa o smoke test. Retorna True se todos os invariantes passaram."""
    print(f"\n{'=' * 60}")
    print(f"  CONNECTOR SMOKE — {project_root.name}")
    if game_data_dir:
        print(f"  game_data_dir: {game_data_dir}")
    print(f"{'=' * 60}")

    results: list[tuple[str, bool, str]] = []  # (label, passed, detail)

    project_json = project_root / "project.json"
    extract_py = project_root / "connector" / "extract.py"
    dialogs_csv = project_root / "artifacts" / "dialogs.csv"

    if not extract_py.is_file():
        print(f"ERRO: extract.py não encontrado em {extract_py}")
        sys.exit(2)

    # ── Invariante 1: extract.py roda sem erro ────────────────────────────────
    cmd = [sys.executable, str(extract_py), str(project_root)]
    if game_data_dir:
        cmd.append(str(game_data_dir))

    proc = subprocess.run(cmd, capture_output=True, text=True)
    inv1 = proc.returncode == 0
    detail1 = proc.stdout.strip().split("\n")[-1] if proc.stdout.strip() else ""
    if not inv1:
        err = (proc.stderr or proc.stdout or "sem mensagem de erro").strip().split("\n")[-1]
        detail1 = f"exit {proc.returncode}: {err[:120]}"
    results.append(("extract.py exit 0", inv1, detail1))

    # ── Invariante 2: colunas obrigatórias ───────────────────────────────────
    inv2, detail2 = False, "dialogs.csv não gerado"
    id_col = "offset"
    if dialogs_csv.is_file():
        if project_json.is_file():
            try:
                cfg = json.loads(project_json.read_text(encoding="utf-8"))
                id_col = cfg.get("source", {}).get("id_column", "offset")
            except Exception:
                pass
        with dialogs_csv.open(encoding="utf-8", newline="") as f:
            cols = set(next(csv.reader(f), []))
        text_cols = [c for c in cols if c.startswith("text_")]
        required = {id_col, "byte_budget"}
        missing = required - cols
        if missing:
            detail2 = f"colunas faltando: {sorted(missing)} | encontradas: {sorted(cols)}"
        elif not text_cols:
            detail2 = f"nenhuma coluna text_* | colunas: {sorted(cols)}"
        else:
            inv2 = True
            detail2 = f"{sorted(cols)}"
    results.append((f"colunas ({id_col}, text_*, byte_budget)", inv2, detail2))

    # ── Invariante 3: ≥ 1 linha extraída ─────────────────────────────────────
    inv3, detail3 = False, "dialogs.csv não existe ou está vazio"
    if inv2 and dialogs_csv.is_file():
        with dialogs_csv.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        text_col = next((c for c in (rows[0].keys() if rows else []) if c.startswith("text_")), None)
        non_empty = [r for r in rows if r.get(text_col, "").strip()] if text_col else []
        inv3 = len(non_empty) >= 1
        detail3 = f"{len(non_empty)} linhas não-vazias extraídas"
        if inv3 and non_empty:
            sample = non_empty[0]
            detail3 += f" | ex: {sample.get(id_col, '')!r} → {str(sample.get(text_col, ''))[:60]!r}"
    results.append(("≥ 1 linha não-vazia extraída", inv3, detail3))

    # ── Invariante 4: round-trip byte-idêntico ────────────────────────────────
    if roundtrip:
        inv4, detail4 = _run_roundtrip(project_root, game_data_dir, dialogs_csv, project_json, id_col)
        results.append(("round-trip byte-idêntico", inv4, detail4))

    # ── Relatório ─────────────────────────────────────────────────────────────
    all_passed = all(r[1] for r in results)
    print()
    for label, passed, detail in results:
        mark = "✓" if passed else "✗"
        print(f"  {mark} {label}")
        if detail:
            print(f"      {detail}")
    print()
    n_pass = sum(1 for _, p, _ in results if p)
    n_total = len(results)
    status = "PASS" if all_passed else "FAIL"
    print(f"  SMOKE: {status} ({n_pass}/{n_total})")
    print(f"{'=' * 60}\n")

    return all_passed


def _run_roundtrip(
    project_root: Path,
    game_data_dir: Path | None,
    dialogs_csv: Path,
    project_json: Path,
    id_col: str,
) -> tuple[bool, str]:
    """Testa round-trip: identity reinsert → compare com fonte."""
    reinsert_py = project_root / "connector" / "reinsert.py"
    if not reinsert_py.is_file():
        return False, "reinsert.py não encontrado (implementar antes de testar round-trip)"

    if not dialogs_csv.is_file():
        return False, "dialogs.csv não existe — rodar sem --roundtrip primeiro"

    # Descobrir fonte original para comparação
    source_path = _find_source(project_root, project_json, game_data_dir)
    if source_path is None:
        return False, (
            "fonte original não encontrada. "
            "Declarar em project.json[connector][source_binary] ou passar game_data_dir"
        )
    source_hash = _sha256(source_path)

    # Criar identity approved_translations.csv temporário (3 primeiras strings)
    with dialogs_csv.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    text_col = next((c for c in (rows[0].keys() if rows else []) if c.startswith("text_")), None)
    if not text_col or not rows:
        return False, "dialogs.csv vazio ou sem coluna text_*"

    # Salvar approved_translations.csv original se existir (restaurar depois)
    approved = project_root / "artifacts" / "approved_translations.csv"
    backup = None
    if approved.is_file():
        backup = approved.with_suffix(".smoke_backup")
        shutil.copy2(approved, backup)

    try:
        sample = rows[:3]
        with approved.open("w", encoding="utf-8", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=[id_col, "text_target"])
            wr.writeheader()
            for row in sample:
                wr.writerow({id_col: row[id_col], "text_target": row[text_col]})

        with tempfile.TemporaryDirectory() as tmp:
            output_dir = project_root / "output"
            output_dir.mkdir(exist_ok=True)

            cmd = [sys.executable, str(reinsert_py), str(project_root)]
            if game_data_dir:
                cmd.append(str(game_data_dir))
            proc = subprocess.run(cmd, capture_output=True, text=True)

            if proc.returncode != 0:
                err = (proc.stderr or proc.stdout or "erro desconhecido").strip().split("\n")[-1]
                return False, f"reinsert.py exit {proc.returncode}: {err[:120]}"

            # Encontrar o arquivo de output gerado
            output_file = _find_output(project_root, source_path)
            if output_file is None:
                return False, "reinsert.py rodou mas não gerou output/ — verificar implementação"

            output_hash = _sha256(output_file)
            if source_hash == output_hash:
                return True, f"SHA256 idêntico ({source_hash[:12]}…)"
            else:
                return False, (
                    f"SHA256 diverge: fonte={source_hash[:12]}… saída={output_hash[:12]}… "
                    f"— strings codificadas com bytes diferentes do original"
                )
    finally:
        if backup and backup.is_file():
            shutil.copy2(backup, approved)
            backup.unlink()
        elif not backup and approved.is_file():
            approved.unlink()  # era temporário


def _find_source(project_root: Path, project_json: Path, game_data_dir: Path | None) -> Path | None:
    """Localiza o arquivo-fonte original para comparação de round-trip."""
    if project_json.is_file():
        try:
            cfg = json.loads(project_json.read_text(encoding="utf-8"))
            declared = cfg.get("connector", {}).get("source_binary")
            if declared:
                p = project_root / declared
                if p.is_file():
                    return p
        except Exception:
            pass
    if game_data_dir and game_data_dir.is_dir():
        # Para Unity e similares: não há single-file source; round-trip é diferente
        return None
    return None


def _find_output(project_root: Path, source: Path) -> Path | None:
    """Encontra o arquivo gerado pelo reinsert.py em output/."""
    output_dir = project_root / "output"
    if not output_dir.is_dir():
        return None
    # Mesmo nome que a fonte
    candidate = output_dir / source.name
    if candidate.is_file():
        return candidate
    # Qualquer arquivo em output/ com a mesma extensão
    for f in output_dir.iterdir():
        if f.suffix == source.suffix and f.is_file():
            return f
    return None


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    if not args:
        print("Uso: python connector_smoke.py <project_root> [game_data_dir] [--roundtrip]")
        sys.exit(1)

    project_root = Path(args[0])
    game_data_dir = Path(args[1]) if len(args) > 1 else None

    if not project_root.is_dir():
        print(f"ERRO: diretório não encontrado: {project_root}")
        sys.exit(2)

    ok = smoke(project_root, game_data_dir, roundtrip="--roundtrip" in flags)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
