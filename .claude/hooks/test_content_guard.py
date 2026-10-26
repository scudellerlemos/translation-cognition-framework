import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_guard import _DECOMP, _GIT_WRITE, _OK_EMAIL, path_problem, scan_tree  # noqa: E402

DENY = [
    ".env",
    "projects/bof4/.env",
    "RISCOS.local.md",
    "projects/utawarerumono_prelude/artifacts/spoiler_audit.json",
    "projects/utawarerumono_prelude/artifacts/glossary.local.csv",
    "projects/utawarerumono/output/ScriptEvent.sdat",
    "projects/bof4/source_dat/AREAD001.DAT",
    "projects/bof4/artifacts/scenes/AREAD001/dialogs.csv",
    "projects/bof4/artifacts/scenes/AREAD012/translations_AREAD012.json",
    "projects/bof4/artifacts/scenes/AREAD012/approved_AREAD012.csv",
    "projects/utawarerumono/artifacts/evidence/tela.png",
    "projects/souldiers/artifacts/qa_revisao/para_revisar/review_cap_None.xlsx",
    "projects/utawarerumono/artifacts/review_cap_11.csv",
    "projects/utawarerumono/artifacts/archive/interjection_corrections.csv",
    "projects/bof4/artifacts/kb_phase_worklist_all.md",
    "projects/utawarerumono/artifacts/scenes/ch_12_13/bench_12_13.haiku.json",
    "projects/trails_sky_sc/artifacts/scenes/mp0010_01/_build_translations.py",
    "docs/print.png",
    "docs/planilha.xlsx",
    "tools/sora_2nd.exe",
    "arquivo_sem_extensao",
    # artefato gerado de nome desconhecido, em extensao permitida: default-deny
    "projects/bof4/artifacts/novo_relatorio_gerado.md",
    "projects/bof4/artifacts/scenes/AREAD001/qualquer_coisa.json",
    "projects/jogo_novo/artifacts/state/cache_de_falas.json",
]
ALLOW = [
    ".env.example",
    "LICENSE",
    "VERSION",
    ".github/CODEOWNERS",
    ".gitignore",
    "README.md",
    "framework/runtime/kb_gate.py",
    "framework/skills/operacao/rodar-onda/rodar_ondas.ps1",
    "projects/demo/artifacts/scenes/demo01/dialogs.csv",
    "projects/bof4/artifacts/kb_phase_worklist.md",
    "projects/bof4/artifacts/glossary.csv",
    "projects/jogo_novo/artifacts/state/voice_cards.json",
    "projects/jogo_novo/connector/extract.py",
    "projects/utawarerumono/artifacts/qa_revisao/devolvido/.gitkeep",
    "projects/utawarerumono/artifacts/archive/interjection_reference.md",
    "projects/utawarerumono/output/.gitignore",
]


@pytest.mark.parametrize("path", DENY)
def test_denied(path):
    assert path_problem(path)


@pytest.mark.parametrize("path", ALLOW)
def test_allowed(path):
    assert path_problem(path) is None


def test_decompiler_signature():
    assert _DECOMP.search(b"  iVar1 = FUN" + b"_0044a2f0(param_1);")
    assert _DECOMP.search(b"mov eax, DAT" + b"_005c1a20")
    assert not _DECOMP.search(b"def FUN_helper(): pass  # offset 0x44a2f0")


def test_email():
    assert _OK_EMAIL.search("108143319+scudellerlemos@users.noreply.github.com")
    assert _OK_EMAIL.search("noreply@github.com")
    assert not _OK_EMAIL.search("alguem@gmail.com")


def test_hook_only_on_git_writes():
    assert _GIT_WRITE.search("git add . && git commit -m x")
    assert _GIT_WRITE.search("git push origin main")
    assert not _GIT_WRITE.search("git status")
    assert not _GIT_WRITE.search("python -m pytest")
    # caminho do repo tem `-git` e script pode citar "add": nao e git write
    assert not _GIT_WRITE.search(r"cd C:\Users\x\projetos-git\repo && python -c \"s.add(1)\"")
    assert not _GIT_WRITE.search("python x.py projetos-git/repo commit")
    assert _GIT_WRITE.search("cd repo && git add -A")
    assert _GIT_WRITE.search("git -C repo commit -m x")
    assert _GIT_WRITE.search("echo ok; git push")


def test_repo_is_clean():
    """O proprio repo passa no guard -- e o teste que falha se alguem versionar conteudo de jogo."""
    assert scan_tree() == []
