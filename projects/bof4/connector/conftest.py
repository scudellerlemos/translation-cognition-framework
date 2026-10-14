"""conftest.py — configuração de opções CLI para os testes do conector BoF4."""


def pytest_addoption(parser):
    parser.addoption(
        "--dat-dir",
        default=None,
        help="Caminho para o diretório english/DAT do Breath of Fire 4",
    )
