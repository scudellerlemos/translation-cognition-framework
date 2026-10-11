"""Guard de conteudo: nada de jogo (binario, roteiro, traducao de cena, print, planilha de revisao,
saida de descompilador) nem e-mail pessoal entra no repo.

Tres usos, mesma regra:
  python .claude/hooks/content_guard.py                  # CI/local: rastreados + nao-ignorados
  python .claude/hooks/content_guard.py --commits A..B   # CI: e-mail de autor/committer do range
  (PreToolUse Bash|PowerShell, JSON no stdin)            # barra `git add/commit/push` do agente

Extensao e ALLOWLIST, e projects/*/artifacts/ tambem (ARTIFACTS_ALLOWED): o que nao esta na
lista falha -- tipo novo ou artefato gerado novo exige decisao explicita aqui. Falha FECHADO como o block_no_verify.
"""
import json
import re
import subprocess
import sys

ALLOWED_EXT = {"py", "md", "json", "jsonl", "csv", "yml", "yaml", "txt", "toml", "sql", "ini", "cfg",
               "gitignore", "gitkeep", "gitattributes", "example", "coveragerc-ml"}
ALLOWED_NAMES = {"LICENSE", "VERSION"}
# projects/demo e sintetico (dialogo ficticio) -- unico lugar onde dialogs.csv e versionado.
_DEMO = re.compile(r"^projects/demo/artifacts/.*/dialogs\.csv$")
DENIED_PATHS = [(re.compile(rx), why) for rx, why in [
    (r"(^|/)\.env(\.local)?$", "segredo (.env)"),
    (r"\.local\.md$", "nota local (*.local.md)"),
    (r"^projects/[^/]+/(output|source_dat|manual_tests)/", "binario do jogo (original ou remontado)"),
    (r"^projects/[^/]+/artifacts/.*(dialogs\.csv|translations_[^/]*\.json|translation_plan[^/]*\.json"
     r"|approved_[^/]*\.csv|back_translation_[^/]*\.json|translation_memory\.jsonl)$", "roteiro/traducao de cena"),
    (r"^projects/[^/]+/artifacts/(evidence|research_cache)/", "print do jogo / texto bruto de fonte"),
    (r"^projects/[^/]+/artifacts/qa_revisao/(para_revisar|devolvido)/", "planilha de revisao"),
    (r"(^|/)(review_[^/]*\.csv|interjection_(corrections|revisions)\.csv)$", "planilha de revisao"),
    (r"^projects/[^/]+/artifacts/kb_phase_worklist_[^/]*\.md$", "worklist gerada (trechos do jogo)"),
    (r"(^|/)(bench_[^/]*\.json|_build_translations\.py)$", "traducao de cena embutida"),
]]
# projects/<jogo>/artifacts/ e DEFAULT-DENY: so entra o que esta nesta lista (caminho relativo a
# artifacts/). E onde os geradores escrevem -- um gerador novo que cite fala do jogo (caso das
# worklists de kb_phase) nasce bloqueado ate alguem decidir aqui, olhando o conteudo, que pode.
ARTIFACTS_ALLOWED = {
    "api_ledger.jsonl", "cost_report.md", "decision_log.md", "entities.csv", "entities_candidates.json",
    "extraction_log.md", "glossary.csv", "kb_phase_worklist.md", "kb_ratified.csv", "metrics.jsonl",
    "qa_effectiveness.jsonl", "qa_report.md", "reinsertion_report.md", "research_log.md", "residue.json",
    "run_state.json", "scenes_index.json", "spoiler_audit.json", "spoiler_ledger.json", "tone_analysis.md",
    "universe_knowledge_base.md", "warnings.jsonl",
    "state/decision_index.json", "state/portrait_codes.json", "state/voice_cards.json",
    "qa_revisao/LEIA-ME.md", "qa_revisao/teste_ingame/relato_tester.csv",
    # legado do Utawarerumono (piloto, pre-padronizacao) -- nao usar como precedente
    "archive/aliases_map.json", "archive/entities_candidates.json", "archive/extraction_log.md",
    "archive/interjection_reference.md", "archive/micro_qa_log.json", "archive/translation_status.json",
    "scenes/ch_11_03/calibration_report.md",
}
_ARTIFACT = re.compile(r"^projects/[^/]+/artifacts/(.+)$")
# Saida de descompilador (Ghidra/IDA): nota de RE fica local, nunca no repo.
_DECOMP = re.compile(rb"\b(?:FUN|DAT|LAB|PTR|sub)_[0-9a-fA-F]{6,8}\b")
_OK_EMAIL = re.compile(r"(@users\.noreply\.github\.com|^noreply@github\.com)$")
_GIT_WRITE = re.compile(r"\bgit\b.*\b(add|commit|push)\b", re.I | re.S)


def path_problem(path: str) -> str | None:
    name = path.rsplit("/", 1)[-1]
    if _DEMO.search(path) or name in (".gitignore", ".gitkeep"):
        return None
    for rx, why in DENIED_PATHS:
        if rx.search(path):
            return why
    art = _ARTIFACT.match(path)
    if art and art[1] not in ARTIFACTS_ALLOWED:
        return "artefato fora da allowlist (ARTIFACTS_ALLOWED) -- gerado novo: ignore, ou libere apos conferir o conteudo"
    ext = name.rsplit(".", 1)[-1] if "." in name else ""
    if name not in ALLOWED_NAMES and ext not in ALLOWED_EXT:
        return f"extensao fora da allowlist (.{ext or '?'})"
    return None


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, check=True, encoding="utf-8").stdout


def scan_tree() -> list[str]:
    """Rastreados + nao rastreados que o .gitignore NAO cobre (o que um `git add .` pegaria)."""
    out = []
    for path in filter(None, _git("ls-files", "-z", "--cached", "--others", "--exclude-standard").split("\0")):
        why = path_problem(path)
        if not why:
            try:
                with open(path, "rb") as fh:
                    if _DECOMP.search(fh.read()):
                        why = "saida de descompilador (FUN_/DAT_...)"
            except OSError:  # apagado no working tree, ainda no index
                pass
        if why:
            out.append(f"{path}: {why}")
    return out


def scan_commits(rng: str) -> list[str]:
    emails = {e for e in _git("log", "--format=%ae%n%ce", rng).split() if not _OK_EMAIL.search(e)}
    return [f"commit com e-mail pessoal ({e}) -- use o noreply do GitHub" for e in sorted(emails)]


def main() -> int:
    if "--commits" in sys.argv:
        problems = scan_commits(sys.argv[sys.argv.index("--commits") + 1])
    elif sys.stdin.isatty() or len(sys.argv) > 1:
        problems = scan_tree()
    else:  # hook: so age em git add/commit/push
        raw = sys.stdin.read()
        if raw.strip() and not _GIT_WRITE.search(json.loads(raw).get("tool_input", {}).get("command", "")):
            return 0
        problems = scan_tree()
        if problems:
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse", "permissionDecision": "deny",
                "permissionDecisionReason": "content_guard: conteudo proibido no repo -- ignore no .gitignore "
                                            "ou remova antes de commitar:\n" + "\n".join(problems[:20])}}))
        return 0
    for p in problems:
        print(f"ERRO {p}")
    print(f"content_guard: {len(problems)} problema(s)" if problems else "content_guard: OK")
    return 1 if problems else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - fail closed
        print(f"content_guard: erro ({exc!r}) -- bloqueando por seguranca", file=sys.stderr)
        sys.exit(2)
