#!/usr/bin/env python3
"""exe_text.py — textos de interface (menu, dica, confirmacao) do game.exe do Prelude.

O executavel (PE x86, base 0x400000, sem tabela de realocacao) guarda os textos de sistema em ingles como strings
ASCII terminadas em NUL dentro de .rdata, ao lado do japones em UTF-8. Cada texto e achado por ponteiros absolutos
de 4 bytes (em tabelas de .data ou em `push`/`mov` do codigo). Quase nao ha folga entre as strings, entao o
portugues NAO e gravado no lugar: vai para uma secao nova (.ptbr) no fim do arquivo e cada ponteiro e trocado pelo
endereco novo. Sem traducao nenhuma, a saida so ganha a secao e os ponteiros continuam apontando para o original.

Ordem do pipeline: exe original -> font.py (acentos) -> exe_text.py. Este modulo parte do exe que sai do font.py.

Uso:
  python exe_text.py extract <exe> <saida.csv>              -> offset,text_en,refs,text_pt (text_pt vazio)
  python exe_text.py apply <exe> <traducoes.csv> <saida.exe>
  python exe_text.py check <exe> <traducoes.csv>            -> ida e volta da largura (exit 1 se algum passar do EN)
"""
import csv
import re
import struct
import sys
from pathlib import Path

from font import fit, read_table

SEC_NAME = b".ptbr\0\0\0"
SEC_FLAGS = 0xC0000040  # leitura+escrita, dados inicializados: o jogo pode formatar em cima do texto
# faixa de .rdata onde ficam os textos de tela (antes dela: shaders/RTTI; depois: nomes de thread e de tecla)
UI_START, UI_END = 0x50E000, 0x529000
# palavras soltas de exibicao. Prova de que nao sao chave de comparacao (disassembly do game.exe): nenhuma
# referencia vem de `cmp`/strcmp; ou estao em tabelas .rdata paralelas por idioma (linhas ja/zh/ko/en lado a lado),
# ou em vetores montados na pilha na ordem do enum (elementos, tipos de habilidade), ou em seletores por idioma
# (`cmp ecx, 0xa` escolhe entre 'None' / 無 / 없음, 'Normal' / 普通 / 기본, 'Fortress' / 城塞 / 요새) cujo ponteiro vai
# direto para a rotina de desenho. Identificador interno (act*, *Task, evSet*, semantica de shader) fica de fora.
ROTULOS = {
    "Magecraft", "Thaumaturgy", "Item", "Wait", "Yes", "Return", "Advance", "Equip", "Inventory", "Save", "Load",
    "Suspend", "Rewind", "Retry", "Settings", "Tutorial", "Glossary", "Resume", "Bonus", "Credits", "<Locked>",
    "Gallery",
    "Items", "Equipment", "Costume", "Collection", "None", "Normal", "Move", "Heal", "Window", "Rewards", "Fortress",
    "Water", "Fire", "Earth", "Wind", "Dark", "Light", "Neutral",
    "<Physical>", "<Heal>", "<Magecraft>", "<Special>", "<Support>", "<Magical>",
    "<Equipment>", "<Item>", "<Costume>",
    "<People>", "<Tutorial>", "<Location>", "<Unregistered>", "<Overview>",
    "Battle", "Training", "Event", "Base",
    "Wallpaper", "Reminiscing", "Abh-kamu", "Mother", "Lamentation", "Congratulations", "Defeat", "Awakening",
}


