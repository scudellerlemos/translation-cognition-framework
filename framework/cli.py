"""cli.py — CLI unificada do Translation Cognition Framework.

Ponto de entrada único para operações do pipeline. Substitui os 15+ scripts
invocados manualmente por subcomandos organizados.

Uso:
  python framework/cli.py translate <project> <scene> [--backend ollama|api]
  python framework/cli.py bench     <project> <scene> [--model qwen2.5:14b]
  python framework/cli.py db migrate <bof4_root> <dest_db>
  python framework/cli.py db summary <db_path> <project_id>
  python framework/cli.py ollama status
  python framework/cli.py ollama pull <model>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_RUNTIME = _HERE / "runtime"
_DB = _HERE / "db"
_SKILLS = _HERE / "skills"
for _p in (_RUNTIME, _DB, _SKILLS):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))


# ── translate ──────────────────────────────────────────────────────────────────

def cmd_translate(args):
    import run_scene as rs
    result = rs.run_scene(
        args.project, args.scene,
        backend=args.backend,
        require_back=getattr(args, "require_back", False),
        do_verify=not getattr(args, "no_verify", False),
        skip_kb_gate=getattr(args, "skip_kb_gate", False),
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("status") in ("verified", "planned") else 1


# ── bench ──────────────────────────────────────────────────────────────────────

def cmd_bench(args):
    from bench_local import run_bench
    from ollama_client import OLLAMA_MODEL_DEFAULT
    run_bench(
        Path(args.project), args.scene,
        model=getattr(args, "model", None) or OLLAMA_MODEL_DEFAULT,
        out_path=Path(args.out) if getattr(args, "out", None) else None,
    )
    return 0


# ── db ─────────────────────────────────────────────────────────────────────────

def cmd_db_migrate(args):
    from migrate_from_flat import migrate
    result = migrate(Path(args.bof4_root), Path(args.dest_db),
                     project_id=args.project_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def cmd_db_summary(args):
    from store import Store
    with Store(args.db_path) as db:
        summary = db.summary(args.project_id)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def cmd_db_export(args):
    """Exporta os flats de intercâmbio (approved_translations.csv + translation_memory.jsonl)
    a partir do DB — Fase 6 (cutover): DB autoritativo, flat derivado."""
    from export_to_flat import export
    result = export(Path(args.db_path), args.project_id, Path(args.out_dir))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def cmd_db_index(args):
    """Indexa embeddings da TM no banco SQLite."""
    import sqlite3

    from embedder import Embedder
    from store import Store
    with Store(args.db_path):
        con = sqlite3.connect(args.db_path)
        emb = Embedder()
        n = emb.index_project(con, project_id=args.project_id,
                               force=getattr(args, "force", False))
        con.close()
    print(f"Indexados: {n} vetores para projeto '{args.project_id}'")
    return 0


# ── skill ────────────────────────────────────────────────────────────────────────

def cmd_skill_list(args):
    import registry
    for s in registry.all_skills():
        print(f"{s.skill_id}  {s.kind:<14} {s.name}")
    return 0


def cmd_skill_check(args):
    import registry
    s = registry.get(args.skill_id)
    if s is None:
        print(f"skill desconhecida: {args.skill_id}", file=sys.stderr)
        return 2
    problems = s.check_inputs(Path(args.project))
    if problems:
        for p in problems:
            print(f"GATE: {p}")
        return 1
    print(f"OK: gate de entrada da skill {s.skill_id} ({s.name}) satisfeito")
    return 0


def cmd_skill_run(args):
    import registry
    s = registry.get(args.skill_id)
    if s is None:
        print(f"skill desconhecida: {args.skill_id}", file=sys.stderr)
        return 2
    kwargs = {}
    for k in ("scene", "chapter", "dat_dir", "backend"):
        v = getattr(args, k, None)
        if v is not None:
            kwargs[k] = v
    result = s.run(Path(args.project), **kwargs)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("status") in ("ok", "planned", "verified") else 1


# ── ollama ─────────────────────────────────────────────────────────────────────

def cmd_ollama_status(args):
    from ollama_client import OLLAMA_HOST, OLLAMA_MODEL_DEFAULT, health_check, list_models
    ok = health_check()
    print(f"Ollama em {OLLAMA_HOST}: {'OK' if ok else 'OFFLINE'}")
    if ok:
        models = list_models()
        print(f"Modelos disponíveis: {models or '(nenhum)'}")
        print(f"Modelo padrão: {OLLAMA_MODEL_DEFAULT}")
    return 0 if ok else 1


def cmd_ollama_pull(args):
    import subprocess
    print(f"Baixando {args.model}...")
    result = subprocess.run(["ollama", "pull", args.model])
    return result.returncode


# ── main ───────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="framework",
        description="Translation Cognition Framework — CLI unificada",
    )
    sub = ap.add_subparsers(dest="command", required=True)

    # translate
    p_tr = sub.add_parser("translate", help="Traduz uma cena (run_scene)")
    p_tr.add_argument("project", help="Diretório do projeto")
    p_tr.add_argument("scene", help="ID da cena (ex: AREAD001)")
    p_tr.add_argument("--backend", default="api",
                      choices=["in-session", "api", "ollama"])
    p_tr.add_argument("--no-verify", action="store_true")
    p_tr.add_argument("--skip-kb-gate", action="store_true")
    p_tr.add_argument("--require-back", action="store_true")
    p_tr.set_defaults(func=cmd_translate)

    # bench
    p_bench = sub.add_parser("bench", help="Benchmark Ollama vs baseline Sonnet")
    p_bench.add_argument("project", help="Raiz do projeto BoF4 (com aprovados)")
    p_bench.add_argument("scene", help="Cena a benchmarkar")
    p_bench.add_argument("--model", default=None)
    p_bench.add_argument("--out", default=None, help="Salva resultado JSON")
    p_bench.set_defaults(func=cmd_bench)

    # db
    p_db = sub.add_parser("db", help="Operações no banco SQLite")
    db_sub = p_db.add_subparsers(dest="db_command", required=True)

    p_mig = db_sub.add_parser("migrate", help="Migra flat files para SQLite")
    p_mig.add_argument("bof4_root", help="Raiz do projeto BoF4")
    p_mig.add_argument("dest_db", help="Banco de destino (.db)")
    p_mig.add_argument("--project-id", default="bof4")
    p_mig.set_defaults(func=cmd_db_migrate)

    p_sum = db_sub.add_parser("summary", help="Resumo do banco")
    p_sum.add_argument("db_path")
    p_sum.add_argument("project_id")
    p_sum.set_defaults(func=cmd_db_summary)

    p_exp = db_sub.add_parser("export", help="Exporta flats de intercâmbio do DB (Fase 6)")
    p_exp.add_argument("db_path")
    p_exp.add_argument("project_id")
    p_exp.add_argument("out_dir", help="Diretório de saída (ex.: projects/<x>/artifacts)")
    p_exp.set_defaults(func=cmd_db_export)

    p_idx = db_sub.add_parser("index", help="Indexa embeddings da TM")
    p_idx.add_argument("db_path")
    p_idx.add_argument("project_id")
    p_idx.add_argument("--force", action="store_true")
    p_idx.set_defaults(func=cmd_db_index)

    # skill
    p_sk = sub.add_parser("skill", help="Roda skills do pipeline (registry det./orquestração)")
    sk_sub = p_sk.add_subparsers(dest="skill_command", required=True)

    sk_sub.add_parser("list", help="Lista as skills registradas (id, kind, nome)").set_defaults(
        func=cmd_skill_list
    )
    p_skc = sk_sub.add_parser("check", help="Roda só o gate de entrada de uma skill")
    p_skc.add_argument("skill_id", help="ID da skill (ex: 00, 06, 07, 08)")
    p_skc.add_argument("project", help="Diretório do projeto")
    p_skc.set_defaults(func=cmd_skill_check)

    p_skr = sk_sub.add_parser("run", help="Roda uma skill ponta-a-ponta")
    p_skr.add_argument("skill_id", help="ID da skill (ex: 00, 06, 07, 08)")
    p_skr.add_argument("project", help="Diretório do projeto")
    p_skr.add_argument("--scene", default=None, help="cena (skills 06)")
    p_skr.add_argument("--chapter", default=None, help="capítulo (skill 07)")
    p_skr.add_argument("--dat-dir", dest="dat_dir", default=None, help="dir dos DATs (skills 00/08)")
    p_skr.add_argument("--backend", default=None, choices=["in-session", "api", "ollama"])
    p_skr.set_defaults(func=cmd_skill_run)

    # ollama
    p_ol = sub.add_parser("ollama", help="Gerencia o Ollama local")
    ol_sub = p_ol.add_subparsers(dest="ollama_command", required=True)

    ol_sub.add_parser("status", help="Verifica se Ollama está rodando").set_defaults(
        func=cmd_ollama_status
    )
    p_pull = ol_sub.add_parser("pull", help="Baixa um modelo")
    p_pull.add_argument("model", help="Nome do modelo (ex: qwen2.5:14b)")
    p_pull.set_defaults(func=cmd_ollama_pull)

    return ap


def main():
    ap = build_parser()
    args = ap.parse_args()
    sys.exit(args.func(args) or 0)


if __name__ == "__main__":
    main()
