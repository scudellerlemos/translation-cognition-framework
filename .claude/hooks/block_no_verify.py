"""PreToolUse (Bash|PowerShell): bloqueia git commit/push que pulam hooks/assinatura.

Falha FECHADO: qualquer erro aqui sai com codigo 2 (bloqueia); o settings.json ainda
faz `|| exit 2` caso o proprio python nao exista. Limite conhecido: um script que chama
git por dentro (python x.py) escapa de qualquer regex sobre a string do comando.
"""
import json
import re
import sys

I = re.I
# texto de mensagem (-m "...", -am '...', --message=...) nao pode causar falso positivo
_MSG = re.compile(r"""(?:\s-[a-z]*m|\s--message)(?:=|\s+)(?:"[^"]*"|'[^']*')""", I)
_GIT = re.compile(r"\bgit\b", I)
_COMMIT_PUSH = re.compile(r"\b(commit|push)\b", I)
# (regex, so_vale_em_commit) -- config/hooksPath valem em qualquer comando git (setar antes, commitar depois)
_RULES = [
    (re.compile(r"--no-verify\b", I), False),
    (re.compile(r"--no-gpg-sign\b", I), False),
    (re.compile(r"\bcommit\b[^;&|\n]*\s-[a-z]*n[a-z]*\b", I), True),        # -n / -anm = --no-verify
    (re.compile(r"commit\.gpgsign[\s=]+(false|0|no|off)\b", I), False),     # chave de config e case-insensitive
    (re.compile(r"core\.hooks?path", I), False),
]
_ENV_SKIP = re.compile(r"\b(SKIP|HUSKY)\s*=", I)                              # pre-commit SKIP=..., HUSKY=0


def blocked(cmd: str) -> bool:
    cmd = _MSG.sub(" ", cmd)
    if not _GIT.search(cmd):
        return False
    is_cp = bool(_COMMIT_PUSH.search(cmd))
    if is_cp and _ENV_SKIP.search(cmd):
        return True
    return any(rx.search(cmd) for rx, only_commit in _RULES if is_cp or not only_commit)


def main() -> None:
    cmd = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    if blocked(cmd):
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    "Bloqueado: pular hooks/assinatura do git (--no-verify, -n, --no-gpg-sign, "
                    "commit.gpgsign=false, core.hooksPath, SKIP=/HUSKY=) nao e permitido neste projeto."
                ),
            }
        }))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 - fail closed
        print(f"block_no_verify: erro ({exc!r}) -- bloqueando por seguranca", file=sys.stderr)
        sys.exit(2)
