"""
script_generator.py — gerador de candidato de conector para engines desconhecidas.

Gera um extract.py com código pré-preenchido baseado nas evidências detectadas,
em vez de um skeleton com NotImplementedError em todos os pontos.

Três padrões de stub, escolhidos automaticamente pelas evidências:

  LINEAR_SCAN   — arquivo denso de texto (ASCII/UTF-8, sem pointer table):
                  varre sequencialmente, encontra strings null-terminated.
                  Funciona de caixa para muitos formatos simples.

  TOKEN_TABLE   — binário com tokens de controle [XX] (ex: Capcom-like):
                  estrutura de tabela byte→char + tokens de controle.
                  O dev preenche o mapa de caracteres e os tokens.

  POINTER_TABLE — binário estruturado com TOC de ponteiros:
                  lê array de offsets uint32 e jump para cada string.
                  O dev adapta o tamanho e posição do TOC.

Para engine conhecida este módulo NÃO é chamado — o conector de referência é reutilizado.
"""
from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Padrão 1: LINEAR SCAN (texto denso, ASCII/UTF-8, sem pointer table)
# Código pronto para testar; precisa só ajustar MIN_LEN e encoding se necessário.
# ---------------------------------------------------------------------------
_LINEAR_SCAN_STUB = '''\
import csv
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# TODO: verificar as constantes abaixo inspecionando o arquivo no HxD/010 Editor
# CONFIG — ajustar conforme o arquivo real
# ---------------------------------------------------------------------------
_MIN_STRING_LEN = 3      # ignorar strings menores que isso
_TERMINATOR = b"\\x00"   # terminador de string (geralmente null)
_ENCODING = "{encoding}" # detectado pela evidência; ajustar se errado
# ---------------------------------------------------------------------------


def _is_printable(b: int) -> bool:
    """Bytes que contam como parte de uma string de texto."""
    return 0x20 <= b <= 0x7E or b in (0x09, 0x0A, 0x0D)


def iter_string_offsets(data: bytes, _cfg: dict):
    """Varredura linear: encontra strings null-terminated imprimíveis."""
    i = 0
    while i < len(data):
        if _is_printable(data[i]):
            start = i
            while i < len(data) and data[i] != 0x00:
                i += 1
            if (i - start) >= _MIN_STRING_LEN:
                yield start
            i += 1  # pula o terminador
        else:
            i += 1


def decode_string(data: bytes, offset: int, _table) -> tuple[str, int]:
    """Lê a string null-terminated a partir de offset. Retorna (texto, byte_budget)."""
    end = offset
    while end < len(data) and data[end] != 0x00:
        end += 1
    text = data[offset:end].decode(_ENCODING, errors="replace")
    byte_budget = (end + 1) - offset  # inclui o terminador
    return text, byte_budget


def load_table(_table_path: Path):
    """Linear scan não usa tabela de caracteres — retorna None."""
    return None


def main(project_json: Path, source_override: str | None = None):
    import json
    cfg = json.loads(project_json.read_text(encoding="utf-8"))
    root = project_json.parent

    from pathlib import Path as P
    src = P(source_override) if source_override else (root / cfg["connector"]["source_binary"])
    data = src.read_bytes()

    id_col = cfg["source"]["id_column"]
    rows = []
    for offset in iter_string_offsets(data, cfg):
        text, budget = decode_string(data, offset, None)
        rows.append({{id_col: f"0x{{offset:x}}", "text_en": text, "byte_budget": budget}})

    out = root / cfg["source"]["file"]
    import csv as _csv
    with out.open("w", newline="", encoding="utf-8") as f:
        w = _csv.DictWriter(f, fieldnames=[id_col, "text_en", "byte_budget"])
        w.writeheader()
        w.writerows(rows)
    print(f"Extraídas {{len(rows)}} strings → {{out}}")

    # PRÓXIMO PASSO:
    # 1. Abrir o arquivo no HxD/010 e comparar o output com as strings visíveis
    # 2. Se encontrou ruído (bytes não-texto no output): ajustar _is_printable()
    # 3. Se encoding errado: ajustar _ENCODING
    # 4. Rodar round-trip: python framework/connectors/connector_smoke.py <projeto> --roundtrip


if __name__ == "__main__":
    try:                                              # Windows cp1252: permitir setas/acentos no stdout
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("project.json")
    override = sys.argv[2] if len(sys.argv) > 2 else None
    main(proj, override)
'''

