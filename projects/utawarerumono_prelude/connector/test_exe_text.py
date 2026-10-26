"""Testes sinteticos do exe_text.py: um PE x86 minimo montado em memoria (sem arquivo de jogo)."""
import struct

import exe_text as E
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

BASE = 0x400000
HDR, TXT, RDA, DAT = 0x400, 0x400, 0x600, 0x800  # offsets de arquivo; cada secao tem 0x200 bytes
VA = {TXT: 0x1000, RDA: 0x2000, DAT: 0x3000}


@pytest.fixture(autouse=True)
def faixa_pequena(monkeypatch):
    monkeypatch.setattr(E, "UI_START", RDA)
    monkeypatch.setattr(E, "UI_END", RDA + 0x200)


def monta_pe(textos: list[str]) -> tuple[bytes, list[int]]:
    """PE com os textos em .rdata, uma tabela de ponteiros em .data e um `push imm32` em .text por texto."""
    exe = bytearray(DAT + 0x200)
    exe[0:2] = b"MZ"
    struct.pack_into("<I", exe, 0x3C, 0x80)
    pe = 0x80
    exe[pe:pe + 4] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", exe, pe + 4, 0x14C, 3, 0, 0, 0, 0xE0, 0x102)
    opt = pe + 24
    struct.pack_into("<H", exe, opt, 0x10B)
    struct.pack_into("<I", exe, opt + 28, BASE)
    struct.pack_into("<II", exe, opt + 32, 0x1000, 0x200)
    struct.pack_into("<I", exe, opt + 56, 0x4000)
    tab = opt + 0xE0
    for i, (nome, raw) in enumerate([(b".text", TXT), (b".rdata", RDA), (b".data", DAT)]):
        struct.pack_into("<8sIIIIIIHHI", exe, tab + 40 * i, nome, 0x200, VA[raw], 0x200, raw, 0, 0, 0, 0, 0x40000040)
    pos, offs = RDA + 1, []  # um NUL antes do primeiro texto
    for k, t in enumerate(textos):
        offs.append(pos)
        exe[pos:pos + len(t) + 1] = t.encode() + b"\0"
        va = BASE + VA[RDA] + (pos - RDA)
        struct.pack_into("<I", exe, DAT + 4 * k, va)  # tabela alinhada em .data
        exe[TXT + 5 * k] = 0x68  # push imm32
        struct.pack_into("<I", exe, TXT + 5 * k + 1, va)
        pos += len(t) + 1
    return bytes(exe), offs


def primeira_diferenca(a: bytes, b: bytes) -> str:
    """Relatorio de diff binario: offset da primeira diferenca e tamanho dos dois arquivos."""
    n = next((i for i in range(min(len(a), len(b))) if a[i] != b[i]), None)
    return f"primeira diferenca em {n if n is None else hex(n)}; tamanhos {len(a)} x {len(b)}"


texto_en = st.from_regex(r"[A-Za-z]{3,8} [A-Za-z]{2,8}", fullmatch=True)
texto_pt = st.text(alphabet="abcdefghij áéíóúçãõ.,!?\n{}%sd", min_size=1, max_size=40)


def test_extrai_textos_e_ponteiros():
    exe, offs = monta_pe(["Open the menu", "Save game now"])
    achados = E.extract(exe)
    assert [i["offset"] for i in achados] == offs
    assert all(len(i["refs"]) == 2 for i in achados)  # tabela em .data + push em .text


def test_descarta_ponteiro_falso_no_codigo():
    """call rel32 (E8) + 3 bytes que, lidos como u32, caem num texto: nao e ponteiro."""
    exe, offs = monta_pe(["Open the menu"])
    va = BASE + VA[RDA] + (offs[0] - RDA)
    falso = bytearray(exe)
    falso[TXT + 0x50:TXT + 0x54] = struct.pack("<I", va)  # 4 bytes soltos que coincidem com o endereco
    falso[TXT + 0x4F] = 0xE8  # o byte anterior e opcode; o u32 comeca no opcode: (E8 | rel32 baixo)
    falso[TXT + 0x4F:TXT + 0x53] = struct.pack("<I", va)
    falso[TXT + 0x53] = 0x90
    assert len(E.extract(bytes(falso))[0]["refs"]) == 2  # so a tabela e o push de verdade
    assert E.interior_refs(bytes(falso), E.extract(bytes(falso))) == []


@settings(max_examples=60, deadline=None)
@given(st.lists(texto_en, min_size=1, max_size=12, unique=True), st.data())
def test_aplica_e_le_de_volta(textos, data):
    exe, offs = monta_pe(textos)
    pt = {o: data.draw(texto_pt) for o in offs}
    saida = E.apply(exe, pt)
    itens = E.extract(exe)
    assert E.read_back(saida, itens) == {o: E.fit(t) for o, t in pt.items()}
    # fora dos ponteiros e do cabecalho, o original nao muda
    refs = {r + k for it in itens for r in it["refs"] for k in range(4)}
    cab = range(HDR)
    mudou = [i for i in range(len(exe)) if exe[i] != saida[i] and i not in refs and i not in cab]
    assert not mudou, primeira_diferenca(exe, saida)
    assert len(saida) > len(exe)


def test_largura_e_a_da_linha_mais_larga_sem_tokens():
    av = {ord("a"): 10, ord("b"): 7}
    assert E._largura(av, "aab") == 27
    assert E._largura(av, "{c5}aa{c-}\nb") == 20  # token nao ocupa tela; vale a linha mais larga
    assert E._largura(av, "z") == 14  # glifo fora da tabela cai no padrao


def test_palavra_solta_de_exibicao_e_extraida(monkeypatch):
    exe, _ = monta_pe(["Water", "evSetBattleEventTrigger"])
    assert [i["text"] for i in E.extract(exe)] == ["Water"]  # rotulo entra; identificador interno nao


def test_sem_traducao_so_ganha_a_secao():
    exe, _ = monta_pe(["Open the menu"])
    saida = E.apply(exe, {})
    assert E.Pe(saida).nsec == 4 and saida[:len(exe)][HDR:] == exe[HDR:]


def test_recusa_offset_que_nao_e_texto():
    exe, _ = monta_pe(["Open the menu"])
    with pytest.raises(ValueError):
        E.apply(exe, {RDA + 0x100: "x"})
