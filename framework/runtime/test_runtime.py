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
    assert f"translations_{context_pack.sfx_of(SCENE)}.json" in txt


# ------------------------------- budget (translit) ----------------------------

def test_translit_len_drops_accents():
    # comprimento medido na forma transliterada (o que vai p/ os bytes): acentos/cedilha somem
    assert model._translit_len("Glossário") == len("Glossario")
    assert model._translit_len("coração") == len("coracao")
    assert model._translit_len("abc") == 3


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

def _pack_for_reuse(lines, tm_exact, sfx="12_09"):
    return {"sfx": sfx, "lines": lines, "tm_exact": tm_exact}


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
        sfx="12_09")
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
    pack = {"sfx": "99_01", "lines": [{"offset": "0x1", "source": "Yes."}],
            "tm_exact": [{"source": "Yes.", "target": "Sim.", "speaker": "X", "from_scene": "99_02"}]}
    params, reuse, novel = model._translate_params(pack, "claude-sonnet-4-6")
    assert params is None and novel == [] and set(reuse) == {"0x1"}


def _btext(offsets):
    return json.dumps({"lines": [
        {"offset": o, "speaker": "X", "tone_register": "n", "intent": "i",
         "risk_level": "low", "risk_notes": "", "t": "Oi"} for o in offsets]})


def test_parse_batch_lines_and_coverage():
    tok = context_pack.TOKEN
    pack = {"sfx": "99_01", "tm_exact": [],
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


class _FakeBatches:
    """Fake da Batch API ciente de RODADAS: scene_rounds[cid] = [texto_rodada0, texto_rodada1, ...];
    results() devolve, por cid submetido, o proximo texto da fila (vazio se acabar)."""
    def __init__(self, scene_rounds):
        self.scene_rounds = {k: list(v) for k, v in scene_rounds.items()}
        self._submitted = []

    def create(self, requests):
        self._submitted = [r["custom_id"] for r in requests]
        return _types.SimpleNamespace(id="batch_x", processing_status="in_progress")

    def retrieve(self, _id):
        return _types.SimpleNamespace(processing_status="ended")

    def results(self, _id):
        out = []
        for cid in self._submitted:
            q = self.scene_rounds.get(cid, [])
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
        "ch_99_01": {"sfx": "99_01", "tm_exact": [], "lines": [{"offset": "0x1", "source": "Hi"}]},
        "ch_99_02": {"sfx": "99_02", "tm_exact": [],
                     "lines": [{"offset": "0x9", "source": "A"}, {"offset": "0xa", "source": "B"}]},
        "ch_99_03": {"sfx": "99_03", "tm_exact": [], "lines": [{"offset": "0xb", "source": "C"}]},
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
    # ledger: 99_01 x1, 99_02 x2 (2 rodadas), 99_03 x2; tudo batch=True, custo 50%
    rows = [json.loads(l) for l in
            (tmp_path / "artifacts" / "api_ledger.jsonl").read_text("utf-8").splitlines()]
    n = {}
    for r in rows:
        n[r["scene"]] = n.get(r["scene"], 0) + 1
        assert r["batch"] is True
    assert n == {"ch_99_01": 1, "ch_99_02": 2, "ch_99_03": 2}


def test_batch_translate_resumes_existing(monkeypatch, tmp_path):
    # cena ja com translations completas em disco -> NAO re-batcha (idempotente; nao re-gasta o pago)
    (tmp_path / "artifacts" / "ch_99_01").mkdir(parents=True)
    packs = {"ch_99_01": {"sfx": "99_01", "tm_exact": [], "lines": [{"offset": "0x1", "source": "Hi"}]}}
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
