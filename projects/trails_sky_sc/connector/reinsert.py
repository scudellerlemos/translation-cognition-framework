#!/usr/bin/env python3
"""
reinsert.py — Trails in the Sky 2nd Chapter (Falcom remake engine, 2026)

Contrato:
    entrada : artifacts/approved_translations.csv (offset, text_pt)
              artifacts/dialogs.csv (byte_budget original por offset, gerado por extract.py)
              data_dir (pac/steam/script_en.pac)
    saída   : output/script_en.pac (cópia do contêiner com scena/*.dat traduzidos)
              artifacts/reinsertion_report.md

Regras:
- 100% determinístico. LLM NUNCA toca no .pac diretamente.
- O .pac original NUNCA é sobrescrito; a cópia modificada vai para output/.
- Replace same-size: a tradução é gravada no MESMO offset, respeitando o MESMO byte_budget
  da string original em inglês (trunca/faz padding com \0) — nenhuma outra estrutura do
  arquivo (header do `#scp`, índice do contêiner FPAC) precisa mudar, porque nenhum ponteiro
  é tocado (ver table_schema.md "DECISÃO DE ESTRATÉGIA"). Consequência: pt-BR mais longo que
  o inglês é truncado — não há expansão nesta fase (upgrade path: mapear o array de records
  de 32 bytes pra permitir realocação, se isso virar bloqueio real de qualidade).
- Tradução é gravada como UTF-8 (charset do #scp confirmado em 2026-08-23 comparando
  script_en.pac x script.pac (japonês): o texto japonês no mesmo arquivo scena/*.dat decodifica
  como UTF-8 válido — ver table_schema.md "Charset (UTF-8, confirmado)"). Truncamento no
  byte_budget nunca corta um caractere multibyte ao meio (decode/re-encode com errors="ignore"
  descarta bytes finais incompletos em vez de gravar UTF-8 inválido).
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


def _resolve_data_dir(cli_override: str | None) -> Path:
    return connector_io.resolve_source_path(
        cli_arg=cli_override, env_var="TRAILS_SKY_SC_DATA_DIR", exc=RuntimeError,
        error_hint=(
            "Diretorio do jogo nao encontrado. Defina TRAILS_SKY_SC_DATA_DIR ou passe como "
            "argumento."
        ),
    )


def _load_byte_budgets(dialogs_csv: Path) -> dict[str, int]:
    """offset -> byte_budget original (de dialogs.csv, gerado por extract.py)."""
    budgets: dict[str, int] = {}
    with dialogs_csv.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            budgets[row["offset"]] = int(row["byte_budget"])
    return budgets


def truncate_for_budget(text: str, budget: int) -> bytes:
    """Trunca `text` pro `budget` em bytes UTF-8-safe e faz padding com \\0 (payload final,
    tamanho == budget). Extraido de rebuild_pac pra ser reusado por verify_chapter.py na
    leitura de volta (mesma logica, sem 2ª implementacao que possa divergir)."""
    raw = text.encode("utf-8")[: budget - 1]
    raw = raw.decode("utf-8", errors="ignore").encode("utf-8")
    return raw.ljust(budget, b"\x00")


def rebuild_pac(
    pac_bytes: bytes,
    entries: list[tuple[str, int, int, int]],
    translations: dict[str, str],
    budgets: dict[str, int],
) -> tuple[bytes, int]:
    """Retorna (bytes do .pac com `translations` aplicadas nas strings de scena/, nº de
    strings efetivamente alteradas). Same-size replace: nenhum offset/índice do contêiner
    FPAC ou do header `#scp` muda — só os bytes da string, dentro do orçamento original.

    translations={} -> bytes ORIGINAIS, sem tocar no buffer (fast-path de identidade, usado
    por test_roundtrip*.py pra provar round-trip byte-idêntico).
    """
    if not translations:
        return pac_bytes, 0

    by_file: dict[str, dict[int, str]] = {}
    for key, text_pt in translations.items():
        file_part, _, off_part = key.partition(":")
        by_file.setdefault(file_part, {})[int(off_part, 16)] = text_pt

    buf = bytearray(pac_bytes)
    changed = 0

    for name, _size, addr, _crc in entries:
        if "/scena/" not in name or not name.endswith(".dat"):
            continue
        rel_name = "scena/" + name.split("/scena/", 1)[1]
        file_translations = by_file.get(rel_name)
        if not file_translations:
            continue

        for offset, text_pt in file_translations.items():
            key = f"{rel_name}:0x{offset:x}"
            budget = budgets.get(key)
            if budget is None:
                continue
            payload = truncate_for_budget(text_pt, budget)
            abs_off = addr + offset
            buf[abs_off:abs_off + budget] = payload
            changed += 1

    return bytes(buf), changed


def read_scena_strings(pac_bytes: bytes, entries: list[tuple[str, int, int, int]]
                        ) -> dict[str, str]:
    """Lê de volta offset -> texto (até o primeiro \\0) re-varrendo com a MESMA heurística de
    extract.py (`_scan_strings`) — usado só pelos testes de round-trip pra confirmar o que
    ficou gravado. Limitação herdada do re-scan: traduções curtas (<_MIN_LEN) ou sem espaço
    ficam invisíveis aqui mesmo tendo sido gravadas corretamente — não é uma limitação do
    reinsert em si (que escreve direto no offset conhecido via dialogs.csv, sem depender de
    re-scan); um verify_chapter.py futuro deve ler pelos offsets do dialogs.csv, não re-varrer."""
    import extract as E

    out: dict[str, str] = {}
    for name, size, addr, _crc in entries:
        if "/scena/" not in name or not name.endswith(".dat"):
            continue
        rel_name = "scena/" + name.split("/scena/", 1)[1]
        blob = pac_bytes[addr:addr + size]
        if blob[:4] != b"#scp":
            continue
        for offset, text in E._scan_strings(blob):
            out[f"{rel_name}:0x{offset:x}"] = text
    return out


def reinsert(project_root: Path, data_dir: Path) -> int:
    """Aplica as traduções aprovadas em script_en.pac e salva a cópia em output/.

    Retorna o número de strings reinseridas.
    """
    artifacts = project_root / "artifacts"
    approved_csv = artifacts / "approved_translations.csv"
    dialogs_csv = artifacts / "dialogs.csv"
    if not approved_csv.is_file():
        raise FileNotFoundError(f"Arquivo de traducoes nao encontrado: {approved_csv}")
    if not dialogs_csv.is_file():
        raise FileNotFoundError(
            f"dialogs.csv nao encontrado (rode extract.py primeiro): {dialogs_csv}"
        )

    translations: dict[str, str] = {}
    with approved_csv.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            key = row.get("offset", "").strip()
            val = row.get("text_pt", "").strip()
            if key and val:
                translations[key] = val

    budgets = _load_byte_budgets(dialogs_csv)

    pac_path = data_dir / _SCRIPT_PAC
    if not pac_path.is_file():
        raise FileNotFoundError(f"script_en.pac nao encontrado: {pac_path}")
    pac_bytes, entries = fpac_unpack.read_index(pac_path)

    new_bytes, changed = rebuild_pac(pac_bytes, entries, translations, budgets)

    output_dir = project_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_pac = output_dir / "script_en.pac"
    out_pac.write_bytes(new_bytes)

    report_path = artifacts / "reinsertion_report.md"
    report_path.write_text(
        "# Reinsertion Report — Trails in the Sky 2nd Chapter\n\n"
        f"Traducoes carregadas: {len(translations)}\n"
        f"Strings reinseridas: {changed}\n"
        f"Saida: {out_pac}\n",
        encoding="utf-8",
    )
    print(f"Reinserido: {changed} strings -> {out_pac}")
    return changed


def main():
    project_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    data_dir_arg = sys.argv[2] if len(sys.argv) > 2 else None
    data_dir = _resolve_data_dir(data_dir_arg)
    reinsert(project_root, data_dir)


if __name__ == "__main__":
    main()
