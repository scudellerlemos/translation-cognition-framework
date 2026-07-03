"""conftest.py — configuração de opções CLI para os testes do conector Souldiers."""


def pytest_addoption(parser):
    parser.addoption(
        "--data-dir",
        default=None,
        help="Caminho para Souldiers_Data/StreamingAssets/aa/StandaloneWindows64",
    )
