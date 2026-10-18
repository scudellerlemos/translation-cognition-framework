"""O texto do jogo e dado nao confiavel (SECURITY.md, secao 'Texto do jogo'): nenhuma chamada de LLM que o
le pode ter ferramenta. Estes testes travam o contrato; alargar uma permissao exige mudar o teste de proposito."""
import ast
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
RUNTIME = Path(__file__).resolve().parent


def _fontes():
    return [p for p in sorted(RUNTIME.glob("*.py")) if not p.name.startswith("test_")]


def test_nenhuma_chamada_de_api_passa_tools():
    """Chamadas de API do runtime (traducao, retrotraducao, batch) nunca declaram `tools`."""
    achados = []
    for p in _fontes():
        for n in ast.walk(ast.parse(p.read_text(encoding="utf-8"))):
            if isinstance(n, ast.keyword) and n.arg in ("tools", "tool_choice"):
                achados.append(f"{p.name}:{n.value.lineno}")
            if isinstance(n, ast.Constant) and n.value in ("tools", "tool_choice"):
                achados.append(f"{p.name}:{n.lineno}")
    assert not achados, f"ferramenta declarada em chamada que le texto do jogo: {achados}"


def test_triagem_de_risco_roda_claude_sem_ferramenta():
    src = (RUNTIME / "risk_triage_run.py").read_text(encoding="utf-8")
    assert re.search(r"'--allowedTools',\s*''", src), "triagem deve chamar `claude -p --allowedTools ''`"
    assert "dangerously" not in src.lower() and "bypassPermissions" not in src


def test_agente_tradutor_mantem_so_as_ferramentas_minimas():
    fm = (RAIZ / ".claude" / "agents" / "scene-translator.md").read_text(encoding="utf-8").split("---")[1]
    tools = {t.strip() for t in re.search(r"^tools:\s*(.+)$", fm, re.M)[1].split(",")}
    assert tools == {"Read", "Write", "Edit", "Bash"}, f"ferramentas do tradutor mudaram: {sorted(tools)}"
