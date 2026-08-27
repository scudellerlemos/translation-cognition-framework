#!/usr/bin/env python3
"""
extract.py — Trails in the Sky 2nd Chapter (Falcom remake engine, 2026 — contêiner FPAC)

Contrato:
    entrada : pac/steam/script_en.pac dentro da instalação do jogo, via env var
              TRAILS_SKY_SC_DATA_DIR ou arg CLI
    saída   : artifacts/dialogs.csv (offset, file, text_en, byte_budget)
              artifacts/extraction_log.md

Escopo — Fase 0: SOMENTE arquivos `script_en/scena/*.dat` (script interno `#scp`). `ani/`,
`ai/`, `battle/` ficam fora (animação/IA/batalha, sem diálogo) — ver table_schema.md Camada 0.

Regras:
- 100% determinístico. NUNCA usar LLM aqui.
- O `#scp` interno NÃO foi mapeado (VM/bytecode não decodificado, RE pausada — ver
  table_schema.md "DECISÃO DE ESTRATÉGIA"). Extração é heurística: varre sequências ASCII
  imprimíveis terminadas em \0, sem entender a estrutura do bytecode.
- Filtro: string precisa ter pelo menos 1 espaço — nomes de função/label internos do
  bytecode (`sound.PlayBGM`, `OnMapReinit`, `sora_2nd_ev_09_35_01`) não têm espaço; texto de
  diálogo/UI tem. ponytail: heurística de espaço, alguns rótulos de 1 palavra (ex: "Trailer")
  ficam de fora — upgrade path: mapear o array de records de 32 bytes (table_schema.md) pra
  localizar strings por ponteiro em vez de varredura, se isso virar bloqueio real.
- offset = "<arquivo>:0x<hex>" — o offset numérico sozinho se repete entre arquivos .dat
  diferentes, então precisa do nome do arquivo pra ser único (id_column do project.json).
- byte_budget = tamanho da string + 1 (terminador \0). reinsert.py trunca/faz padding pra
  caber exatamente nesse espaço — nenhum ponteiro do #scp ou do contêiner FPAC é tocado.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_FRAMEWORK_CONNECTORS = _HERE.parent.parent.parent / "framework" / "connectors"
if str(_FRAMEWORK_CONNECTORS) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK_CONNECTORS))
import connector_io  # noqa: E402  (utilitarios compartilhados entre conectores, #86)

if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import fpac_unpack  # noqa: E402

_SCRIPT_PAC = Path("pac") / "steam" / "script_en.pac"
_SCENA_MAGIC = b"#scp"
_MIN_LEN = 4


def _scan_strings(blob: bytes) -> list[tuple[int, str]]:
    """Varredura heurística: sequências ASCII imprimíveis (0x20-0x7e) terminadas em \\0, com
    pelo menos 1 espaço (filtra nomes de função/label do bytecode — ver docstring do módulo).
    Retorna [(offset, texto)] com offset relativo ao início de `blob`."""
    out: list[tuple[int, str]] = []
    i = 0
    n = len(blob)
    while i < n:
        if 0x20 <= blob[i] < 0x7F:
            start = i
            j = i
            while j < n and 0x20 <= blob[j] < 0x7F:
                j += 1
            if j < n and blob[j] == 0 and (j - start) >= _MIN_LEN:
                text = blob[start:j].decode("ascii")
                if " " in text:
                    out.append((start, text))
            i = j + 1
        else:
            i += 1
    return out


def _resolve_data_dir(cli_override: str | None) -> Path:
    """Resolve o diretório de instalação do jogo: CLI > env var TRAILS_SKY_SC_DATA_DIR."""
    return connector_io.resolve_source_path(
        cli_arg=cli_override, env_var="TRAILS_SKY_SC_DATA_DIR", exc=RuntimeError,
        error_hint=(
            "Diretorio do jogo nao encontrado. Defina TRAILS_SKY_SC_DATA_DIR ou passe como "
            "argumento.\nExemplo: python extract.py projects/trails_sky_sc "
            "\"C:\\...\\Trails in the Sky 2nd Chapter Demo\""
        ),
    )


def extract(project_root: Path, data_dir: Path) -> int:
    """Extrai diálogos de `script_en/scena/*.dat` e grava artifacts/dialogs.csv.

    Retorna o número de linhas extraídas.
    """
    artifacts = project_root / "artifacts"
    out_csv = artifacts / "dialogs.csv"
    out_log = artifacts / "extraction_log.md"

    pac_path = data_dir / _SCRIPT_PAC
    if not pac_path.is_file():
        raise FileNotFoundError(f"script_en.pac nao encontrado: {pac_path}")

    data, entries = fpac_unpack.read_index(pac_path)
    scena_entries = [
        (name, size, addr) for name, size, addr, _crc in entries
        if "/scena/" in name and name.endswith(".dat")
    ]

    rows: list[dict] = []
    log_lines = ["# Extraction Log — Trails in the Sky 2nd Chapter\n"]
    skipped_magic = 0

    for name, size, addr in scena_entries:
        blob = data[addr:addr + size]
        rel_name = "scena/" + name.split("/scena/", 1)[1]
        if blob[:4] != _SCENA_MAGIC:
            skipped_magic += 1
            log_lines.append(f"- AVISO: magic invalido em {rel_name}, pulado\n")
            continue

        file_rows = 0
        for offset, text in _scan_strings(blob):
            rows.append({
                "offset": f"{rel_name}:0x{offset:x}",
                "file": rel_name,
                "text_en": text,
                "byte_budget": len(text) + 1,
            })
            file_rows += 1
        log_lines.append(f"- {rel_name}: {file_rows} strings extraidas\n")

    connector_io.write_dialogs_csv(out_csv, ["offset", "file", "text_en", "byte_budget"], rows)

    log_lines.append(
        f"\nTotal: {len(rows)} strings extraidas de {len(scena_entries) - skipped_magic} "
        f"arquivos scena/ ({skipped_magic} pulados por magic invalido)\n"
    )
    connector_io.write_extraction_log(out_log, "".join(log_lines))

    print(f"Extraido: {len(rows)} linhas -> {out_csv}")
    return len(rows)


def main():
    project_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    data_dir_arg = sys.argv[2] if len(sys.argv) > 2 else None
    data_dir = _resolve_data_dir(data_dir_arg)
    extract(project_root, data_dir)


if __name__ == "__main__":
    main()
