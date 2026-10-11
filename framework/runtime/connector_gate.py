#!/usr/bin/env python3
"""
connector_gate.py — GATE DE COMPLETUDE DE CONECTOR (espelha kb_gate.py).

Descoberto no onboarding do Souldiers (2026-07-02): `project.json` declarava "Fase 0 concluida" com
so `extract.py`/`reinsert.py` prontos -- `build_plan_chapter.py`/`verify_chapter.py` nunca existiram,
ou seja, round-trip NUNCA tinha sido validado de verdade. Mesma classe de bug do gap de KB: "fase
declarada concluida" sem nenhum gate automatico checando o conjunto completo de artefatos antes do
primeiro gasto real em traducao.

Checagens (deterministas, sem rede):
  HARD (bloqueiam sempre, nao bypassavel):
    - build_plan_script E verify_script (via connector_mgr, resolve overrides de project.json)
      existem no disco. Sem eles, nenhum round-trip e fisicamente possivel.
    - e NAO sao a copia intocada do _skeleton (scaffold_project copia o skeleton p/ connector/ --
      a copia sem adaptar nao pode passar o gate, mesma governanca do placeholder de KB).
  problems (bloqueiam, sem flag de bypass):
    - nenhuma cena do projeto tem verified=True em run_state.json -- round-trip nunca rodou verde
      nem uma vez. Reusa o `run_state.json` que ja existe (connector_mgr grava `connector_hash` la
      a cada verify bem-sucedido) -- nao precisa de manifest/timestamp novo. Excecao: run_scene
      de 1 cena COM verify (o piloto) nao e bloqueado por isto -- e ele que produz o 1o round-trip
      verde; o bloqueio vale p/ a escala (run_chapter) e p/ run_scene sem verify.
    - conector hex_binary com texto legivel no binario de origem que nao esta em nenhuma string
      extraida (residual_text.py) -- extract cortando/pulando string. Round-trip identico nao pega
      isso: extract e reinsert erram no mesmo lugar (BoF4, issue #222).
    - conector hex_binary sem connector.data_dir_env (ou env nao setada) -- o check acima nao tem
      como rodar, e check que nao roda nao pode contar como verde.
  warnings (nunca bloqueiam):
    - connector/test_roundtrip.py ausente -- dev-only (pytest), nao e chamado pelo runtime.

connector_gate roda ANTES do kb_gate (em run_scene.py e run_chapter.py): sem conector completo, uma
KB reconciliada nao serve de nada (nao ha como traduzir/validar nada de verdade).

Uso (CLI):  python connector_gate.py <projeto>
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent / "connectors"))
import paths  # noqa: E402  (paths.py: fonte unica do contrato de caminhos de artefato)
import residual_text  # noqa: E402  (framework/connectors: texto que o extract deixou para tras)
from connector_mgr import (
    _connector_script,  # noqa: E402  (mesmo resolvedor de path que run_scene usa)
)


class StaleReadError(RuntimeError):
    """Gate de leitura completa: o conteudo alegado como lido nao bate com o disco AGORA."""

_SCRIPTS = (("build_plan_script", "build_plan_chapter.py"), ("verify_script", "verify_chapter.py"))
_SKELETON = _HERE.parent / "connectors" / "_skeleton"


def _is_unadapted_skeleton(p: Path, default: str) -> bool:
    sk = _SKELETON / default
    if not sk.is_file():
        return False
    return p.read_bytes().replace(b"\r\n", b"\n") == sk.read_bytes().replace(b"\r\n", b"\n")  # autocrlf


def _has_green_roundtrip(root: Path) -> bool:
    """True se ALGUMA cena do projeto ja tem verified=True em run_state.json -- reusa o estado que
    connector_mgr/run_scene ja gravam a cada verify bem-sucedido (connector_hash + verified)."""
    rs = paths.run_state(root)
    if not rs.is_file():
        return False
    try:
        scenes = json.loads(rs.read_text(encoding="utf-8")).get("scenes", {})
    except (json.JSONDecodeError, OSError):
        return False
    return any(v.get("verified") is True for v in scenes.values())


def _source_dir(conn: dict) -> Path | None:
    """Pasta dos binarios de origem: a env var nomeada em connector.data_dir_env (o caminho nunca
    vai para o project.json). None = projeto nao declarou ou a env nao esta setada."""
    env = os.environ.get(conn.get("data_dir_env") or "")
    return Path(env) if env else None


def _residual_text(root: Path, cfg: dict) -> tuple[list[str], list[str]]:
    """(problems, warnings) do check de texto residual -- so conector hex_binary. Round-trip
    identico nao prova extracao completa: ver framework/connectors/residual_text.py (issue #222)."""
    conn = cfg.get("connector") or {}
    if conn.get("type") != "hex_binary":
        return [], []
    src_cfg = cfg.get("source") or {}
    csv_path = root / src_cfg.get("file", "artifacts/dialogs.csv")
    src = _source_dir(conn)
    if src is None or not src.is_dir() or not csv_path.is_file():
        return ["texto residual NAO checado — declare connector.data_dir_env e sete essa env "
                "apontando para os binarios de origem; sem isso string truncada na extracao "
                "passa despercebida (round-trip continua verde)."], []
    try:
        r = residual_text.check(csv_path, src, text_column=src_cfg.get("text_column", "text_en"))
    except KeyError as e:
        return [], [f"texto residual NAO checado — {csv_path.name} sem a coluna {e}."]
    if r["passed"]:
        return [], []
    worst = ", ".join(f"{n} {m}/{t}" for n, m, t in r["per_file"][:3])
    return [f"extracao incompleta: {r['n_residual']}/{r['n_runs']} trecho(s) de texto legivel do "
            f"binario ({r['ratio']:.1%}) nao estao em nenhuma string extraida — o extract.py esta "
            f"cortando ou pulando strings (ex.: {r['examples'][0]!r}; piores: {worst}). Detalhe: "
            f"python framework/connectors/residual_text.py {csv_path} {src}"], []


def check(root) -> dict:
    """Retorna {hard_problems: [...], problems: [...], warnings: [...]}. Nao depende de cena (a
    completude de conector e uma propriedade do PROJETO, nao de uma cena especifica)."""
    root = Path(root)
    cfg_path = root / "project.json"
    hard_problems: list[str] = []
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.is_file() else {}
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
        # cfg={} faria _connector_script() cair pros paths DEFAULT calado -- se o projeto usa
        # connector.build_plan_script/verify_script customizado, o gate passaria checando o
        # arquivo ERRADO em vez de acusar o project.json quebrado. Vira hard_problem em vez de
        # mascarar (mesma convencao de kb_gate.check()).
        cfg = {}
        hard_problems.append(f"project.json corrompido/ilegivel ({e}) — corrija antes de continuar "
                              f"(overrides de connector.* ficam invisiveis enquanto isso).")
    for key, default in _SCRIPTS:
        p = _connector_script(root, cfg, key, default)
        if not p.is_file():
            hard_problems.append(
                f"{key} ausente ({p}) — sem ele nenhum round-trip e possivel. Este gate nao pode ser pulado."
            )
        elif _is_unadapted_skeleton(p, default):
            hard_problems.append(
                f"{key} ({p}) ainda e a copia intocada do _skeleton — adapte ao formato do jogo "
                f"(Fase 0). Este gate nao pode ser pulado."
            )
    problems: list[str] = []
    if not hard_problems and not _has_green_roundtrip(root):
        problems.append(
            "nenhuma cena com round-trip verde registrado (run_state.json) — rode o piloto de 1 cena "
            "via run_scene.py (com verify) antes de traduzir em escala."
        )
    warnings: list[str] = []
    if not hard_problems:
        residual_problem, residual_warning = _residual_text(root, cfg)
        problems += residual_problem
        warnings += residual_warning
    if not (root / "connector" / "test_roundtrip.py").is_file():
        warnings.append(
            "connector/test_roundtrip.py ausente — round-trip nunca validado via teste automatizado "
            "(dev-only, nao bloqueia o runtime)."
        )
    return {"hard_problems": hard_problems, "problems": problems, "warnings": warnings}


def assert_fresh_read(script_path, claimed_content: str) -> None:
    """Gate de LEITURA COMPLETA: antes de editar um conector existente, o caller PRECISA ter
    lido o arquivo por inteiro AGORA (nao de memoria antiga). Interpretacao operacional escolhida
    (a mais codificavel/testavel de provar programaticamente): o caller passa o CONTEUDO INTEIRO
    que alega ter lido (nao um path) -- a unica forma de produzir isso e te-lo lido de verdade. O
    gate compara o hash do conteudo alegado contra o hash do arquivo NO DISCO agora; diverge =
    ou o arquivo mudou desde a leitura, ou o conteudo nunca foi lido de verdade (alucinado/stale).
    Levanta StaleReadError (nunca retorna False silenciosamente) -- forca o caller a lidar com isso."""
    script_path = Path(script_path)
    if not script_path.is_file():
        raise StaleReadError(f"{script_path} nao existe — nada para validar leitura")
    actual = hashlib.sha1(script_path.read_bytes(), usedforsecurity=False).hexdigest()
    claimed = hashlib.sha1(claimed_content.encode("utf-8"), usedforsecurity=False).hexdigest()
    if actual != claimed:
        raise StaleReadError(
            f"{script_path}: conteudo alegado nao bate com o disco agora — releia antes de editar"
        )


def main():
    ap_project = sys.argv[1] if len(sys.argv) > 1 else None
    if not ap_project:
        print("uso: python connector_gate.py <projeto>")
        sys.exit(2)
    r = check(ap_project)
    for w in r["warnings"]:
        print(f"[warn] {w}")
    for p in r["hard_problems"]:
        print(f"[HARD-BLOCK] {p}")
    for p in r["problems"]:
        print(f"[BLOCK] {p}")
    all_problems = r["hard_problems"] + r["problems"]
    print("\nOK: conector completo." if not all_problems else
          f"\nBLOQUEADO: {len(all_problems)} problema(s) de completude de conector.")
    sys.exit(1 if all_problems else 0)


if __name__ == "__main__":
    main()
