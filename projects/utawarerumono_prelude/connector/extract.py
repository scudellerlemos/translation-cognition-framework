#!/usr/bin/env python3
"""extract.py — conector Utawarerumono: Prelude to the Fallen (escrito do zero; formato em table_schema.md).

Extrator DETERMINISTICO: Data/DataBase2.sdat -> artifacts/dialogs.csv (so a coluna EN dos membros
ScriptTextData_*). O parser do contêiner e dos membros mora aqui e e importado por reinsert.py/verify_chapter.py,
para os dois lados compartilharem o MESMO formato (garante o round-trip).

Uso: python extract.py [project.json|raiz] [<DataBase2.sdat | pasta Data>]
     (sem o 2o argumento: variavel de ambiente connector.data_dir_env, ex.: UTAP_DATA_DIR)
"""
import contextlib
import hashlib
import json
import struct
import sys
from dataclasses import dataclass
from pathlib import Path

_FRAMEWORK_CONNECTORS = Path(__file__).resolve().parents[3] / "framework" / "connectors"
if str(_FRAMEWORK_CONNECTORS) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK_CONNECTORS))
import connector_io  # noqa: E402

SDAT_NAME = "DataBase2.sdat"
TEXT_PREFIX = "ScriptTextData_"
# escopo "completo": alem das cenas, nomes, mensagens de sistema, unidades e nomes de fase. StageTextData tem
# layout proprio (ver read_stage_member): no proprio jogo os ponteiros das colunas 2 e 3 estao errados.
STAGE_MEMBER = "StageTextData.bin"
EXTRA_MEMBERS = ("NameTextData.bin", "SysMessageTextData.bin", "UnitTextData.bin", STAGE_MEMBER)
LANGS = ("ja", "ko", "zh", "en")
EN_COL = LANGS.index("en")
_PACK_TAG = b"Pack        "


class Unsupported(ValueError):
    """Membro fora do layout estrito (nao e extraido nem alterado)."""


def _align(n: int) -> int:
    return (n + 15) // 16 * 16


def _u32(d: bytes, o: int) -> int:
    return struct.unpack_from("<I", d, o)[0]


# ---------------------------------------------------------------------------
# 1. CONTEINER .sdat
# ---------------------------------------------------------------------------
@dataclass
class Sdat:
    head: bytes             # tudo antes do 1o membro (tags, nomes, tabela Pack)
    tail: bytes             # bytes depois do ultimo membro
    pack_pairs_at: int      # offset da 1a (offset, size) em `head`
    names: list[str]
    members: list[bytes]


def read_sdat(data: bytes) -> Sdat:
    pk = data.index(_PACK_TAG)
    count = _u32(data, pk + 16)
    pairs_at = pk + 20
    pairs = [(_u32(data, pairs_at + 8 * i), _u32(data, pairs_at + 8 * i + 4)) for i in range(count)]
    names_blk = data[16 + _u32(data, 16):pk].rstrip(b"\0").split(b"\0")
    names = [n.decode("ascii") for n in names_blk]
    if len(names) != count:
        raise ValueError(f"{len(names)} nome(s) para {count} membro(s)")
    pos = pairs[0][0]
    for o, s in pairs:
        if o != _align(pos) or any(data[pos:o]):
            raise ValueError("membros fora do alinhamento de 16 bytes com padding zerado")
        pos = o + s
    return Sdat(data[:pairs[0][0]], data[pos:], pairs_at, names,
                [data[o:o + s] for o, s in pairs])


def write_sdat(sd: Sdat, members: list[bytes]) -> bytes:
    head = bytearray(sd.head)
    body, off = bytearray(), len(head)
    for i, m in enumerate(members):
        pad = _align(off) - off
        body += bytes(pad) + m
        off += pad
        struct.pack_into("<II", head, sd.pack_pairs_at + 8 * i, off, len(m))
        off += len(m)
    return bytes(head) + bytes(body) + sd.tail


# ---------------------------------------------------------------------------
# 2. MEMBRO DE TEXTO (n linhas x cols strings UTF-8, pool contiguo)
# ---------------------------------------------------------------------------
def read_text_member(b: bytes) -> tuple[int, int, list[bytes]]:
    """(n, cols, strings[n*cols] sem o NUL). Levanta Unsupported fora do layout estrito."""
    n = _u32(b, 0)
    if n == 0 or len(b) < 8:
        raise Unsupported("membro vazio")
    first = _u32(b, 4)
    if (first - 4) % (4 * n) or not 1 <= (first - 4) // (4 * n) <= 8:
        raise Unsupported("tabela de ponteiros com tamanho inesperado")
    cols = (first - 4) // (4 * n)
    ptrs = [_u32(b, 4 + 4 * j) for j in range(n * cols)]
    out, pos = [], first
    for p in ptrs:
        if p != pos:
            raise Unsupported("pool nao contiguo ou ponteiros fora de ordem")
        end = b.find(b"\0", p)
        if end < 0:
            raise Unsupported("string sem terminador")
        out.append(b[p:end])
        pos = end + 1
    if pos != len(b):
        raise Unsupported("bytes sobrando depois do pool")
    return n, cols, out


