#!/usr/bin/env python3
"""
test_roundtrip.py — gate de regressão do conector (pytest).

Trava automaticamente os invariantes que antes só rodavam inline:
  1. Round-trip de IDENTIDADE: reinserir o source (sem traduzir) reproduz o binário byte-a-byte,
     sem relocação e sem resíduo.
  2. Binário-fonte intacto (read-only) após a reinserção.
  3. Cada head relocado (FILE-RELATIVO) aponta para DENTRO do próprio arquivo e a string lida ali
     é a transliteração do alvo aprovado (validado nas coordenadas da saída, não circular).
  4. O patch IPS aplicado ao original reproduz o output byte-a-byte.
  5. PLANO B: relocação INTRA-ARQUIVO — nenhum alvo cai fora do `size` do arquivo (o EOF-append foi
     reprovado in-game); e o Pack reconstruído fica íntegro (contíguo, alinhado a 16, nomes/footer).
  6. GOVERNANÇA: nenhum texto da obra hardcoded nos `.py` do conector (data-driven, genérico).

Rodar:  pytest projects/utawarerumono/connector/
Requer: artifacts/ScriptEvent.sdat (binário-fonte) e os artefatos gerados pelo pipeline
        (dialogs.csv, approved_translations.csv).
"""
import csv
import hashlib
import struct
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sdat_format as S          # noqa: E402
import reinsert as R            # noqa: E402

ROOT = HERE.parent
ART = ROOT / "artifacts"
SRC = ART / "ScriptEvent.sdat"

# O binário-fonte é gitignored (copyright) e pode faltar em CI: pula só os testes que precisam dele.
# O guard de texto-no-script (test_no_work_text_in_scripts) NÃO depende do binário e roda sempre.
requires_bin = pytest.mark.skipif(not SRC.is_file(), reason="binário-fonte ausente em artifacts/")


@pytest.fixture(scope="module")
def original():
    return SRC.read_bytes()


@pytest.fixture(scope="module")
def applied(original):
    """Roda a reinserção uma vez (sem CLI → usa project.json) e devolve os artefatos de saída."""
    src_hash_before = hashlib.md5(original).hexdigest()
    sys.argv[:] = ["reinsert.py"]            # força resolução por project.json (sem arg de teste)
    R.main()
    out = (ROOT / "output" / SRC.name).read_bytes()
    ips = (ROOT / "output" / (SRC.name + ".ips")).read_bytes()
    src_hash_after = hashlib.md5(SRC.read_bytes()).hexdigest()
    return {"out": out, "ips": ips, "src_before": src_hash_before, "src_after": src_hash_after}


@requires_bin
def test_roundtrip_identity(original):
    """Reinserir o SOURCE (alvo == source) reproduz o original byte-a-byte, sem repoint/resíduo."""
    budgets = R.load_budgets()
    buf, repoints, report = R.build_output(original, budgets, approved={})
    assert bytes(buf) == original, "round-trip de identidade NÃO é byte-idêntico"
    assert repoints == [], "identidade não deveria gerar repoint"
    residuo = [r for r in report if r[1] == "T4_residuo"]
    assert residuo == [], f"identidade não deveria gerar resíduo: {residuo}"


@requires_bin
def test_source_untouched(applied):
    """O binário-fonte em disco não muda (gravação só em output/)."""
    assert applied["src_before"] == applied["src_after"]


@requires_bin
def test_no_residue(original):
    """Com o modelo file-relativo, tudo é repointável: resíduo T4 = 0 (sem ajuste in_place forçado)."""
    _buf, _repoints, report = R.build_output(original, R.load_budgets(), {
        r["offset"]: r["text_target"]
        for r in csv.DictReader((ART / "approved_translations.csv").open(encoding="utf-8"))})
    residue = [r[0] for r in report if r[1] == "T4_residuo"]
    assert not residue, f"resíduo T4 deveria ser 0: {residue[:8]}"