class Pe:
    """So o que o conector precisa de um PE x86: secoes e conversao raw <-> VA."""

    def __init__(self, exe: bytes):
        self.pe = struct.unpack_from("<I", exe, 0x3C)[0]
        if exe[self.pe:self.pe + 4] != b"PE\0\0" or struct.unpack_from("<H", exe, self.pe + 24)[0] != 0x10B:
            raise ValueError("nao e um PE de 32 bits")
        self.nsec = struct.unpack_from("<H", exe, self.pe + 6)[0]
        self.opt = self.pe + 24
        self.base = struct.unpack_from("<I", exe, self.opt + 28)[0]
        self.sec_align, self.file_align = struct.unpack_from("<II", exe, self.opt + 32)
        self.tab = self.opt + struct.unpack_from("<H", exe, self.pe + 20)[0]
        self.secs = [struct.unpack_from("<8sIIII", exe, self.tab + 40 * i) for i in range(self.nsec)]

    def va(self, raw: int) -> int:
        for _, _vsize, va, rsize, roff in self.secs:
            if roff <= raw < roff + rsize:
                return self.base + va + (raw - roff)
        raise ValueError(f"offset {raw:#x} fora das secoes")

    def raw(self, va: int) -> int:
        for _, _vsize, sva, rsize, roff in self.secs:
            if self.base + sva <= va < self.base + sva + rsize:
                return roff + (va - self.base - sva)
        raise ValueError(f"VA {va:#x} fora das secoes")


def _refs_to(exe: bytes, pe: Pe, lo: int, hi: int) -> dict[int, list[int]]:
    """VA -> posicoes (offset de arquivo) onde esse VA aparece como u32, para VA em [lo, hi)."""
    out: dict[int, list[int]] = {}
    top = {(lo >> 16) & 0xFF, ((hi - 1) >> 16) & 0xFF}
    rng = range(min(top), max(top) + 1)
    code = next(s for s in pe.secs if s[0].startswith(b".text"))
    # so codigo e dados do programa: .rsrc (recursos comprimidos), cabecalho e secoes alheias nao guardam ponteiros
    vale = [(s[4], s[4] + s[3]) for s in pe.secs if s[0].split(bytes(1))[0] in (b".text", b".rdata", b".data")]
    for i in range(len(exe) - 3):
        if exe[i + 3] == 0 and exe[i + 2] in rng and any(a <= i < b for a, b in vale):
            # em tabela de dados o ponteiro e alinhado a 4; so no codigo (imediato de instrucao) pode nao ser
            if i % 4 and not code[4] <= i < code[4] + code[3]:
                continue
            v = struct.unpack_from("<I", exe, i)[0]
            if lo <= v < hi:
                out.setdefault(v, []).append(i)
    return out


def _operandos(exe: bytes, pe: Pe) -> set[int]:
    """Posicoes de arquivo de imediatos/deslocamentos de 4 bytes de verdade, pelo disassembly de .text.

    Varrer bytes acha 'ponteiros' falsos: o opcode de um `call rel32` (E8) ou um `nop` junto dos 3 primeiros
    bytes da instrucao seguinte formam um u32 que cai por acaso na faixa dos textos (3 casos no game.exe).
    So conta como ponteiro o u32 que o disassembler decodifica como operando de uma instrucao.
    """
    try:
        import capstone
    except ImportError as e:
        raise SystemExit("exe_text precisa do capstone para validar os ponteiros do codigo: pip install capstone") from e
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.detail, md.skipdata = True, True
    _, _, _, rsize, roff = next(s for s in pe.secs if s[0].startswith(b".text"))
    ops = set()
    for ins in md.disasm(exe[roff:roff + rsize], 0):
        if ins.mnemonic == ".byte":
            continue
        for off, size in ((ins.imm_offset, ins.imm_size), (ins.disp_offset, ins.disp_size)):
            if size == 4 and off:
                ops.add(roff + ins.address + off)
    return ops


def _tela(s: str, via_tabela: bool) -> bool:
    if re.search(r"[\\/:]|\.\w{2,4}$|_|error|Error|::|0x", s):
        return False
    if re.fullmatch(r"[a-z]+[A-Z]\w*|[A-Za-z]+\d+\w*", s):
        return False
    if " " in s or s.startswith("{") or "{c" in s or "%" in s:
        return True
    return s in ROTULOS


