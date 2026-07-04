#!/usr/bin/env python3
"""
extract.py — conector hex_binary para Utawarerumono: Mask of Deception (versão ENG/Steam)

Extrai o corpus de um ARCO (conjunto de scripts do container) para dialogs.csv, em
ORDEM DE EXIBIÇÃO (= ordem de armazenamento dentro de cada script).

Formato do container ScriptEvent.sdat: ver connector/sdat_format.py e connector/table_schema.md.
- Cabeçalho "Filename" + tabela de nomes + seção "Pack" (offset/size por script).
- Cada script = [bytecode 'STSC' ...][bloco de texto: strings UTF-8 null-terminated contíguas].

Determinístico. O offset (hex) é o id_column — âncora para reinserção.
byte_budget = nº de bytes UTF-8 da string (sem o terminador \\0).

ESCOPO (SCENES): por padrão extrai o 1º script do 1º arco (cena de abertura, 11_01_000S).
Ajuste SCENES (prefixos de nome de script) para extrair mais cenas/arcos.

Caminho do binário (NUNCA hardcoded): o usuário fornece o arquivo a traduzir.
Resolução: (1) argumento de linha de comando; senão (2) connector.source_binary do project.json.
"""
import sys
from pathlib import Path

import sdat_format as S

_HERE = Path(__file__).resolve().parent
_FRAMEWORK_CONNECTORS = _HERE.parent.parent.parent / "framework" / "connectors"
if str(_FRAMEWORK_CONNECTORS) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK_CONNECTORS))
import connector_io  # noqa: E402  (utilitarios compartilhados entre conectores, #86)

# --- config do arco a extrair ---
# Prefixos de nome de script (CC_SS_NNNT.BIN). 11_01 + 11_02 = 2 primeiras cenas do 1º arco.
SCENES = ("11_01", "11_02")

ROOT = Path(__file__).resolve().parent.parent          # raiz do projeto
OUT = ROOT / "artifacts" / "dialogs.csv"


def resolve_source() -> Path:
    """Caminho do binário a traduzir: CLI > connector.source_binary do project.json.
    Sem hardcode. O usuário deve fornecer o arquivo."""
    p = connector_io.resolve_source_path(
        cli_arg=sys.argv[1] if len(sys.argv) > 1 else None,
        project_json=ROOT / "project.json", cfg_key="source_binary", relative_base=ROOT,
        error_hint=("ERRO: forneça o binário a traduzir via argumento "
                    "(`python extract.py <caminho>`) ou preencha "
                    "`connector.source_binary` no project.json."),
    )
    if not p.is_file():
        sys.exit(f"ERRO: binário não encontrado: {p}\n"
                 "Aponte `connector.source_binary` (no project.json) ou o argumento de CLI "
                 "para o arquivo do jogo a traduzir.")
    return p


def main():
    src = resolve_source()
    data = src.read_bytes()

    files = S.parse_pack(data)
    targets = S.files_for_scenes(files, SCENES)
    if not targets:
        sys.exit(f"ERRO: nenhum script casa os prefixos {SCENES}. "
                 f"Ex. de nomes: {[f.name for f in files[:5]]}")

    rows = []
    per_scene = []
    for f in targets:
        block = S.extract_text_block(data, f)
        per_scene.append((f.name, len(block)))
        for off, text, budget in block:
            rows.append({"offset": f"0x{off:x}", "text_source": text, "byte_budget": budget})

    connector_io.write_dialogs_csv(OUT, ["offset", "text_source", "byte_budget"], rows)

    print(f"Container: {len(files)} scripts. Arco extraído: {[f.name for f in targets]}")
    for name, c in per_scene:
        print(f"  {name}: {c} linhas")
    print(f"TOTAL: {len(rows)} linhas -> {OUT}")


if __name__ == "__main__":
    main()