@requires_bin
def test_translated_pointers(original):
    """Cada head relocado: o ponteiro gravado (FILE-RELATIVO: file_start + valor) aponta para DENTRO
    do próprio arquivo, e a string lida ali == transliterate(alvo). Validado nas coordenadas da SAÍDA
    (o arquivo desloca quando um arquivo anterior cresce) — não circular."""
    approved = {r["offset"]: r["text_target"]
                for r in csv.DictReader((ART / "approved_translations.csv").open(encoding="utf-8"))}
    assert approved, "approved_translations.csv vazio"
    src_by = {o: s for o, s, _ in R.load_budgets()}

    buf, repoints, _ = R.build_output(original, R.load_budgets(), approved)
    out = bytes(buf)
    fo = {f.index: f for f in S.parse_pack(original)}
    fn = {f.index: f for f in S.parse_pack(out)}

    ptr_bad, str_bad = [], []
    for head_hex, idx, new_local, ptr_sites, _run in repoints:
        fO, fN = fo[idx], fn[idx]
        exp = R.transliterate(approved.get(head_hex, src_by.get(head_hex, ""))).encode("utf-8")
        for s_hex in ptr_sites:
            new_site = fN.offset + (int(s_hex, 16) - fO.offset)   # corrige o deslocamento do arquivo
            val = struct.unpack_from("<I", out, new_site)[0]
            tgt = fN.offset + val
            if not (val == new_local and fN.offset <= tgt < fN.end):
                ptr_bad.append((head_hex, s_hex, hex(val)))
            elif S.read_cstr(out, tgt) != exp:
                str_bad.append((head_hex, exp.decode("utf-8", "replace"),
                                S.read_cstr(out, tgt).decode("utf-8", "replace")))
    assert not ptr_bad, f"ponteiro file-relativo fora do arquivo / valor errado: {ptr_bad[:5]}"
    assert not str_bad, f"string relocada != transliterate(alvo): {str_bad[:5]}"


@requires_bin
def test_planob_within_file(original):
    """PLANO B: todo alvo relocado cai DENTRO da região do seu arquivo (file_start ≤ alvo < file_end);
    nunca além do `size` declarado. É o que diferencia do EOF-append (reprovado in-game)."""
    approved = {r["offset"]: r["text_target"]
                for r in csv.DictReader((ART / "approved_translations.csv").open(encoding="utf-8"))}
    buf, repoints, _ = R.build_output(original, R.load_budgets(), approved)
    out = bytes(buf)
    fn = {f.index: f for f in S.parse_pack(out)}
    assert len(out) >= len(original), "output não deveria encolher"
    outside = []
    for head_hex, idx, new_local, _sites, _run in repoints:
        fN = fn[idx]
        tgt = fN.offset + new_local
        if not (fN.offset <= tgt < fN.end):
            outside.append((head_hex, fN.name, hex(new_local), hex(fN.size)))
    assert not outside, f"alvo(s) relocado(s) FORA do arquivo (quebraria in-game): {outside[:5]}"


@requires_bin
def test_pack_rebuild_integrity(original):
    """O container reconstruído mantém o Pack íntegro: mesmo nº/ordem/nomes de arquivos, contíguos,
    alinhados a 16 bytes; arquivos NÃO alterados ficam byte-idênticos; footer preservado."""
    approved = {r["offset"]: r["text_target"]
                for r in csv.DictReader((ART / "approved_translations.csv").open(encoding="utf-8"))}
    buf, _repoints, _ = R.build_output(original, R.load_budgets(), approved)
    out = bytes(buf)
    fo = sorted(S.parse_pack(original), key=lambda f: f.offset)
    fn = sorted(S.parse_pack(out), key=lambda f: f.offset)

    assert [f.name for f in fo] == [f.name for f in fn], "conjunto/ordem de arquivos mudou"
    assert all(a.end == b.offset for a, b in zip(fn, fn[1:])), "arquivos não contíguos na saída"
    assert all(f.offset % 16 == 8 and f.size % 16 == 0 for f in fn), "alinhamento de 16 bytes quebrado"
    # arquivos cujo conteúdo é idêntico (comparando por nome, ignorando deslocamento de posição)
    oN = {f.name: f for f in fn}
    changed = [f.name for f in fo
               if original[f.offset:f.end] != out[oN[f.name].offset:oN[f.name].end]]
    # só os arquivos das cenas traduzidas podem ter mudado
    assert all(c.startswith(("11_01", "11_02")) for c in changed), \
        f"arquivo fora das cenas traduzidas foi alterado: {changed}"
    assert original[fo[-1].end:] == out[fn[-1].end:], "footer final do container não preservado"