# ---------------------------------------------------------------------------
# Padrão 2: TOKEN TABLE (binário com tokens de controle [XX], ex: Capcom)
# O dev preenche BYTE_TO_CHAR e CONTROL_MAP lendo a tabela do jogo.
# ---------------------------------------------------------------------------
_TOKEN_TABLE_STUB = '''\
import csv
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG — preencher lendo a tabela de caracteres do jogo (ex: table_schema.md)
# ---------------------------------------------------------------------------
BYTE_TO_CHAR: dict[int, str] = {{
    # 0x20: " ", 0x21: "!", ... preencher do table_schema do jogo
}}
CONTROL_MAP: list[tuple[bytes, str]] = [
    # (b"\\x01\\x00", "\\n"),   # exemplo: control code → token
    # ordenar por comprimento DECRESCENTE p/ casar sequências longas primeiro
]
TERMINATOR = b"\\x00"
# ---------------------------------------------------------------------------


def load_table(_table_path: Path):
    return (BYTE_TO_CHAR, sorted(CONTROL_MAP, key=lambda x: -len(x[0])), TERMINATOR)


def decode_string(data: bytes, offset: int, table) -> tuple[str, int]:
    byte_to_char, control_map, terminator = table
    out = []
    i = offset
    while not data[i:i+len(terminator)] == terminator:
        matched = False
        for seq, tok in control_map:
            if data[i:i+len(seq)] == seq:
                out.append(tok)
                i += len(seq)
                matched = True
                break
        if matched:
            continue
        ch = byte_to_char.get(data[i], f"[{{data[i]:02X}}]")
        out.append(ch)
        i += 1
    byte_budget = (i + len(terminator)) - offset
    return "".join(out), byte_budget


def iter_string_offsets(data: bytes, project_cfg: dict):
    """Localizar via pointer_table declarada no project.json, ou adaptar p/ varredura."""
    # TODO: ler a pointer_table do project_cfg e saltar para cada offset
    raise NotImplementedError(
        "Adaptar: ler a tabela de ponteiros do arquivo e yield cada offset de string"
    )


def main(project_json: Path, source_override: str | None = None):
    import json
    cfg = json.loads(project_json.read_text(encoding="utf-8"))
    root = project_json.parent

    src = Path(source_override) if source_override else (root / cfg["connector"]["source_binary"])
    data = src.read_bytes()
    table = load_table(root / cfg["connector"]["table_schema"])

    id_col = cfg["source"]["id_column"]
    rows = []
    for offset in iter_string_offsets(data, cfg):
        text, budget = decode_string(data, offset, table)
        rows.append({{id_col: f"0x{{offset:x}}", "text_en": text, "byte_budget": budget}})

    out = root / cfg["source"]["file"]
    import csv as _csv
    with out.open("w", newline="", encoding="utf-8") as f:
        w = _csv.DictWriter(f, fieldnames=[id_col, "text_en", "byte_budget"])
        w.writeheader()
        w.writerows(rows)
    print(f"Extraídas {{len(rows)}} strings → {{out}}")


if __name__ == "__main__":
    try:                                              # Windows cp1252: permitir setas/acentos no stdout
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("project.json")
    override = sys.argv[2] if len(sys.argv) > 2 else None
    main(proj, override)
'''

