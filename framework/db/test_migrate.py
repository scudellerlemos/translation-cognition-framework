"""test_migrate.py — contrato da migração flat-files → SQLite.

Guarda regressões de "silent-zero" (migração importando 0 de um artefato que existe, por
mismatch de coluna/path) e garante que o banco bate com o que a migração reporta. Usa o
fixture `bof4_migrated` (migração única por sessão); só o teste de idempotência re-migra.
Usa só stdlib — roda em CI sem deps de ML.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "framework" / "runtime"))
sys.path.insert(0, str(HERE))

from migrate_from_flat import migrate  # noqa: E402
from store import Store  # noqa: E402

BOF4 = ROOT / "projects" / "breath_of_fire_4"


def test_migrate_imports_all_present_artifact_types(synthetic_migrated):
    """> 0 em cada tipo de artefato presente num projeto sintetico (todos os tipos de
    migrate_from_flat cobertos). (decisions/spoiler ficam vazios de proposito — só checa
    as chaves presentes.)"""
    _root, _db, result = synthetic_migrated
    assert result["scenes"] > 0, result
    assert result["scene_lines"] > 0, "dialogs.csv por cena existe mas scene_lines importou 0"
    assert result["translations"] > 0, result
    assert result["glossary"] > 0, "glossary.csv existe mas importou 0 — mismatch de coluna?"
    assert result["entities"] > 0, "entities.csv existe mas importou 0 — mismatch de coluna?"
    assert result["voice_cards"] > 0, "voice_cards.json existe (artifacts/state/) mas importou 0 — path errado?"
    assert result["back_translations"] > 0, "back_translation_*.json existe mas importou 0"
    assert result["kb"] > 0, "universe_knowledge_base.md existe mas importou 0 seções"
    assert result["jobs"] > 0, result
    assert result["metrics"] > 0, "metrics.jsonl existe mas importou 0 — mismatch?"
    assert result["warnings"] > 0, "warnings.jsonl existe mas importou 0"
    assert result["qa_effectiveness"] > 0, "qa_effectiveness.jsonl existe mas importou 0"
    assert "decisions" in result and "spoiler" in result, result


def test_migrate_counts_roundtrip_to_store(bof4_migrated):
    db_path, result = bof4_migrated
    with Store(db_path) as db:
        summary = db.summary("bof4")
    assert summary["scenes"] == result["scenes"], (summary, result)
    assert summary["scene_lines"] == result["scene_lines"], (summary, result)
    assert summary["translations"] == result["translations"], (summary, result)
    assert summary["tm_approved"] == result["approved"], (summary, result)
    assert summary["glossary"] == result["glossary"], (summary, result)
    assert summary["entities"] == result["entities"], (summary, result)
    assert summary["voice_cards"] == result["voice_cards"], (summary, result)
    assert summary["decisions"] == result["decisions"], (summary, result)
    assert summary["spoiler"] == result["spoiler"], (summary, result)
    assert summary["kb"] == result["kb"], (summary, result)
    assert summary["metrics"] == result["metrics"], (summary, result)
    assert summary["warnings"] == result["warnings"], (summary, result)
    assert summary["qa_effectiveness"] == result["qa_effectiveness"], (summary, result)


def test_migrate_glossary_lossless(bof4_migrated):
    """O glossário no DB preserva aliases/category (que o context_pack usa/renderiza)."""
    db_path, _ = bof4_migrated
    with Store(db_path) as db:
        g = db.get_glossary("bof4")
    assert g, "glossary vazio"
    assert any(r.get("category") for r in g), "category não migrou (regressão lossy)"
    assert any(r.get("aliases") for r in g), "aliases não migrou (regressão lossy)"


def test_migrate_voice_cards_keep_lines(bof4_migrated):
    """Voice cards preservam o formato do context_pack (aliases + lines)."""
    db_path, _ = bof4_migrated
    with Store(db_path) as db:
        vc = db.get_voice_cards("bof4")
    assert vc, "voice_cards vazio"
    assert any(c.get("lines") for c in vc), "lines não migraram (formato context_pack perdido)"


def test_strip_codes_clean_form():
    """strip_codes remove os [XX] e normaliza espaços (forma limpa p/ leitura/semântica)."""
    from store import strip_codes
    faithful = '[14][C1]@"Voce[01]quer dizer?[02]Certo"'
    clean = strip_codes(faithful)
    assert "[01]" not in clean and "[14]" not in clean and "[02]" not in clean
    assert "Voce quer dizer?" in clean and "Certo" in clean


def test_get_translations_exposes_clean(synthetic_migrated):
    """get_translations expõe source_clean/target_clean sem códigos, mantendo o fiel."""
    _root, db_path, _ = synthetic_migrated
    with Store(db_path) as db:
        tm = db.get_translations("syn", approved_only=True)
    assert tm
    r = next(t for t in tm if "[" in (t.get("target") or ""))   # uma linha com códigos
    assert "[" in r["target"] and "[" not in r["target_clean"]  # fiel tem, clean não


def test_migrate_idempotent(tmp_path):
    """Rodar a migração 2x no mesmo banco não duplica (upsert, não insert)."""
    db_path = tmp_path / "t.db"
    first = migrate(BOF4, db_path, project_id="bof4")
    migrate(BOF4, db_path, project_id="bof4")
    with Store(db_path) as db:
        summary = db.summary("bof4")
    assert summary["translations"] == first["translations"], (summary, first)
    assert summary["tm_approved"] == first["approved"], (summary, first)
    assert summary["scene_lines"] == first["scene_lines"], (summary, first)
    # observabilidade: UNIQUE garante que re-migrar não duplica (ao contrário do jobs)
    assert summary["metrics"] == first["metrics"], (summary, first)
    assert summary["warnings"] == first["warnings"], (summary, first)
    assert summary["qa_effectiveness"] == first["qa_effectiveness"], (summary, first)
    # jobs não tem UNIQUE; o mirror faz clear+reload p/ não inflar o custo a cada re-index
    assert summary["api_calls"] == first["jobs"], (summary, first)


def test_migrate_translations_have_content(synthetic_migrated):
    """REGRESSÃO: translations migravam com source/target VAZIOS (lia colunas inexistentes).
    Agora target vem do approved_*.csv (completo/fiel) e source do dialogs.csv."""
    _root, db_path, _ = synthetic_migrated
    with Store(db_path) as db:
        tm = db.get_translations("syn", approved_only=False)
    assert tm, "translations vazio"
    empty = [t for t in tm if not (t.get("source") and t.get("target"))]
    assert not empty, f"{len(empty)}/{len(tm)} translations com source/target vazio"


def test_migrate_decisions_reveal_explicit_tag_and_universal_shortcut(tmp_path):
    """#105: reveal explicito (tag <!-- reveal: ... --> no decision_log.md, ja extraido em
    decision_index.json por state_index.build_decision_index) tem prioridade; sem tag, universal=1
    ganha reveal='safe' automatico (atalho aprovado); universal=0 sem tag fica None (default-deny,
    ate revisao humana)."""
    state_dir = tmp_path / "artifacts" / "state"
    state_dir.mkdir(parents=True)
    (state_dir / "decision_index.json").write_text(json.dumps([
        {"title": "Regra de ponteiro", "tags": ["ponteiro"], "universal": True,
         "summary": "sempre preservar offsets", "reveal": None},
        {"title": "Nina e revelada dragao", "tags": [], "universal": False,
         "summary": "Nina revela ser o dragao", "reveal": "ch_12"},
        {"title": "Decisao de trama pendente", "tags": [], "universal": False,
         "summary": "ainda nao revisado", "reveal": None},
    ], ensure_ascii=False), encoding="utf-8")

    db_path = tmp_path / "t.db"
    migrate(tmp_path, db_path, project_id="p")
    with Store(db_path) as db:
        decisions = {d["title"]: d for d in db.get_decisions("p")}

    assert decisions["Regra de ponteiro"]["reveal"] == "safe"          # universal sem tag -> atalho
    assert decisions["Nina e revelada dragao"]["reveal"] == "ch_12"    # tag explicita preservada
    assert decisions["Decisao de trama pendente"]["reveal"] is None    # nao-universal sem tag -> default-deny


def test_migrate_project_title_from_json(bof4_migrated):
    """O título do projeto vem do project.json (não hardcoded) — pré-req do write-path multi-projeto."""
    db_path, _ = bof4_migrated
    with Store(db_path) as db:
        row = db._con.execute(
            "SELECT title, source_lang, target_lang FROM projects WHERE id='bof4'").fetchone()
    assert row and row[0] == "Breath of Fire IV", row
    # idiomas vêm de source_language/target_language do project.json (nomenclatura real)
    assert (row[1], row[2]) == ("en", "pt-BR"), row


def test_migrate_translations_count_dedups_overlapping_csvs(tmp_path):
    """#3 (review): offsets repetidos entre múltiplos approved_*.csv contam UMA vez (= linhas do
    DB), não por linha de CSV — senão o result mente vs store.summary."""
    proj = tmp_path / "p"
    sc = proj / "artifacts" / "scenes" / "s1"
    sc.mkdir(parents=True)
    (proj / "project.json").write_text('{"title":"T","media_type":"game"}', encoding="utf-8")
    (sc / "dialogs.csv").write_text("offset,text_source\nX:0:1,Hi\n", encoding="utf-8")
    (sc / "approved_a.csv").write_text("offset,text_target\nX:0:1,Oi\n", encoding="utf-8")
    (sc / "approved_b.csv").write_text("offset,text_target\nX:0:1,Oi rev\n", encoding="utf-8")
    db = tmp_path / "p.db"
    result = migrate(proj, db, project_id="p")
    with Store(db) as d:
        summ = d.summary("p")
    assert result["translations"] == 1, result       # 1 offset distinto, não 2 linhas
    assert summ["translations"] == result["translations"], (summ, result)


def test_migrate_metrics_content(bof4_migrated):
    """metrics: 1 linha por cena, escalares preenchidos e `raw` (translate/back) preservado."""
    db_path, result = bof4_migrated
    with Store(db_path) as db:
        m = db.get_metrics("bof4")
    assert m, "metrics vazio"
    assert len(m) == result["metrics"], "contagem de metrics diverge do reportado"
    assert all(r.get("scene_id") for r in m), "metrics sem scene_id"
    # `raw` reidrata p/ dict e mantém os blocos aninhados que não viram coluna
    withraw = next((r for r in m if r.get("raw")), None)
    assert withraw and isinstance(withraw["raw"], dict), "raw não reidratou p/ dict"
    assert "translate" in withraw["raw"], "raw perdeu o bloco translate (lossy)"


def test_migrate_warnings_content(bof4_migrated):
    """warnings: lista de strings reidratada (não fica como string JSON crua)."""
    db_path, _ = bof4_migrated
    with Store(db_path) as db:
        w = db.get_warnings("bof4")
    assert w, "warnings vazio"
    assert any(isinstance(r.get("warnings"), list) and r["warnings"] for r in w), \
        "warnings não reidratou p/ lista"
