import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from block_no_verify import blocked  # noqa: E402

BLOCK = [
    "git commit --no-verify -m x",
    "git push --no-verify",
    "git commit -n -m x",
    "git commit -anm x",
    "git commit --amend -n",
    "git commit --no-gpg-sign",
    "git -c commit.gpgsign=false commit -m x",
    "git -c commit.gpgSign=false commit -m x",
    "git -c commit.gpgsign=0 commit",
    "git -c core.hooksPath=NUL commit -m x",
    "git config commit.gpgsign false",
    "SKIP=ruff git commit -m x",
    '$env:HUSKY="0"; git commit -m x',
    'git add . && git commit -m "ok" --no-verify',
]
ALLOW = [
    "git commit -m 'remove --no-verify do script'",
    'git commit -am "doc: --no-verify e -n"',
    "git commit -F msg.txt",
    "git push origin worktree-x",
    "git push -n",                      # dry-run, nao e --no-verify
    "git commit --no-edit --amend",
    "git status",
    "ls -n",
    "echo --no-verify",
]


@pytest.mark.parametrize("cmd", BLOCK)
def test_blocks(cmd):
    assert blocked(cmd)


@pytest.mark.parametrize("cmd", ALLOW)
def test_allows(cmd):
    assert not blocked(cmd)


def _run_hook(stdin: str):
    return subprocess.run([sys.executable, str(Path(__file__).with_name("block_no_verify.py"))],  # nosec B603
                          input=stdin, capture_output=True, text=True)


def test_hook_emits_deny_json_for_blocked_and_nothing_for_allowed():
    r = _run_hook('{"tool_input": {"command": "git commit -n -m x"}}')
    assert r.returncode == 0 and '"permissionDecision": "deny"' in r.stdout
    r = _run_hook('{"tool_input": {"command": "git status"}}')
    assert r.returncode == 0 and r.stdout == ""


def test_hook_fails_closed_on_garbage_stdin():
    r = subprocess.run([sys.executable, str(Path(__file__).with_name("block_no_verify.py"))],  # nosec B603
                       input="not json", capture_output=True, text=True)
    assert r.returncode == 2
