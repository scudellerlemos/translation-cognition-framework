#!/usr/bin/env python3
"""
fingerprint_monitor.py — D3: manifesto + versionamento + fingerprint de conector.

`connector_mgr._connector_hash` ja faz hash dos SCRIPTS do conector (build_plan_chapter.py +
verify_chapter.py), gravado por-cena em run_state.json a cada verify bem-sucedido -- isso NAO e
duplicado aqui. O que faltava: (1) um manifesto FORMAL por-projeto (tier/engine/versao/status,
nao so um hash solto em run_state.json) e (2) fingerprint dos ARQUIVOS-FONTE do jogo (um patch do
Steam mudando o .bundle/.DAT nao e detectado por NADA hoje -- _connector_hash so ve os scripts).

Escopo deliberado: NAO amarrado no hot path de run_scene/run_chapter (ler os arquivos-fonte do
jogo exige o data_dir da instalacao, que pode nem estar montado em CI/teste). E um check de
PROJETO INTEIRO, rodado manualmente via CLI quando o operador suspeita que o jogo foi atualizado --
complementa (nao substitui) `_warn_if_connector_stale`, que continua cobrindo so o drift de SCRIPT
por-cena.

Puro/deterministico: nenhuma funcao aqui chama datetime.now() -- o timestamp e passado pelo caller
(mesmo padrao de kb_fetch.py `fetched_em`).

Uso: python fingerprint_monitor.py <projeto> --check-source <arquivo1> [<arquivo2> ...]
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
from connector_mgr import (
    _connector_hash,  # noqa: E402  (reusa o hash de scripts existente, nao duplica)
)


def _manifest_path(root) -> Path:
    return Path(root) / "connector_manifest.json"


def compute_fingerprint(file_paths: list) -> str:
    """SHA1 concatenado dos arquivos (ordem estavel, paths ordenados antes de ler) -- deterministico
    e sensivel a qualquer mudanca de 1 byte em qualquer arquivo da lista."""
    h = hashlib.sha1(usedforsecurity=False)
    for p in sorted(Path(p) for p in file_paths):
        if p.is_file():
            h.update(p.read_bytes())
    return h.hexdigest()


def write_manifest(root, *, tier, engine_id, connector_version, scripts_fingerprint,
                   source_sample_files, source_fingerprint, timestamp_iso,
                   status="never", at_scene=None) -> Path:
    """Grava connector_manifest.json na raiz do projeto (identidade/config, ao lado de
    project.json -- nao e artefato de runtime, entao nao vive em artifacts/)."""
    root = Path(root)
    manifest = {
        "version": 1,
        "tier": tier,
        "engine_id": engine_id,
        "connector_version": connector_version,
        "scripts_fingerprint": scripts_fingerprint,
        "source_sample_files": [str(p) for p in source_sample_files],
        "source_fingerprint": source_fingerprint,
        "last_validated": {"status": status, "at_scene": at_scene, "timestamp_iso": timestamp_iso},
    }
    out = _manifest_path(root)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def read_manifest(root) -> dict | None:
    p = _manifest_path(root)
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def check_source_drift(root, current_fingerprint: str) -> bool:
    """True = os arquivos-fonte do jogo MUDARAM desde o manifesto (patch/atualizacao do jogo) --
    ou o manifesto nao existe/nao tem fingerprint registrada (nao ha base de comparacao, entao
    tambem conta como 'drift' — nao ha garantia de que o conector ainda e valido)."""
    manifest = read_manifest(root)
    if not manifest or not manifest.get("source_fingerprint"):
        return True
    return manifest["source_fingerprint"] != current_fingerprint


def check_scripts_drift(root, cfg: dict) -> bool:
    """True = os SCRIPTS do conector mudaram desde o manifesto. Reusa _connector_hash (mesmo hash
    que connector_mgr/run_scene ja usam) -- nao recalcula com logica propria."""
    manifest = read_manifest(root)
    if not manifest or not manifest.get("scripts_fingerprint"):
        return True
    return manifest["scripts_fingerprint"] != _connector_hash(Path(root), cfg)


def main():
    import argparse
    ap = argparse.ArgumentParser(description="D3: fingerprint de arquivos-fonte + manifesto de conector.")
    ap.add_argument("project")
    ap.add_argument("--check-source", nargs="+", metavar="ARQUIVO",
                    help="verifica se estes arquivos-fonte mudaram desde o manifesto registrado")
    a = ap.parse_args()
    root = Path(a.project)
    if a.check_source:
        current = compute_fingerprint(a.check_source)
        drifted = check_source_drift(root, current)
        if drifted:
            print("[fingerprint_monitor] AVISO: arquivos-fonte MUDARAM (ou nenhum manifesto "
                  "registrado ainda) desde a ultima validacao -- re-rode o round-trip antes de "
                  "confiar no conector.")
            sys.exit(1)
        print("[fingerprint_monitor] OK: arquivos-fonte identicos ao manifesto registrado.")
        sys.exit(0)
    manifest = read_manifest(root)
    if not manifest:
        print("[fingerprint_monitor] nenhum connector_manifest.json ainda.")
        sys.exit(1)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
