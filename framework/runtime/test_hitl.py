"""test_hitl.py — humano no laco (escopo, ratificacao, onda, fila) e triagem de risco, em projeto sintetico."""
import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import hitl  # noqa: E402
import paths  # noqa: E402
import risk_triage  # noqa: E402


def _project(root: Path, n_scenes: int = 1) -> Path:
    (root / "project.json").write_text(json.dumps({"hitl": True}), encoding="utf-8")
    paths.artifacts(root).mkdir(parents=True, exist_ok=True)
    rows = ["offset,file,text_en"]
    for i in range(n_scenes):
        s = f"S{i:02}"
        rows += [f"{s}:0,{s},The Warmaster marches at dawn today", f"{s}:1,{s},Warmaster!"]
        d = paths.scene_dir(root, s)
        d.mkdir(parents=True, exist_ok=True)
        paths.dialogs(root, s).write_text("\n".join([rows[0]] + rows[-2:]) + "\n", encoding="utf-8")
        lines = [{"offset": f"{s}:0", "text_source": "The Warmaster marches at dawn today", "risk_level": "low",
                  "base_translation": "O Mestre de Guerra marcha ao amanhecer"},
                 {"offset": f"{s}:1", "text_source": "Warmaster!", "base_translation": "Mestre!", "risk_level": "low"}]
        paths.translation_plan(root, s, s).write_text(json.dumps({"lines": lines}), encoding="utf-8")
        paths.translations(root, s, s).write_text(json.dumps({"lines": {
            ln["offset"]: {"t": ln["base_translation"], "risk_level": "low"} for ln in lines}}), encoding="utf-8")
    paths.dialogs_flat(root).write_text("\n".join(rows) + "\n", encoding="utf-8")
    paths.glossary(root).write_text(
        "term,category,target_translation,handling_rule,aliases,updated_date\n"
        "Warmaster,titulo,Mestre de Guerra,traduzir,,2026-01-01\n", encoding="utf-8")
    return root


def test_project_without_the_key_is_untouched(tmp_path):
    (tmp_path / "project.json").write_text("{}", encoding="utf-8")
    assert not hitl.enabled(tmp_path)


def test_scope_needs_acceptance_and_reopens_when_corpus_changes(tmp_path):
    root = _project(tmp_path)
    n_scenes, n_lines, _ = hitl.corpus(root)
    assert (n_scenes, n_lines) == (1, 2)
    assert "sem aceite" in hitl.scope_problems(root, 1, 2)[0]
    hitl._log(root, kind="escopo", by="ana", scenes=1, lines=2, action="accept")
    assert hitl.scope_problems(root, 1, 2) == []
    assert "mudou" in hitl.scope_problems(root, 1, 3)[0]


def test_frequent_glossary_term_blocks_until_ratified(tmp_path):
    root = _project(tmp_path)
    text = hitl.corpus(root)[2]
    assert hitl.pending_glossary(root, text) == [("Warmaster", "Mestre de Guerra", 2)]
    assert hitl._ratify(root, "ana", []) == 1
    assert hitl.pending_glossary(root, text) == []
    assert "ana" in paths.kb_ratified(root).read_text(encoding="utf-8")


def test_named_term_is_ratified_even_outside_the_frequent_ones(tmp_path, capsys):
    root = _project(tmp_path)
    with paths.glossary(root).open("a", encoding="utf-8") as fh:      # termo que nao aparece no corpus
        fh.write("Elders,grupo,Anciões,traduzir,,2026-01-01" + chr(10))
    assert hitl._ratify(root, "ana", []) == 1                          # so o frequente
    assert hitl._ratify(root, "ana", ["elders", "Inexistente"]) == 1
    assert "Inexistente" in capsys.readouterr().err
    assert hitl._ratify(root, "ana", ["Elders"]) == 0                  # ja ratificado: nao duplica


