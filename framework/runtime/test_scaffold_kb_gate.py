"""test_scaffold_kb_gate.py — trava de regressao pro gap real do onboarding do Souldiers:
scaffold_project.py e kb_gate.py sao mantidos por skills/codigo separados e ja
divergiram silenciosamente 2x (glossary.csv sem 'updated_date'; universe_knowledge_base.md nunca
scaffoldado). Este teste roda o par ponta-a-ponta pra qualquer divergencia futura quebrar aqui,
nao num piloto pago de outro jogo.
"""
import json
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import connector_gate  # noqa: E402
import kb_gate  # noqa: E402
import paths  # noqa: E402
import scaffold_project  # noqa: E402
import state_index  # noqa: E402


def _write_project_json(root: Path, title: str) -> None:
    (root / "project.json").write_text(json.dumps({
        "title": title, "media_type": "game", "kb_frontier": "00_00",
    }), encoding="utf-8")


def test_scaffold_glossary_has_updated_date_column():
    assert "updated_date" in scaffold_project._GLOSSARY_HEADERS


def test_fresh_scaffold_alone_still_fails_kb_gate(tmp_path):
    """scaffold() NAO deve, sozinho, satisfazer o gate — senao o hard-block de pesquisa
    reconciliada (governanca anti-fabricacao) estaria sendo furado por um placeholder."""
    scaffold_project.scaffold(tmp_path, title="T")
    _write_project_json(tmp_path, "T")
    r = kb_gate.check(tmp_path, "00_00")
    assert r["hard_problems"], "scaffold sozinho nao pode passar o hard-gate (sem pesquisa real)"


