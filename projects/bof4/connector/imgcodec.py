"""Codec das secoes de imagem comprimida do BoF4 (`flags & 0xFFFF == 1`) -- ver table_schema.md, secao 9.

LZ77 + Huffman no molde do LHA -lh1-, com bits LSB-first dentro de cada byte:
- literal/comprimento: Huffman dinamico do LHA (dhuf.c) com 321 simbolos -- 0-255 literal,
  256-320 copia de 3 a 67 bytes;
- depois de um comprimento vem a posicao: prefixo estatico (6 bits altos) + 6 bits baixos LSB-first;
  distancia = posicao + 1, janela de 4096 bytes pre-preenchida com zeros;
- fim: simbolo 256 + posicao 4095, completado com zeros ate fechar o byte.

Limite: quando a raiz chega a 0x8000 (32768 simbolos) o jogo reconstroi a arvore com um desempate proprio,
ainda nao decodificado -- `decode`/`encode` levantam NotImplementedError nesse ponto.

A imagem descomprimida sao blocos de 64x32 bytes (32x32 palavras da VRAM do PS1), em ordem de leitura.
"""
N_SYM = 321
MIN_LEN, MAX_LEN = 3, 67
MAX_DIST = 4095         # 4096 e a posicao do marcador de fim
TILE_W, TILE_H = 64, 32
REBUILD = 0x8000        # frequencia da raiz em que o jogo reconstroi a arvore
_CHAIN = 64             # ponytail: busca gulosa em cadeia curta; comprime um pouco pior que o original


def _pos_codes() -> list[str]:
    """Prefixo de cada um dos 64 valores altos de posicao (indice = valor).

    Tamanhos do -lh1- (1 de 3 bits, 3 de 4, 8 de 5, 12 de 6, 24 de 7, 16 de 8), codigo canonico
    complementado; dentro de cada tamanho, a ordem e a do codigo lido de tras para frente, decrescente.
    """
    codes, code, prev = [], 0, 3
    for count, bits in ((1, 3), (3, 4), (8, 5), (12, 6), (24, 7), (16, 8)):
        code <<= bits - prev
        prev = bits
        for _ in range(count):
            codes.append(format(~code & ((1 << bits) - 1), f'0{bits}b'))
            code += 1
    return sorted(codes, key=lambda c: (len(c), -int(c[::-1], 2)))


_POS = _pos_codes()
_POS_DEC = {c: hi for hi, c in enumerate(_POS)}


class _DHuf:
    """Huffman dinamico do LHA (dhuf.c: start_c_dyn / swap_inc / update_c), sem a reconstrucao."""

    def __init__(s, n):
        s.n = n
        ts = n * 2
        s.child, s.parent, s.block, s.edge, s.freq = ([0] * ts for _ in range(5))
        s.stock = list(range(ts))
        s.s_node = [0] * n
        j = ts - 2
        for i in range(n):
            s.freq[j] = 1
            s.child[j] = ~i
            s.s_node[i] = j
            s.block[j] = 1
            j -= 1
        s.avail = 2
        s.edge[1] = n - 1
        i = ts - 2
        while j >= 0:
            f = s.freq[j] = s.freq[i] + s.freq[i - 1]
            s.child[j] = i
            s.parent[i] = s.parent[i - 1] = j
            if f == s.freq[j + 1]:
                s.block[j] = s.block[j + 1]
            else:
                s.block[j] = s.stock[s.avail]
                s.avail += 1
            s.edge[s.block[j]] = j
            i -= 2
            j -= 1

    def _swap_inc(s, p):
        child, parent, block, edge, stock, s_node, freq = (
            s.child, s.parent, s.block, s.edge, s.stock, s.s_node, s.freq)
        b = block[p]
        q = edge[b]
        if q != p:
            r, t = child[p], child[q]
            child[p], child[q] = t, r
            if r >= 0:
                parent[r] = parent[r - 1] = q
            else:
                s_node[~r] = q
            if t >= 0:
                parent[t] = parent[t - 1] = p
            else:
                s_node[~t] = p
            p = q
        elif b != block[p + 1]:
            freq[p] += 1
            if freq[p] == freq[p - 1]:
                s.avail -= 1
                stock[s.avail] = b
                block[p] = block[p - 1]
            return parent[p]
        edge[b] += 1
        freq[p] += 1
        if freq[p] == freq[p - 1]:
            block[p] = block[p - 1]
        else:
            block[p] = stock[s.avail]
            s.avail += 1
            edge[block[p]] = p
        return parent[p]

    def update(s, sym):
        if s.freq[0] == REBUILD:
            # ponytail: o jogo reconstroi a arvore aqui e a regra de desempate dele nao e a do LHA (nao
            # decodificada). Vale para fluxos de ate 32768 simbolos; implementar quando uma imagem maior precisar.
            raise NotImplementedError('imagem comprimida passa de 32768 simbolos (reconstrucao da arvore)')
        s.freq[0] += 1
        q = s.s_node[sym]
        while q:
            q = s._swap_inc(q)

    def code(s, sym) -> str:
        q, bits = s.s_node[sym], []
        while q:
            p = s.parent[q]
            bits.append('0' if q == s.child[p] else '1')
            q = p
        return ''.join(reversed(bits))


