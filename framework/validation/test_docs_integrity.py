"""Consistencia entre docs, versao e CI: falha quando um deles anda sem o outro."""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
_STATUS = {"proposto", "aceito", "rejeitado", "substituido", "obsoleto"}


def _adrs():
    return sorted((RAIZ / "docs" / "adr").glob("*.md"))


def test_adrs_sao_sequenciais_e_tem_status_valido():
    nums = []
    for p in _adrs():
        m = re.match(r"(\d{4})-.+\.md$", p.name)
        assert m, f"nome fora do padrao NNNN-slug.md: {p.name}"
        n = int(m[1])
        nums.append(n)
        txt = p.read_text(encoding="utf-8")
        assert re.match(rf"# ADR {m[1]} ", txt), f"{p.name}: titulo deve comecar com '# ADR {m[1]} '"
        st = re.search(r"\*\*Status:\*\*\s*([\wéíóúçãõ]+)", txt)
        assert st, f"{p.name}: sem linha '**Status:**'"
        valor = st[1].lower().replace("é", "e").replace("í", "i")
        assert valor in _STATUS, f"{p.name}: status '{st[1]}' fora de {sorted(_STATUS)}"
    assert nums == list(range(1, len(nums) + 1)), f"ADRs com buraco ou repetidos: {nums}"


def test_version_bate_com_a_entrada_mais_recente_do_changelog_com_versao():
    versao = (RAIZ / "VERSION").read_text(encoding="utf-8").strip()
    assert re.fullmatch(r"\d+\.\d+\.\d+", versao), versao
    cab = re.findall(r"^## .*?\bv(\d+\.\d+\.\d+)\b", (RAIZ / "docs" / "CHANGELOG.md").read_text(encoding="utf-8"), re.M)
    assert cab and cab[0] == versao, f"VERSION={versao}, primeira versao no CHANGELOG={cab[:1]}"


def test_workflow_de_ml_roda_todo_teste_do_embedder():
    """O job de cobertura real so mede o que esta na lista; teste novo do embedder fora dela derruba o piso."""
    wf = (RAIZ / ".github" / "workflows" / "ml-coverage-optional.yml").read_text(encoding="utf-8")
    listados = set(re.findall(r"framework/[\w/]+\.py", wf))
    for t in listados:
        assert (RAIZ / t).is_file(), f"workflow cita teste inexistente: {t}"
    existentes = {p.relative_to(RAIZ).as_posix() for p in (RAIZ / "framework" / "db").glob("test_embedder*.py")}
    existentes.add("framework/db/test_validate_model.py")
    assert existentes <= listados, f"fora da lista do workflow de ML: {sorted(existentes - listados)}"


def test_codeowners_existe_e_cobre_o_repo_todo():
    co = (RAIZ / ".github" / "CODEOWNERS").read_text(encoding="utf-8")
    assert re.search(r"^\*\s+@\S+", co, re.M)
