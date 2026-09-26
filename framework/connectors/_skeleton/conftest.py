"""conftest.py — testes do conector (adaptado do BoF4/Trails).

- Poe connector/ no sys.path: reinsert.py faz `from extract import ...` e os testes importam os dois.
- --source-binary: o binario real do jogo e gitignored (licenciamento); passe o caminho na CLI
  ou declare connector.source_binary (relativo) no project.json. Sem ele o round-trip real pula
  e so o sintetico (test_roundtrip_synthetic.py) roda.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def pytest_addoption(parser):
    try:
        parser.addoption("--source-binary", default=None,
                         help="Caminho do binario-fonte do jogo (fora do repo)")
    except ValueError:  # outro conftest de conector ja registrou (pytest em varios projetos juntos)
        pass
