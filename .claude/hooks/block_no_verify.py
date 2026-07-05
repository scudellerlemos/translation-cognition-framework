import json
import re
import sys

d = json.load(sys.stdin)
cmd = d.get("tool_input", {}).get("command", "")

is_git_commit_or_push = re.search(r"\bgit\b", cmd) and re.search(r"\b(commit|push)\b", cmd)
is_bypass = re.search(r"(--no-verify|--no-gpg-sign|-c\s+commit\.gpgsign=false)", cmd)

if is_git_commit_or_push and is_bypass:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Bloqueado: --no-verify/--no-gpg-sign/commit.gpgsign=false nao e "
                "permitido neste projeto (regra global do usuario, CLAUDE.md)."
            ),
        }
    }))
