#!/usr/bin/env python3
"""
test_runtime.py — gates do harness `framework/runtime/` (pytest).

Prova as 3 propriedades que sustentam a arquitetura-alvo:
  - context_pack e DETERMINISTA (rodar 2x -> pack.json byte-identico) e LIMITADO (O(cena): subconjunto
    do glossario/vozes, nao o estado inteiro).
  - state_index e IDEMPOTENTE (rodar 2x -> indices byte-identicos) e a TM e reconstruivel.
  - GOVERNANCA: nenhum work-text (dialogo/traducao) hardcoded nos .py do runtime.

Roda na instancia de referencia (utawarerumono) — unica disponivel, como o test_cost_model.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack          # noqa: E402
import state_index           # noqa: E402
import run_chapter           # noqa: E402
import run_scene             # noqa: E402
import kb_gate               # noqa: E402
import model                 # noqa: E402
import cost_report           # noqa: E402

REPO = _HERE.parents[1]
PROJECT = REPO / "projects" / "utawarerumono"
SCENE = "ch_12_01"           # cena leve, sem dependencia de traducao


def _norm_accents(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


@pytest.fixture(scope="module")
def built():
    state_index.build(PROJECT)
    return True


# ------------------------------- state_index ----------------------------------

def test_state_index_idempotent(built):
    state = PROJECT / "artifacts" / "state"
    first = {p.name: p.read_bytes() for p in state.glob("*")}
    state_index.build(PROJECT)
    second = {p.name: p.read_bytes() for p in state.glob("*")}
    assert first.keys() == second.keys()
    for name in first:
        assert first[name] == second[name], f"{name} mudou entre rebuilds (nao idempotente)"


def test_tm_reconstructible_and_keyed(built):
    tm = [json.loads(l) for l in
          (PROJECT / "artifacts" / "state" / "translation_memory.jsonl")
          .read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(tm) > 1000, "TM deveria conter o capitulo 11 inteiro (~2129 linhas)"
    e = tm[0]
    assert set(e) >= {"scene", "offset", "speaker", "source", "target", "src_key"}
    # a chave e funcao determinista do source normalizado
    assert e["src_key"] == state_index._key(e["source"])


def test_voice_cards_present(built):
    cards = json.loads((PROJECT / "artifacts" / "state" / "voice_cards.json")
                       .read_text(encoding="utf-8"))
    assert cards, "esperava perfis de voz destilados do tone_analysis.md"
    for c in cards.values():
        assert "criticality" in c and "lines" in c


# ------------------------------- context_pack ---------------------------------

def test_context_pack_deterministic(built):
    context_pack.write_pack(PROJECT, SCENE)
    p = PROJECT / "artifacts" / SCENE / "pack.json"
    first = p.read_bytes()
    context_pack.write_pack(PROJECT, SCENE)
    assert p.read_bytes() == first, "pack.json mudou entre execucoes (nao determinista)"


def test_context_pack_bounded(built):
    pack = context_pack.build_pack(PROJECT, SCENE)
    full = context_pack.load_glossary(PROJECT / "artifacts" / "glossary.csv")
    full_terms = {g["term"] for g in full}
    sub_terms = {g["term"] for g in pack["glossary_subset"]}
    assert sub_terms <= full_terms, "subconjunto do glossario deve estar contido no glossario completo"
    assert len(sub_terms) < len(full_terms), "cena pequena nao deveria puxar o glossario inteiro"
    all_cards = json.loads((PROJECT / "artifacts" / "state" / "voice_cards.json")
                           .read_text(encoding="utf-8"))
    assert set(pack["voice_cards"]) <= set(all_cards)
    # cobre exatamente as linhas da cena
    dialogs = context_pack.load_dialogs(PROJECT / "artifacts" / SCENE / "dialogs.csv")
    assert pack["n_lines"] == len(dialogs) == len(pack["lines"])


def test_scene_prompt_self_contained(built):
    context_pack.write_pack(PROJECT, SCENE)
    txt = (PROJECT / "artifacts" / SCENE / "scene_prompt.md").read_text(encoding="utf-8")
    # contem a doutrina (Carta), as linhas e o formato de saida exigido
    assert "CARTA DE GOVERNANCA" in txt
    assert "Linhas a traduzir" in txt
    assert f"translations_{context_pack.scene_id_of(SCENE)}.json" in txt


# ------------------------------- budget (translit) ----------------------------

def test_translit_len_drops_accents():
    # comprimento medido na forma transliterada (o que vai p/ os bytes): acentos/cedilha somem
    assert model._translit_len("Glossário") == len("Glossario")
    assert model._translit_len("coração") == len("coracao")
    assert model._translit_len("abc") == 3


# ------------------------------- retrieval keyword (RAG-parcial) --------------
# Match mais inteligente no context_pack: plural/inflexao + decisoes por conteudo do summary.

def test_present_plural_tolerance():
    assert context_pack._present("Cohort", "the ukon's cohorts arrive")      # plural -> casa (era perdido)
    assert context_pack._present("gigiri", "venomous gigiris everywhere")
    assert context_pack._present("general", "the generals gathered")
    assert context_pack._present("Eight Pillar Generals", "the eight pillar generals met")  # multi-palavra
    assert not context_pack._present("cohort", "a cohabitation pact")        # nao vira substring solta
    assert not context_pack._present("man", "command the troops")            # \b protege dentro de palavra


def test_select_decisions_matches_by_summary():
    decisions = [
        {"title": "Regra de cor", "tags": ["cor"], "universal": False,
         "summary": "como tratar o token de Oshtor na renderizacao"},
        {"title": "Outra", "tags": ["xyz"], "universal": False, "summary": "nada a ver"},
    ]
    # 'Oshtor' nao esta nas TAGS, mas esta no SUMMARY -> surfa por conteudo
    assert [d["title"] for d in context_pack.select_decisions(decisions, ["Oshtor"], [])] == ["Regra de cor"]
    # sem match em tag nem summary -> nada
    assert context_pack.select_decisions(decisions, ["Rulutieh"], []) == []


# ------------------------------- spoiler filter -------------------------------

def test_spoiler_filter():
    led = {"entries": [
        {"entity": "Ukon", "spoiler_level": "major", "reveal": "beyond_frontier",
         "triggers": ["Ukon"], "pre_reveal": "nao revelar"},
        {"entity": "MemFig", "spoiler_level": "major", "reveal": "beyond_frontier",
         "triggers": ["Woman"], "scenes": ["12_14"], "pre_reveal": "x"},
        {"entity": "JaRevelado", "spoiler_level": "minor", "reveal": "11_02",
         "triggers": ["Haku"], "pre_reveal": "y"},
    ]}
    # futuro + trigger por palavra inteira -> dispara
    g = context_pack.select_spoiler_guards(led, "ukon chegou na vila", "12_04")
    assert [x["entity"] for x in g] == ["Ukon"]
    # trigger como SUBSTRING dentro de palavra NAO dispara (limite de palavra)
    assert context_pack.select_spoiler_guards(led, "ele deu um comando ao humano", "12_04") == []
    # disparo por cena explicita
    g2 = context_pack.select_spoiler_guards(led, "sem trigger textual aqui", "12_14")
    assert any(x["entity"] == "MemFig" for x in g2)
    # reveal no passado (<= cena) -> nao e futuro -> nao dispara mesmo presente
    assert context_pack.select_spoiler_guards(led, "Haku acordou", "12_04") == []


# ------------------------------- kb_gate --------------------------------------
# Gate de cobertura: research reconciliado + KB presente; fronteira bloqueia cena alem do pesquisado.

def _kb_project(tmp_path, *, reconciled=True, frontier=None, with_kb=True):
    art = tmp_path / "artifacts"
    (art / "state").mkdir(parents=True)
    status = "**Status:** reconciled" if reconciled else "**Status:** in_progress"
    (art / "research_log.md").write_text(
        f"# Research\n{status}\n**Fronteira de spoiler:** Cap. 11\n", encoding="utf-8")
    if with_kb:
        (art / "glossary.csv").write_text("term,target_translation\nHaku,Haku\n", encoding="utf-8")
        (art / "universe_knowledge_base.md").write_text("# KB\n## Haku\n", encoding="utf-8")
        (art / "state" / "voice_cards.json").write_text('{"Haku": {}}', encoding="utf-8")
    cfg = {"source": {"file": "x"}}
    if frontier:
        cfg["kb_frontier"] = frontier
    (tmp_path / "project.json").write_text(json.dumps(cfg), encoding="utf-8")
    return tmp_path


def test_kb_gate_passes_when_reconciled_and_present(tmp_path):
    root = _kb_project(tmp_path)
    assert kb_gate.check(root, "ch_12_03")["problems"] == []


def test_kb_gate_blocks_unreconciled(tmp_path):
    root = _kb_project(tmp_path, reconciled=False)
    probs = kb_gate.check(root, "ch_12_03")["problems"]
    assert any("reconcil" in p.lower() for p in probs)


def test_kb_gate_blocks_missing_artifacts(tmp_path):
    root = _kb_project(tmp_path, with_kb=False)
    assert kb_gate.check(root, "ch_12_03")["problems"], "KB ausente deve bloquear"


def test_kb_gate_frontier_blocks_beyond(tmp_path):
    root = _kb_project(tmp_path, frontier="12_05")
    assert kb_gate.check(root, "ch_12_03")["problems"] == [], "cena dentro da fronteira passa"
    beyond = kb_gate.check(root, "ch_12_09")["problems"]
    assert any("fronteira" in p.lower() for p in beyond), "cena alem da fronteira deve bloquear"
    assert kb_gate.check(root, "ch_13_01")["problems"], "capitulo seguinte deve bloquear"


# ------------------------------- run_chapter ----------------------------------
# Driver de capitulo: ordem das cenas, resume (skip de verified) e para-na-falha.
# Sem rede — run_scene e mockado (a unica parte de IA fica isolada em model.py).

def _fake_chapter(tmp_path, scenes):
    art = tmp_path / "artifacts"
    for s in scenes:
        d = art / f"ch_{s}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "dialogs.csv").write_text("offset,text_source,byte_budget\n0x1,Hi,5\n", encoding="utf-8")
    return tmp_path


def test_paths_contract():
    # H2: paths.py e a FONTE UNICA do contrato de paths de artefato. Este teste FIXA as strings exatas
    # (congeladas — caps ja traduzidos dependem delas); qualquer rename acidental falha aqui.
    import paths
    r = Path("/proj")
    rel = lambda p: p.relative_to(r).as_posix()
    assert rel(paths.run_state(r)) == "artifacts/run_state.json"
    assert rel(paths.ledger(r)) == "artifacts/api_ledger.jsonl"
    assert rel(paths.metrics(r)) == "artifacts/metrics.jsonl"
    assert rel(paths.glossary(r)) == "artifacts/glossary.csv"
    assert rel(paths.entities(r)) == "artifacts/entities.csv"
    assert rel(paths.kb_worklist(r, "16")) == "artifacts/kb_phase_worklist_16.md"
    assert rel(paths.translation_memory(r)) == "artifacts/state/translation_memory.jsonl"
    assert rel(paths.voice_cards(r)) == "artifacts/state/voice_cards.json"
    assert rel(paths.decision_index(r)) == "artifacts/state/decision_index.json"
    assert rel(paths.dialogs(r, "ch_16_01")) == "artifacts/ch_16_01/dialogs.csv"
    assert rel(paths.pack(r, "ch_16_01")) == "artifacts/ch_16_01/pack.json"
    assert rel(paths.translations(r, "ch_16_01", "16_01")) == "artifacts/ch_16_01/translations_16_01.json"
    assert rel(paths.translation_plan(r, "ch_16_01", "16_01")) == "artifacts/ch_16_01/translation_plan_16_01.json"
    assert rel(paths.back_translation(r, "ch_16_01", "16_01")) == "artifacts/ch_16_01/back_translation_16_01.json"


def test_spoiler_check_detects_pre_reveal_leak(tmp_path):
    # H6: o checker pega nome/titulo pos-reveal vazando em cena ANTERIOR ao reveal; ignora pos-reveal.
    import spoiler_check, paths
    (tmp_path / "artifacts" / "ch_50_01").mkdir(parents=True)
    (tmp_path / "artifacts" / "ch_50_09").mkdir(parents=True)
    led = {"entries": [{"id": "x", "entity": "Ukon", "reveal": "50_05",
                        "forbidden_pre_reveal": ["Oshtor"]}]}
    paths.spoiler_ledger(tmp_path).write_text(json.dumps(led), encoding="utf-8")
    # cena 50_01 (ANTES do reveal 50_05) com 'Oshtor' -> VAZA
    paths.translations(tmp_path, "ch_50_01", "50_01").write_text(
        json.dumps({"lines": {"0x1": {"t": "Sim, Oshtor chegou."}}}), encoding="utf-8")
    # cena 50_09 (APOS o reveal) com 'Oshtor' -> seguro (nome ja conhecido)
    paths.translations(tmp_path, "ch_50_09", "50_09").write_text(
        json.dumps({"lines": {"0x2": {"t": "Oshtor lidera."}}}), encoding="utf-8")
    leaks = spoiler_check.check(tmp_path)
    assert len(leaks) == 1 and leaks[0]["scene"] == "ch_50_01" and leaks[0]["forbidden"] == "Oshtor"
    # sem o nome -> limpo (prova que nao e sempre-positivo)
    paths.translations(tmp_path, "ch_50_01", "50_01").write_text(
        json.dumps({"lines": {"0x1": {"t": "Sim, Ukon chegou."}}}), encoding="utf-8")
    assert spoiler_check.check(tmp_path) == []


def test_spoiler_no_leak_in_committed_translations():
    # H6 (regressao sobre dados reais): nenhuma traducao commitada vaza spoiler de nome/titulo.
    import spoiler_check
    root = Path(__file__).resolve().parents[2] / "projects" / "utawarerumono"
    if not (root / "artifacts" / "spoiler_ledger.json").is_file():
        pytest.skip("projeto utawarerumono nao disponivel")
    leaks = spoiler_check.check(root)
    assert leaks == [], f"vazamento de spoiler nas traducoes: {leaks[:3]}"


def test_batch_smoke_evaluate():
    # O smoke vivo de batch (batch_smoke.py) toca a API real; aqui testamos OFFLINE a logica de
    # avaliacao — que ela PEGA cada modo de divergencia que ja nos custou dinheiro.
    import batch_smoke
    sc = "ch_00_00"
    healthy = [{"kind": "translate", "model": "claude-haiku-4-5", "batch": True, "cost_usd": 0.01},
               {"kind": "translate", "model": "claude-sonnet-4-6", "batch": True, "cost_usd": 0.01}]
    ok, probs = batch_smoke.evaluate({sc: "written"}, healthy, sc)
    assert ok and probs == []
    # (b) nao convergiu
    ok, probs = batch_smoke.evaluate({sc: "coverage_failed"}, healthy, sc)
    assert not ok and any("convergiu" in p for p in probs)
    # (c) Haiku sumiu (regressao tipo 400-do-effort) — so Sonnet no ledger
    ok, probs = batch_smoke.evaluate({sc: "written"}, [healthy[1]], sc)
    assert not ok and any("Haiku" in p for p in probs)
    # (d) caiu pro interativo full-price
    fell = healthy + [{"kind": "translate", "model": "claude-sonnet-4-6", "batch": False, "cost_usd": 0.5}]
    ok, probs = batch_smoke.evaluate({sc: "written"}, fell, sc)
    assert not ok and any("INTERATIVA" in p for p in probs)


def test_verify_status_parses_structured_line():
    # H1: run_scene le a linha VERIFY_STATUS (protocolo estruturado), nao faz grep de prosa.
    out = ("Capitulo ch_x: ...\n  round-trip identico: False\n"
           'VERIFY_STATUS: {"ok": false, "fitting_failure": true, "residuo_t4": 2, "out_of_file": 0, "n_fails": 1}\n'
           "\nFALHAS:\n  - resíduo T4 = 2 (esperado 0)\n")
    st = run_scene._verify_status(out)
    assert st["fitting_failure"] is True and st["residuo_t4"] == 2
    assert run_scene._verify_status("sem status aqui") == {}          # conector legado -> {}
    assert run_scene._verify_status("VERIFY_STATUS: {quebrado") == {}  # json invalido -> {} (nao explode)


def test_run_chapter_orders_and_resumes(monkeypatch, tmp_path):
    root = _fake_chapter(tmp_path, ("99_02", "99_01", "99_03"))   # fora de ordem de proposito
    (root / "artifacts" / "run_state.json").write_text(
        json.dumps({"scenes": {"ch_99_01": {"status": "verified", "verified": True}}}),
        encoding="utf-8")
    calls = []
    monkeypatch.setattr(run_chapter.RS, "run_scene",
                        lambda r, scene, **kw: calls.append(scene) or
                        {"status": "verified", "scene": scene, "verified": True})
    r = run_chapter.run_chapter(root, "99", backend="api")
    assert r["status"] == "complete"
    assert calls == ["ch_99_02", "ch_99_03"], "ch_99_01 ja verified deve ser pulado; resto em ordem"


def test_run_survives_non_utf8_subprocess_output():
    # REGRESSAO: um filho que emite byte nao-utf-8 (acento cp1252 no console Windows) NAO pode quebrar
    # a thread leitora do subprocess — era isso que derrubava o run_chapter no meio da run e deixava o
    # chip da UI preso (sem saida limpa). _run usa errors='replace' -> nunca quebra; ASCII fica intacto.
    code = r"import sys; sys.stdout.buffer.write(b'fora do arquivo \xed\n')"
    rc, out = run_scene._run([sys.executable, "-c", code])
    assert rc == 0
    assert "fora do arquivo" in out.lower(), "match ASCII deve sobreviver; byte ruim vira replacement"


def test_run_chapter_stops_on_failure(monkeypatch, tmp_path):
    root = _fake_chapter(tmp_path, ("99_01", "99_02"))
    monkeypatch.setattr(run_chapter.RS, "run_scene",
                        lambda r, scene, **kw:
                        {"status": "verify_failed" if scene == "ch_99_01" else "verified",
                         "scene": scene})
    r = run_chapter.run_chapter(root, "99", backend="api")
    assert r["status"] == "stopped" and r["stopped_at"] == "ch_99_01"


# ------------------------------- telemetria de custo --------------------------
# O ledger (api_ledger.jsonl) registra TODA chamada cobrada — inclusive cenas que falham/escalam,
# que o metrics.jsonl (resumo so-de-sucesso) perdia. cost_report agrega + cruza com run_state.

def test_cost_of_known_pricing():
    # Sonnet: in $3/M, out $15/M; cache_read = 0.1x in, cache_write = 1.25x in
    c = model.cost_of("claude-sonnet-4-6",
                      {"in": 1_000_000, "out": 1_000_000, "cache_read": 0, "cache_write": 0})
    assert round(c, 4) == round(3.0 + 15.0, 4)
    assert model.cost_of("modelo-inexistente", {"in": 9}) == 0.0
    assert model.cost_of("claude-opus-4-8", {}) == 0.0


def test_log_api_call_appends_ledger(tmp_path):
    (tmp_path / "artifacts").mkdir()
    model.log_api_call(tmp_path, "ch_99_01", "translate", "claude-sonnet-4-6",
                       {"in": 100, "out": 50, "cache_read": 0, "cache_write": 0})
    model.log_api_call(tmp_path, "ch_99_01", "translate", "claude-sonnet-4-6",
                       {"in": 200, "out": 80, "cache_read": 0, "cache_write": 0})   # retry: 2a chamada
    model.log_api_call(tmp_path, "ch_99_01", "back", "claude-opus-4-8",
                       {"in": 10, "out": 10, "cache_read": 0, "cache_write": 0})
    rows = [json.loads(l) for l in
            (tmp_path / "artifacts" / "api_ledger.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 3, "cada chamada cobrada = 1 linha (retries inclusos)"
    assert all(r["cost_usd"] > 0 for r in rows)
    # custo-verdade da cena soma TODAS as chamadas (run_scene._ledger_scene_cost)
    assert run_scene._ledger_scene_cost(tmp_path, "ch_99_01") == round(sum(r["cost_usd"] for r in rows), 5)
    # usage vazio nao registra (nao polui o ledger)
    model.log_api_call(tmp_path, "ch_99_01", "translate", "claude-sonnet-4-6", None)
    rows2 = (tmp_path / "artifacts" / "api_ledger.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(rows2) == 3


def test_cost_report_aggregates_and_flags_waste(tmp_path):
    art = tmp_path / "artifacts"
    art.mkdir()
    # cena boa (fechou verified) + cena ruim (so gastou, nao fechou) -> o gasto da ruim e DESPERDICIO
    model.log_api_call(tmp_path, "ch_99_01", "translate", "claude-sonnet-4-6", {"in": 1000, "out": 500})
    model.log_api_call(tmp_path, "ch_99_02", "translate", "claude-sonnet-4-6", {"in": 1000, "out": 500})
    model.log_api_call(tmp_path, "ch_99_02", "translate", "claude-sonnet-4-6", {"in": 1000, "out": 500})
    (art / "run_state.json").write_text(json.dumps(
        {"scenes": {"ch_99_01": {"status": "verified", "verified": True},
                    "ch_99_02": {"status": "verify_failed", "verified": False}}}), encoding="utf-8")
    rep = cost_report.report(tmp_path)
    assert rep["n_calls"] == 3
    assert rep["verified_scenes"] == 1
    # desperdicio = so o gasto da 99_02 (2 chamadas), nao da 99_01
    assert rep["wasted_usd"] == rep["by_scene"]["ch_99_02"]["cost_usd"]
    assert rep["wasted_usd"] < rep["total_usd"]
    assert rep["by_kind"]["translate"] == rep["total_usd"]
    assert cost_report._fmt(rep, by_scene=True)   # nao quebra ao formatar


# ------------------------------- dedup por TM (R5 custo) ----------------------
# Reaproveita traducao de OUTRA cena (mesma fonte) -> nao re-gera (corta tokens de saida).

def _pack_for_reuse(lines, tm_exact, scene_id="12_09"):
    return {"scene_id": scene_id, "lines": lines, "tm_exact": tm_exact}


def test_reuse_picks_cross_scene_hit():
    pack = _pack_for_reuse(
        [{"offset": "0x1", "source": "Yes."}, {"offset": "0x2", "source": "Brand new line."}],
        [{"source": "Yes.", "target": "Sim.", "speaker": "Haku", "from_scene": "12_03"}])
    reuse = model._select_reuse(pack, enabled=True)
    assert set(reuse) == {"0x1"}, "so a linha com hit de TM e reaproveitada"
    assert reuse["0x1"]["t"] == "Sim." and reuse["0x1"]["risk_level"] == "low"


def test_reuse_excludes_own_scene():
    # a TM contem a PROPRIA cena (re-run) -> NAO reusar (sabotaria o escalonamento de fitting)
    pack = _pack_for_reuse(
        [{"offset": "0x1", "source": "Yes."}],
        [{"source": "Yes.", "target": "Sim.", "speaker": "Haku", "from_scene": "12_09"}],
        scene_id="12_09")
    assert model._select_reuse(pack, enabled=True) == {}


def test_reuse_parity_guard():
    # chave de TM ignora \n; se a traducao tem nº de quebras != da fonte ATUAL, NAO reusa (build_plan reprova)
    tok = context_pack.TOKEN
    pack = _pack_for_reuse(
        [{"offset": "0x1", "source": f"A{tok}B"}],                 # fonte tem 1 quebra
        [{"source": "A B", "target": "A B sem quebra", "speaker": "X", "from_scene": "12_03"}])
    assert model._select_reuse(pack, enabled=True) == {}, "paridade de quebra bloqueia reuso"
    pack2 = _pack_for_reuse(
        [{"offset": "0x1", "source": f"A{tok}B"}],
        [{"source": "A B", "target": f"Ce{tok}De", "speaker": "X", "from_scene": "12_03"}])
    assert set(model._select_reuse(pack2, enabled=True)) == {"0x1"}, "quebras casando -> reusa"


def test_reuse_disabled_on_escalation():
    pack = _pack_for_reuse(
        [{"offset": "0x1", "source": "Yes."}],
        [{"source": "Yes.", "target": "Sim.", "speaker": "Haku", "from_scene": "12_03"}])
    assert model._select_reuse(pack, enabled=False) == {}, "escalonamento re-traduz fresco (sem reuso)"


# ------------------------------- escalonamento cirurgico ----------------------
# Re-traduz SO as linhas acima do budget (nao a cena inteira) -> corte de custo no caminho apertado.

def test_over_offsets_selects_only_overflowing():
    budgets = {"0x1": 10, "0x2": 5, "0x3": None, "0x4": 8}
    lines = {
        "0x1": {"t": "ok"},                       # 2 bytes <= 10 -> nao
        "0x2": {"t": "muito longo demais"},       # > 5 -> SIM
        "0x3": {"t": "qualquer"},                 # budget None -> ignora
        "0x4": {"t": "coração"},                  # translit 'coracao' = 7 <= 8 -> nao (acentos somem)
    }
    assert model._over_offsets(budgets, lines, 1.0) == ["0x2"]
    assert model._over_offsets({"0x2": 5}, {"0x2": {"t": "seis66"}}, 2.0) == []   # tolerancia folgada


# ------------------------------- batch API (R5 custo, -50%) -------------------
import types as _types   # noqa: E402


def test_cost_of_batch_is_half():
    u = {"in": 1_000_000, "out": 1_000_000}
    full = model.cost_of("claude-sonnet-4-6", u)
    assert round(model.cost_of("claude-sonnet-4-6", u, batch=True), 6) == round(full * 0.5, 6)


def test_translate_params_none_when_fully_reused():
    pack = {"scene_id": "99_01", "lines": [{"offset": "0x1", "source": "Yes."}],
            "tm_exact": [{"source": "Yes.", "target": "Sim.", "speaker": "X", "from_scene": "99_02"}]}
    params, reuse, novel = model._translate_params(pack, "claude-sonnet-4-6")
    assert params is None and novel == [] and set(reuse) == {"0x1"}


def _btext(offsets):
    return json.dumps({"lines": [
        {"offset": o, "speaker": "X", "tone_register": "n", "intent": "i",
         "risk_level": "low", "risk_notes": "", "t": "Oi"} for o in offsets]})


def test_parse_batch_lines_and_coverage():
    tok = context_pack.TOKEN
    pack = {"scene_id": "99_01", "tm_exact": [],
            "lines": [{"offset": "0x1", "source": "Hi"}, {"offset": "0x2", "source": f"A{tok}B"}]}
    lines = model._parse_batch_lines(pack, _btext(["0x1"]))   # so 0x1
    assert set(lines) == {"0x1"}
    miss, badpar = model._batch_coverage(pack, lines)
    assert miss == ["0x2"] and badpar == []
    lines["0x2"] = {"t": f"C{tok}D"}                          # mescla 0x2 com paridade certa
    assert model._batch_coverage(pack, lines) == ([], [])
    lines["0x2"] = {"t": "CD sem quebra"}                     # paridade errada -> badpar
    assert model._batch_coverage(pack, lines)[1] == ["0x2"]


def _fake_msg(text, usage=(100, 50)):
    block = _types.SimpleNamespace(type="text", text=text)
    u = _types.SimpleNamespace(input_tokens=usage[0], output_tokens=usage[1],
                               cache_read_input_tokens=0, cache_creation_input_tokens=0)
    return _types.SimpleNamespace(content=[block], usage=u)


# a Batch API real rejeita custom_id fora deste padrao (400) — o fake VALIDA isso p/ pegar regressao
# (ex.: o separador '@@' do tiering quebrava ao vivo mas passava com fake permissivo). Ver _FakeBatches.
_CUSTOM_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")


class _FakeBatches:
    """Fake da Batch API ciente de RODADAS e de TIER: scene_rounds[scene] = [texto_r0, texto_r1, ...];
    custom_id e 'scene__tier' -> a fila e por CENA. results() devolve o proximo texto da cena (vazio se
    acabar). models[] registra os modelos submetidos (p/ checar roteamento de tier). VALIDA o padrao do
    custom_id como a API real (raise se invalido)."""
    def __init__(self, scene_rounds):
        self.scene_rounds = {k: list(v) for k, v in scene_rounds.items()}
        self._submitted = []
        self.models = []
        self.contents = []        # (custom_id, user_content) de cada request submetido (p/ checar a nota)

    def create(self, requests):
        for r in requests:
            if not _CUSTOM_ID_RE.match(r["custom_id"]):
                raise ValueError(f"custom_id invalido p/ Batch API: {r['custom_id']!r} "
                                 f"(deve casar ^[a-zA-Z0-9_-]{{1,64}}$)")
            # Haiku 4.5 / Sonnet 4.5 dao 400 com output_config.effort — o fake VALIDA (pega regressao:
            # o batch mandava effort p/ TODO modelo -> os requests Haiku do tier cheap 400-avam ao vivo).
            mdl = r["params"]["model"]
            if (mdl.startswith("claude-haiku") or mdl == "claude-sonnet-4-5") \
                    and "effort" in r["params"].get("output_config", {}):
                raise ValueError(f"output_config.effort invalido p/ {mdl} (Batch API 400)")
        self._submitted = [r["custom_id"] for r in requests]
        self.models += [r["params"]["model"] for r in requests]
        self.contents += [(r["custom_id"], r["params"]["messages"][0]["content"]) for r in requests]
        return _types.SimpleNamespace(id="batch_x", processing_status="in_progress")

    def retrieve(self, _id):
        return _types.SimpleNamespace(processing_status="ended")

    def results(self, _id):
        out = []
        for cid in self._submitted:
            scene = cid.split("__", 1)[0]
            q = self.scene_rounds.get(scene, [])
            text = q.pop(0) if q else _btext([])
            out.append(_types.SimpleNamespace(custom_id=cid, result=_types.SimpleNamespace(
                type="succeeded", message=_fake_msg(text))))
        return iter(out)


def test_batch_translate_accumulates_across_rounds(monkeypatch, tmp_path):
    # 3 cenas: 99_01 cobre na 1a; 99_02 DROPA 1 linha na 1a e cobre na 2a (ACUMULA -> nao cai p/
    # interativo); 99_03 nunca cobre -> coverage_failed apos as rodadas.
    for s in ("ch_99_01", "ch_99_02", "ch_99_03"):
        (tmp_path / "artifacts" / s).mkdir(parents=True)
    packs = {
        "ch_99_01": {"scene_id": "99_01", "tm_exact": [], "lines": [{"offset": "0x1", "source": "Hi"}]},
        "ch_99_02": {"scene_id": "99_02", "tm_exact": [],
                     "lines": [{"offset": "0x9", "source": "A"}, {"offset": "0xa", "source": "B"}]},
        "ch_99_03": {"scene_id": "99_03", "tm_exact": [], "lines": [{"offset": "0xb", "source": "C"}]},
    }
    monkeypatch.setattr(context_pack, "write_pack", lambda r, s: packs[s])
    monkeypatch.setattr(context_pack, "render_prompt", lambda pack, carta="": "PROMPT")
    monkeypatch.setattr(model, "_carta_text", lambda: "CARTA")
    fake = _types.SimpleNamespace(messages=_types.SimpleNamespace(batches=_FakeBatches({
        "ch_99_01": [_btext(["0x1"])],                       # cobre na rodada 0
        "ch_99_02": [_btext(["0x9"]), _btext(["0xa"])],      # rodada 0 dropa 0xa; rodada 1 completa
        "ch_99_03": [_btext([]), _btext([])],                # nunca cobre
    })))
    monkeypatch.setattr(model, "_client", lambda: fake)
    st = model.batch_translate(tmp_path, ["ch_99_01", "ch_99_02", "ch_99_03"],
                               poll_seconds=0, max_rounds=2)
    assert st == {"ch_99_01": "written", "ch_99_02": "written", "ch_99_03": "coverage_failed"}
    # 99_02 ACUMULOU as duas linhas (re-batch so do que faltou)
    d = json.loads((tmp_path / "artifacts" / "ch_99_02" / "translations_99_02.json").read_text("utf-8"))
    assert set(d["lines"]) == {"0x9", "0xa"}
    assert not (tmp_path / "artifacts" / "ch_99_03" / "translations_99_03.json").is_file()
    # FEEDBACK CORRETIVO: a re-rodada (rnd>0) de 99_02 leva a nota com o offset que faltou (0xa) — sem
    # isso o batch repetia o erro e cenas de narracao caiam pro interativo full-price (coverage_failed).
    fb = fake.messages.batches
    c_9902 = [c for cid, c in fb.contents if cid.startswith("ch_99_02")]
    assert "CORRECAO NECESSARIA" not in c_9902[0], "rodada 0 nao leva nota (cena inteira, sem feedback)"
    assert any("CORRECAO NECESSARIA" in c and "0xa" in c for c in c_9902[1:]), \
        "re-rodada deve anexar a nota corretiva com os offsets faltantes/paridade-errada"
    # ledger: 99_01 x1, 99_02 x2 (2 rodadas), 99_03 x2; tudo batch=True, custo 50%
    rows = [json.loads(l) for l in
            (tmp_path / "artifacts" / "api_ledger.jsonl").read_text("utf-8").splitlines()]
    n = {}
    for r in rows:
        n[r["scene"]] = n.get(r["scene"], 0) + 1
        assert r["batch"] is True
        assert r["model"] == model.MODEL_TRANSLATE_CHEAP, "linhas single-line -> tier cheap (Haiku)"
    assert n == {"ch_99_01": 1, "ch_99_02": 2, "ch_99_03": 2}


def test_tier_of_routes_by_break_token():
    tok = context_pack.TOKEN
    assert model._tier_of("linha simples") == "cheap"        # sem \n -> Haiku
    assert model._tier_of(f"linha{tok}com quebra") == "main"  # com \n -> Sonnet
    assert model._tier_of("") == "cheap"


def test_batch_tiering_routes_models(monkeypatch, tmp_path):
    # cena com 1 linha single-line (-> Haiku) e 1 multi-linha (-> Sonnet): 2 requests, 2 modelos
    tok = context_pack.TOKEN
    (tmp_path / "artifacts" / "ch_99_01").mkdir(parents=True)
    packs = {"ch_99_01": {"scene_id": "99_01", "tm_exact": [],
                          "lines": [{"offset": "0x1", "source": "simples"},
                                    {"offset": "0x2", "source": f"tem{tok}quebra"}]}}
    monkeypatch.setattr(context_pack, "write_pack", lambda r, s: packs[s])
    monkeypatch.setattr(context_pack, "render_prompt", lambda pack, carta="": "PROMPT")
    monkeypatch.setattr(model, "_carta_text", lambda: "CARTA")
    fb = _FakeBatches({"ch_99_01": [_btext(["0x1"]) ]})      # rodada 0 nao importa o conteudo exato aqui
    # texto que cobre cada offset com paridade certa
    good = json.dumps({"lines": [
        {"offset": "0x1", "speaker": "X", "tone_register": "n", "intent": "i",
         "risk_level": "low", "risk_notes": "", "t": "ok"},
        {"offset": "0x2", "speaker": "X", "tone_register": "n", "intent": "i",
         "risk_level": "low", "risk_notes": "", "t": f"a{tok}b"}]})
    fb.scene_rounds["ch_99_01"] = [good]
    monkeypatch.setattr(model, "_client",
                        lambda: _types.SimpleNamespace(messages=_types.SimpleNamespace(batches=fb)))
    st = model.batch_translate(tmp_path, ["ch_99_01"], poll_seconds=0, max_rounds=1)
    # os DOIS modelos foram submetidos (Haiku p/ single-line, Sonnet p/ multi-linha)
    assert model.MODEL_TRANSLATE_CHEAP in fb.models and model.MODEL_TRANSLATE in fb.models
    # tiering desligado -> tudo no modelo principal
    fb2 = _FakeBatches({"ch_99_01": [good]})
    monkeypatch.setattr(model, "_client",
                        lambda: _types.SimpleNamespace(messages=_types.SimpleNamespace(batches=fb2)))
    model._write_translations(tmp_path, "ch_99_01", {"lines": {}})   # limpa p/ re-rodar
    (tmp_path / "artifacts" / "ch_99_01" / "translations_99_01.json").unlink()
    model.batch_translate(tmp_path, ["ch_99_01"], poll_seconds=0, max_rounds=1, tiered=False)
    assert model.MODEL_TRANSLATE_CHEAP not in fb2.models


class _FakeTruncating:
    """Imita a FALHA REAL do endpoint de batch (medida no 15_06): TRUNCA a resposta nas primeiras
    `limit` linhas pedidas (deterministico). render_prompt embute os offsets pedidos (em ordem) p/ o
    fake saber o que foi pedido e devolver so o prefixo. So as linhas alem do `limit` ficam faltando."""
    def __init__(self, limit):
        self.limit = limit
        self._reqs = []
    def create(self, requests):
        self._reqs = [(r["custom_id"], r["params"]["messages"][0]["content"]) for r in requests]
        return _types.SimpleNamespace(id="b", processing_status="x")
    def retrieve(self, _id):
        return _types.SimpleNamespace(processing_status="ended")
    def results(self, _id):
        tok = context_pack.TOKEN
        out = []
        for cid, content in self._reqs:
            asked = [w[2:] for w in content.split() if w.startswith("o:")]   # offsets embutidos, em ordem
            keep = asked[:self.limit]                                        # TRUNCA no teto
            lines = [{"offset": o, "speaker": "X", "tone_register": "n", "intent": "i",
                      "risk_level": "low", "risk_notes": "", "t": f"a{tok}b"} for o in keep]
            out.append(_types.SimpleNamespace(custom_id=cid, result=_types.SimpleNamespace(
                type="succeeded", message=_fake_msg(json.dumps({"lines": lines})))))
        return iter(out)


def test_batch_chunking_beats_truncation(monkeypatch, tmp_path):
    # REGRESSAO (causa-raiz cap.15, medida no 15_06): o endpoint de batch TRUNCA a saida estruturada
    # longa (~100 linhas/resposta, deterministico -> 120/221 sempre faltando, re-mandar nao adianta).
    # Fix: CHUNKING — quebrar a cena em requests <= _BATCH_CHUNK; cada um volta completo -> converge.
    tok = context_pack.TOKEN
    (tmp_path / "artifacts" / "ch_96_01").mkdir(parents=True)
    lines = [{"offset": f"0x{i:02x}", "source": f"L{i}{tok}x"} for i in range(20)]   # 20 multi-linha
    packs = {"ch_96_01": {"scene_id": "96_01", "tm_exact": [], "lines": lines}}
    monkeypatch.setattr(context_pack, "write_pack", lambda r, s: packs[s])
    monkeypatch.setattr(context_pack, "render_prompt",
                        lambda pack, carta="": "P " + " ".join("o:" + r["offset"] for r in pack["lines"]))
    monkeypatch.setattr(model, "_carta_text", lambda: "CARTA")
    trunc = _FakeTruncating(5)        # o "modelo" so devolve 5 linhas por resposta

    # SEM chunking (chunk grande): 1 request de 20 -> volta 5; em 2 rodadas nao alcança as 20 -> falha
    monkeypatch.setattr(model, "_BATCH_CHUNK", 100)
    monkeypatch.setattr(model, "_client",
                        lambda: _types.SimpleNamespace(messages=_types.SimpleNamespace(batches=trunc)))
    st = model.batch_translate(tmp_path, ["ch_96_01"], poll_seconds=0, max_rounds=2)
    assert st["ch_96_01"] == "coverage_failed", "sem chunking, a truncação impede a cobertura no orçamento de rodadas"

    # COM chunking (5 linhas/chunk <= teto de truncação): cada chunk volta completo -> converge na rodada 0
    (tmp_path / "artifacts" / "ch_96_01" / "translations_96_01.json").unlink(missing_ok=True)
    trunc2 = _FakeTruncating(5)
    monkeypatch.setattr(model, "_BATCH_CHUNK", 5)
    monkeypatch.setattr(model, "_client",
                        lambda: _types.SimpleNamespace(messages=_types.SimpleNamespace(batches=trunc2)))
    st = model.batch_translate(tmp_path, ["ch_96_01"], poll_seconds=0, max_rounds=2)
    assert st["ch_96_01"] == "written", "com chunking (<= teto) a cena CONVERGE no batch (-50% capturado)"
    d = json.loads((tmp_path / "artifacts" / "ch_96_01" / "translations_96_01.json").read_text("utf-8"))
    assert len(d["lines"]) == 20, "todas as 20 linhas cobertas via chunks"


def test_batch_retries_transient_network(monkeypatch, tmp_path):
    # REGRESSAO (cap.18): o back-batch morreu por TIMEOUT DE REDE — as chamadas de batch (create/results)
    # nao tinham backoff (so o caminho interativo/_stream_final tinha). Agora _with_backoff cobre TODOS
    # os pontos de rede do batch. Fake levanta erro transitorio 1x em create E em results -> deve re-tentar.
    import httpx
    monkeypatch.setattr(model.time, "sleep", lambda *a, **k: None)   # nao espera o backoff no teste
    (tmp_path / "artifacts" / "ch_98_01").mkdir(parents=True)
    packs = {"ch_98_01": {"scene_id": "98_01", "tm_exact": [], "lines": [{"offset": "0x1", "source": "Hi"}]}}
    monkeypatch.setattr(context_pack, "write_pack", lambda r, s: packs[s])
    monkeypatch.setattr(context_pack, "render_prompt", lambda pack, carta="": "P")
    monkeypatch.setattr(model, "_carta_text", lambda: "C")
    n = {"create": 0, "results": 0}

    class _Flaky(_FakeBatches):
        def create(self, requests):
            n["create"] += 1
            if n["create"] == 1:
                raise httpx.ConnectError("blip de rede")     # cai na 1a, cura no retry
            return super().create(requests)

        def results(self, _id):
            n["results"] += 1
            if n["results"] == 1:
                raise httpx.ReadTimeout("timeout no fetch dos resultados")
            return super().results(_id)

    fb = _Flaky({"ch_98_01": [_btext(["0x1"])]})
    monkeypatch.setattr(model, "_client",
                        lambda: _types.SimpleNamespace(messages=_types.SimpleNamespace(batches=fb)))
    st = model.batch_translate(tmp_path, ["ch_98_01"], poll_seconds=0, max_rounds=1)
    assert st["ch_98_01"] == "written", "retry de rede -> o batch ainda converge (nao morre no timeout)"
    assert n["create"] == 2 and n["results"] == 2, "create e results foram re-tentados 1x apos o erro transitorio"


def test_merge_best_parity_keeps_good_line(monkeypatch):
    # uma re-rodada que REGRIDE uma linha ja boa nao pode desfazer o ganho (o dict.update cego perdia)
    tok = context_pack.TOKEN
    srcmap = {"0x1": f"a{tok}b"}
    dest = {"0x1": {"t": f"x{tok}y"}}                         # ja BOA (1 token, como a fonte)
    model._merge_best_parity(dest, {"0x1": {"t": "sem quebra"}}, srcmap)   # nova RUIM (0 token)
    assert dest["0x1"]["t"] == f"x{tok}y", "linha boa preservada contra regressao"
    model._merge_best_parity(dest, {"0x1": {"t": f"p{tok}q"}}, srcmap)     # nova tb boa -> usa a nova
    assert dest["0x1"]["t"] == f"p{tok}q"


def test_batch_translate_resumes_existing(monkeypatch, tmp_path):
    # cena ja com translations completas em disco -> NAO re-batcha (idempotente; nao re-gasta o pago)
    (tmp_path / "artifacts" / "ch_99_01").mkdir(parents=True)
    packs = {"ch_99_01": {"scene_id": "99_01", "tm_exact": [], "lines": [{"offset": "0x1", "source": "Hi"}]}}
    monkeypatch.setattr(context_pack, "write_pack", lambda r, s: packs[s])
    monkeypatch.setattr(context_pack, "render_prompt", lambda pack, carta="": "PROMPT")
    monkeypatch.setattr(model, "_carta_text", lambda: "CARTA")
    model._write_translations(tmp_path, "ch_99_01", {"lines": {"0x1": {"t": "Oi"}}})   # traducao previa

    class _Exploding:                                    # qualquer submissao = falha o teste
        def create(self, requests): raise AssertionError("nao deveria submeter batch (cena ja traduzida)")
        def retrieve(self, _id): raise AssertionError("nao deveria")
        def results(self, _id): raise AssertionError("nao deveria")
    monkeypatch.setattr(model, "_client",
                        lambda: _types.SimpleNamespace(messages=_types.SimpleNamespace(batches=_Exploding())))
    st = model.batch_translate(tmp_path, ["ch_99_01"], poll_seconds=0)
    assert st["ch_99_01"] == "written"
    assert not (tmp_path / "artifacts" / "api_ledger.jsonl").is_file(), "zero chamada -> zero ledger"


def test_run_chapter_batch_marks_pretranslated(monkeypatch, tmp_path):
    root = _fake_chapter(tmp_path, ("99_01", "99_02"))
    monkeypatch.setattr(run_chapter.M, "batch_translate",
                        lambda r, scenes, **kw: {s: "written" for s in scenes})
    monkeypatch.setattr(run_chapter.kb_gate, "check", lambda r, s: {"problems": [], "warnings": []})
    seen = {}
    monkeypatch.setattr(run_chapter.RS, "run_scene",
                        lambda r, scene, **kw: seen.__setitem__(scene, kw.get("pretranslated")) or
                        {"status": "verified", "scene": scene, "verified": True})
    run_chapter.run_chapter(root, "99", backend="api", batch=True)
    assert seen == {"ch_99_01": True, "ch_99_02": True}, "cenas do batch devem ir pretranslated"


def test_run_chapter_max_usd_aborts(monkeypatch, tmp_path):
    # TETO DE GASTO: aborta ANTES da proxima cena quando o custo do capitulo passa de --max-usd.
    root = _fake_chapter(tmp_path, ("99_01", "99_02", "99_03"))
    monkeypatch.setattr(run_chapter.kb_gate, "check", lambda r, s: {"problems": [], "warnings": []})
    monkeypatch.setattr(run_chapter, "_verified", lambda r, s: False)
    ran = []
    monkeypatch.setattr(run_chapter.RS, "run_scene",
                        lambda r, scene, **kw: ran.append(scene) or
                        {"status": "verified", "scene": scene, "verified": True})
    # custo do capitulo cresce $2 por cena ja rodada (mock do ledger)
    monkeypatch.setattr(run_chapter, "_chapter_cost", lambda r, c: 2.0 * len(ran))
    res = run_chapter.run_chapter(root, "99", backend="api", max_usd=3.0)
    # antes 99_01: $0<3 roda; antes 99_02: $2<3 roda; antes 99_03: $4>=3 ABORTA
    assert res["status"] == "stopped_budget" and res["stopped_at"] == "ch_99_03"
    assert ran == ["ch_99_01", "ch_99_02"], "para antes da 3a cena (teto estourado)"


# ----------------------- back-translation em BATCH (Tier 1 de custo) ----------------------

def _plan(offsets_risk):
    """translation_plan minimo: [{offset, risk_level, text_source, base_translation, speaker}]."""
    return {"lines": [{"offset": o, "risk_level": rk, "text_source": f"src{o}",
                       "base_translation": f"alvo{o}", "speaker": "X", "risk_notes": ""}
                      for o, rk in offsets_risk]}


def _backtext(offsets):
    return json.dumps({"entries": [{"offset": o, "back_en": "back", "verdict": "pass", "note": ""}
                                   for o in offsets]})


def test_high_risk_lines_reads_plan(tmp_path):
    d = tmp_path / "artifacts" / "ch_77_01"
    d.mkdir(parents=True)
    (d / "translation_plan_77_01.json").write_text(
        json.dumps(_plan([("0x1", "low"), ("0x2", "high"), ("0x3", "critical")])), encoding="utf-8")
    hl = model.high_risk_lines(tmp_path, "ch_77_01")
    assert [h["offset"] for h in hl] == ["0x2", "0x3"]        # so high/critical
    assert hl[0]["source"] == "src0x2" and hl[0]["target"] == "alvo0x2"
    assert model.high_risk_lines(tmp_path, "ch_77_99") == []  # sem plano -> vazio


def test_back_params_deterministic_shape():
    p1 = model._back_params([{"offset": "0x1", "source": "a", "target": "b", "speaker": "X"}], "claude-opus-4-8")
    p2 = model._back_params([{"offset": "0x1", "source": "a", "target": "b", "speaker": "X"}], "claude-opus-4-8")
    assert p1 == p2 and p1["model"] == "claude-opus-4-8"
    assert p1["output_config"]["format"]["schema"] is model._BACK_SCHEMA


def test_batch_back_translate(monkeypatch, tmp_path):
    # 3 cenas: 77_01 e 77_02 com linhas high -> batch; 77_03 sem high -> no_high (sem request).
    for s, plan in (("ch_77_01", _plan([("0x1", "high"), ("0x2", "low")])),
                    ("ch_77_02", _plan([("0x9", "critical")])),
                    ("ch_77_03", _plan([("0xb", "low")]))):
        d = tmp_path / "artifacts" / s
        d.mkdir(parents=True)
        (d / f"translation_plan_{context_pack.scene_id_of(s)}.json").write_text(json.dumps(plan), encoding="utf-8")
    fb = _FakeBatches({"ch_77_01": [_backtext(["0x1"])], "ch_77_02": [_backtext(["0x9"])]})
    monkeypatch.setattr(model, "_client",
                        lambda: _types.SimpleNamespace(messages=_types.SimpleNamespace(batches=fb)))
    st = model.batch_back_translate(tmp_path, ["ch_77_01", "ch_77_02", "ch_77_03"], poll_seconds=0)
    assert st == {"ch_77_01": "reviewed", "ch_77_02": "reviewed", "ch_77_03": "no_high"}
    assert fb.models == [model.MODEL_BACK, model.MODEL_BACK]   # so as 2 com high foram submetidas, Opus
    bt = json.loads((tmp_path / "artifacts" / "ch_77_01" / "back_translation_77_01.json").read_text("utf-8"))
    assert bt["reviewed"] == 1 and bt["entries"][0]["offset"] == "0x1"
    rows = [json.loads(l) for l in
            (tmp_path / "artifacts" / "api_ledger.jsonl").read_text("utf-8").splitlines()]
    assert len(rows) == 2 and all(r["batch"] is True and r["kind"] == "back" for r in rows)

    # RESUME idempotente: re-rodar nao re-cobra (back_translation ja existe)
    fb2 = _FakeBatches({"ch_77_01": [_backtext(["0x1"])], "ch_77_02": [_backtext(["0x9"])]})
    monkeypatch.setattr(model, "_client",
                        lambda: _types.SimpleNamespace(messages=_types.SimpleNamespace(batches=fb2)))
    st2 = model.batch_back_translate(tmp_path, ["ch_77_01", "ch_77_02"], poll_seconds=0)
    assert st2 == {"ch_77_01": "reviewed", "ch_77_02": "reviewed"} and fb2.models == []


# ----------------------------- driver de Fase 0 ------------------------------
import kb_phase  # noqa: E402


def _kb_phase_proj(tmp_path, scenes, glossary_terms=(), entities=(), *, reconciled=True, frontier="00_00"):
    art = tmp_path / "artifacts"
    import csv as _csv
    import io as _io
    for scene, lines in scenes.items():
        d = art / scene
        d.mkdir(parents=True)
        buf = _io.StringIO()
        w = _csv.writer(buf)
        w.writerow(["offset", "text_source", "byte_budget"])
        for i, t in enumerate(lines):
            w.writerow([f"0x{i}", t, 80])
        (d / "dialogs.csv").write_text(buf.getvalue(), encoding="utf-8")
    g = "term,category,target_translation,handling_rule,spoiler_level,aliases,notes\n" + "".join(
        f"{t},Cat,X,manter,none,,\n" for t in glossary_terms)
    (art / "glossary.csv").write_text(g, encoding="utf-8")
    e = "canonical_name,category,aliases,importance,confidence,notes\n" + "".join(
        f"{n},Cat,{al},main,high,\n" for n, al in entities)
    (art / "entities.csv").write_text(e, encoding="utf-8")
    (art / "research_log.md").write_text(
        "**Status:** reconciled\n" if reconciled else "**Status:** draft\n", encoding="utf-8")
    (tmp_path / "project.json").write_text(
        json.dumps({"connector": {}, "kb_frontier": frontier}, indent=2), encoding="utf-8")
    return tmp_path


def test_kb_phase_clean_cand_strips_noise():
    assert kb_phase._clean_cand("CARRY") == ""                  # ALL-CAPS grito
    assert kb_phase._clean_cand("AARGH OW") == ""
    assert kb_phase._clean_cand("M-Master Haku") == "Haku"      # gagueira + titulo de borda
    assert kb_phase._clean_cand("The Mystery Twins") == "Mystery Twins"  # stopword de borda aparada
    assert kb_phase._clean_cand("Sword of Truth") == "Sword of Truth"    # stopword INTERIOR mantida


def test_kb_phase_covered_titles_and_plural():
    kb = kb_phase._kb_blob_from(["Haku", "Ukon", "Cohort", "Oshtor"], [])
    assert kb_phase._covered("Master Haku", kb)                 # titulo + nome coberto
    assert kb_phase._covered("Ukon Cohorts", kb)                # plural casa singular 'Cohort'
    assert kb_phase._covered("Oshtor", kb)
    assert not kb_phase._covered("Mystery Twins", kb)


def test_kb_phase_discover_classifies(tmp_path):
    root = _kb_phase_proj(
        tmp_path,
        {"ch_77_01": ["Oshtor met the Mystery Twins.", "The Ukon Cohorts marched. CARRY on."],
         "ch_77_02": ["Look, the Mystery Twins again!", "The Imperial Guard stood firm."]},
        glossary_terms=["Oshtor", "Ukon", "Cohort"])
    d = kb_phase.discover(root, "77")
    cov = {r["cand"] for r in d["covered"]}
    blk = {r["cand"] for r in d["block"]}
    assert "Ukon Cohorts" in cov and "Oshtor" in cov         # cobertos (plural/nome)
    assert "Mystery Twins" in blk                            # recorre em 2 cenas -> bloqueia
    assert "Imperial Guard" not in blk                       # 1 cena -> nao bloqueia
    assert "CARRY" not in (blk | {r["cand"] for r in d["gap"]})  # grito filtrado


def test_kb_phase_coverage_blocks_then_passes(tmp_path):
    base = {"ch_77_01": ["Oshtor met the Mystery Twins."],
            "ch_77_02": ["The Mystery Twins fled."]}
    root = _kb_phase_proj(tmp_path, base, glossary_terms=["Oshtor"])
    cov = kb_phase.coverage(root, "77")
    assert any("Mystery Twins" in p for p in cov["problems"])  # bloqueia: termo recorrente fora da KB

    root2 = _kb_phase_proj(tmp_path / "ok", base, glossary_terms=["Oshtor", "Mystery Twins"])
    assert kb_phase.coverage(root2, "77")["problems"] == []      # agora coberto -> passa

    root3 = _kb_phase_proj(tmp_path / "unrec", base, glossary_terms=["Oshtor", "Mystery Twins"],
                        reconciled=False)
    assert any("reconciled" in p for p in kb_phase.coverage(root3, "77")["problems"])


def test_kb_phase_apply_frontier_advances_only(tmp_path):
    root = _kb_phase_proj(tmp_path, {"ch_77_01": ["Hi."], "ch_77_03": ["Bye."]}, frontier="77_01")
    assert kb_phase.apply_frontier(root, "77") == "77_03"        # avanca p/ ultimo scene_id
    assert '"kb_frontier": "77_03"' in (root / "project.json").read_text("utf-8")
    assert kb_phase.apply_frontier(root, "77") == "77_03"        # idempotente, nao regride
    # nunca regride: fronteira ja adiante
    root2 = _kb_phase_proj(tmp_path / "ahead", {"ch_77_01": ["Hi."]}, frontier="99_00")
    assert kb_phase.apply_frontier(root2, "77") == "99_00"


# ------------------------------- governanca -----------------------------------

def test_no_work_text_in_runtime_scripts():
    """Nenhuma fala/traducao do corpus pode estar hardcoded nos .py do runtime."""
    phrases = set()
    art = PROJECT / "artifacts"
    csvs = list(art.glob("approved_*.csv")) + list(art.glob("*/approved_*.csv"))
    import csv as _csv
    for f in csvs:
        with f.open(encoding="utf-8") as fh:
            for r in _csv.DictReader(fh):
                t = (r.get("text_target") or "").replace("\\n", " ")
                n = _norm_accents(t)
                if len(n) >= 22:                 # so frases longas (evita falso-positivo de palavras comuns)
                    phrases.add(n)
    assert phrases, "esperava frases do corpus p/ o guard"
    for py in _HERE.glob("*.py"):
        src = _norm_accents(py.read_text(encoding="utf-8"))
        hit = next((p for p in phrases if p in src), None)
        assert hit is None, f"work-text hardcoded em {py.name}: '{hit[:40]}...'"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