# ---------------------------------------------------------------------------
# Padrão 3: POINTER TABLE (binário estruturado com TOC — hex_binary skeleton)
# Versão anotada do skeleton genérico, mais orientada que o original.
# ---------------------------------------------------------------------------
_POINTER_TABLE_STUB = '''\
import csv
import struct
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG — ajustar ao formato do arquivo inspecionado no hex editor
# ---------------------------------------------------------------------------
_TOC_OFFSET = 0          # byte onde começa a tabela de ponteiros
_TOC_ENTRY_SIZE = 4      # bytes por entrada (geralmente 4 = uint32)
_TOC_ENTRY_COUNT = None  # None = ler do cabeçalho; ou fixar um número
_PTR_FORMAT = "<I"       # "<I" = little-endian uint32; ">I" = big-endian
_STR_ENCODING = "ascii"  # encoding das strings (ascii, utf-8, shift-jis)
_TERMINATOR = b"\\x00"
# ---------------------------------------------------------------------------


def load_table(_table_path: Path):
    """Pointer table não usa tabela de caracteres externa — retorna None."""
    return None


def decode_string(data: bytes, offset: int, _table) -> tuple[str, int]:
    end = offset
    while end < len(data) and data[end:end+len(_TERMINATOR)] != _TERMINATOR:
        end += 1
    text = data[offset:end].decode(_STR_ENCODING, errors="replace")
    return text, (end + len(_TERMINATOR)) - offset


def iter_string_offsets(data: bytes, project_cfg: dict):
    """Lê a tabela de ponteiros e yield cada offset de string.

    Adaptar _TOC_OFFSET, _TOC_ENTRY_SIZE e _TOC_ENTRY_COUNT ao formato real.
    """
    count = _TOC_ENTRY_COUNT
    if count is None:
        # Exemplo: primeiros 4 bytes = número de entradas (Capcom DAT-like)
        count, = struct.unpack_from(_PTR_FORMAT, data, _TOC_OFFSET)

    toc_start = _TOC_OFFSET + (4 if _TOC_ENTRY_COUNT is None else 0)
    for i in range(count):
        ptr_off = toc_start + i * _TOC_ENTRY_SIZE
        if ptr_off + _TOC_ENTRY_SIZE > len(data):
            break
        offset, = struct.unpack_from(_PTR_FORMAT, data, ptr_off)
        if 0 < offset < len(data):
            yield offset


def main(project_json: Path, source_override: str | None = None):
    import json
    cfg = json.loads(project_json.read_text(encoding="utf-8"))
    root = project_json.parent

    src = Path(source_override) if source_override else (root / cfg["connector"]["source_binary"])
    data = src.read_bytes()
    table = load_table(Path("."))  # pointer table não usa tabela

    id_col = cfg["source"]["id_column"]
    rows = []
    for offset in iter_string_offsets(data, cfg):
        text, budget = decode_string(data, offset, table)
        rows.append({{id_col: f"0x{{offset:x}}", "text_en": text, "byte_budget": budget}})

    out = root / cfg["source"]["file"]
    import csv as _csv
    with out.open("w", newline="", encoding="utf-8") as f:
        w = _csv.DictWriter(f, fieldnames=[id_col, "text_en", "byte_budget"])
        w.writeheader()
        w.writerows(rows)
    print(f"Extraídas {{len(rows)}} strings → {{out}}")

    # PRÓXIMO PASSO:
    # 1. Abrir o arquivo no HxD; localizar onde estão as strings de texto
    # 2. Ajustar _TOC_OFFSET e _TOC_ENTRY_COUNT conforme o cabeçalho real
    # 3. Rodar: python connector_smoke.py <projeto> [data_dir] --roundtrip


if __name__ == "__main__":
    try:                                              # Windows cp1252: permitir setas/acentos no stdout
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("project.json")
    override = sys.argv[2] if len(sys.argv) > 2 else None
    main(proj, override)
'''