def decode(data: bytes, size: int) -> bytes:
    """Descomprime `data` ate `size` bytes (`(flags >> 16) * 256` no TOC)."""
    bits = int.from_bytes(data, 'little')
    pos = 0
    tree = _DHuf(N_SYM)
    child = tree.child
    out = bytearray()
    while len(out) < size:
        c = child[0]
        while c > 0:
            c = child[c - (bits >> pos & 1)]
            pos += 1
        c = ~c
        tree.update(c)
        if c < 256:
            out.append(c)
            continue
        code = ''
        while code not in _POS_DEC:
            if len(code) == 8:
                raise ValueError('codigo de posicao invalido')
            code += '01'[bits >> pos & 1]
            pos += 1
        dist = (_POS_DEC[code] << 6 | bits >> pos & 63) + 1
        pos += 6
        for _ in range(c - 256 + MIN_LEN):
            out.append(out[-dist] if dist <= len(out) else 0)
    c = child[0]
    while c > 0:
        c = child[c - (bits >> pos & 1)]
        pos += 1
    if ~c != 256 or bits >> pos != 0x3F00 or pos + 14 > len(data) * 8:
        raise ValueError('fluxo comprimido sem o marcador de fim')
    return bytes(out)


def encode(raw: bytes) -> bytes:
    """Comprime `raw` num fluxo que `decode` (e o jogo) abre. Nao reproduz o parse do original."""
    tree = _DHuf(N_SYM)
    out = []
    seen: dict[bytes, list[int]] = {}

    def put(sym):
        out.append(tree.code(sym))
        tree.update(sym)

    def put_pos(p):
        out.append(_POS[p >> 6] + format(p & 63, '06b')[::-1])

    i, n = 0, len(raw)
    while i < n:
        best, dist = 0, 0
        limit = min(MAX_LEN, n - i)
        for j in reversed(seen.get(raw[i:i + MIN_LEN], ())[-_CHAIN:]):
            if i - j > MAX_DIST:
                break
            m = MIN_LEN
            while m < limit and raw[j + m] == raw[i + m]:
                m += 1
            if m > best:
                best, dist = m, i - j
        if best >= MIN_LEN:
            put(256 + best - MIN_LEN)
            put_pos(dist - 1)
        else:
            put(raw[i])
            best = 1
        for k in range(i, min(i + best, n - MIN_LEN + 1)):
            seen.setdefault(raw[k:k + MIN_LEN], []).append(k)
        i += best
    put(256)
    put_pos(4095)
    stream = ''.join(out)
    return int(stream[::-1], 2).to_bytes(-(-len(stream) // 8), 'little')


def untile(raw: bytes, cols: int) -> bytes:
    """Blocos 64x32 -> imagem linear de `cols * 64` bytes por linha (`cols` = `extra >> 8 & 0xFF`)."""
    block = TILE_W * TILE_H
    rows = []
    for band in range(0, len(raw), block * cols):
        for y in range(TILE_H):
            rows += [raw[band + t * block + y * TILE_W:][:TILE_W] for t in range(cols)]
    return b''.join(rows)


def tile(linear: bytes, cols: int) -> bytes:
    """Inversa de `untile`."""
    width = cols * TILE_W
    out = []
    for band in range(0, len(linear), width * TILE_H):
        for t in range(cols):
            out += [linear[band + y * width + t * TILE_W:][:TILE_W] for y in range(TILE_H)]
    return b''.join(out)


if __name__ == '__main__':
    import os
    sample = bytes(1000) + os.urandom(300) + b'abcabcabc' * 200 + bytes(range(256)) * 20
    assert decode(encode(sample), len(sample)) == sample
    try:
        encode(os.urandom(REBUILD + 8))
        raise AssertionError('devia recusar fluxo que cruza a reconstrucao')
    except NotImplementedError:
        pass
    assert len(set(_POS)) == 64 and _POS[:4] == ['111', '1011', '1101', '1100'] and _POS[63] == '00000000'
    grid = bytes(range(256)) * 64            # 16384 bytes = 8 blocos
    assert tile(untile(grid, 4), 4) == grid and untile(grid, 4) != grid
    print('ok')
