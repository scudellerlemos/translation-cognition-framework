#!/usr/bin/env python3
"""font.py — acentos pt-BR na fonte ORIGINAL do texto EN do Prelude (table_schema.md, Secao 5).

O texto EN (dialogo e menu) sai de `Data/ENG/Texture/font.tex` (atlas RGBA 256x256, so o alpha desenha) e de uma
tabela BMFont binaria embutida no executavel (121 entradas de 20 B: u32 codigo Unicode ordenado + x,y,w,h,
xoffset,yoffset,xadvance + page + chnl; fonte "KoreanPGDM", pagina 256x256). Nao ha acento nela.

Aqui cada letra acentuada = glifo da letra-base copiado do proprio atlas + acento tirado dos tracos da propria fonte
(` espelhado/escalado, ~ e , escalados), desenhado em area livre do atlas (abaixo da linha 175). A entrada nova
REAPROVEITA a de um glifo que nenhum texto usa (SACRIFICE): o tamanho da tabela e do exe nao muda e a fonte segue
identica a original. A tabela e reordenada por codigo (busca binaria).

Uso: python font.py <exe original> <font.tex original> <dir de saida>   -> escreve game.exe e font.tex novos
"""
import struct
import sys
import unicodedata
from pathlib import Path

N = 256
FREE_Y = 178
ENTRY = struct.Struct("<I7hBB")
TARGETS = "áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ"
# glifos que nenhum EN desenha (dialogs.csv) — viram os acentuados; ` ~ , sao copiados antes de sumirem (~ NAO pode ser sacrificado: 60 usos, ex. ♪~♪~~)
SACRIFICE = "×™□△◇○☆✖⑪⑫⑬⑭⑮⑯{}\\|^`_<#$"
# o que a tabela nao tem (aspas curvas, reticencias, travessao) vira o equivalente que ela tem
FIT = str.maketrans({"“": '"', "”": '"', "«": '"', "»": '"', "‘": "'", "’": "'", "–": "-", "—": "―"})
TABLE_MARK = b"KoreanPGDM_26_binary_0.tga\0"


def fit(text: str) -> str:
    return text.translate(FIT).replace("…", "...")


def lz_decode(buf: bytes) -> bytes:
    assert buf[:4] == b"LZ77"
    size, ops, off = struct.unpack_from("<III", buf, 4)
    flags, p, dst, bits, fl, fi = buf[16:off], off, bytearray(), 0, 0, 0
    for _ in range(ops):
        if bits == 0:
            bits, fl, fi = 8, flags[fi], fi + 1
        if fl & 0x80:
            o, n = buf[p], buf[p + 1] + 3
            p += 2
            for _ in range(n):
                dst.append(dst[-o])
        else:
            dst.append(buf[p])
            p += 1
        fl, bits = (fl << 1) & 0xFF, bits - 1
    assert len(dst) == size
    return bytes(dst)


def lz_encode(raw: bytes) -> bytes:
    """So literais (flags zero): maior que o original, mas o jogo le igual."""
    nflags = (len(raw) + 7) // 8
    return b"LZ77" + struct.pack("<III", len(raw), len(raw), 16 + nflags) + bytes(nflags) + raw


def read_tex(tex: bytes) -> list[bytearray]:
    pnglen = struct.unpack_from("<I", tex, 24)[0]
    raw = lz_decode(tex[0x20:0x20 + pnglen])
    return [bytearray(raw[y * N * 4 + 3:(y + 1) * N * 4:4]) for y in range(N)]   # so o alpha


def write_tex(tex: bytes, alpha: list[bytearray]) -> bytes:
    lz = lz_encode(b"".join(b"".join(b"\xff\xff\xff" + bytes((a,)) for a in row) for row in alpha))
    head = bytearray(tex[:0x20])
    struct.pack_into("<I", head, 12, len(lz) + 32)
    struct.pack_into("<I", head, 24, len(lz))
    body = bytes(head) + lz
    return body + bytes(-len(body) % 16) + tex[tex.index(b"Parts"):]


def read_table(exe: bytes) -> tuple[int, list[tuple]]:
    p = exe.index(TABLE_MARK) + len(TABLE_MARK)
    assert exe[p] == 4
    n = struct.unpack_from("<I", exe, p + 1)[0] // ENTRY.size
    return p + 5, [ENTRY.unpack_from(exe, p + 5 + ENTRY.size * i) for i in range(n)]


def _crop(g):
    rows = [y for y, r in enumerate(g) if any(r)]
    cols = [x for x in range(len(g[0])) if any(r[x] for r in g)]
    return [r[cols[0]:cols[-1] + 1] for r in g[rows[0]:rows[-1] + 1]]