# ---------------------------------------------------------------------------
# REINSERT — pares de decode_string() acima. #108: candidato pré-preenchido,
# não um conector completo — o agente/dev ainda adapta e valida via round-trip.
# ---------------------------------------------------------------------------
_LINEAR_SCAN_REINSERT_STUB = '''\
import csv
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG — mesmo _ENCODING do extract.py gerado; ajustar _APPROVED_CSV se o
# pipeline gravar a tradução aprovada em outro caminho.
# ---------------------------------------------------------------------------
_ENCODING = "{encoding}"
_APPROVED_CSV = "artifacts/approved.csv"  # TODO: ajustar ao caminho real do pipeline
# ---------------------------------------------------------------------------


def encode_string(text: str) -> bytes:
    return text.encode(_ENCODING, errors="replace")


def main(project_json: Path, source_override: str | None = None):
    import json
    cfg = json.loads(project_json.read_text(encoding="utf-8"))
    root = project_json.parent

    src = Path(source_override) if source_override else (root / cfg["connector"]["source_binary"])
    data = bytearray(src.read_bytes())
    id_col = cfg["source"]["id_column"]

    with (root / _APPROVED_CSV).open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        offset = int(row[id_col], 16)
        raw = encode_string(row["text_target"])
        end = offset
        while end < len(data) and data[end] != 0x00:
            end += 1
        budget = (end + 1) - offset  # espaço original (inclui terminador null)
        if len(raw) + 1 > budget:
            raise SystemExit(
                f"ERRO: offset {{row[id_col]}}: tradução ({{len(raw) + 1}}b) excede o "
                f"espaço original ({{budget}}b) -- sem realocação de TOC neste padrão"
            )
        data[offset:offset + len(raw)] = raw
        data[offset + len(raw):offset + budget] = b"\\x00" * (budget - len(raw))

    out_dir = root / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / src.name
    out_path.write_bytes(bytes(data))
    print(f"Reinseridas {{len(rows)}} strings → {{out_path}}")

    # PRÓXIMO PASSO:
    # 1. Rodar round-trip: python framework/connectors/connector_smoke.py <projeto> --roundtrip
    # 2. Round-trip byte-idêntico (texto == source) = conector aprovado


if __name__ == "__main__":
    try:                                              # Windows cp1252: permitir setas/acentos no stdout
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("project.json")
    override = sys.argv[2] if len(sys.argv) > 2 else None
    main(proj, override)
'''

_TOKEN_TABLE_REINSERT_STUB = '''\
import csv
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG — MESMOS BYTE_TO_CHAR/CONTROL_MAP do extract.py gerado (copiar de lá,
# preenchidos lendo a tabela de caracteres do jogo). Invertidos automaticamente
# abaixo -- não editar CHAR_TO_BYTE/_CONTROL_MAP_ENCODE à mão.
#
# CUIDADO: se um token do CONTROL_MAP produzir o MESMO texto que um char do
# BYTE_TO_CHAR (ex.: os dois mapeando pra "A"), o encode SEMPRE prioriza o
# token -- round-trip fica lossy nesse caso. Evitar sobreposição de saída
# entre as duas tabelas.
# ---------------------------------------------------------------------------
BYTE_TO_CHAR: dict[int, str] = {{
    # 0x20: " ", 0x21: "!", ... MESMO dict do extract.py gerado
}}
CONTROL_MAP: list[tuple[bytes, str]] = [
    # (b"\\x01\\x00", "\\n"),   # MESMA lista do extract.py gerado
]
TERMINATOR = b"\\x00"
_UNMAPPED_RX = re.compile(r"\\[([0-9A-Fa-f]{{2}})\\]")  # fallback do decode: byte cru como [XX]
_APPROVED_CSV = "artifacts/approved.csv"  # TODO: ajustar ao caminho real do pipeline
# ---------------------------------------------------------------------------

CHAR_TO_BYTE = {{v: k for k, v in BYTE_TO_CHAR.items()}}
_CONTROL_MAP_ENCODE = sorted(CONTROL_MAP, key=lambda x: -len(x[1]))  # tokens longos primeiro


def encode_string(text: str) -> bytes:
    out = bytearray()
    i = 0
    while i < len(text):
        matched = False
        for seq, tok in _CONTROL_MAP_ENCODE:
            if text.startswith(tok, i):
                out += seq
                i += len(tok)
                matched = True
                break
        if matched:
            continue
        m = _UNMAPPED_RX.match(text, i)
        if m:
            out.append(int(m.group(1), 16))
            i = m.end()
            continue
        ch = text[i]
        if ch in CHAR_TO_BYTE:
            out.append(CHAR_TO_BYTE[ch])
        else:
            raise SystemExit(f"ERRO: caractere '{{ch}}' sem mapeamento em BYTE_TO_CHAR")
        i += 1
    return bytes(out) + TERMINATOR


def main(project_json: Path, source_override: str | None = None):
    import json
    cfg = json.loads(project_json.read_text(encoding="utf-8"))
    root = project_json.parent

    src = Path(source_override) if source_override else (root / cfg["connector"]["source_binary"])
    data = bytearray(src.read_bytes())
    id_col = cfg["source"]["id_column"]

    with (root / _APPROVED_CSV).open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        offset = int(row[id_col], 16)
        raw = encode_string(row["text_target"])
        end = offset
        while data[end:end + len(TERMINATOR)] != TERMINATOR:
            end += 1
        budget = (end + len(TERMINATOR)) - offset
        if len(raw) > budget:
            raise SystemExit(
                f"ERRO: offset {{row[id_col]}}: tradução ({{len(raw)}}b) excede o espaço "
                f"original ({{budget}}b) -- sem realocação de TOC neste padrão"
            )
        data[offset:offset + len(raw)] = raw
        data[offset + len(raw):offset + budget] = TERMINATOR * (budget - len(raw))

    out_dir = root / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / src.name
    out_path.write_bytes(bytes(data))
    print(f"Reinseridas {{len(rows)}} strings → {{out_path}}")


if __name__ == "__main__":
    try:                                              # Windows cp1252: permitir setas/acentos no stdout
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("project.json")
    override = sys.argv[2] if len(sys.argv) > 2 else None
    main(proj, override)
'''

