"""Rotulos de interface desenhados em imagem (folha principal: menu, loja, acampamento, salvar...).

A folha e uma secao 256x256, 4bpp, comprimida (imgcodec), repetida em varios .DAT. Cada rotulo ocupa uma
faixa de 8 px: corpo da letra nas linhas 1-6 (minusculas 2-6), contorno de 1 px em volta. Dois estilos:
contorno 1 (letra clara, corpo 0xB) e contorno 7 (caixa cinza, letra escura, corpo 1).

O alfabeto sai da propria folha: os rotulos originais sao cortados em letras e as palavras novas sao montadas
com elas (nenhum pixel do jogo fica no repo). Letra que a folha nao tem vem do outro estilo ou de `_DRAWN`.
So o retangulo de cada rotulo e redesenhado; a folha e reconhecida pelo conteudo da area de rotulos, nao
pelo nome do arquivo.

Limite de largura: o jogo recorta cada rotulo num retangulo proprio. Onde a regua mediu, vale o medido
(6o campo de cada rotulo); no resto vale a celula ate o proximo rotulo. Nao coube -> tenta a proxima candidata;
nenhuma coube -> o rotulo fica como esta.
"""
import hashlib
import json
import struct
import unicodedata
from pathlib import Path

import imgcodec

FLAGS, KIND, W, COLS = 0x00800001, 0x1a000200, 256, 2
AREA = (24, 128)                                   # linhas da folha que so tem rotulo
# sha1[:16] da area original (ver _area_hash) -> (tabela, rotulos [indice] que essa variante cobre com arte)
SHEETS = {'6d0412d1b02653c8': ('principal', frozenset()),                      # menu, acampamento, loja, salvar
          '483c3cc357dec579': ('principal', frozenset({14, 20, 35, 56, 57})),  # final do jogo / minigame
          '2dc467a88f45b915': ('principal', frozenset({23, 35, 52, 57})),      # loja dos Manillos
          '5dc4f7fdb19817f0': ('sistema', frozenset()),                        # campo, fim de batalha, pesca
          'be9d8e4f0b651fed': ('batalha', frozenset())}                        # tela de batalha
BODY = {1: 0xB, 7: 1, 3: 1}                        # contorno -> cor do corpo (3 = botao de batalha)
_TO_DARK = {0xB: 1, 9: 2, 7: 4, 4: 5, 2: 6}        # estilo 1 -> estilo 7 (mesma rampa, sentido inverso)
_TO_LIGHT = {1: 0xB, 2: 9, 3: 7, 4: 7, 5: 4, 6: 2}

# {tabela: [[y, x0, x1, original, candidatas em ordem de preferencia(, largura medida no jogo)], ...]} -- o texto
# fica no project.json ("image_labels"): script do conector nao carrega texto da obra
TABLES = json.loads((Path(__file__).parent.parent / 'project.json').read_text(encoding='utf-8')).get('image_labels', {})
LABELS = TABLES.get('principal', [])
# letra colada na vizinha no original: (tabela, indice) -> (quantas letras iniciais valem, colunas da ultima ou None)
_PARTIAL = {('principal', 10): (1, 5), ('principal', 22): (4, None), ('sistema', 4): (1, 5)}
# letras que a folha nao tem em nenhum estilo (desenho proprio, linhas 0-7; x = corpo)
_DRAWN = {
    'V': ['.....', 'x...x', 'x...x', 'x...x', '.x.x.', '.x.x.', '..x..', '.....'],
    'v': ['.....', '.....', 'x...x', 'x...x', '.x.x.', '.x.x.', '..x..', '.....'],
    'j': ['..', '.x', '..', '.x', '.x', '.x', 'x.', '..'],
}
_MARKS = {'̂': [(1, -1), (0, 0), (1, 1)], '́': [(1, 0), (0, 1)], '̃': [(1, -1), (0, 0), (1, 1), (0, 2)], '̧': [(7, 0)]}