def build_text_member(n: int, cols: int, strings: list[bytes]) -> bytes:
    pos = 4 + 4 * n * cols
    ptrs = []
    for s in strings:
        ptrs.append(pos)
        pos += len(s) + 1
    return struct.pack("<I", n) + struct.pack(f"<{len(ptrs)}I", *ptrs) + b"".join(s + b"\0" for s in strings)


def read_stage_member(b: bytes) -> tuple[int, int, list[bytes]]:
    """StageTextData: (n, 4, strings[n*4] na ordem JA, KO, ZH, EN) lidas do pool, nao dos ponteiros.

    O pool traz, linha a linha, JA, KO, ZH, EN em sequencia (strings contiguas). Os ponteiros do proprio jogo
    nao servem de guia: JA e KO acertam, a coluna 3 aponta para o ZH e a coluna 2 cai de -10 a +21 bytes
    em torno do EN. Levanta Unsupported se o pool nao tem exatamente n*4 strings ou se JA/KO nao batem. Le tambem o membro
    ja corrigido por build_stage_member (colunas 2 e 3 no EN), entao e idempotente.
    """
    n = _u32(b, 0)
    if n == 0 or len(b) < 8 or (_u32(b, 4) - 4) != 16 * n:
        raise Unsupported("StageTextData: tabela de ponteiros com tamanho inesperado")
    pool = 4 + 16 * n
    strings = b[pool:].split(b"\0")
    if strings.pop() != b"" or len(strings) != 4 * n:
        raise Unsupported("StageTextData: pool nao tem n*4 strings")
    pos = pool
    for r in range(n):
        p_ko = pos + len(strings[4 * r]) + 1
        if _u32(b, 4 + 16 * r) != pos or _u32(b, 8 + 16 * r) != p_ko:
            raise Unsupported("StageTextData: ponteiro JA/KO fora do pool contiguo")
        pos = p_ko + sum(len(x) + 1 for x in strings[4 * r + 1:4 * r + 4])
    return n, 4, strings


def build_stage_member(n: int, strings: list[bytes]) -> bytes:
    """Inverso de read_stage_member, com os ponteiros corrigidos: JA, KO, e as colunas 2 e 3 apontam para o EN
    (o jogo le o EN de uma delas conforme a ordem de colunas; as duas mostram o mesmo texto). O ZH fica no pool."""
    pos = 4 + 16 * n
    ptrs = []
    for r in range(n):
        ja, ko, zh, en = strings[4 * r:4 * r + 4]
        p_ja, p_ko = pos, pos + len(ja) + 1
        p_en = p_ko + len(ko) + 1 + len(zh) + 1
        ptrs += [p_ja, p_ko, p_en, p_en]
        pos = p_en + len(en) + 1
    return struct.pack("<I", n) + struct.pack(f"<{len(ptrs)}I", *ptrs) + b"".join(s + b"\0" for s in strings)


def build_member(name: str, n: int, cols: int, strings: list[bytes]) -> bytes:
    return build_stage_member(n, strings) if name == STAGE_MEMBER else build_text_member(n, cols, strings)


def residual_members(src: Path) -> dict[str, bytes]:
    """{nome do membro: bytes} do .sdat, para o connector_gate conferir texto que o extract deixou para tras."""
    sd = read_sdat(Path(src).read_bytes())
    return dict(zip(sd.names, sd.members, strict=True))


def scene_of(name: str) -> str:
    return (name[len(TEXT_PREFIX):] if name.startswith(TEXT_PREFIX) else name).removesuffix(".bin")


def text_members(sd: Sdat):
    """Gera (scene, indice_do_membro, n, cols, strings, motivo) dos ScriptTextData; motivo != "" = fora do layout."""
    for i, (name, m) in enumerate(zip(sd.names, sd.members, strict=True)):
        if not (name.startswith(TEXT_PREFIX) or name in EXTRA_MEMBERS):
            continue
        try:
            n, cols, strings = (read_stage_member if name == STAGE_MEMBER else read_text_member)(m)
            if cols != len(LANGS):
                raise Unsupported(f"{cols} colunas (esperado {len(LANGS)})")
            yield scene_of(name), i, n, cols, strings, ""
        except Unsupported as e:
            yield scene_of(name), i, 0, 0, [], str(e)


