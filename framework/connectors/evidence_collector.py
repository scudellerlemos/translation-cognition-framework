"""
evidence_collector.py — coleta evidências brutas de um diretório de jogo.

Parte do Generic Connector System (D1). Varre o diretório e produz um dict
de evidências que o tier_classifier usa para decidir T1/T2/T3.

Sem dependências externas além da stdlib. 100% determinístico e sem rede.

Uso:
    from evidence_collector import collect
    evidence = collect(Path("/path/to/game"))
"""
from __future__ import annotations

import fnmatch
import math
import re
import statistics
from collections import Counter
from pathlib import Path

# Limite de arquivos amostrados para métricas pesadas (entropia, densidade de string)
_SAMPLE_N = 20
# Bytes lidos por arquivo para análise (256 KB basta para magic + entropia + densidade)
_READ_BYTES = 262144
# Limiar de string imprimível ASCII para considerar "texto" (excluindo nulos e controle)
_ASCII_PRINTABLE_MIN = 0x20
_ASCII_PRINTABLE_MAX = 0x7E
# Padrão de tokens de controle Capcom [XX]
_CONTROL_TOKEN_RE = re.compile(rb"\[[0-9A-Fa-f]{2}\]")


def collect(game_dir: Path) -> dict:
    """Varre game_dir e devolve evidências brutas para o tier_classifier.

    Retorna:
      file_count      : total de arquivos encontrados
      families        : {prefixo_extensão: count} — ex.: {"AREAD.DAT": 60}
      magic_bytes     : {hex_8bytes: [lista de arquivos]} — primeiros 8 bytes por arquivo
      sample_encodings: {"ascii": 0.78, "utf8": 0.15, "binary": 0.07} — por amostra
      has_control_tokens: bool — algum arquivo tem padrão [XX]
      entropy_mean    : float — entropia de Shannon média sobre a amostra
      string_density  : float — proporção de bytes imprimíveis sobre a amostra
    """
    game_dir = Path(game_dir)
    if not game_dir.is_dir():
        return _empty_evidence(f"diretório não encontrado: {game_dir}")

    all_files = [f for f in game_dir.rglob("*") if f.is_file()]
    file_count = len(all_files)

    families: Counter = Counter()
    for f in all_files:
        key = f"{f.stem[:5].upper()}.{f.suffix.lstrip('.').upper()}" if f.suffix else f.stem[:5].upper()
        families[key] += 1

    sample = _sample_files(all_files, _SAMPLE_N)

    magic_index: dict[str, list[str]] = {}
    encodings: list[str] = []
    entropies: list[float] = []
    densities: list[float] = []
    has_control_tokens = False

    for f in sample:
        try:
            data = f.read_bytes()[:_READ_BYTES]
        except OSError:
            continue

        # magic bytes (primeiros 8 bytes em hex)
        magic = data[:8].hex() if len(data) >= 8 else data.hex()
        magic_index.setdefault(magic, []).append(f.name)

        enc = _estimate_encoding(data)
        encodings.append(enc)

        entropies.append(_shannon_entropy(data))
        densities.append(_string_density(data))

        if not has_control_tokens and _CONTROL_TOKEN_RE.search(data):
            has_control_tokens = True

    enc_counts = Counter(encodings)
    total_enc = max(len(encodings), 1)
    sample_encodings = {k: round(v / total_enc, 3) for k, v in enc_counts.items()}

    return {
        "file_count": file_count,
        "families": dict(families.most_common(20)),
        "magic_bytes": magic_index,
        "sample_encodings": sample_encodings,
        "has_control_tokens": has_control_tokens,
        "entropy_mean": round(statistics.mean(entropies), 3) if entropies else 0.0,
        "string_density": round(statistics.mean(densities), 3) if densities else 0.0,
    }


def _sample_files(files: list[Path], n: int) -> list[Path]:
    """Retorna até n arquivos representativos, distribuídos por extensão."""
    if len(files) <= n:
        return files
    by_ext: dict[str, list[Path]] = {}
    for f in files:
        by_ext.setdefault(f.suffix.lower(), []).append(f)
    sample: list[Path] = []
    exts = list(by_ext.keys())
    i = 0
    while len(sample) < n:
        ext = exts[i % len(exts)]
        candidates = by_ext[ext]
        idx = len(sample) // len(exts)
        if idx < len(candidates):
            sample.append(candidates[idx])
        i += 1
        if i > n * len(exts):
            break
    return sample[:n]


def _detect_magic(data: bytes) -> str | None:
    """Primeiros 8 bytes em hex, ou None se dado vazio."""
    if not data:
        return None
    return data[:8].hex()


def _estimate_encoding(data: bytes) -> str:
    """Classifica o encoding predominante do dado:
    'ascii'  — 100% caracteres na faixa 0x20-0x7E + whitespace/controle comum
    'utf8'   — decodifica como UTF-8 mas tem bytes fora do ASCII
    'binary' — não é texto válido
    """
    if not data:
        return "binary"
    printable = sum(1 for b in data
                    if _ASCII_PRINTABLE_MIN <= b <= _ASCII_PRINTABLE_MAX or b in (9, 10, 13))
    if printable / len(data) > 0.90:
        return "ascii"
    try:
        data.decode("utf-8")
        return "utf8"
    except UnicodeDecodeError:
        return "binary"


def _shannon_entropy(data: bytes) -> float:
    """Entropia de Shannon em bits/byte.
    ~7.5+ = cifrado/comprimido; ~4-5 = texto; ~0-2 = dados esparsos.
    """
    if not data:
        return 0.0
    counts = Counter(data)
    total = len(data)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def _string_density(data: bytes) -> float:
    """Proporção de bytes imprimíveis (0x20-0x7E) no dado."""
    if not data:
        return 0.0
    printable = sum(1 for b in data if _ASCII_PRINTABLE_MIN <= b <= _ASCII_PRINTABLE_MAX)
    return printable / len(data)


def _empty_evidence(error: str) -> dict:
    return {
        "file_count": 0,
        "families": {},
        "magic_bytes": {},
        "sample_encodings": {},
        "has_control_tokens": False,
        "entropy_mean": 0.0,
        "string_density": 0.0,
        "error": error,
    }