def pixels(lin: bytes) -> list[list[int]]:
    px = []
    for b in lin:
        px += [b & 15, b >> 4]
    return [px[y * W:(y + 1) * W] for y in range(len(px) // W)]


def pack(rows) -> bytes:
    return bytes(r[i] | r[i + 1] << 4 for r in rows for i in range(0, W, 2))


def _area_hash(rows) -> str:
    return hashlib.sha1(bytes(v for r in rows[AREA[0]:AREA[1]] for v in r), usedforsecurity=False).hexdigest()[:16]


def _cell(rows, y, x0, x1):
    """(contorno, colunas do corpo [8 valores cada], x da primeira coluna com tinta) do rotulo original."""
    cell = [r[x0:x1] for r in rows[y:y + 8]]
    edge = [v for v in cell[0] + cell[7] if v]
    fill = max(set(edge), key=edge.count)
    cols = [[cell[r][c] if cell[r][c] not in (0, fill) else 0 for r in range(8)] for c in range(x1 - x0)]
    ink = [c for c in range(x1 - x0) if any(cell[r][c] for r in range(8))]
    return fill, cols, x0 + ink[0], x0 + ink[-1] + 1


def _segments(cols):
    segs, s = [], None
    for c, col in enumerate(cols + [[0]]):
        if any(col) and s is None:
            s = c
        elif not any(col) and s is not None:
            segs.append(cols[s:c])
            s = None
    return segs


def atlas(rows, skip=frozenset(), table='principal') -> dict[int, dict[str, list[list[int]]]]:
    """{contorno: {letra: colunas}} tirado dos rotulos originais; completa com o outro estilo e `_DRAWN`."""
    out: dict[int, dict] = {1: {}, 7: {}}
    for i, (y, x0, x1, text, *_) in enumerate(TABLES[table]):
        if i in skip:
            continue
        fill, cols, _, _ = _cell(rows, y, x0, x1)
        segs = _segments(cols)
        n, cut = (len(text), None) if len(segs) == len(text) else _PARTIAL.get((table, i), (0, None))
        for k, (ch, seg) in enumerate(zip(text[:n], segs, strict=False)):
            out[fill].setdefault(ch, seg[:cut] if k == n - 1 else seg)
    if table == 'batalha':                              # letra dos botoes: a que falta, e a que tem descendente
        for ch, seg in _button_glyphs(rows).get(3, {}).items():   # (g, p: na caixa o original e achatado, "g" le "8")
            if any(col[8] for col in seg):
                continue                                # nao cabe na faixa de 8 linhas
            if any(col[7] for col in seg):
                out[7][ch] = [col[:8] for col in seg]
                out[1].pop(ch, None)                    # o estilo claro recebe a mesma letra pela conversao
            else:
                out[7].setdefault(ch, [col[:8] for col in seg])
    for fill, other, conv in ((1, 7, _TO_LIGHT), (7, 1, _TO_DARK)):
        g = out[fill]
        if 'C' in g and 'O' not in g:               # O = metade esquerda do C espelhada
            g['O'] = g['C'][:3] + g['C'][1::-1]
        for ch, bitmap in _DRAWN.items():
            g.setdefault(ch, [[BODY[fill] if row[c] == 'x' else 0 for row in bitmap] for c in range(len(bitmap[0]))])
        for ch, seg in out[other].items():
            g.setdefault(ch, [[conv.get(v, BODY[fill]) if v else 0 for v in col] for col in seg])
    return out


def _glyph(g: dict, ch: str, body: int) -> list[list[int]]:
    base, *marks = unicodedata.normalize('NFD', ch)
    cols = [list(c) for c in g[base]]
    for m in marks:
        if base == 'i':
            cols[0][1] = 0                          # o acento entra no lugar do pingo
        mid = (len(cols) - 1) // 2
        for row, dx in _MARKS[m]:
            x = mid + dx
            while x >= len(cols):
                cols.append([0] * 8)
            cols[max(x, 0)][row] = body
    return cols


def render(g: dict, text: str, fill: int, h: int = 8, space: int = 3) -> list[list[int]]:
    """Palavra -> colunas (`h` valores) ja com o contorno: corpo, e `fill` em volta dele (vizinhanca de 8)."""
    cols = [[0] * h]
    for ch in text:
        cols += ([[0] * h] * space) if ch == ' ' else _glyph(g, ch, BODY[fill]) + [[0] * h]
    n = len(cols)
    out = [list(c) for c in cols]
    for x in range(n):
        for y in range(h):
            if not cols[x][y] and any(cols[i][j] for i in range(max(x - 1, 0), min(x + 2, n))
                                      for j in range(max(y - 1, 0), min(y + 2, h))):
                out[x][y] = fill
    return out


def translate(rows, skip=frozenset(), table='principal', g=None) -> list[tuple[str, str]]:
    """Redesenha os rotulos em `rows` (no lugar), menos os de indice em `skip`. Devolve [(original, o que ficou)]."""
    g = g or atlas(rows, skip, table)
    done = []
    for i, (y, x0, x1, text, cands, *crop) in enumerate(TABLES[table]):
        if i in skip:
            done.append((text, text))
            continue
        fill, _, a, b = _cell(rows, y, x0, x1)
        limit = min(crop[0] if crop else W, x1 - a - 1)      # 1 px de folga ate o vizinho
        new = next((r for r in (render(g[fill], c, fill) for c in cands
                                if all(unicodedata.normalize('NFD', ch)[0] in g[fill] for ch in c.replace(' ', '')))
                    if len(r) <= limit), None)
        if new is None:
            done.append((text, text))
            continue
        for x in range(a, max(b, a + len(new))):
            for r in range(8):
                rows[y + r][x] = new[x - a][r] if x - a < len(new) else 0
        done.append((text, next(c for c in cands if len(render(g[fill], c, fill)) == len(new))))
    return done


_BTN_H = 9                                         # faixa do texto de botao: 8 linhas + descendente
_FROM_BOX = {3: {1: 1, 2: 2, 3: 2}}                # letra do estilo de caixa -> estilo de botao (contorno 3)
# ordinais da ordem de turno (arte): (x0, x1, y0, y1) do sufixo a apagar; o anel do "o" entra em (x0 + 1, y0 + 1)
_ORDINALS, _ORD_X, _ORD_EDGE = [(58, 70, 19, 28), (78, 88, 19, 28), (60, 71, 30, 40)], (52, 88), 6
_RING = [(1, 0), (0, 1), (2, 1), (1, 2), (0, 4), (1, 4), (2, 4)]


def _button_glyphs(rows) -> dict[int, dict[str, list[list[int]]]]:
    """{contorno: {letra: colunas de 9}} tirado dos proprios botoes (so de botao sem letra colada na vizinha)."""
    out: dict[int, dict] = {}
    for y, x0, x1, text, _ in TABLES.get('botoes', []):
        bg, edge = _btn_colors(rows, y, x0, x1)
        cols = [[rows[y + r][x] if rows[y + r][x] not in (bg, edge) else 0 for r in range(_BTN_H)] for x in range(x0, x1)]
        segs = _segments(cols)
        if len(segs) == len(text):
            for ch, seg in zip(text, segs, strict=True):
                out.setdefault(edge, {}).setdefault(ch, seg)
    return out


def _btn_colors(rows, y, x0, x1) -> tuple[int, int]:
    """(fundo, contorno) do botao: o fundo e o canto de baixo; o contorno, o valor mais comum fora ele na 1a linha."""
    bg, top = rows[y + _BTN_H - 1][x0], rows[y][x0:x1]
    return bg, max(set(top), key=lambda v: (v != bg, top.count(v)))


def buttons(rows, boxed: dict) -> list[tuple[str, str]]:
    """Botoes de comando e aviso de comando da batalha (tabela "botoes": [y, x0, x1, original, candidatas]),
    texto centrado. Mesma letra dos rotulos, com descendente; o que faltar vem de `boxed` (estilo de caixa)."""
    own = _button_glyphs(rows)
    done = []
    for y, x0, x1, text, cands in TABLES.get('botoes', []):
        bg, edge = _btn_colors(rows, y, x0, x1)
        g = dict(own.get(edge, {}))
        conv = _FROM_BOX.get(edge)
        for ch, seg in boxed.items():
            g.setdefault(ch, [[(conv.get(v, 0) if conv else v) for v in col] + [0] * (_BTN_H - 8) for col in seg])
        fit = [(c, r) for c, r in ((c, render(g, c, edge, _BTN_H, 2)) for c in cands
                                   if all(unicodedata.normalize('NFD', ch)[0] in g for ch in c.replace(' ', '')))
               if len(r) <= x1 - x0]
        if not fit:
            done.append((text, text))
            continue
        cand, new = fit[0]
        for c in range(1, len(new) - 1):                # furo de 1 px no contorno deixaria o fundo aparecer na caixa
            for r in range(_BTN_H):
                if not new[c][r] and new[c - 1][r] and new[c + 1][r]:
                    new[c][r] = edge
        a = x0 + (x1 - x0 - len(new)) // 2
        for x in range(x0, x1):
            for r in range(_BTN_H):
                rows[y + r][x] = (new[x - a][r] if 0 <= x - a < len(new) else 0) or bg
        done.append((text, cand))
    return done


def ordinals(rows) -> None:
    """1st/2nd/3rd -> 1o/2o/3o: apaga o sufixo e desenha o anel sublinhado; o contorno e refeito so nessa area."""
    def body(x, y):
        return _ORD_X[0] <= x < _ORD_X[1] and rows[y][x] not in (0, _ORD_EDGE)
    for x0, x1, y0, y1 in _ORDINALS:
        for y in range(y0, y1):
            for x in range(x0, x1):
                if body(x, y):
                    rows[y][x] = 0
        for dx, dy in _RING:
            rows[y0 + 1 + dy][x0 + 1 + dx] = 1
        ring = {(x0 + 1 + dx, y0 + 1 + dy) for dx, dy in _RING}
        for y in range(y0 - 1, y1 + 1):                 # contorno orfao some; em volta do anel nasce; o do numero fica
            for x in range(x0 - 1, x1 + 1):
                near = {(i, j) for i in (x - 1, x, x + 1) for j in (y - 1, y, y + 1)}
                if rows[y][x] == _ORD_EDGE and not any(body(i, j) for i, j in near):
                    rows[y][x] = 0
                elif not rows[y][x] and near & ring:
                    rows[y][x] = _ORD_EDGE


def patch(dat: bytes, patch_dat_file) -> bytes:
    """`dat` com a folha de rotulos em portugues em toda secao que a carrega; senao devolve o mesmo objeto.
    `patch_dat_file` e o do reinsert (troca a secao e acerta o TOC)."""
    for sec in range(struct.unpack_from('<I', dat, 0)[0] // 16):
        off, size, flags, kind = struct.unpack_from('<4I', dat, sec * 16)      # relido: o TOC muda a cada troca
        if (flags, kind) != (FLAGS, KIND):
            continue
        rows = pixels(imgcodec.untile(imgcodec.decode(dat[off:off + size], 32768), COLS))
        sheet = SHEETS.get(_area_hash(rows))
        if sheet is None:
            continue
        g = atlas(rows, sheet[1], sheet[0])                # antes de qualquer troca: o alfabeto sai do original
        if sheet[0] == 'batalha':
            buttons(rows, g[7])
            ordinals(rows)
        translate(rows, sheet[1], sheet[0], g)
        dat = patch_dat_file(dat, sec, imgcodec.encode(imgcodec.tile(pack(rows), COLS)))
    return dat
