"""Onda 2 (integridade): nenhum escritor do framework grava direto no destino.

Duas camadas: (1) ESTADO = lista de escritores cuja prova e checada por nome; (2) a varredura no fim do arquivo,
que cobre TODO write_text/write_bytes/open('w'|'a') do framework sem lista de excecoes: a funcao que grava tem
de usar atomic_write(_csv), append_line, locked ou tmp + replace. "Regeneravel" nao e criterio.
"""
import ast
import csv
import json
import os
from pathlib import Path

import paths
import pytest
import tm_correct

RUNTIME = Path(__file__).resolve().parent
CONNECTORS = RUNTIME.parent / "connectors"

# (arquivo, funcao, o que prova que e seguro)
ESTADO = [
    (RUNTIME / "session_lot.py", "_save", "atomic_write"),
    (RUNTIME / "kb_phase.py", "apply_frontier", "atomic_write"),
    (RUNTIME / "kb_reconcile.py", "promote", "atomic_write"),
    (RUNTIME / "tm_correct.py", "_write_approved", "atomic_write_csv"),
    (RUNTIME / "session_usage.py", "rebuild", "locked"),
    (RUNTIME / "hitl.py", "_ratify_csv", "locked"),
    (CONNECTORS / "connector_io.py", "sync_translations_db", "replace"),
    (RUNTIME / "hitl.py", "_write_queue", "atomic_write"),
    (RUNTIME / "hitl.py", "_add_alias", "atomic_write"),
    (RUNTIME / "review_page.py", "save", "atomic_write"),
    (RUNTIME / "fingerprint_monitor.py", "write_manifest", "atomic_write"),
]


def _funcao(arquivo: Path, nome: str) -> ast.FunctionDef:
    for n in ast.walk(ast.parse(arquivo.read_text(encoding="utf-8"))):
        if isinstance(n, ast.FunctionDef) and n.name == nome:
            return n
    raise AssertionError(f"{nome} nao existe em {arquivo.name}")


@pytest.mark.parametrize(("arquivo", "nome", "prova"), ESTADO, ids=[f"{a.name}:{n}" for a, n, _ in ESTADO])
def test_escritor_de_estado_usa_gravacao_segura(arquivo, nome, prova):
    fn = _funcao(arquivo, nome)
    chamadas = {c.func.attr if isinstance(c.func, ast.Attribute) else getattr(c.func, "id", "")
                for c in ast.walk(fn) if isinstance(c, ast.Call)}
    assert prova in chamadas, f"{arquivo.name}:{nome} deve chamar {prova}"
    assert "write_text" not in chamadas, f"{arquivo.name}:{nome} grava estado com write_text direto"


def test_atomic_write_csv_preserva_aspas_quebra_de_linha_e_utf8(tmp_path):
    p = tmp_path / "a.csv"
    rows = [("0x1", 'ele disse "oi"\nsegunda linha'), ("0x2", "cafe, acucar")]
    paths.atomic_write_csv(p, ["offset", "text_target"], rows)
    with p.open(encoding="utf-8", newline="") as fh:
        assert [tuple(r) for r in csv.reader(fh)] == [("offset", "text_target"), *rows]
    assert [x.name for x in tmp_path.iterdir()] == ["a.csv"]


def test_csv_de_aprovados_nao_fica_truncado_se_a_troca_falha(tmp_path, monkeypatch):
    p = tmp_path / "approved_a.csv"
    tm_correct._write_approved(p, [{"offset": "0x1", "text_target": "bom"}])
    antes = p.read_bytes()

    def _boom(*_a, **_k):
        raise OSError("disco cheio")
    monkeypatch.setattr(os, "replace", _boom)
    with pytest.raises(OSError, match="disco cheio"):
        tm_correct._write_approved(p, [{"offset": "0x1", "text_target": "novo"}])
    assert p.read_bytes() == antes, "o arquivo bom anterior tem de sobreviver"
    assert [x.name for x in tmp_path.iterdir()] == ["approved_a.csv"], "sem temporario sobrando"