# ---------------------------------------------------------------------------
# 3. MAIN
# ---------------------------------------------------------------------------
def story_order(db: bytes, scenes: set[str]) -> list[str]:
    """Ordem das cenas no jogo: EventManagerData.bin do ENG/DataBase.sdat (registros de 48 bytes; a chave do evento
    e o campo 3, NN_NN_NN = chave/100000, chave/1000%100, chave%1000/10). So entram cenas que existem no projeto."""
    pk = db.index(b"Pack        ")
    names = db[16 + _u32(db, 16):pk].rstrip(b"\0").split(b"\0")
    o, size = struct.unpack_from("<II", db, pk + 20 + 8 * names.index(b"EventManagerData.bin"))
    b = db[o:o + size]
    order: list[str] = []
    for i in range(_u32(b, 0)):
        k = struct.unpack_from("<12I", b, 4 + 48 * i)[3]
        sid = f"{k // 100000:02d}_{k // 1000 % 100:02d}_{k % 1000 // 10:02d}"
        if sid in scenes and sid not in order:
            order.append(sid)
    return order


def write_story_order(root: Path, src: Path, scenes: set[str]) -> str:
    """Grava artifacts/ordem_cenas.txt a partir do DataBase.sdat ao lado do .sdat de texto (Data/ENG/DataBase.sdat);
    devolve a linha para o extraction_log. Sem o arquivo do jogo (fonte copiada sozinha), mantem o que ja existe."""
    out = root / "artifacts" / "ordem_cenas.txt"
    for cand in (src.parent / "ENG" / "DataBase.sdat", src.parent / "DataBase.sdat"):
        if cand.is_file():
            order = story_order(cand.read_bytes(), scenes)
            out.write_text("\n".join(order) + "\n", encoding="utf-8")
            return f"- Ordem das cenas: {len(order)} de {len(scenes)} em {out.name} (de {cand.name}, EventManagerData)\n"
    return ("- Ordem das cenas: DataBase.sdat nao encontrado ao lado da fonte; " +
            ("ordem_cenas.txt anterior mantido\n" if out.is_file() else "ordem NAO confirmada (sem ordem_cenas.txt)\n"))


def resolve_sdat(conn: dict, cli_override: str | None) -> Path:
    p = connector_io.resolve_source_path(
        cli_arg=cli_override, env_var=conn.get("data_dir_env"),
        error_hint=f"informe o DataBase2.sdat ou a pasta Data (arg 2 ou variavel {conn.get('data_dir_env')})")
    return p / SDAT_NAME if p.is_dir() else p


def main(project_json: Path, source_override: str | None = None):
    with contextlib.suppress(AttributeError, ValueError, OSError):
        sys.stdout.reconfigure(encoding="utf-8")
    cfg = json.loads(project_json.read_text(encoding="utf-8"))
    root = project_json.parent
    src = resolve_sdat(cfg["connector"], source_override)
    data = src.read_bytes()
    sd = read_sdat(data)

    id_col, text_col = cfg["source"]["id_column"], cfg["source"]["text_column"]
    rows, skipped, n_empty = [], [], 0
    for scene, mi, n, _, strings, why in text_members(sd):
        if why:
            skipped.append(f"{sd.names[mi]}: {why}")
            continue
        for idx in range(n):
            text = strings[idx * len(LANGS) + EN_COL].decode("utf-8")
            if not text:
                n_empty += 1
                continue
            rows.append({id_col: f"{scene}:{idx}", "scene": scene, "file": sd.names[mi], "idx": idx, text_col: text,
                         "byte_budget": len(text.encode("utf-8")) + 1})

    connector_io.write_dialogs_csv(root / cfg["source"]["file"],
                                   [id_col, "scene", "file", "idx", text_col, "byte_budget"], rows)
    scene_ids = {r["scene"] for r in rows}
    scenes = len(scene_ids)
    order_line = write_story_order(root, src, scene_ids)
    connector_io.write_extraction_log(
        root / "artifacts" / "extraction_log.md",
        "# Extraction Log\n\n"
        f"- Fonte: {src.name} ({len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()[:16]})\n"
        f"- Membros no contêiner: {len(sd.names)}; membros de texto extraídos: {scenes} (cenas + Name/SysMessage/Unit/Stage)\n"
        f"- Strings EN extraídas: {len(rows)}; EN vazias (ficam como estão): {n_empty}\n"
        f"- Fora do layout estrito (não extraídos): {len(skipped)}\n" + order_line +
        "- StageTextData.bin: fora do escopo (ponteiro EN do próprio jogo aponta para o meio da string)\n"
        + "".join(f"  - {s}\n" for s in skipped))
    print(f"Extraídas {len(rows)} strings de {scenes} cenas -> {root / cfg['source']['file']}")


if __name__ == "__main__":
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("project.json")
    if proj.is_dir():
        proj = proj / "project.json"
    main(proj, sys.argv[2] if len(sys.argv) > 2 else None)