_POINTER_TABLE_REINSERT_STUB = '''\
import csv
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG — mesmo _STR_ENCODING do extract.py gerado.
# ---------------------------------------------------------------------------
_STR_ENCODING = "ascii"  # TODO: mesmo valor de _STR_ENCODING no extract.py gerado
_TERMINATOR = b"\\x00"
_APPROVED_CSV = "artifacts/approved.csv"  # TODO: ajustar ao caminho real do pipeline
# ---------------------------------------------------------------------------


def encode_string(text: str) -> bytes:
    return text.encode(_STR_ENCODING, errors="replace") + _TERMINATOR


def main(project_json: Path, source_override: str | None = None):
    import json
    cfg = json.loads(project_json.read_text(encoding="utf-8"))
    root = project_json.parent

    src = Path(source_override) if source_override else (root / cfg["connector"]["source_binary"])
    data = bytearray(src.read_bytes())
    id_col = cfg["source"]["id_column"]

    with (root / _APPROVED_CSV).open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        offset = int(row[id_col], 16)
        raw = encode_string(row["text_target"])
        end = offset
        while data[end:end + len(_TERMINATOR)] != _TERMINATOR:
            end += 1
        budget = (end + len(_TERMINATOR)) - offset
        if len(raw) > budget:
            # Padrão com TOC explícita -- ADAPTAR aqui p/ realocar o final do arquivo e
            # reescrever a entrada correspondente na tabela de ponteiros, se necessário.
            raise SystemExit(
                f"ERRO: offset {{row[id_col]}}: tradução ({{len(raw)}}b) excede o espaço "
                f"original ({{budget}}b) -- realocação de TOC não implementada neste candidato"
            )
        data[offset:offset + len(raw)] = raw
        data[offset + len(raw):offset + budget] = _TERMINATOR * (budget - len(raw))

    out_dir = root / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / src.name
    out_path.write_bytes(bytes(data))
    print(f"Reinseridas {{len(rows)}} strings → {{out_path}}")

    # PRÓXIMO PASSO:
    # 1. Rodar: python connector_smoke.py <projeto> [data_dir] --roundtrip
    # 2. Se alguma tradução crescer além do espaço original: implementar realocação de TOC


if __name__ == "__main__":
    try:                                              # Windows cp1252: permitir setas/acentos no stdout
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("project.json")
    override = sys.argv[2] if len(sys.argv) > 2 else None
    main(proj, override)
'''