# --- leitura: estado corrompido nao e recriado em silencio -------------------------------------------
def test_read_json_ausente_devolve_default_e_valido_devolve_dado(tmp_path):
    assert paths.read_json(tmp_path / "nao_existe.json", {"x": 1}) == {"x": 1}
    (tmp_path / "ok.json").write_text('{"a": 2}', encoding="utf-8")
    assert paths.read_json(tmp_path / "ok.json") == {"a": 2}


def test_read_json_corrompido_levanta_com_arquivo_e_como_recuperar(tmp_path):
    p = tmp_path / "run_state.json"
    p.write_text('{"scenes": {"a": ', encoding="utf-8")
    with pytest.raises(paths.StateCorrupt) as ei:
        paths.read_json(p, {})
    msg = str(ei.value)
    assert "run_state.json" in msg and "linha 1" in msg and "git checkout" in msg


def test_checkpoint_com_run_state_corrompido_nao_sobrescreve_o_arquivo(tmp_path):
    import run_scene
    (tmp_path / "artifacts").mkdir()
    p = paths.run_state(tmp_path)
    p.write_text("{truncado", encoding="utf-8")
    with pytest.raises(paths.StateCorrupt):
        run_scene._checkpoint(tmp_path, "ch_01", {"status": "verified"})
    assert p.read_text(encoding="utf-8") == "{truncado", "o estado ruim fica como esta para ser recuperado"


def test_read_jsonl_ignora_linha_truncada_com_um_aviso(tmp_path, capsys):
    p = tmp_path / "ledger.jsonl"
    p.write_text('{"a": 1}\n\n{"a": 2}\n{"a": 3, "x', encoding="utf-8")        # ultima linha cortada por queda
    assert paths.read_jsonl(p) == [{"a": 1}, {"a": 2}]
    err = capsys.readouterr().err
    assert err.count("AVISO") == 1 and "1 linha(s)" in err
    assert paths.read_jsonl(tmp_path / "nao_existe.jsonl") == []


def test_ledger_de_sessao_com_linha_truncada_nao_derruba_marks(tmp_path):
    import session_usage
    (tmp_path / "artifacts").mkdir()
    p = tmp_path / "artifacts" / "phase_marks.jsonl"
    p.write_text('{"t": 2.0, "stage": "b"}\n{"t": 1.0, "stage": "a"}\n{"t": 3', encoding="utf-8")
    assert session_usage.marks(tmp_path) == [(1.0, "a"), (2.0, "b")]


def test_rebuild_do_ledger_nao_perde_linha_de_api_gravada_em_paralelo(tmp_path, monkeypatch):
    import subprocess
    import sys

    import session_usage
    monkeypatch.setattr(session_usage, "sync", lambda root, tdir=None: [])      # so o trecho que reescreve o ledger
    (tmp_path / "artifacts").mkdir()
    lp = paths.ledger(tmp_path)
    lp.write_text('{"source": "session", "k": "velha"}\n', encoding="utf-8")
    worker = ("import sys, json\nsys.path.insert(0, {here!r})\nimport paths\nfor k in range(40):\n"
              "    paths.append_line({lp!r}, json.dumps({{'source': 'api', 'w': {w}, 'k': k}}) + chr(10))\n")
    procs = [subprocess.Popen([sys.executable, "-c", worker.format(here=str(RUNTIME), lp=str(lp), w=w)])
             for w in range(3)]
    while any(p.poll() is None for p in procs):
        session_usage.rebuild(tmp_path)
    assert all(p.returncode == 0 for p in procs)
    session_usage.rebuild(tmp_path)
    rows = [json.loads(x) for x in lp.read_text(encoding="utf-8").splitlines()]
    assert {(r["w"], r["k"]) for r in rows} == {(w, k) for w in range(3) for k in range(40)}
    assert all(r["source"] == "api" for r in rows) and len(rows) == 120