def extract(exe: bytes) -> list[dict]:
    """Textos de tela com seus ponteiros: [{offset, text, refs}] por offset de arquivo."""
    pe = Pe(exe)
    lo, hi = pe.va(UI_START), pe.va(UI_END - 1) + 1
    refs = _refs_to(exe, pe, lo, hi)
    code = next(s for s in pe.secs if s[0].startswith(b".text"))
    ops = _operandos(exe, pe)
    refs = {v: [r for r in rs if r in ops or not code[4] <= r < code[4] + code[3]] for v, rs in refs.items()}
    data_ini = min((roff for n, _, _, _, roff in pe.secs if n.startswith(b".data")), default=0)
    out = []
    for m in re.finditer(rb"(?<=\x00)[\x09\x0a\x20-\x7e]{3,}\x00", exe[UI_START:UI_END]):
        off = UI_START + m.start()
        rf = refs.get(pe.va(off))
        text = m.group(0)[:-1].decode("ascii")
        if rf and re.search(r"[A-Za-z]{3}", text) and _tela(text, any(r >= data_ini for r in rf)):
            out.append({"offset": off, "text": text, "refs": rf})
    return out


def interior_refs(exe: bytes, items: list[dict]) -> list[tuple[int, int]]:
    """Ponteiros que caem no MEIO de um texto (sufixo compartilhado): trocar o texto quebraria esses."""
    pe = Pe(exe)
    spans = [(it["offset"], it["offset"] + len(it["text"])) for it in items]
    lo, hi = pe.va(min(a for a, _ in spans)), pe.va(max(b for _, b in spans))
    refs = _refs_to(exe, pe, lo, hi + 1)
    code, ops = next(s for s in pe.secs if s[0].startswith(b".text")), _operandos(exe, pe)
    refs = {v: [r for r in rs if r in ops or not code[4] <= r < code[4] + code[3]] for v, rs in refs.items()}
    bad = []
    for a, b in spans:
        for v in range(pe.va(a) + 1, pe.va(b) + 1):
            bad += [(a, p) for p in refs.get(v, [])]
    return bad


