"""connector_io.py — utilitários compartilhados entre extract.py de conectores (#86).

Extrai SÓ o que é genuinamente comum aos 3 conectores hoje (BoF4/Souldiers/Utawarerumono):
resolução de caminho de origem, escrita de dialogs.csv e de extraction_log.md. O parsing
binário/UnityPy/sdat de cada formato continua 100% específico por projeto — não há classe
base nem interface obrigatória aqui, só funções puras que os conectores adotam onde servem.
"""
from __future__ import annotations

import csv
import json
import os
import re
from collections import Counter
from pathlib import Path


def resolve_source_path(
    *,
    cli_arg: str | None = None,
    env_var: str | None = None,
    project_json: Path | None = None,
    cfg_key: str | None = None,
    relative_base: Path | None = None,
    error_hint: str = "",
    exc: type[BaseException] = SystemExit,
    allow_missing: bool = False,
) -> Path | None:
    """Resolve caminho de origem com precedência CLI > env var > project.json[connector][cfg_key].

    `relative_base`: se o caminho vier do project.json e não for absoluto, resolve contra esta
    base (só se aplica à fonte project.json — CLI/env var são usados como fornecidos).
    `allow_missing`: se True, retorna None em vez de levantar `exc` quando nenhuma fonte resolve
    o caminho (uso: chamador quer combinar a checagem de "não configurado" com a de "não existe").
    """
    if cli_arg:
        return Path(cli_arg)
    if env_var and os.environ.get(env_var):
        return Path(os.environ[env_var])
    if project_json is not None and cfg_key:
        cfg = json.loads(Path(project_json).read_text(encoding="utf-8"))
        declared = cfg.get("connector", {}).get(cfg_key)
        if declared:
            p = Path(declared)
            if relative_base is not None and not p.is_absolute():
                p = relative_base / p
            return p
    if allow_missing:
        return None
    raise exc(error_hint)


def write_dialogs_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    """mkdir + csv.DictWriter — mecânica idêntica nos 3 conectores, só fieldnames muda."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def write_extraction_log(path: Path, text: str) -> None:
    """mkdir + write_text — o texto formatado (contagens etc.) continua responsabilidade do conector."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def structural_token_rx(formatting_tokens: list[str], formatting_token_patterns: list[str]) -> re.Pattern:
    """Regex dos tokens de formatacao do engine (<C1>/<P2>/etc., de project.json). MESMA regex usada
    tanto no retry de traducao (framework/runtime/model.py, dentro do fitting loop) quanto no gate
    pos-hoc do conector (build_plan_chapter.py) — extraida aqui pra nunca divergir entre as duas
    checagens (bug real: 7/447 linhas em mp0010_01, 2026-08-24, quando cada lado tinha sua propria
    copia da mesma logica)."""
    literal = [re.escape(t) for t in formatting_tokens]
    parts = literal + [f"(?:{p})" for p in formatting_token_patterns]
    return re.compile("|".join(parts)) if parts else re.compile(r"(?!)")


def structural_tokens_match(rx: re.Pattern, source: str, text: str) -> bool:
    """True se `text` preserva o MESMO multiset de tokens de formatacao que `source` (conta E tipo)."""
    return Counter(rx.findall(source or "")) == Counter(rx.findall(text or ""))