# ---- varredura: TODO ponto de escrita do framework prova, na propria funcao, que grava com seguranca --------
# Sem lista de excecoes e sem classificacao manual: "regeneravel" nao e criterio. Quem grava direto usa uma das
# primitivas abaixo (tmp + replace, escrita atomica, anexo sob trava) ou o teste falha.
FRAMEWORK = RUNTIME.parent
_MODOS_ESCRITA = {"w", "a", "x", "wb", "ab", "xb", "w+", "a+"}
_PROVAS = {"atomic_write", "atomic_write_csv", "append_line", "locked", "replace"}


def _nome_chamado(call: ast.Call) -> str:
    f = call.func
    return f.attr if isinstance(f, ast.Attribute) else f.id if isinstance(f, ast.Name) else ""


def _modo_literal(call: ast.Call) -> str | None:
    arg = call.args[1:2] if isinstance(call.func, ast.Name) else call.args[:1]
    cand = [a for a in arg if isinstance(a, ast.Constant)]
    cand += [k.value for k in call.keywords if k.arg == "mode" and isinstance(k.value, ast.Constant)]
    return next((c.value for c in cand if isinstance(c.value, str)), None)


def _escreve(call: ast.Call) -> bool:
    nome = _nome_chamado(call)
    if nome in ("write_text", "write_bytes"):
        return isinstance(call.func, ast.Attribute)
    return nome == "open" and _modo_literal(call) in _MODOS_ESCRITA


def _pontos_de_escrita(path: Path, base: Path = FRAMEWORK) -> list[tuple[str, str, bool]]:
    """(arquivo, funcao, tem_prova) de cada escrita direta; escrita fora de funcao nunca tem prova."""
    achados: list[tuple[str, str, bool]] = []
    rel = path.relative_to(base).as_posix()

    def visita(no, fn, chamadas):
        for ch in ast.iter_child_nodes(no):
            if isinstance(ch, ast.FunctionDef | ast.AsyncFunctionDef):
                prova = {_nome_chamado(c) for c in ast.walk(ch) if isinstance(c, ast.Call)} & _PROVAS
                visita(ch, ch.name, bool(prova))
                continue
            if isinstance(ch, ast.Call) and _escreve(ch):
                achados.append((rel, fn, chamadas))
            visita(ch, fn, chamadas)

    visita(ast.parse(path.read_text(encoding="utf-8")), "<modulo>", False)
    return achados


def _fontes_do_framework():
    for p in sorted(FRAMEWORK.rglob("*.py")):
        rel = p.relative_to(FRAMEWORK).as_posix()
        if p.name.startswith("test_") or p.name == "conftest.py" or "/_skeleton/" in rel or "__pycache__" in rel:
            continue
        if rel.startswith("connectors/") and rel.count("/") > 1:       # conectores por jogo
            continue
        yield p


def test_todo_ponto_de_escrita_prova_gravacao_segura_na_propria_funcao():
    """write_text/write_bytes/open('w'|'a') so passam se a funcao usa atomic_write(_csv), append_line, locked
    ou tmp + replace. Escrita direta nova (ou fora de funcao) falha aqui; nao ha lista de excecoes."""
    sem_prova = sorted({(f, fn) for p in _fontes_do_framework() for f, fn, ok in _pontos_de_escrita(p) if not ok})
    assert not sem_prova, f"escrita direta sem prova de gravacao segura (use paths.atomic_write): {sem_prova}"


def test_a_varredura_enxerga_pontos_de_escrita_conhecidos():
    """Guarda do guarda: se o scanner parasse de achar escrita, o teste acima passaria vazio."""
    achados = {(f, fn) for p in _fontes_do_framework() for f, fn, _ in _pontos_de_escrita(p)}
    conhecidos = {("connectors/connector_io.py", "write_dialogs_csv"), ("distribution/patcher.py", "instalar"),
                  ("runtime/hitl.py", "_ratify_csv"), ("runtime/paths.py", "append_line")}
    assert conhecidos <= achados, f"scanner nao achou: {sorted(conhecidos - achados)}"


