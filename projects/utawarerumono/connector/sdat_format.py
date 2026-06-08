#!/usr/bin/env python3
"""
sdat_format.py — formato do container ScriptEvent.sdat (Aquaplus), compartilhado por
extract.py e reinsert.py. Mantê-lo único garante o round-trip (mesma leitura nos dois lados).

Formato (engenharia reversa — ver connector/table_schema.md):

  [Filename    ] (12 bytes) + u32 ptr p/ seção Pack + array de u32 (offsets dos nomes)
  Tabela de NOMES: registros de 15 bytes (nome de 14 chars `CC_SS_NNNT.BIN` + \\0), em ordem.
  [Pack        ] (12 bytes) + u32 (tam) + u32 count + count*(u32 offset, u32 size)
  Dados: cada arquivo = [cabeçalho/bytecode 'STSC' ...][bloco de texto: strings UTF-8
         null-terminated e contíguas]. Os ponteiros de exibição são `50 00`+u32 (offset
         ABSOLUTO no arquivo), espalhados pelo bytecode (uma string pode ser referenciada
         de vários scripts — pool de texto reusado).

Convenções:
- offset (hex) = id_column (endereço absoluto da string no arquivo).
- byte_budget = nº de bytes UTF-8 da string (sem o \\0).
- "dialogue block" de um arquivo = a corrida de strings de texto real ao fim do seu bloco
  de dados (após o bytecode). É o que o jogador lê naquele script.
"""
from __future__ import annotations
import struct
from dataclasses import dataclass

FILENAME_MAGIC = b"Filename    "   # 12 bytes
PACK_MAGIC = b"Pack        "       # 12 bytes
NAME_STRIDE = 15                   # registro de nome: 14 chars + \0
TEXT_OPCODE = b"\x50\x00"          # opcode de exibição de texto, precede o ponteiro absoluto
MAX_RUN = 100000                   # trava de segurança ao caminhar um run (alta: runs de narração
                                   # têm dezenas de continuações; truncar corromperia a relocação)


@dataclass(frozen=True)
class ScriptFile:
    index: int
    name: str
    offset: int
    size: int

    @property
    def end(self) -> int:
        return self.offset + self.size


# --------------------------------------------------------------------------- índice do container
def parse_pack(data: bytes) -> list[ScriptFile]:
    """Lê a seção Pack -> lista de ScriptFile (index, name, offset, size), em ordem.
    Os nomes vêm da tabela de NOMES (stride 15) logo após o array de offsets do header."""
    pack = data.find(PACK_MAGIC)
    if pack < 0:
        raise ValueError("seção 'Pack' não encontrada — container inesperado")
    p = pack + len(PACK_MAGIC)
    count = struct.unpack_from("<I", data, p + 4)[0]
    base = p + 8
    files = []
    # tabela de nomes: começa logo após o array de u32 do header 'Filename'
    name_base = data.find(b"\x00", len(FILENAME_MAGIC) + 4) + 1
    # alinhar: o primeiro nome real é o 1º registro CC_SS_...; localizado de forma robusta
    first = data.find(b".BIN")
    name_base = first - 10  # 'CC_SS_NNNT' = 10 chars antes de '.BIN'
    for k in range(count):
        off, size = struct.unpack_from("<II", data, base + 8 * k)
        rec = data[name_base + NAME_STRIDE * k: name_base + NAME_STRIDE * k + 14]
        name = rec.decode("latin1", "replace").rstrip("\x00")
        files.append(ScriptFile(k, name, off, size))
    return files


def files_for_scenes(files: list[ScriptFile], prefixes: tuple[str, ...]) -> list[ScriptFile]:
    """Arquivos cujo nome começa por algum prefixo (ex.: ('11_01','11_02','11_03'))."""
    return [f for f in files if any(f.name.startswith(p) for p in prefixes)]


# --------------------------------------------------------------------------- leitura de strings
def read_cstr(data: bytes, off: int) -> bytes:
    end = data.find(b"\x00", off)
    if end == -1:
        end = len(data)
    return data[off:end]


def is_dialogue(raw: bytes) -> bool:
    """Heurística: string de TEXTO real (não bytecode). UTF-8 válido, tem letra,
    quase tudo imprimível, e não é nome de arquivo de script nem magic do container."""
    if len(raw) < 2:
        return False
    try:
        s = raw.decode("utf-8")
    except UnicodeDecodeError:
        return False
    if not any(c.isalpha() for c in s):
        return False
    if s.endswith(".BIN") or s.startswith("STSC"):   # nome de script / magic do container
        return False
    printable = sum(1 for c in s if c.isprintable() or c == "\t")
    return printable / len(s) >= 0.95