def test_scaffold_plus_real_kb_content_passes_gate(tmp_path):
    """Reproduz o fluxo completo: scaffold -> preencher como a skill 03/04 preencheria ->
    state_index.build() deriva voice_cards -> kb_gate.check() deve passar limpo."""
    scaffold_project.scaffold(tmp_path, title="T")
    _write_project_json(tmp_path, "T")
    art = paths.artifacts(tmp_path)

    (art / "universe_knowledge_base.md").write_text(
        "## PersonagemA\n\n**Definicao:**\nlore real, com fonte.\n\n**Fontes:**\n- SRC-001\n",
        encoding="utf-8")
    (art / "research_log.md").write_text(
        "# Research Log — T\n\n**Status:** reconciled\n\n## Fontes Avaliadas\n"
        "| ID | Fonte | Tier |\n|----|-------|------|\n| SRC-001 | Wiki | 2 |\n",
        encoding="utf-8")

    import csv
    glossary_path = art / "glossary.csv"
    with glossary_path.open("a", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerow(
            ["Dragon", "creature", "Dragao", "verbatim", "none", "", "", "2026-01-01"])

    # tone_analysis.md ja sai do scaffold com o marcador certo (### Nome — `voice_criticality: X`)
    # para PersonagemA/B/C — nao precisa editar para o gate/build_voice_cards reconhecerem.

    state_index.build(tmp_path, sync_db=False)

    r = kb_gate.check(tmp_path, "00_00")
    assert r["hard_problems"] == [], r["hard_problems"]
    assert r["problems"] == [], r["problems"]


def test_scaffold_creates_profile_reference_files(tmp_path):
    """Gap real do onboarding do Trails Sky SC (2026-08-23): o onboarding doc afirma que
    scaffold cria profile/, mas o codigo nunca criava -- profile/ ficou vazio ate o checklist
    de gate (que exige voice_profiles_reference.md/terminology_seeds.md) ser notado tarde."""
    scaffold_project.scaffold(tmp_path, title="T")
    profile = tmp_path / "profile"
    for fname in [
        "voice_profiles_reference.md", "terminology_seeds.md",
        "identity_pairs_reference.md", "example_test_suites.md",
    ]:
        assert (profile / fname).is_file(), f"scaffold nao criou profile/{fname}"


def test_scaffold_copies_skeleton_but_copy_still_fails_connector_gate(tmp_path):
    """scaffold() copia o _skeleton p/ connector/ (ponto de partida da Fase 0, com test_roundtrip*
    e conftest), mas a copia INTOCADA nao pode passar o hard-gate -- mesma governanca do KB:
    nunca engana o gate com placeholder."""
    scaffold_project.scaffold(tmp_path, title="T")
    conn = tmp_path / "connector"
    for f in ("build_plan_chapter.py", "verify_chapter.py", "extract.py", "reinsert.py", "table_schema.md",
              "test_roundtrip.py", "test_roundtrip_synthetic.py", "conftest.py"):
        assert (conn / f).is_file(), f"scaffold nao copiou connector/{f}"
    r = connector_gate.check(tmp_path)
    assert sum("_skeleton" in p for p in r["hard_problems"]) == 2, r["hard_problems"]
    assert r["warnings"] == []   # test_roundtrip.py ja veio do skeleton


def test_scaffold_plus_real_connector_scripts_passes_gate(tmp_path):
    scaffold_project.scaffold(tmp_path, title="T")
    _write_project_json(tmp_path, "T")
    conn = tmp_path / "connector"
    (conn / "build_plan_chapter.py").write_text("# real", encoding="utf-8")
    (conn / "verify_chapter.py").write_text("# real", encoding="utf-8")
    (conn / "test_roundtrip.py").write_text("# real", encoding="utf-8")
    paths.run_state(tmp_path).parent.mkdir(parents=True, exist_ok=True)
    paths.run_state(tmp_path).write_text(
        json.dumps({"scenes": {"s1": {"status": "verified", "verified": True}}}), encoding="utf-8")
    r = connector_gate.check(tmp_path)
    assert r == {"hard_problems": [], "problems": [], "warnings": []}


def test_scaffold_rerun_skips_existing_files(tmp_path, capsys):
    """2a chamada em cima do mesmo diretorio deve SKIP tudo que a 1a criou, nao sobrescrever."""
    scaffold_project.scaffold(tmp_path, title="T")
    n_created = capsys.readouterr().out.count("CRIADO")
    (tmp_path / "project.json").write_text("{}", encoding="utf-8")
    scaffold_project.scaffold(tmp_path, title="T")
    out = capsys.readouterr().out
    assert "CRIADO" not in out and out.count("SKIP") == n_created
    assert (tmp_path / "project.json").read_text(encoding="utf-8") == "{}"


def test_scaffold_generates_project_json_from_template(tmp_path):
    root = tmp_path / "meu_jogo"
    root.mkdir()
    scaffold_project.scaffold(root, title='Jogo "X"')
    cfg = json.loads((root / "project.json").read_text(encoding="utf-8"))
    assert cfg["title"] == 'Jogo "X"'
    assert cfg["db"] == {"path": "meu_jogo.db", "project_id": "meu_jogo"}
    assert cfg["kb_frontier"] == "" and "connector" in cfg
    r = kb_gate.check(root, "00_00")
    assert any("kb_frontier nao declarada" in p for p in r["hard_problems"])


def test_scaffold_kb_artifacts_have_schema_but_do_not_pass_gate(tmp_path):
    """KB .md/research_log/kb_ratified/spoiler_ledger nascem no schema que o runtime le, mas a
    KB-stub (marcador) e o research_log 'pending' nunca satisfazem o gate."""
    scaffold_project.scaffold(tmp_path, title="T")
    art = paths.artifacts(tmp_path)
    assert json.loads(paths.spoiler_ledger(tmp_path).read_text(encoding="utf-8")) == {"entries": []}
    assert paths.kb_ratified(tmp_path).read_text(encoding="utf-8").startswith("name,ratified_by,date")
    _write_project_json(tmp_path, "T")
    r = kb_gate.check(tmp_path, "00_00")
    assert any("placeholder do scaffold" in p for p in r["hard_problems"]), r["hard_problems"]
    assert any("status: reconciled" in p for p in r["problems"]), r["problems"]
    assert (art / "universe_knowledge_base.md").read_text(encoding="utf-8").count(scaffold_project.KB_PLACEHOLDER) == 1


def test_scaffold_reports_ok_when_both_gates_already_pass(tmp_path):
    """Reproduz o projeto pronto (KB + conector completos) ANTES de rodar scaffold() de novo --
    os relatorios de status devem imprimir OK em vez de listar pendencias."""
    scaffold_project.scaffold(tmp_path, title="T")
    _write_project_json(tmp_path, "T")
    art = paths.artifacts(tmp_path)
    (art / "universe_knowledge_base.md").write_text(
        "## PersonagemA\n\n**Definicao:**\nlore real, com fonte.\n\n**Fontes:**\n- SRC-001\n",
        encoding="utf-8")
    (art / "research_log.md").write_text(
        "# Research Log — T\n\n**Status:** reconciled\n\n## Fontes Avaliadas\n"
        "| ID | Fonte | Tier |\n|----|-------|------|\n| SRC-001 | Wiki | 2 |\n",
        encoding="utf-8")
    import csv
    with (art / "glossary.csv").open("a", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerow(
            ["Dragon", "creature", "Dragao", "verbatim", "none", "", "", "2026-01-01"])
    state_index.build(tmp_path, sync_db=False)

    conn = tmp_path / "connector"
    (conn / "build_plan_chapter.py").write_text("# real", encoding="utf-8")
    (conn / "verify_chapter.py").write_text("# real", encoding="utf-8")
    (conn / "test_roundtrip.py").write_text("# real", encoding="utf-8")
    paths.run_state(tmp_path).parent.mkdir(parents=True, exist_ok=True)
    paths.run_state(tmp_path).write_text(
        json.dumps({"scenes": {"s1": {"status": "verified", "verified": True}}}), encoding="utf-8")

    scaffold_project._report_connector_gate_status(tmp_path)
    scaffold_project._report_kb_gate_status(tmp_path)


def test_report_connector_gate_status_handles_exception(tmp_path, monkeypatch):
    """Se connector_gate.check() explodir (projeto ainda incompleto demais p/ nem checar), o
    scaffold NAO deve propagar -- so avisa e segue."""
    import connector_gate as cg
    monkeypatch.setattr(cg, "check", lambda root: (_ for _ in ()).throw(RuntimeError("boom")))
    scaffold_project._report_connector_gate_status(tmp_path)  # nao deve levantar


def test_report_kb_gate_status_handles_exception(tmp_path, monkeypatch):
    _write_project_json(tmp_path, "T")
    monkeypatch.setattr(kb_gate, "check", lambda root, scene: (_ for _ in ()).throw(RuntimeError("boom")))
    scaffold_project._report_kb_gate_status(tmp_path)  # nao deve levantar


def test_report_kb_gate_status_without_project_json(tmp_path, capsys):
    scaffold_project._report_kb_gate_status(tmp_path)
    assert "project.json ainda nao existe" in capsys.readouterr().out


def test_project_template_declares_keys_the_gates_and_connector_read():
    """O template nao tinha kb_frontier/connector/formatting_token_patterns -- todo projeto real
    (BoF4, Souldiers, Trails, Uta) adicionou na mao depois de tropecar no gate. kb_frontier vazio
    (nao placeholder com digitos: _pos() leria os digitos como fronteira real) cai no hard-block
    instrutivo do kb_gate."""
    from config import CONNECTOR_KNOWN_KEYS, validate_connector_types
    tpl = Path(__file__).resolve().parents[1] / "templates" / "project.template.json"
    cfg = json.loads(tpl.read_text(encoding="utf-8"))
    assert cfg["kb_frontier"] == ""
    assert cfg["formatting_token_patterns"] == []
    assert set(cfg["connector"]) <= CONNECTOR_KNOWN_KEYS
    assert {"extract_script", "reinsert_script", "table_schema", "source_binary"} <= set(cfg["connector"])
    assert validate_connector_types(cfg) == []


def test_fresh_scaffold_e2e_gates_report_exactly_the_onboarding_steps(tmp_path, monkeypatch):
    """E2E: scaffold puro (sem project.json escrito a mao) -> os 2 gates listam EXATAMENTE os passos
    reais de onboarding (adaptar conector, sintetizar KB, declarar fronteira, reconciliar pesquisa,
    rodar state_index) -- nada de 'ausente'/'corrompido' que o scaffold deveria ter criado. E o
    connector/ copiado roda a propria suite limpo (so skips ate a Fase 0)."""
    # stack de ML e passo de AMBIENTE (testado em test_gates_db_gated), nao do scaffold: fora daqui.
    monkeypatch.setattr(kb_gate, "_check_semantic_stack", lambda cfg, res: None)
    scaffold_project.scaffold(tmp_path, title="T")
    c = connector_gate.check(tmp_path)
    assert [("build_plan" in p, "_skeleton" in p) for p in c["hard_problems"]] == [(True, True), (False, True)]
    assert c["problems"] == [] and c["warnings"] == []
    k = kb_gate.check(tmp_path, "01")
    assert len(k["hard_problems"]) == 2, k["hard_problems"]
    assert "placeholder do scaffold" in k["hard_problems"][0]
    assert "kb_frontier nao declarada" in k["hard_problems"][1]
    assert len(k["problems"]) == 2, k["problems"]
    assert "status: reconciled" in k["problems"][0] and "voice_cards.json" in k["problems"][1]
    assert k["warnings"] == [] and k["pending_decisions"] == []
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "connector"],
                       cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