def test_varredura_pega_escrita_direta_nova(tmp_path):
    fonte = tmp_path / "runtime" / "_x.py"
    fonte.parent.mkdir()
    fonte.write_text('''
def grava(p):
    p.write_text("x")

def le(p):
    return open(p).read()

def grava2(p):
    with open(p, "w") as fh:
        fh.write("x")

def anexa(p):
    p.open("a").close()
''', encoding="utf-8")
    achados = _pontos_de_escrita(fonte, tmp_path)
    assert achados == [("runtime/_x.py", "grava", False), ("runtime/_x.py", "grava2", False),
                       ("runtime/_x.py", "anexa", False)]


def test_varredura_aceita_escrita_com_prova_e_rejeita_a_sem_prova(tmp_path):
    fonte = tmp_path / "m.py"
    fonte.write_text('''
import os

def segura(p, t):
    tmp = p.with_name("x.tmp")
    tmp.write_text(t)
    os.replace(tmp, p)

def direta(p, t):
    p.write_text(t)

p0 = open("a", "w")
''', encoding="utf-8")
    assert _pontos_de_escrita(fonte, tmp_path) == [("m.py", "segura", True), ("m.py", "direta", False),
                                                   ("m.py", "<modulo>", False)]


# --- migrados na re-auditoria (nota 4): queda na troca preserva o original ------------------------------
def _fila(root):
    import hitl
    hitl._write_queue(root, [{"scene": "a", "offset": "0x1", "kind": "k"}])
    return hitl.queue_path(root), lambda: hitl._write_queue(root, [{"scene": "b", "offset": "0x2", "kind": "k"}])


def _alias(root):
    import hitl
    g = paths.glossary(root)
    g.parent.mkdir(parents=True, exist_ok=True)
    g.write_bytes(b"\xef\xbb\xbfterm,aliases\r\nfoo,\r\nbar,\r\n")
    return g, lambda: hitl._add_alias(root, "foo", "baz")


def _planilha(root):
    import review_page
    box = root / "box"
    box.mkdir()
    review_page.save(box, "escalonamento.csv", b"a,b\r\n1,2\r\n")
    return box / "escalonamento.csv", lambda: review_page.save(box, "escalonamento.csv", b"novo")


def _manifesto(root):
    import fingerprint_monitor as fm
    kw = dict(tier="t", engine_id="e", connector_version="1", scripts_fingerprint="x", source_sample_files=[],
              source_fingerprint="y", timestamp_iso="2026-10-18T00:00:00Z")
    fm.write_manifest(root, **kw)
    return fm._manifest_path(root), lambda: fm.write_manifest(root, **{**kw, "tier": "outro"})


@pytest.mark.parametrize("montar", [_fila, _alias, _planilha, _manifesto])
def test_estado_migrado_nao_fica_truncado_se_a_troca_falha(tmp_path, monkeypatch, montar):
    alvo, regrava = montar(tmp_path)
    antes = alvo.read_bytes()

    def _boom(*_a, **_k):
        raise OSError("disco cheio")
    monkeypatch.setattr(os, "replace", _boom)
    with pytest.raises(OSError, match="disco cheio"):
        regrava()
    assert alvo.read_bytes() == antes, "o arquivo bom anterior tem de sobreviver"
    assert not [x for x in alvo.parent.iterdir() if x.name.endswith(".tmp")], "sem temporario sobrando"


def test_alias_preserva_bom_e_crlf_do_glossario(tmp_path):
    g, regrava = _alias(tmp_path)
    regrava()
    raw = g.read_bytes()
    assert raw.startswith(b"\xef\xbb\xbf") and b"\r\n" in raw and b"foo,baz" in raw
