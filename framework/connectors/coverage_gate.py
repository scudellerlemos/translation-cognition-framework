#!/usr/bin/env python3
"""
coverage_gate.py — D2: dry-run OBRIGATORIO do candidato de extract.py (T2) contra multiplas
amostras reais, ANTES do round-trip formal (connector_smoke.py/test_roundtrip.py).

Contexto: script_generator.py gera um candidato de extract.py com um dos 3 padroes
(linear_scan/token_table/pointer_table) -- todos expondo o MESMO contrato de funcao:
  iter_string_offsets(data: bytes, project_cfg: dict) -> Iterator[int]
  decode_string(data: bytes, offset: int, table) -> tuple[str, int]
  load_table(table_path: Path) -> table

Antes do D2, esse candidato so era testado manualmente contra 1 arquivo -- risco real de
overfitting a 1 amostra. coverage_gate roda o candidato (via importlib, SEM subprocess/SEM
project.json completo) contra os N MAIORES arquivos reais do jogo, mede cobertura via
string_density (evidence_collector.py, reusada aqui, nao duplicada) como proxy do "quanto
conteudo textual deveria existir".

Piso (COVERAGE_FLOOR=0.85) aplicado ao MINIMO entre arquivos, NAO a media -- pega o candidato que
so funciona numa amostra (media alta esconderia 1 arquivo com cobertura pessima).

Interface T3 (contrato de escape): reusavel sem adaptacao -- depende so do contrato de funcao,
nao de quem escreveu o modulo (LLM via script_generator.py, ou humano via T3).

Uso: python coverage_gate.py <candidato.py> <game_dir> [--floor 0.85] [--min-files 3] [--table PATH]
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
from evidence_collector import _string_density  # noqa: E402  (reusa a mesma metrica, nao duplica)

_COVERAGE_FLOOR = 0.85
_MIN_FILES = 3
_READ_BYTES = 262144   # mesmo teto do evidence_collector, consistencia de amostragem


def load_candidate(path):
    """Importa dinamicamente o candidato de extract.py como modulo (sem subprocess, sem
    project.json). Levanta ImportError com mensagem clara se faltar o contrato minimo (candidato
    ainda tem NotImplementedError/esqueleto nao resolvido)."""
    path = Path(path)
    spec = importlib.util.spec_from_file_location(f"_candidate_{path.stem}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for fn in ("iter_string_offsets", "decode_string", "load_table"):
        if not hasattr(module, fn):
            raise ImportError(f"{path}: candidato nao expõe '{fn}' — contrato incompleto")
    return module


def pick_sample_files(game_dir, n: int = _MIN_FILES) -> list[Path]:
    """N MAIORES arquivos por tamanho (nao aleatorio) -- arquivos grandes tem mais chance de
    exercitar variacoes reais do formato (multiplas secoes, casos de borda) que um arquivo
    pequeno residual esconderia."""
    game_dir = Path(game_dir)
    files = [f for f in game_dir.rglob("*") if f.is_file()]
    return sorted(files, key=lambda f: f.stat().st_size, reverse=True)[:n]


def file_coverage(candidate, path, table=None) -> dict:
    """Roda o candidato contra 1 arquivo. Retorna {path, n_strings, covered_bytes, expected_bytes,
    coverage_ratio, offsets}. Nunca levanta -- erro no candidato vira coverage_ratio=0.0 + 'error'
    (o proprio erro ja e um sinal de reprovacao, capturado no relatorio)."""
    path = Path(path)
    data = path.read_bytes()
    expected_bytes = _string_density(data[:_READ_BYTES]) * len(data)
    offsets: list[tuple[int, int]] = []
    covered_bytes = 0
    try:
        for off in candidate.iter_string_offsets(data, {}):
            _text, budget = candidate.decode_string(data, off, table)
            offsets.append((off, budget))
            covered_bytes += budget
    except Exception as e:
        return {"path": str(path), "n_strings": 0, "covered_bytes": 0,
                "expected_bytes": round(expected_bytes, 1), "coverage_ratio": 0.0,
                "offsets": [], "error": str(e)}
    ratio = 1.0 if expected_bytes <= 0 else min(1.0, covered_bytes / expected_bytes)
    return {"path": str(path), "n_strings": len(offsets), "covered_bytes": covered_bytes,
            "expected_bytes": round(expected_bytes, 1), "coverage_ratio": round(ratio, 3),
            "offsets": offsets}


def check(candidate_path, game_dir, *, floor: float = _COVERAGE_FLOOR,
         min_files: int = _MIN_FILES, table_path=None) -> dict:
    """Dry-run completo: carrega candidato, amostra min_files MAIORES arquivos, mede cobertura em
    cada um. Retorna {passed, floor, per_file: [...], min_coverage, problems: [...]}."""
    candidate_path, game_dir = Path(candidate_path), Path(game_dir)
    problems: list[str] = []
    try:
        candidate = load_candidate(candidate_path)
    except Exception as e:
        return {"passed": False, "floor": floor, "per_file": [], "min_coverage": 0.0,
                "problems": [f"candidato nao carregou: {e}"]}
    try:
        table = candidate.load_table(Path(table_path) if table_path else Path("."))
    except Exception as e:
        return {"passed": False, "floor": floor, "per_file": [], "min_coverage": 0.0,
                "problems": [f"load_table falhou: {e}"]}
    sample = pick_sample_files(game_dir, min_files)
    if len(sample) < min_files:
        problems.append(f"apenas {len(sample)} arquivo(s) encontrado(s) em {game_dir}, "
                        f"precisa de >= {min_files} pra validar generalizacao")
    per_file = [file_coverage(candidate, p, table) for p in sample]
    min_coverage = min((r["coverage_ratio"] for r in per_file), default=0.0)
    if per_file and min_coverage < floor:
        worst = min(per_file, key=lambda r: r["coverage_ratio"])
        problems.append(f"cobertura minima {min_coverage:.0%} < piso {floor:.0%} "
                        f"(pior arquivo: {worst['path']})")
    return {"passed": not problems, "floor": floor, "per_file": per_file,
            "min_coverage": round(min_coverage, 3), "problems": problems}


def main():
    import argparse
    ap = argparse.ArgumentParser(description="D2: dry-run de cobertura do candidato T2 (extract.py).")
    ap.add_argument("candidate")
    ap.add_argument("game_dir")
    ap.add_argument("--floor", type=float, default=_COVERAGE_FLOOR)
    ap.add_argument("--min-files", type=int, default=_MIN_FILES)
    ap.add_argument("--table", default=None, help="path da tabela de caracteres (formatos token_table)")
    a = ap.parse_args()
    r = check(a.candidate, a.game_dir, floor=a.floor, min_files=a.min_files, table_path=a.table)
    print(f"coverage_gate: {'OK' if r['passed'] else 'BLOQUEADO'} "
          f"(cobertura minima {r['min_coverage']:.0%}, piso {r['floor']:.0%})")
    for p in r["problems"]:
        print(f"  [BLOCK] {p}")
    for f in r["per_file"]:
        err = f" [ERRO: {f['error']}]" if f.get("error") else ""
        print(f"    {f['path']}: {f['n_strings']} string(s), cobertura {f['coverage_ratio']:.0%}{err}")
    if not r["passed"]:
        sys.exit(1)

    from adversarial_validator import check as adv_check
    adv = adv_check(r["per_file"])
    print(f"\nadversarial_validator: {'OK' if adv['passed'] else 'BLOQUEADO'}")
    for p in adv["problems"]:
        print(f"  [BLOCK] {p}")
    sys.exit(0 if adv["passed"] else 1)


if __name__ == "__main__":
    main()