def _scale(g, w, h):
    """Reducao por media de area (preserva o peso do traco)."""
    gh, gw = len(g), len(g[0])
    out = []
    for y in range(h):
        y0, y1 = y * gh / h, (y + 1) * gh / h
        row = []
        for x in range(w):
            x0, x1 = x * gw / w, (x + 1) * gw / w
            tot = wgt = 0.0
            for j in range(int(y0), min(gh, int(y1) + 1)):
                for i in range(int(x0), min(gw, int(x1) + 1)):
                    a = (min(y1, j + 1) - max(y0, j)) * (min(x1, i + 1) - max(x0, i))
                    if a > 0:
                        tot, wgt = tot + a * g[j][i], wgt + a
            row.append(min(255, int(tot / wgt * 1.25)))
        out.append(row)
    return out


def _accents(alpha, tab, small):
    """acento -> bitmap, a partir dos tracos da propria fonte."""
    def cut(ch):
        _, x, y, w, h = tab[ord(ch)][:5]
        return _crop([list(alpha[y + j][x:x + w]) for j in range(h)])
    gh, aw = (5, 4) if small else (6, 5)
    grave = _scale(cut("`"), aw, gh)
    acute = [r[::-1] for r in grave]
    cedil = _scale(cut(","), 4, 5)
    tilde = _scale(cut("~"), 10 if small else 11, 4 if small else 5)
    circ = _scale(cut("^"), 9 if small else 11, 5 if small else 6)
    return {"́": acute, "̀": grave, "̂": circ, "̃": tilde, "̧": cedil}


def build(exe: bytes, tex: bytes) -> tuple[bytes, bytes, dict[str, str]]:
    """(game.exe novo, font.tex novo, {acentuada: glifo sacrificado})."""
    alpha = read_tex(tex)
    at, ents = read_table(exe)
    tab = {e[0]: e for e in ents}
    arts = {s: _accents(alpha, tab, s) for s in (False, True)}
    px, py, rowh = 0, FREE_Y, 0
    new, used = {}, {}
    for ch, old in zip(TARGETS, SACRIFICE, strict=True):
        base_ch, mark = unicodedata.normalize("NFD", ch)
        _, bx, by, bw, bh, xo, yo, xa, page, chnl = tab[ord(base_ch)]
        art = arts[ch.isupper()][mark]
        aw, ah = len(art[0]), len(art)
        cell = [list(alpha[by + j][bx:bx + bw]) for j in range(bh)]
        if mark == "̧":                       # cedilha: abaixo, preso ao fundo do c
            top, extra = bh - 2, 3
        elif base_ch == "i":                       # tira o pingo: o agudo ocupa o lugar dele
            gap = next(j for j in range(1, bh) if not any(cell[j]))
            for j in range(gap):
                cell[j] = [0] * bw
            art, ah, top, extra = _scale(art, aw, ah - 1), ah - 1, 1, 1
        else:
            top, extra = 1, ah + 1                  # 1 linha em branco no topo: sem corte na borda do atlas
        cols = [x for x in range(bw) if any(r[x] for r in cell)]
        cx = (cols[0] + cols[-1] + 1) / 2
        pad = max(0, -(-(aw - bw) // 2))
        W, H = bw + 2 * pad, bh + extra
        out = [[0] * W for _ in range(H)]
        shift = extra if mark != "̧" else 0
        for j, r in enumerate(cell):
            if 0 <= j + shift < H:
                out[j + shift][pad:pad + bw] = r
        left = min(max(0, round(cx - aw / 2) + pad), W - aw)
        for j, r in enumerate(art):
            for i, a in enumerate(r):
                out[top + j][left + i] = max(out[top + j][left + i], a)
        if px + W > N:
            px, py, rowh = 0, py + rowh + 2, 0
        assert py + H <= N, "atlas sem espaco livre"
        for j, r in enumerate(out):
            alpha[py + j][px:px + W] = bytes(r)
        new[ord(ch)] = (ord(ch), px, py, W, H, xo - pad, yo - (shift if mark != "̧" else 0), xa, page, chnl)
        used[ch] = old
        px, rowh = px + W + 2, max(rowh, H)
    drop = {ord(c) for c in SACRIFICE}
    final = sorted([e for e in ents if e[0] not in drop] + list(new.values()))
    assert len(final) == len(ents)
    out_exe = bytearray(exe)
    for i, e in enumerate(final):
        ENTRY.pack_into(out_exe, at + ENTRY.size * i, *e)
    return bytes(out_exe), write_tex(tex, alpha), used


if __name__ == "__main__":
    exe, tex, dst = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    ne, nt, used = build(exe.read_bytes(), tex.read_bytes())
    dst.mkdir(parents=True, exist_ok=True)
    (dst / "game.exe").write_bytes(ne)
    (dst / "font.tex").write_bytes(nt)
    print(f"{len(used)} glifos acentuados; entradas reaproveitadas: {''.join(used.values())}")