def test_gate_blocks_on_scope_but_only_warns_on_glossary_and_wave(tmp_path, capsys, monkeypatch):
    root = _project(tmp_path, n_scenes=hitl.WAVE_SCENES)
    hitl.note_verified(root, [f"S{i:02}" for i in range(hitl.WAVE_SCENES)])
    assert len(hitl.gate(root, ["NOVA"])) == 1 and "escopo" in hitl.gate(root, ["NOVA"])[0]
    hitl._log(root, kind="escopo", by="ana", scenes=hitl.WAVE_SCENES, lines=2 * hitl.WAVE_SCENES, action="accept")
    capsys.readouterr()
    assert hitl.gate(root, ["NOVA"]) == []                              # termo sem ratificar + onda aberta
    out = capsys.readouterr().out
    assert out.count("aviso (nao bloqueia)") == 2 and "Warmaster" in out
    # decisao dada na conversa: o log guarda a frase literal
    monkeypatch.setattr(sys, "argv", ["hitl.py", "ack", str(root), "--reviewer", "ana", "--quote", " pode seguir "])
    monkeypatch.setattr(hitl, "_VIA", {})
    hitl.main()
    last = json.loads((paths.artifacts(root) / "hitl_log.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert (last["kind"], last["via"], last["quote"]) == ("onda", "conversa", "pode seguir")


def test_wave_checkpoint_blocks_only_new_scenes_until_ack(tmp_path):
    root = _project(tmp_path, n_scenes=hitl.WAVE_SCENES)
    done = [f"S{i:02}" for i in range(hitl.WAVE_SCENES)]
    assert not hitl.note_verified(root, done[:-1])
    assert hitl.wave_problems(root, ["NOVA"]) == []
    assert hitl.note_verified(root, done[-1:])
    sample = (paths.qa_outbox(root) / "onda_amostra.csv").read_text(encoding="utf-8-sig").splitlines()
    assert 1 < len(sample) <= hitl.WAVE_SAMPLE + 1
    assert "ponto de controle" in hitl.wave_problems(root, ["NOVA"])[0]
    paths.pack(root, "S00").write_text("{}", encoding="utf-8")          # cena ja em andamento nao trava
    assert hitl.wave_problems(root, ["S00"]) == []


def test_queue_alias_becomes_glossary_rule_and_closes_the_item(tmp_path):
    root = _project(tmp_path)
    item = {"scene": "S00", "offset": "S00:1", "kind": "glossario", "term": "Warmaster",
            "expected": "mestre de guerra", "source_en": "Warmaster!", "target_pt": "Mestre!", "reason": "x"}
    assert hitl.enqueue(root, [item]) == 1
    assert hitl.enqueue(root, [item]) == 0                               # mesma fala nao entra duas vezes
    assert len(hitl.open_items(root)) == 1
    rows = hitl.read_queue(root)
    rows[0]["alias"] = "Mestre"
    hitl._write_queue(root, rows)
    assert hitl.open_items(root) == []
    r = hitl.resolve(root, "ana")
    assert (r["alias"], r["open"]) == (1, 0)
    assert "Mestre de Guerra,traduzir,Mestre," in paths.glossary(root).read_text(encoding="utf-8")
    log = (paths.artifacts(root) / "hitl_log.jsonl").read_text(encoding="utf-8")
    assert '"by": "ana"' in log and "Warmaster!" not in log              # registra quem decidiu, nao a fala


def test_prune_closes_only_glossary_items_the_lint_no_longer_reports(tmp_path):
    root = _project(tmp_path)
    base = {"expected": "", "source_en": "", "target_pt": "", "reason": "x"}
    hitl.enqueue(root, [dict(base, scene="S00", offset="S00:1", kind="glossario", term="Ice"),     # some
                        dict(base, scene="S00", offset="S00:2", kind="glossario", term="Ice"),     # lint ainda acusa
                        dict(base, scene="S00", offset="S00:3", kind="tradutor", term="")])        # pedido do tradutor
    assert hitl.prune(root, [{"scene": "S00", "offset": "S00:2", "term": "Ice"}]) == 1
    assert [r["offset"] for r in hitl.open_items(root)] == ["S00:2", "S00:3"]
    assert '"by": "glossary_lint"' in (paths.artifacts(root) / "hitl_log.jsonl").read_text(encoding="utf-8")


def test_collect_reads_translator_escalation(tmp_path):
    root = _project(tmp_path)
    tf = paths.translations(root, "S00", "S00")
    data = json.loads(tf.read_text(encoding="utf-8"))
    data["lines"]["S00:0"]["escalate"] = "titulo sem forma no glossario"
    tf.write_text(json.dumps(data), encoding="utf-8")
    items = [i for i in hitl.collect(root, ["S00"]) if i["kind"] == "tradutor"]
    assert [(i["offset"], i["reason"]) for i in items] == [("S00:0", "titulo sem forma no glossario")]


def test_resolve_clears_translator_escalation(tmp_path):
    root = _project(tmp_path)
    tf = paths.translations(root, "S00", "S00")
    data = json.loads(tf.read_text(encoding="utf-8"))
    data["lines"]["S00:0"]["escalate"] = "titulo sem forma"
    tf.write_text(json.dumps(data), encoding="utf-8")
    hitl.enqueue(root, [i for i in hitl.collect(root, ["S00"]) if i["kind"] == "tradutor"])
    rows = hitl.read_queue(root)
    rows[0]["correcao"] = "Texto decidido"
    hitl._write_queue(root, rows)
    hitl.resolve(root, "ana")
    assert "escalate" not in json.loads(tf.read_text(encoding="utf-8"))["lines"]["S00:0"]
    assert [i for i in hitl.collect(root, ["S00"]) if i["kind"] == "tradutor"] == []


def test_resolve_accepts_translator_escalation_without_term(tmp_path):
    root = _project(tmp_path)
    tf = paths.translations(root, "S00", "S00")
    data = json.loads(tf.read_text(encoding="utf-8"))
    data["lines"]["S00:0"]["escalate"] = "nome sem forma"
    tf.write_text(json.dumps(data), encoding="utf-8")
    hitl.enqueue(root, [i for i in hitl.collect(root, ["S00"]) if i["kind"] == "tradutor"])
    rows = hitl.read_queue(root)
    assert not rows[0]["term"]
    rows[0]["alias"] = "forma da fala"
    hitl._write_queue(root, rows)
    r = hitl.resolve(root, "ana")
    assert (r["alias"], r["aceito"], r["open"]) == (0, 1, 0)      # aceite do tradutor nao conta como alias de glossario
    assert "escalate" not in json.loads(tf.read_text(encoding="utf-8"))["lines"]["S00:0"]


def test_triage_dedups_repeats_and_raises_every_copy(tmp_path):
    root = _project(tmp_path, n_scenes=3)
    r = risk_triage.export(root, batch=10)
    assert (r["pairs"], r["lines"], r["batches"]) == (1, 3, 1)          # 3 copias = 1 par; rotulo curto fora
    d = risk_triage._dir(root)
    pid = (d / "lote_001.tsv").read_text(encoding="utf-8").split("\t")[0]
    (d / "veredito_001.tsv").write_text(f"{pid}\tsentido trocado\nffffffffff\tinventado\n", encoding="utf-8")
    got = risk_triage.apply(root)
    assert (got["raised"], got["unknown_ids"], got["scenes"]) == (3, 1, ["S00", "S01", "S02"])
    e = json.loads(paths.translations(root, "S02", "S02").read_text(encoding="utf-8"))["lines"]
    assert e["S02:0"]["risk_level"] == "high" and e["S02:0"]["risk_notes"] == "triagem: sentido trocado"
    assert e["S02:1"]["risk_level"] == "low"


def test_quality_sample_scores_error_rate_and_judge(tmp_path):
    import csv

    import quality_sample
    root = _project(tmp_path, n_scenes=3)
    risk_triage.export(root, batch=10)
    d = risk_triage._dir(root)
    flagged = (d / "lote_001.tsv").read_text(encoding="utf-8").split("\t")[0]
    (d / "veredito_001.tsv").write_text(f"{flagged}\tsentido trocado\n", encoding="utf-8")
    r = quality_sample.export(root, n=10)
    assert (r["population"], r["rows"], r["flagged"]) == (2, 2, 1)       # 2 pares unicos; o apontado ja estava
    sheet = Path(r["path"])
    rows = list(csv.DictReader(sheet.read_text(encoding="utf-8-sig").splitlines()))
    assert "origem" not in rows[0]                                       # julgamento as cegas
    for row in rows:
        row["veredito"] = "erro" if row["id"] == flagged else "ok"
    with sheet.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=quality_sample.COLS)
        w.writeheader()
        w.writerows(rows)
    got = quality_sample.score(root, "ana")
    assert (got["judged"], got["errors"], got["error_rate"]) == (2, 1, 0.5)
    assert got["error_rate_weighted"] == 0.5                             # 3 copias erradas de 6 falas
    assert (got["triage_rate"], got["judge_precision"], got["judge_recall"]) == (1.0, 1.0, 1.0)
    lo, hi = quality_sample.wilson(0, 200)
    assert lo == 0.0 and 0.015 < hi < 0.02                               # 0 erro em 200 ainda admite ~1,9%


def test_path_is_a_human_choice_and_switching_needs_a_new_one(tmp_path):
    root = _project(tmp_path)
    assert "sem decisao" in hitl.path_problems(root, "api")[0]
    hitl._log(root, kind="caminho", by="ana", backend="in-session", action="choose")
    assert hitl.path_problems(root, "in-session") == []
    assert "decidido para o caminho 'in-session'" in hitl.path_problems(root, "api")[0]
    hitl._log(root, kind="caminho", by="ana", backend="api", action="choose")
    assert hitl.path_problems(root, "api") == []


def test_pattern_lint_blocks_sample_export(tmp_path, monkeypatch):
    import pattern_lint
    import pytest
    import quality_review
    import quality_sample
    root = _project(tmp_path, n_scenes=3)
    assert pattern_lint.lint(root)["blocking"] == {}
    monkeypatch.setattr(quality_review, "_PTPT", re.compile("."))   # toda traducao vira "pt-PT?"
    r = pattern_lint.lint(root)
    assert r["counts"]["pt-PT?"] > 0 and r["blocking"] == {}   # heuristica: avisa, nao bloqueia
    import box_width
    monkeypatch.setattr(box_width, "widths", lambda t, tbl: [999])
    assert set(pattern_lint.lint(root)["blocking"]) == {"largura"}
    with pytest.raises(SystemExit, match="lint de padroes"):
        quality_sample.export(root, n=10)
