"""connector_mgr.py — Interface com os scripts de conector (subprocesso, hash, integridade).

Extraído de run_scene.py para separar a camada de interface com build_plan_chapter.py /
verify_chapter.py da lógica de orquestração de cena.

Funções públicas (usadas por run_scene):
  _connector_script  — resolve path do script (com sandbox de path traversal)
  _connector_hash    — SHA1 dos scripts (audit trail de versão)
  _run               — executa subprocesso com encoding robusto (Windows-safe)
  _verify_status     — parse da linha VERIFY_STATUS: {json} emitida pelo conector
  _warn_if_connector_stale — avisa se conector mudou desde o último verify
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

import paths  # fonte única do contrato de caminhos de artefato

_CONNECTOR_TIMEOUT = 300   # segundos; conector travado (build_plan/verify) não bloqueia o pipeline


def _connector_script(root: Path, cfg: dict, key: str, default: str) -> Path:
    override = cfg.get("connector", {}).get(key)
    p = (root / override) if override else (root / "connector" / default)
    if not p.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"conector fora do projeto: {p!r} (override={override!r})")
    return p


def _connector_hash(root: Path, cfg: dict) -> str:
    """SHA1 do conteúdo dos scripts do conector — identifica a versão em uso no momento da verificação.
    Gravado no run_state.json junto com 'verified=True': artefato sabe com qual conector foi gerado.
    Conector ausente (em-desenvolvimento) = hash de string vazia por slot."""
    h = hashlib.sha1(usedforsecurity=False)
    for key, default in [("build_plan_script", "build_plan_chapter.py"),
                          ("verify_script", "verify_chapter.py")]:
        p = _connector_script(root, cfg, key, default)
        if p.is_file():
            h.update(p.read_bytes())
    return h.hexdigest()[:12]


def _run(cmd, timeout=_CONNECTOR_TIMEOUT) -> tuple[int, str]:
    # ROBUSTEZ (Windows): o filho (build_plan/verify) pode imprimir bytes não-utf-8 (acentos cp1252 no
    # console). Sem proteção, a thread leitora do subprocess quebrava com UnicodeDecodeError e derrubava
    # o run_chapter NO MEIO da run (em background isso deixava o chip da UI preso, sem saída limpa).
    # Dupla defesa: (1) PYTHONIOENCODING/PYTHONUTF8 forçam o filho a EMITIR utf-8; (2) errors='replace'
    # como rede de segurança → nunca quebra. Os matches do run_scene ('fora do arquivo' etc.) são ASCII.
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
    # stdin=DEVNULL: os connectors não leem stdin; evita herdar o stdin do pai (sob captura de
    # pytest/headless o stdin não tem handle de OS → DuplicateHandle falharia no Windows).
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", env=env, stdin=subprocess.DEVNULL,
                           timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return 1, f"[timeout] conector não respondeu em {timeout}s — verifique o script e rode novamente."


def _verify_status(out: str) -> dict:
    """Protocolo estruturado de saída do conector: lê a 1 linha 'VERIFY_STATUS: {json}' que o conector emite.
    Fallback do exit-code — conector legado sem a linha → {} (run_scene usa o exit-code 3 como sinal primário)."""
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("VERIFY_STATUS:"):
            try:
                return json.loads(line[len("VERIFY_STATUS:"):].strip())
            except Exception:
                return {}
    return {}


def _warn_if_connector_stale(root: Path, scene: str, cfg: dict) -> None:
    """S3: avisa se o hash do conector mudou desde o último verify desta cena.
    Não bloqueia (auditoria); apenas garante que o operador saiba que o artefato verificado
    foi gerado com uma versão diferente do conector atual."""
    rs = paths.run_state(root)
    if not rs.is_file():
        return
    try:
        saved = json.loads(rs.read_text(encoding="utf-8")).get("scenes", {}).get(scene, {})
        last_hash = saved.get("connector_hash")
        if last_hash and last_hash != _connector_hash(root, cfg):
            print(f"[S3] AVISO: conector mudou desde o último verify de '{scene}' "
                  f"(hash salvo: {last_hash[:8]}… ≠ atual: {_connector_hash(root, cfg)[:8]}…). "
                  "Re-verificação recomendada.")
    except Exception:
        pass