def extract_text_block(data: bytes, f: ScriptFile, max_gap: int = 2) -> list[tuple[int, str, int]]:
    """Bloco de diálogo do arquivo: a corrida de strings de diálogo com maior MASSA de texto
    (tolerante a pequenos buracos de bytecode de até `max_gap` strings não-diálogo entre elas —
    o texto real é interrompido por opcodes inline esporádicos).
    Retorna [(offset, text, byte_budget)] em ordem de armazenamento (= ordem narrativa)."""
    i = f.offset
    runs: list[list[tuple[int, str, int]]] = []
    cur: list[tuple[int, str, int]] = []
    gap = 0
    while i < f.end:
        end = data.find(b"\x00", i)
        if end == -1 or end > f.end:
            break
        raw = data[i:end]
        if raw and is_dialogue(raw):
            cur.append((i, raw.decode("utf-8"), len(raw)))
            gap = 0
        elif cur:
            gap += 1
            if gap > max_gap:
                runs.append(cur)
                cur = []
                gap = 0
        i = end + 1
    if cur:
        runs.append(cur)
    if not runs:
        return []
    # bloco = a corrida com maior MASSA de texto (bytes) — favorece prosa real sobre ruído curto
    block = max(runs, key=lambda r: sum(len(t) for _, t, _ in r))
    return _trim_edges(block)


# Pontuação que sinaliza fala real (uma linha de diálogo quase sempre termina/contém isto).
_DIALOGUE_PUNCT = set(".?!,;:……-'\"")


def _is_edge_noise(text: str) -> bool:
    """Heurística de RUÍDO de bytecode em BORDA: palavra única, curta, sem espaço e sem pontuação
    de fala (ex.: 'STSC', 'Head', 'head', 'TA', 'gs'). Rótulos de falante reais (Girl/Kuon/...) ficam
    no MEIO do bloco, então só apararmos as pontas é seguro: falas reais de borda têm espaço ou
    pontuação ('Ngh... ghh...', 'She's... waiting...', '...beginning.', 'Right?')."""
    t = text.strip()
    return len(t) <= 6 and (" " not in t) and not any(c in _DIALOGUE_PUNCT for c in t)


def _trim_edges(block: list[tuple[int, str, int]]) -> list[tuple[int, str, int]]:
    """Remove ruído de bytecode coladinho nas pontas do bloco de texto (head/tail)."""
    while block and _is_edge_noise(block[-1][1]):
        block.pop()
    while block and _is_edge_noise(block[0][1]):
        block.pop(0)
    return block


# --------------------------------------------------------------------------- ponteiros (reinsert)
# MODELO DE PONTEIRO: `50 00` + uint32 é um offset RELATIVO ao início do ARQUIVO (Pack) que contém o
# ponteiro. Endereço absoluto da string = file_start_do_site + uint32. Verificado empiricamente: dos
# ~47k sites `50 00`, ~42k só fazem sentido como file-relativo (vs ~63 como absoluto = coincidência).
# Strings NÃO cruzam arquivos: cada ponteiro endereça dentro do próprio script. O 1º desses ponteiros
# de um script é a "entrada" do seu bloco de texto.


def _file_start_of(off: int, starts: list[int], files: list[ScriptFile]) -> int | None:
    """Início do arquivo (Pack) que contém `off`, via busca binária. None se fora de qualquer arquivo."""
    import bisect
    j = bisect.bisect_right(starts, off) - 1
    if 0 <= j < len(files) and files[j].offset <= off < files[j].end:
        return files[j].offset
    return None


def index_pointers(data: bytes, files: list[ScriptFile]) -> dict[int, list[tuple[int, int]]]:
    """Uma varredura: mapeia target_abs -> [(site, file_start)] para todo `50 00`+uint32, tratando o
    uint32 como FILE-RELATIVO (target_abs = file_start_do_site + uint32). `site` é a posição do uint32.
    Passe o resultado (`idx`) para find_pointers/is_head/read_run."""
    starts = [f.offset for f in files]
    idx: dict[int, list[tuple[int, int]]] = {}
    n = len(data)
    i = 0
    while True:
        i = data.find(TEXT_OPCODE, i)
        if i == -1:
            break
        site = i + len(TEXT_OPCODE)
        if site + 4 <= n:
            fs = _file_start_of(i, starts, files)
            if fs is not None:
                tgt = fs + struct.unpack_from("<I", data, site)[0]
                idx.setdefault(tgt, []).append((site, fs))
        i += 1
    return idx


def find_pointers(data: bytes, off: int, idx: dict[int, list[tuple[int, int]]]) -> list[tuple[int, int]]:
    """Ponteiros REAIS para `off` (endereço absoluto): lista de (site, file_start). Requer `idx`."""
    return idx.get(off, [])


def is_head(data: bytes, off: int, idx: dict[int, list[tuple[int, int]]]) -> bool:
    return off in idx


def read_run(data: bytes, head_off: int, idx: dict[int, list[tuple[int, int]]]) -> list[int]:
    """Run = head + continuações (strings sem ponteiro próprio) até o próximo head.
    Captura o run COMPLETO (sem truncar): a relocação precisa mover todas as continuações."""
    members = [head_off]
    nxt = head_off + len(read_cstr(data, head_off)) + 1
    while len(members) < MAX_RUN and nxt < len(data):
        if data[nxt] == 0x00:
            break
        if is_head(data, nxt, idx):
            break
        members.append(nxt)
        nxt += len(read_cstr(data, nxt)) + 1
    return members
