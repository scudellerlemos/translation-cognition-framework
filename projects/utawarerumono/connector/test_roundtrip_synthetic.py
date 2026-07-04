"""
test_roundtrip_synthetic.py — oráculo de round-trip SEMPRE ativo em CI, sem o binário comercial.

Mesmo problema fechado para BoF4 na issue #84 (ver test_roundtrip_synthetic.py de lá): o oráculo
central do projeto (round-trip byte-idêntico extract->reinsert->re-extract) só rodava contra
`artifacts/ScriptEvent.sdat`, que é gitignored (licenciamento) — em CI o binário nunca existe, então
todo `test_roundtrip.py` marcado `@requires_bin` pula (`pytest.skip`).

Este arquivo constrói, EM MEMÓRIA, um container .sdat sintético mínimo que reproduz a estrutura real
do formato Aquaplus (ver sdat_format.py): header "Filename"+tabela de nomes (stride 15) + seção
"Pack" (offset/size por arquivo) + arquivos com bytecode (pointers `50 00`+u32 file-relativo) seguido
de um bloco de texto UTF-8 null-terminated. Exercita a MESMA lógica determinística
(`parse_pack`/`extract_text_block`/`index_pointers`/`build_output`/`rebuild_container`) usada por
extract.py/reinsert.py sobre o binário real — sem depender dele.

Limitação documentada: a fixture usa só HEADS independentes (cada string tem seu próprio pointer
`50 00`); não modela "continuações" (strings sem pointer próprio, lidas em sequência após um head —
ver `read_run`). Isso cobre in_place, relocação intra-arquivo de um run de 1 membro, e a integridade
do Pack multi-arquivo, mas não testa a relocação de um run com >1 membro. Fica para uma fixture futura
se isso vier a ser um ponto de regressão real.
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "connector"))
import reinsert as R  # noqa: E402
import sdat_format as S  # noqa: E402

_FILE_STRINGS = [
    [b"Hello there my friend", b"Bye for now my friend"],
    [b"Thanks a lot dear friend", b"See you soon my friend"],
]


def _build_file_body(strings: list[bytes]) -> tuple[bytes, list[int]]:
    """bytecode (1 pointer `50 00`+u32 por string, cada string um HEAD independente) + bloco de
    texto contíguo null-terminated. Retorna (body_padded_16, [offsets_locais_das_strings])."""
    ptr_block_len = 6 * len(strings)          # cada pointer: 2 bytes opcode + 4 bytes u32 LE
    cur = ptr_block_len
    local_offs = []
    strblock = bytearray()
    for s in strings:
        local_offs.append(cur)
        strblock += s + b"\x00"
        cur += len(s) + 1
    ptrs = b"".join(S.TEXT_OPCODE + struct.pack("<I", o) for o in local_offs)
    body = ptrs + bytes(strblock)
    body += b"\x00" * ((-len(body)) % 16)     # ALIGN=16 (rebuild_container repadroniza pra isso)
    return body, local_offs


def _build_synthetic_sdat(file_strings: list[list[bytes]] = _FILE_STRINGS) -> bytes:
    """Monta um ScriptEvent.sdat sintético: header (Filename + tabela de nomes + Pack) + N arquivos.

    name_base (achado por sdat_format.parse_pack via 1ª ocorrência de b'.BIN' - 10) cai exatamente
    no início da tabela de nomes que construímos aqui; os offsets de arquivo em Pack ficam ≡8 mod16,
    igual ao formato real (não é exigido pelo código, mas mantém a fixture fiel)."""
    region_a = S.FILENAME_MAGIC + b"\x00\x00\x00\x00"
    names = [f"11_0{i + 1}_000S.BIN" for i in range(len(file_strings))]
    assert all(len(n) == 14 for n in names)
    region_b = b"".join(n.encode("ascii") + b"\x00" for n in names)   # stride 15 (14+\0)

    bodies = [_build_file_body(s)[0] for s in file_strings]
    count = len(file_strings)
    region_c_head = S.PACK_MAGIC + struct.pack("<I", 0) + struct.pack("<I", count)
    prelim_len = len(region_a) + len(region_b) + len(region_c_head) + 8 * count

    def _next_off8(n: int) -> int:
        r = n % 16
        return n if r == 8 else n + ((8 - r) if r < 8 else (24 - r))

    header_total = _next_off8(prelim_len)
    filler = b"\x00" * (header_total - prelim_len)

    offsets, cur = [], header_total
    for b in bodies:
        offsets.append(cur)
        cur += len(b)
    entries = b"".join(struct.pack("<II", o, len(b)) for o, b in zip(offsets, bodies))

    header = region_a + region_b + region_c_head + entries + filler
    assert len(header) == header_total
    return header + b"".join(bodies)


def test_synthetic_sdat_is_recognized():
    """parse_pack acha os N arquivos (nome/offset/size corretos) e extract_text_block localiza
    exatamente as strings de diálogo esperadas, em ordem, em cada um."""
    data = _build_synthetic_sdat()
    files = S.parse_pack(data)
    assert [f.name for f in files] == ["11_01_000S.BIN", "11_02_000S.BIN"]
    assert all(f.offset % 16 == 8 and f.size % 16 == 0 for f in files), "alinhamento não replicado"
    assert all(a.end == b.offset for a, b in zip(files, files[1:])), "arquivos não contíguos"

    for f, expected in zip(files, _FILE_STRINGS):
        block = S.extract_text_block(data, f)
        assert [t for _, t, _ in block] == [s.decode() for s in expected]


def _budgets_from(data: bytes, files) -> list[tuple[str, str, int]]:
    """Simula o dialogs.csv: (offset_hex, text_source, byte_budget) na ordem de armazenamento,
    igual ao que extract.py grava a partir de extract_text_block."""
    out = []
    for f in files:
        for off, text, budget in S.extract_text_block(data, f):
            out.append((f"0x{off:x}", text, budget))
    return out


def test_roundtrip_identity_byte_for_byte():
    """reinsert com approved={} (== source) reproduz o container original byte-a-byte, sem
    repoint nem resíduo — o oráculo central do projeto, sem depender do binário comercial."""
    original = _build_synthetic_sdat()
    files = S.parse_pack(original)
    budgets = _budgets_from(original, files)

    buf, repoints, report = R.build_output(original, budgets, approved={})
    assert bytes(buf) == original, "round-trip de identidade NÃO é byte-idêntico"
    assert repoints == [], "identidade não deveria gerar relocação"
    assert not [r for r in report if r[1] == "residuo"], "identidade não deveria gerar resíduo"


def test_roundtrip_translated_inplace_reextracts_correctly():
    """Tradução que CABE no budget grava in_place; re-extraindo (read_cstr no offset original) dá
    exatamente a tradução, e a string VIZINHA no mesmo arquivo fica intacta."""
    original = _build_synthetic_sdat()
    files = S.parse_pack(original)
    budgets = _budgets_from(original, files)
    off_a_hex, _, _ = budgets[0]           # "Hello there my friend" (21 bytes)
    off_b_hex, _, _ = budgets[1]           # "Bye for now my friend" (vizinha, mesmo arquivo)

    approved = {off_a_hex: "Oi amigo"}      # bem mais curto -> cabe in_place
    buf, repoints, report = R.build_output(original, budgets, approved)
    new_data = bytes(buf)

    assert repoints == [], "tradução que cabe não deveria relocar"
    assert S.read_cstr(new_data, int(off_a_hex, 16)) == b"Oi amigo"
    assert S.read_cstr(new_data, int(off_b_hex, 16)) == b"Bye for now my friend", (
        "string vizinha foi corrompida pela edição in_place")
    tiers = {r[0]: r[1] for r in report}
    assert tiers[off_a_hex] == "in_place"


def test_roundtrip_translated_overflow_relocates_and_reextracts():
    """Tradução MAIOR que o budget força relocação intra-arquivo (Plano B): o pointer `50 00` é
    reescrito file-relativo para o novo local, o arquivo cresce (múltiplo de 16, dentro do próprio
    Pack), e re-extrair no NOVO endereço (file_start_novo + novo_offset_local) dá a tradução exata.
    A string vizinha e o 2º arquivo do Pack (que desloca por inteiro) permanecem intactos."""
    original = _build_synthetic_sdat()
    files = S.parse_pack(original)
    budgets = _budgets_from(original, files)
    off_a_hex, src_a, budget_a = budgets[0]
    off_b_hex, src_b, _ = budgets[1]
    long_text = "This translation is much longer than the original budget allows here"
    assert len(long_text) > budget_a, "fixture do teste precisa realmente estourar o budget"

    buf, repoints, report = R.build_output(original, budgets, {off_a_hex: long_text})
    new_data = bytes(buf)

    assert len(repoints) == 1
    head_hex, file_idx, new_local, ptr_sites, run = repoints[0]
    assert head_hex == off_a_hex and file_idx == 0 and run == [int(off_a_hex, 16)]

    new_files = S.parse_pack(new_data)
    f0_new = new_files[0]
    assert f0_new.size % 16 == 0 and f0_new.size > files[0].size, "arquivo deveria ter crescido"
    assert f0_new.offset == files[0].offset, "1º arquivo não deveria mudar de posição"

    # pointer reescrito resolve, dentro do próprio arquivo, para a tradução longa
    target_abs = f0_new.offset + new_local
    assert files[0].offset <= target_abs < f0_new.end, "alvo relocado caiu fora do arquivo"
    assert S.read_cstr(new_data, target_abs) == long_text.encode("utf-8")

    # string vizinha (mesmo arquivo, não relocada) intacta no MESMO endereço absoluto
    assert S.read_cstr(new_data, int(off_b_hex, 16)) == src_b.encode("utf-8")

    # 2º arquivo do Pack: desloca inteiro (arquivo anterior cresceu), mas o CONTEÚDO é idêntico
    growth = f0_new.size - files[0].size
    f1_new = new_files[1]
    assert f1_new.offset == files[1].offset + growth
    assert new_data[f1_new.offset:f1_new.end] == original[files[1].offset:files[1].end]

    residue = [r for r in report if r[1] == "residuo"]
    assert not residue, f"não deveria haver resíduo (relocação intra-arquivo resolve): {residue}"


def test_rebuild_container_preserves_pack_integrity():
    """Reconstrução (sem tradução nenhuma) preserva o Pack íntegro: mesmo nº/ordem/nomes de arquivo,
    contíguos, alinhados a 16 -- mesma checagem que test_pack_rebuild_integrity faz no binário real,
    aqui sem precisar dele."""
    original = _build_synthetic_sdat()
    files = S.parse_pack(original)
    budgets = _budgets_from(original, files)

    buf, _repoints, _report = R.build_output(original, budgets, approved={})
    new_files = S.parse_pack(bytes(buf))

    assert [f.name for f in new_files] == [f.name for f in files]
    assert all(a.end == b.offset for a, b in zip(new_files, new_files[1:]))
    assert all(f.offset % 16 == 8 and f.size % 16 == 0 for f in new_files)
