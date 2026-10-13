"""Acentos pt-BR na fonte de dialogo do BoF4 (INIT.DAT, secao 9) -- ver table_schema.md, secao 4.

O atlas em ingles tem 104 glifos de 24x24 px, 4bpp (codigos 0x20-0x87). Codigo acima disso nao tem
largura no BOF4.exe: o jogo desenha o glifo e NAO avanca o cursor. Isso vira acento sobreposto:
'á' = [A0] (acento, sem avanco) + 'a'. O atlas e estendido ate 0xAB com os 12 acentos abaixo.

Excecao: 'í'. Acento sobreposto so soma tinta, o pingo do 'i' nao some, e o resultado nao parece letra
(teste in-game run2). O 'í' e um glifo proprio (sem pingo, com agudo, 1 byte) na vaga de '>' (0x3E), que
nem o jogo nem a traducao usam. Medido in-game (sonda 3, prints/run3/ascento2.png): cada codigo tem uma
janela de colunas da celula e um avanco; em 0x3E o jogo desenha as colunas 0-11 e avanca ~11 px. O 'i'
original (tinta nas colunas 9-14) entra deslocado 6 px para a esquerda, centrado na janela. O 'í' ocupa
~11 px contra 8 do 'i': nenhuma vaga livre avanca 8 (';' 6-17 e '<' 12-23 tambem ~11, ']' 14, '[' 18,
'|' 24). ';' ficou de fora porque a traducao usa ponto e virgula.
"""
import struct
import unicodedata

W = H = 24
GLYPH = W * H // 2
SECTION = 9             # INIT.DAT: fonte de 24 px
STOCK = 104             # glifos do atlas original
FIRST = 0xA0            # 0x88-0x9F ficam em branco (0x8B/0x90/0x93 ja sao bytes de controle no jogo)

_ACUTE = ('...11', '..11.', '.11..', '11...')
_GRAVE = tuple(r[::-1] for r in _ACUTE)
_CIRC = ('..111..', '.11.11.', '11...11')
_TILDE = ('.111...1', '11.11.11', '1...111.')
_CEDIL = ('.11.', '..11', '111.')
# O pingo do 'i' nao some (acento so soma tinta): tinta cheia nas colunas 4-5, linhas 4-6 da celula do
# acento. O traco tem 3 px e pousa em cima dele (linha 3 = colunas 4-6), para o pingo virar o pe do agudo.
_ACUTE_I = ('...111', '..111.', '.111..', '111...', '..1...')

# (marca Unicode, classe da letra-base) -> (desenho, linha do topo, coluna do centro).
# Colunas medidas in-game (print_ascentp.png): a celula do acento comeca ~2 px antes da tinta da letra.
_LOW, _UP, _BELOW = 4, 0, 21
_MARKS = [
    ('́', 'low', _ACUTE, _LOW, 6), ('̀', 'low', _GRAVE, _LOW, 6),
    ('̂', 'low', _CIRC, _LOW + 1, 6), ('̃', 'low', _TILDE, _LOW + 1, 6),
    ('̧', 'low', _CEDIL, _BELOW, 6), ('́', 'i', _ACUTE_I, 0, 7),
    ('́', 'up', _ACUTE[:3], _UP, 9), ('̀', 'up', _GRAVE[:3], _UP, 8),
    ('̂', 'up', _CIRC, _UP, 8), ('̃', 'up', _TILDE, _UP, 8),
    ('̧', 'up', _CEDIL, _BELOW, 8), ('́', 'I', _ACUTE[:3], _UP, 5),
]
_CLASS = {**dict.fromkeys('aeouc', 'low'), **dict.fromkeys('AEOUC', 'up'), 'i': 'i', 'I': 'I'}
_CODE = {(mark, cls): FIRST + n for n, (mark, cls, *_) in enumerate(_MARKS)}
I_ACUTE = 0x3E          # vaga de '>'
_I_SHIFT = 6            # colunas (par: 2 pixels por byte) que o 'i' original anda para a esquerda
_I_ACUTE_ART = ('....111', '...111.', '..111..', '.111...')     # linhas 3-6, colunas 3-9


def overlay(text: str) -> str:
    """'á' -> '[A0]a'. Letra acentuada sem acento desenhado (ñ, ü, î...) passa intacta."""
    out = []
    for ch in text:
        if ch == 'í':
            out.append(f'[{I_ACUTE:02X}]')
            continue
        d = unicodedata.normalize('NFD', ch)
        code = _CODE.get((d[1], _CLASS.get(d[0]))) if len(d) == 2 else None
        out.append(f'[{code:02X}]{d[0]}' if code else ch)
    return ''.join(out)


def _glyph(art, top, center) -> bytes:
    out = bytearray(GLYPH)
    left = center - len(art[0]) // 2
    for y, row in enumerate(art):
        for x, c in enumerate(row):
            if c == '1':
                p = (top + y) * W + left + x
                out[p >> 1] |= 1 << (4 * (p & 1))       # nibble baixo primeiro; 1 = tinta cheia
    return bytes(out)


def _i_acute(stock_i: bytes) -> bytes:
    """'i' original sem o pingo (linhas 0-8) mais o agudo, tudo _I_SHIFT colunas a esquerda."""
    out = bytearray(_glyph(_I_ACUTE_ART, 3, 12 - _I_SHIFT))
    row, cut = W // 2, _I_SHIFT // 2
    for y in range(9, H):
        out[y * row:(y + 1) * row] = stock_i[y * row + cut:(y + 1) * row] + bytes(cut)
    return bytes(out)


def extend_atlas(init_dat: bytes) -> bytes:
    """INIT.DAT com a secao 9 estendida ate 0xAB. Idempotente: parte sempre dos 104 glifos originais."""
    from reinsert import patch_dat_file  # import tardio: reinsert importa este modulo
    off, _size = struct.unpack_from('<2I', init_dat, SECTION * 16)
    atlas = bytearray(init_dat[off:off + STOCK * GLYPH] + bytes((FIRST - 0x20 - STOCK) * GLYPH))
    slot = (I_ACUTE - 0x20) * GLYPH
    atlas[slot:slot + GLYPH] = _i_acute(bytes(atlas[(0x69 - 0x20) * GLYPH:(0x69 - 0x20 + 1) * GLYPH]))
    atlas = bytes(atlas)
    return patch_dat_file(init_dat, SECTION, atlas + b''.join(_glyph(*m[2:]) for m in _MARKS))


if __name__ == '__main__':
    assert overlay('ação') == 'a[A4]c[A3]ao', overlay('ação')
    assert overlay('É í Í ñ x') == '[A6]E [3E] [AB]I ñ x', overlay('É í Í ñ x')
    i = bytearray(GLYPH)
    for p in (7 * W + 11, 12 * W + 10, 20 * W + 14):        # pingo, haste, serifa
        i[p >> 1] |= 15 << (4 * (p & 1))
    g = _i_acute(bytes(i))
    ink = {(p % W, p // W) for p in range(W * H) if (g[p >> 1] >> (4 * (p & 1))) & 15}
    assert {(4, 12), (8, 20), (6, 4)} <= ink and (5, 7) not in ink, sorted(ink)
    assert 0 <= min(x for x, _ in ink) and max(x for x, _ in ink) <= 11, sorted(ink)     # janela medida
    assert len(_CODE) == 12 and max(_CODE.values()) == 0xAB
    g = _glyph(_ACUTE, _LOW, 6)
    assert len(g) == GLYPH and not any(g[:_LOW * W // 2]) and any(g[_LOW * W // 2:(_LOW + 4) * W // 2])
    print('ok')
