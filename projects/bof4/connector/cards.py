"""Cartoes de titulo de capitulo ("I: ...") -- imagem, nao texto: ver table_schema.md, secao 9.

Uma secao de 256x256 px, 4bpp, comprimida (imgcodec). Cada titulo e uma faixa de 512x32 px
cortada em duas metades empilhadas (esquerda em cima, direita embaixo), centrada em x=256.
Indices da paleta (secao 11): 0 = transparente, 9 = corpo da letra, 8-4 = borda suavizada, 1/3 = contorno.
"""
import struct
from pathlib import Path

import imgcodec

SECTIONS = {'AREAE023.DAT': 10, 'AREAE029.DAT': 13, 'AREAM013.DAT': 13, 'AREAM052.DAT': 7}  # mesma imagem nos 4
FLAGS, COLS = 0x00800001, 2                 # 32768 bytes descomprimidos, 2 blocos por linha
TITLES = ('I: Despertar', 'II: Os Eternos', 'III: Correntes', 'IV: Aquilo Que Passa')
FONT = Path('C:/Windows/Fonts/timesbi.ttf')  # serifada negrita italica, proxima da original; nao versionada
SIZE, TRACK, TOP = 32, 4, 3                  # corpo, espaco extra entre letras e linha do topo das maiusculas
W, H = 512, 32


def _strip(text: str) -> list[bytearray]:
    """Titulo -> 32 linhas de 512 indices de paleta."""
    from PIL import (  # import tardio: so o reinsert dos arquivos do cartao precisa
        Image,
        ImageDraw,
        ImageFont,
    )
    if not FONT.is_file():
        raise SystemExit(f'ERRO: fonte {FONT} nao encontrada (cartao de capitulo)')
    font = ImageFont.truetype(str(FONT), SIZE)
    width = sum(font.getlength(c) + TRACK for c in text) - TRACK
    if width > W - 8:
        raise ValueError(f'titulo nao cabe em {W} px: {text!r}')
    img = Image.new('L', (W, H))
    draw = ImageDraw.Draw(img)
    x = (W - width) / 2
    top = TOP - font.getbbox('I')[1]
    for c in text:
        draw.text((x, top), c, 255, font)
        x += font.getlength(c) + TRACK
    ink = img.load()
    solid = {(x, y) for y in range(H) for x in range(W) if ink[x, y] >= 32}
    rows = [bytearray(W) for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if (x, y) in solid:
                rows[y][x] = 4 + ink[x, y] * 5 // 255
            elif solid & {(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)}:
                rows[y][x] = 1
            elif solid & {(x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1), (x - 1, y - 1)}:
                rows[y][x] = 3
    return rows


def render() -> bytes:
    """Os quatro titulos como imagem linear 4bpp de 256x256 (128 bytes por linha, nibble baixo primeiro)."""
    out = bytearray()
    for text in TITLES:
        rows = _strip(text)
        for half in (0, W // 2):
            for row in rows:
                px = row[half:half + W // 2]
                out += bytes(px[i] | px[i + 1] << 4 for i in range(0, W // 2, 2))
    return bytes(out)


def patch(name: str, dat: bytes) -> bytes:
    """`dat` com o cartao em portugues, se `name` for o arquivo que o carrega; senao devolve intacto."""
    section = SECTIONS.get(name)
    if section is None:
        return dat
    from reinsert import patch_dat_file  # import tardio: reinsert importa este modulo
    flags, extra = struct.unpack_from('<2I', dat, section * 16 + 8)
    if (flags, extra >> 8 & 0xFF) != (FLAGS, COLS):
        raise ValueError(f'{name}: secao {section} nao e o cartao de capitulo esperado')
    return patch_dat_file(dat, section, imgcodec.encode(imgcodec.tile(render(), COLS)))


if __name__ == '__main__':
    lin = render()
    assert len(lin) == 256 * 128 and any(lin[:32 * 128]) and any(lin[32 * 128:64 * 128])
    raw = imgcodec.tile(lin, COLS)
    assert imgcodec.decode(imgcodec.encode(raw), len(raw)) == raw
    print('ok')
