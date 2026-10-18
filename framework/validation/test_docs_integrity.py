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


def _nomes(texto: str) -> set[str]:
    out = set()
    for ln in texto.splitlines():
        ln = ln.split("#")[0].strip()
        m = re.match(r"([A-Za-z0-9][A-Za-z0-9._-]*)", ln) if ln and not ln.startswith("-") else None
        if m:
            out.add(re.sub(r"[-_.]+", "-", m[1]).lower())
    return out


def test_requirements_dev_e_um_lock_com_hash_gerado_das_fontes():
    lock = (RAIZ / "requirements-dev.txt").read_text(encoding="utf-8")
    sem_comentario = [ln for ln in lock.splitlines() if not ln.startswith("#")]
    blocos = re.split(r"\n(?=[A-Za-z0-9])", "\n".join(sem_comentario))
    blocos = [b for b in blocos if b.strip()]
    assert blocos
    for b in blocos:
        nome = b.split()[0]
        assert "==" in nome, f"{nome}: o lock so aceita versao exata (==)"
        assert "--hash=sha256:" in b, f"{nome}: sem hash no lock"
    fontes = _nomes((RAIZ / "requirements-dev-src.txt").read_text(encoding="utf-8"))
    for extra in ("requirements.txt", "requirements-dist.txt"):
        fontes |= _nomes((RAIZ / extra).read_text(encoding="utf-8"))
    faltam = fontes - _nomes(lock)
    assert not faltam, f"nas fontes mas fora do lock (regere com uv pip compile): {sorted(faltam)}"


def test_cobertura_ml_e_obrigatoria_via_agregador():
    """O check de ML so e obrigatorio se for job de test.yml listado no `needs` do agregador e do mark-staging."""
    wf = RAIZ / ".github" / "workflows"
    ml = (wf / "ml-coverage-optional.yml").read_text(encoding="utf-8")
    assert "workflow_call:" in ml
    assert not re.search(r"^  (push|pull_request):", ml, re.M), "disparo proprio cria check fora do agregador"
    t = (wf / "test.yml").read_text(encoding="utf-8")
    assert re.search(r"^  ml-coverage:\n(?:    .*\n)*?    uses: \./\.github/workflows/ml-coverage-optional\.yml", t, re.M)
    needs = re.findall(r"^    needs: \[(.*?)\]", t, re.M)
    assert len(needs) == 2 and all("ml-coverage" in n.split(", ") for n in needs), needs
