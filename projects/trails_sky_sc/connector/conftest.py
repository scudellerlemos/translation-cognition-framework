"""conftest.py — configuração de opções CLI para os testes do conector Trails in the Sky 2nd Chapter."""


def pytest_addoption(parser):
    parser.addoption(
        "--data-dir",
        default=None,
        help="Caminho para a instalacao do jogo (contem sora_2nd.exe, pac/, cursor/)",
    )