def _choose_pattern(evidence: dict) -> tuple[str, str]:
    """Escolhe o padrão de stub com base nas evidências. Retorna (pattern_name, reason)."""
    enc = evidence.get("sample_encodings", {})
    ascii_frac = enc.get("ascii", 0.0)
    utf8_frac = enc.get("utf8", 0.0)
    text_frac = ascii_frac + utf8_frac
    density = evidence.get("string_density", 0.0)
    has_tokens = evidence.get("has_control_tokens", False)

    if has_tokens:
        return "token_table", "tokens de controle detectados (padrão [XX])"

    if text_frac >= 0.6 and density >= 0.30:
        return "linear_scan", (
            f"arquivo denso de texto ({text_frac:.0%} legível, density={density:.2f}) "
            f"— varredura linear é a abordagem mais rápida"
        )

    return "pointer_table", (
        f"binário estruturado (text={text_frac:.0%}, density={density:.2f}) "
        f"— provavelmente usa tabela de ponteiros"
    )


_SKELETON_DIR = Path(__file__).resolve().parent / "_skeleton"


def generate_build_plan_chapter() -> str:
    """Esqueleto de build_plan_chapter.py — protocolo comum (~70-80% identico entre
    conectores, confirmado comparando BoF4/Utawarerumono/Souldiers); so a preservacao de tokens
    estruturais do engine muda por projeto (marcado # ADAPTAR no arquivo). Ao contrario de
    `generate()` (extract.py, 3 padroes por evidencia), aqui NAO ha branching -- e sempre o
    mesmo esqueleto, o dev copia p/ connector/build_plan_chapter.py e adapta."""
    return (_SKELETON_DIR / "build_plan_chapter.py").read_text(encoding="utf-8")


def generate_verify_chapter() -> str:
    """Esqueleto de verify_chapter.py — protocolo de SAIDA comum (exit 0/1/3 +
    VERIFY_STATUS:{json}), consumido por connector_mgr._verify_status/run_scene.py sem mudanca
    entre projetos. A reconstrucao byte-a-byte (`_rebuild`, marcado # ADAPTAR) e 100%
    especifica do formato -- nao da p/ generalizar, exige o mesmo julgamento humano/LLM que
    ja escreve extract.py hoje."""
    return (_SKELETON_DIR / "verify_chapter.py").read_text(encoding="utf-8")


def generate(evidence: dict, engine_hint: str | None = None) -> str:
    """Gera candidato de extract.py para engines desconhecidas com código pré-preenchido.

    Escolhe o padrão de stub automaticamente pelas evidências detectadas.
    """
    pattern, reason = _choose_pattern(evidence)

    enc = evidence.get("sample_encodings", {})
    encoding = "utf-8" if enc.get("utf8", 0) > enc.get("ascii", 0) else "ascii"

    header = _render_header(evidence, engine_hint, pattern, reason)

    if pattern == "linear_scan":
        stub = _LINEAR_SCAN_STUB.format(encoding=encoding)
    elif pattern == "token_table":
        stub = _TOKEN_TABLE_STUB.format()
    else:
        stub = _POINTER_TABLE_STUB.format()

    return header + stub