def apply(exe: bytes, pt: dict[int, str]) -> bytes:
    """Grava os textos pt (offset do original -> portugues) numa secao nova e troca os ponteiros."""
    pe = Pe(exe)
    items = {it["offset"]: it for it in extract(exe)}
    unknown = set(pt) - set(items)
    if unknown:
        raise ValueError(f"offsets que nao sao texto de tela: {sorted(hex(o) for o in unknown)[:5]}")
    last = max(pe.secs, key=lambda s: s[2])
    new_va = -(-(last[2] + max(last[1], last[3])) // pe.sec_align) * pe.sec_align
    blob, where = bytearray(), {}
    for off, text in pt.items():
        where[off] = len(blob)
        blob += fit(text).encode("utf-8") + b"\0"
    rsize = -(-len(blob) // pe.file_align) * pe.file_align
    roff = -(-len(exe) // pe.file_align) * pe.file_align
    out = bytearray(exe) + bytes(roff - len(exe)) + bytes(blob) + bytes(rsize - len(blob))
    for off, pos in where.items():
        new = pe.base + new_va + pos
        for r in items[off]["refs"]:
            struct.pack_into("<I", out, r, new)
    if pe.tab + 40 * (pe.nsec + 1) > min(s[4] for s in pe.secs):
        raise ValueError("sem espaco no cabecalho para mais uma secao")
    struct.pack_into("<8sIIIIIIHHI", out, pe.tab + 40 * pe.nsec, SEC_NAME, len(blob), new_va, rsize, roff, 0, 0, 0, 0,
                     SEC_FLAGS)
    struct.pack_into("<H", out, pe.pe + 6, pe.nsec + 1)
    size_img = struct.unpack_from("<I", out, pe.opt + 56)[0]
    struct.pack_into("<I", out, pe.opt + 56, max(size_img, new_va + -(-len(blob) // pe.sec_align) * pe.sec_align))
    return bytes(out)


def read_back(exe: bytes, items: list[dict]) -> dict[int, str]:
    """Texto que o jogo le hoje em cada offset do original, seguindo o primeiro ponteiro de cada um."""
    pe = Pe(exe)
    out = {}
    for it in items:
        p = pe.raw(struct.unpack_from("<I", exe, it["refs"][0])[0])
        out[it["offset"]] = exe[p:exe.index(b"\0", p)].decode("utf-8")
    return out


def _largura(avancos: dict[int, int], texto: str) -> int:
    """Largura em pixels da linha mais larga: soma dos avancos da fonte, sem os tokens {..}; sem glifo = 14."""
    return max(sum(avancos.get(ord(c), 14) for c in re.sub(r"\{[^}]*\}", "", linha)) for linha in texto.split("\n"))


def excedentes(exe: bytes, pt: dict[int, str]) -> list[tuple[int, int, int]]:
    """Ida e volta da largura: aplica pt, le de volta o que o jogo leria e mede com a fonte do proprio exe.

    Devolve (offset, largura_en, largura_pt) dos textos cuja linha mais larga passa da do ingles: o ingles coube
    na caixa do jogo, entao a linha mais larga dele e o teto seguro para o portugues.
    """
    avancos = {g[0]: g[7] for g in read_table(exe)[1]}
    itens = extract(exe)
    lido = read_back(apply(exe, pt), itens)
    ing = {it["offset"]: it["text"] for it in itens}
    out = []
    for off in pt:
        e, p = _largura(avancos, ing[off]), _largura(avancos, lido[off])
        if p > e:
            out.append((off, e, p))
    return out


def sem_glifo(exe: bytes, pt: dict[int, str]) -> list[tuple[int, str]]:
    """Textos com caractere que a fonte do jogo nao desenha (o glifo some da tela): (offset, caracteres)."""
    tem = {g[0] for g in read_table(exe)[1]}
    out = []
    for off, texto in pt.items():
        falta = sorted({c for c in re.sub(r"\{[^}]*\}", "", fit(texto)) if c != "\n" and ord(c) not in tem})
        if falta:
            out.append((off, "".join(falta)))
    return out


def main(argv: list[str]) -> int:
    if len(argv) == 4 and argv[1] == "extract":
        exe = Path(argv[2]).read_bytes()
        items = extract(exe)
        with open(argv[3], "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["offset", "text_en", "refs", "text_pt"])
            for it in items:
                w.writerow([f"{it['offset']:#x}", it["text"], len(it["refs"]), ""])
        print(f"{len(items)} textos; ponteiros no meio de texto: {len(interior_refs(exe, items))}")
        return 0
    if len(argv) == 5 and argv[1] == "apply":
        exe = Path(argv[2]).read_bytes()
        with open(argv[3], encoding="utf-8-sig", newline="") as f:
            pt = {int(r["offset"], 16): r["text_pt"] for r in csv.DictReader(f) if r["text_pt"]}
        Path(argv[4]).write_bytes(apply(exe, pt))
        print(f"{len(pt)} textos aplicados")
        return 0
    if len(argv) == 4 and argv[1] == "check":
        exe = Path(argv[2]).read_bytes()
        with open(argv[3], encoding="utf-8-sig", newline="") as f:
            linhas = list(csv.DictReader(f))
        pt = {int(r["offset"], 16): r["text_pt"] for r in linhas if r["text_pt"]}
        ing = {int(r["offset"], 16): r["text_en"] for r in linhas}
        ruins = excedentes(exe, pt)
        faltam = sem_glifo(exe, pt)
        for off, cs in faltam:
            print(f"{off:#x} SEM GLIFO {cs!r} {pt[off][:60]!r}")
        for off, e, p in ruins:
            print(f"{off:#x} EN {e:4} PT {p:4} (+{(p - e) * 100 // e}%) {pt[off][:60]!r}  <- {ing[off][:40]!r}")
        print(f"{len(ruins)} de {len(pt)} textos passam da largura do ingles; {len(faltam)} com caractere sem glifo")
        return 1 if ruins or faltam else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