@requires_bin
def test_pointer_model_is_file_relative(original):
    """Prova/trava o modelo: a esmagadora maioria dos sites `50 00` só aponta para uma string quando
    interpretada como FILE-RELATIVA (file_start + uint32), não como absoluta."""
    files = S.parse_pack(original)
    starts = [f.offset for f in files]
    import bisect

    def is_str_start(off):
        return 0 < off < len(original) and original[off - 1] == 0x00 \
            and original.find(b"\x00", off) > off

    rel_only = abs_only = 0
    i = 0
    while True:
        i = original.find(S.TEXT_OPCODE, i)
        if i == -1:
            break
        site = i + 2
        if site + 4 <= len(original):
            j = bisect.bisect_right(starts, i) - 1
            if 0 <= j < len(files) and files[j].offset <= i < files[j].end:
                val = struct.unpack_from("<I", original, site)[0]
                a, r = val, files[j].offset + val
                if is_str_start(r) and not is_str_start(a):
                    rel_only += 1
                elif is_str_start(a) and not is_str_start(r):
                    abs_only += 1
        i += 1
    assert rel_only > 100 * max(abs_only, 1), \
        f"modelo não confirmado file-relativo: rel_only={rel_only} abs_only={abs_only}"


@requires_bin
def test_ips_applies(applied, original):
    """Aplicar o patch IPS ao original reproduz o output byte-a-byte."""
    patch = applied["ips"]
    assert patch[:5] == b"PATCH"
    buf = bytearray(original)
    i = 5
    while patch[i:i + 3] != b"EOF":
        off = int.from_bytes(patch[i:i + 3], "big"); i += 3
        ln = int.from_bytes(patch[i:i + 2], "big"); i += 2
        if ln == 0:                                   # RLE
            rl = int.from_bytes(patch[i:i + 2], "big"); i += 2
            val = patch[i]; i += 1
            buf[off:off + rl] = bytes([val]) * rl
        else:
            if off + ln > len(buf):
                buf.extend(b"\x00" * (off + ln - len(buf)))
            buf[off:off + ln] = patch[i:i + ln]; i += ln
    assert bytes(buf) == applied["out"], "IPS aplicado ao original != output"


# --------------------------------------------------------------------------- governança
import unicodedata  # noqa: E402


def _norm(s: str) -> str:
    """Normaliza p/ comparação insensível a acento e a caixa (NFKD + drop de combining + lower).
    Assim uma frase hardcoded transliterada (sem acento) ainda é flagrada."""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def _corpus_phrases(min_len: int = 14) -> set[str]:
    """Fragmentos de texto da obra (source + alvo + plano), NORMALIZADOS, com ≥ min_len chars,
    partidos em `\\n`. Data-driven e genérico: usa os artefatos do PRÓPRIO projeto, sem nada
    hardcoded da obra (funciona para qualquer instância)."""
    phrases: set[str] = set()
    for name, col in (("dialogs.csv", "text_source"), ("approved_translations.csv", "text_target")):
        f = ART / name
        if not f.is_file():
            continue
        for row in csv.DictReader(f.open(encoding="utf-8")):
            val = (row.get(col) or "").replace("\\n", "\n")
            for chunk in val.split("\n"):
                chunk = chunk.strip()
                if len(chunk) >= min_len:
                    phrases.add(_norm(chunk))
    return phrases


def test_no_work_text_in_scripts():
    """GOVERNANÇA: nenhum texto da obra pode estar embutido nos scripts `.py` do conector — eles devem
    LER as frases dos artefatos de dados (dialogs.csv / approved_translations.csv / translation_plan.json),
    nunca contê-las. Genérico: compara cada `.py` (normalizado, insensível a acento) contra os artefatos
    do projeto — não conhece a obra, e pega até frases transliteradas."""
    phrases = _corpus_phrases()
    assert phrases, "sem frases de referência (dialogs/approved ausentes) — não dá para checar"
    offenders = []
    for py in sorted(HERE.glob("*.py")):
        if py.name == Path(__file__).name:      # o próprio teste pode citar exemplos
            continue
        text = _norm(py.read_text(encoding="utf-8", errors="replace"))
        hits = [p for p in phrases if p in text]
        if hits:
            offenders.append((py.name, len(hits), hits[:2]))
    assert not offenders, (
        "texto da obra hardcoded em script(s) do conector — mova para um artefato de dados "
        f"e leia de lá: {offenders}")