def generate_reinsert(evidence: dict, engine_hint: str | None = None) -> str:
    """Gera candidato de reinsert.py PAREADO com o extract.py de generate() -- mesmo padrão
    (evidência decide o mesmo jeito nos dois), inverte encode/decode. #108: candidato pré-
    preenchido, não um conector completo -- o loop propõe→verifica→refina (ou o dev) ainda
    adapta e valida via round-trip (connector_smoke --roundtrip é o oráculo final).

    Escopo do candidato: escreve no MESMO espaço de bytes original (sem realocar TOC quando a
    tradução cresce) -- suficiente pra a maioria dos casos (byte_budget já limita a tradução
    upstream); casos que precisam crescer o arquivo exigem adaptação manual, sinalizada no
    próprio candidato."""
    pattern, reason = _choose_pattern(evidence)

    enc = evidence.get("sample_encodings", {})
    encoding = "utf-8" if enc.get("utf8", 0) > enc.get("ascii", 0) else "ascii"

    header = _render_reinsert_header(evidence, engine_hint, pattern, reason)

    if pattern == "linear_scan":
        stub = _LINEAR_SCAN_REINSERT_STUB.format(encoding=encoding)
    elif pattern == "token_table":
        stub = _TOKEN_TABLE_REINSERT_STUB.format()
    else:
        stub = _POINTER_TABLE_REINSERT_STUB.format()

    return header + stub


def _render_reinsert_header(evidence: dict, engine_hint: str | None, pattern: str, reason: str) -> str:
    lines = [
        "# GERADO AUTOMATICAMENTE por script_generator.py (engine desconhecida — completar e testar)",
        "# Par de: extract.py gerado por generate() com a MESMA evidência (mesmo padrão)",
        "#",
        "# Evidências detectadas:",
        f"#   file_count    : {evidence.get('file_count', '?')}",
        f"#   encoding      : {_fmt_enc(evidence.get('sample_encodings', {}))}",
        f"#   control_tokens: {evidence.get('has_control_tokens', '?')}",
        f"#   engine_hint   : {engine_hint or 'desconhecido'}",
        "#",
        f"# Padrão escolhido: {pattern.upper()}",
        f"#   Razão: {reason}",
        "#",
        "# PRÉ-REQUISITO: extract.py já validado (strings corretas, sem ruído).",
        "# Se o padrão for TOKEN_TABLE: copiar o MESMO BYTE_TO_CHAR/CONTROL_MAP já preenchido",
        "# no extract.py -- não redigitar, os dois precisam ser espelho exato um do outro.",
        "#",
        "# PRÓXIMOS PASSOS:",
        "#   1. Preencher as constantes de CONFIG marcadas acima (mesmos valores do extract.py)",
        "#   2. Rodar: python framework/connectors/connector_smoke.py <projeto> --roundtrip",
        "#   3. Round-trip byte-idêntico = conector aprovado (ratificação humana final)",
        "#",
        "",
    ]
    return "\n".join(lines)


def _render_header(evidence: dict, engine_hint: str | None, pattern: str, reason: str) -> str:
    lines = [
        "# GERADO AUTOMATICAMENTE por script_generator.py (engine desconhecida — completar e testar)",
        "#",
        "# Evidências detectadas:",
        f"#   file_count    : {evidence.get('file_count', '?')}",
        f"#   encoding      : {_fmt_enc(evidence.get('sample_encodings', {}))}",
        f"#   entropy_mean  : {evidence.get('entropy_mean', '?')}",
        f"#   string_density: {evidence.get('string_density', '?')}",
        f"#   control_tokens: {evidence.get('has_control_tokens', '?')}",
        f"#   engine_hint   : {engine_hint or 'desconhecido'}",
        "#",
        f"# Padrão escolhido: {pattern.upper()}",
        f"#   Razão: {reason}",
        "#",
        "# PRÓXIMOS PASSOS:",
        "#   1. Inspecionar arquivo representativo no HxD/010 Editor",
        "#   2. Preencher as constantes de CONFIG marcadas acima",
        "#   3. Rodar extract e validar output com connector_smoke.py:",
        "#      python framework/connectors/connector_smoke.py <projeto> [game_dir]",
        "#   4. Quando extract funcionar, implementar reinsert.py e rodar --roundtrip",
        "#   5. Round-trip byte-idêntico = conector aprovado",
        "#",
        "",
    ]
    return "\n".join(lines)


def _fmt_enc(encs: dict) -> str:
    return ", ".join(f"{k}: {v:.0%}" for k, v in encs.items()) or "desconhecido"
