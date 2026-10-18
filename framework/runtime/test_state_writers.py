"""Onda 2 (integridade): os escritores de ESTADO real nao gravam direto no destino.

Estado = o que nao se regenera sozinho (traducao, aprovados, project.json, research_log, ledger, ratificacao).
Relatorio regeneravel (prompt, pack, csv de revisao) pode continuar com write_text. Quem entrar na lista abaixo
tem de usar atomic_write / os.replace / locked; esta lista so cresce.
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


# ---- varredura: todo ponto de escrita do framework e ESTADO (acima) ou DERIVADO (abaixo, com motivo) ----------
FRAMEWORK = RUNTIME.parent
_MODOS_ESCRITA = {"w", "a", "x", "wb", "ab", "xb", "w+", "a+"}

# (arquivo relativo a framework/, funcao) -> por que pode gravar direto. Regeneravel = refaz-se a partir de outra fonte.
DERIVADO = {
    ("connectors/connector_io.py", "write_dialogs_csv"): "saida da extracao: regenera do jogo",
    ("connectors/connector_io.py", "write_extraction_log"): "log da extracao",
    ("connectors/connector_smoke.py", "_run_roundtrip"): "arquivo temporario do smoke test",
    ("connectors/discover.py", "_write_stubs"): "scaffold de conector novo",
    ("db/export_to_flat.py", "export_approved"): "exportacao regeneravel do banco",
    ("db/export_to_flat.py", "export_tm"): "exportacao regeneravel do banco",
    ("distribution/build_package.py", "<modulo>"): "empacotamento em dist/",
    ("distribution/patcher.py", "instalar"): "patch no jogo: grava em .tmp e troca, com .bak do original",
    ("runtime/back_translate.py", "_write_back_prompt"): "prompt regeneravel",
    ("runtime/bench_translate.py", "main"): "relatorio de benchmark",
    ("runtime/context_pack.py", "write_pack"): "pack e prompt da cena: regeneram do KB",
    ("runtime/glossary_lint.py", "main"): "relatorio do lint",
    ("runtime/hitl.py", "note_verified"): "CSV de amostra para revisao: regenera do estado da onda",
    ("runtime/hitl.py", "_ratify_csv"): "append sob paths.locked (ver ESTADO)",
    ("runtime/kb_build_ollama.py", "_write_research_log"): "log de pesquisa bruto",
    ("runtime/kb_build_ollama.py", "_write_kb"): "KB gerado: regenera da pesquisa",
    ("runtime/kb_fetch.py", "fetch_and_cache"): "cache de fonte baixada",
    ("runtime/kb_phase.py", "write_worklist"): "worklist regeneravel",
    ("runtime/model.py", "translate"): "scene_prompt.md regeneravel",
    ("runtime/paths.py", "append_line"): "append sob locked",
    ("runtime/quality_gate.py", "export_revise"): "CSV de revisao regeneravel",
    ("runtime/quality_review.py", "write_csv"): "planilha de revisao regeneravel",
    ("runtime/quality_sample.py", "export"): "amostra de qualidade regeneravel",
    ("runtime/review_page.py", "main"): "pagina HTML gerada",
    ("runtime/risk_triage.py", "export"): "lotes de triagem regeneraveis",
    ("runtime/risk_triage_run.py", "_one"): "resposta e veredito por lote; rodar de novo refaz",
    ("runtime/run_scene.py", "_persist_fitting_diagnostics"): "diagnostico regeneravel",
    ("runtime/scaffold_project.py", "text"): "criacao de projeto novo",
    ("runtime/scaffold_project.py", "write_glossary"): "criacao de projeto novo",
    ("runtime/session_lot.py", "cmd_prompt"): "lote temporario (TMP)",
    ("runtime/session_lot.py", "cmd_plan"): "plano temporario",
    ("runtime/session_part.py", "split"): "lote temporario (TMP)",
    ("runtime/session_part.py", "join"): "lote temporario (TMP)",
    ("runtime/spoiler_check.py", "audit_and_persist"): "relatorio da auditoria",
    ("runtime/wave.py", "run"): "log da onda",
    ("validation/cost_model.py", "main"): "relatorio",
    ("validation/naturalness_lint.py", "main"): "relatorio",
}


def _pontos_de_escrita(path: Path, base: Path = FRAMEWORK) -> set[tuple[str, str]]:
    achados: set[tuple[str, str]] = set()

    def modo(call: ast.Call) -> str | None:
        arg = call.args[1:2] if isinstance(call.func, ast.Name) else call.args[:1]
        cand = [a for a in arg if isinstance(a, ast.Constant)] + [k.value for k in call.keywords
                                                                  if k.arg == "mode" and isinstance(k.value, ast.Constant)]
        return next((c.value for c in cand if isinstance(c.value, str)), None)

    def visita(no, fn):
        for ch in ast.iter_child_nodes(no):
            f = ch.name if isinstance(ch, ast.FunctionDef | ast.AsyncFunctionDef) else fn
            if isinstance(ch, ast.Call):
                func = ch.func
                if isinstance(func, ast.Attribute) and func.attr in ("write_text", "write_bytes"):
                    achados.add((path.relative_to(base).as_posix(), f))
                elif (isinstance(func, ast.Attribute) and func.attr == "open") or (isinstance(func, ast.Name) and func.id == "open"):
                    if modo(ch) in _MODOS_ESCRITA:
                        achados.add((path.relative_to(base).as_posix(), f))
            visita(ch, f)

    visita(ast.parse(path.read_text(encoding="utf-8")), "<modulo>")
    return achados


def _fontes_do_framework():
    for p in sorted(FRAMEWORK.rglob("*.py")):
        rel = p.relative_to(FRAMEWORK).as_posix()
        if p.name.startswith("test_") or p.name == "conftest.py" or "/_skeleton/" in rel or "__pycache__" in rel:
            continue
        if rel.startswith("connectors/") and rel.count("/") > 1:       # conectores por jogo
            continue
        yield p


def test_todo_ponto_de_escrita_e_estado_protegido_ou_derivado_declarado():
    """Escritor novo que grava direto (write_text/open('w')) falha aqui ate ser migrado para atomic_write
    (e entrar em ESTADO) ou declarado em DERIVADO com o motivo de ser regeneravel."""
    achados: set[tuple[str, str]] = set()
    for p in _fontes_do_framework():
        achados |= _pontos_de_escrita(p)
    estado = {(f.relative_to(FRAMEWORK).as_posix(), fn) for f, fn, _ in ESTADO}
    novos = sorted(achados - set(DERIVADO) - estado)
    assert not novos, f"escrita direta nao classificada (use paths.atomic_write ou declare em DERIVADO): {novos}"


def test_derivado_nao_guarda_entrada_morta():
    achados: set[tuple[str, str]] = set()
    for p in _fontes_do_framework():
        achados |= _pontos_de_escrita(p)
    mortas = sorted(set(DERIVADO) - achados)
    assert not mortas, f"DERIVADO cita ponto que nao grava mais (remova): {mortas}"


def test_derivado_nao_contem_funcao_de_estado():
    estado = {(f.relative_to(FRAMEWORK).as_posix(), fn) for f, fn, _ in ESTADO}
    dupla = sorted(k for k in DERIVADO if k in estado and k[1] not in {"_ratify_csv"})
    assert not dupla, f"ponto em ESTADO e DERIVADO ao mesmo tempo: {dupla}"


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
    assert achados == {("runtime/_x.py", "grava"), ("runtime/_x.py", "grava2"), ("runtime/_x.py", "anexa")}


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
