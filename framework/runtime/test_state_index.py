"""test_state_index.py — cobre os builders do índice de estado (TM/voz/decisões) e o check-sync.

state_index destila os artefatos por-cena em índices consultáveis. Aqui cada builder é exercitado
com fixtures mínimas (translation_plan, tone_analysis.md, decision_log.md) e o build() completo
dispara os ramos de warning (falante sem voice card, glossário sem updated_date). Só stdlib.
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import paths  # noqa: E402
import state_index as si  # noqa: E402


def test_build_tm_dedups_and_reads_plan(tmp_path):
    art = tmp_path / "artifacts"
    art.mkdir()
    # plano raiz (lista) + plano de capítulo (dict) com o mesmo offset -> capítulo vence no dedup
    (art / "translation_plan_root.json").write_text(json.dumps({
        "scene_group": "root",
        "lines": [{"offset": "A:0:1", "text_source": "Hi", "base_translation": "Oi", "speaker": "Ryu"}]
    }), encoding="utf-8")
    sub = art / "ch_01"
    sub.mkdir()
    (sub / "translation_plan_ch_01.json").write_text(json.dumps({
        "scene_group": "01",
        "lines": {"B:0:1": {"text_source": "Bye", "t": "Tchau", "speaker": "Nina"}}
    }), encoding="utf-8")
    tm = si.build_tm(art)
    srcs = {e["source"] for e in tm}
    assert srcs == {"Hi", "Bye"}
    assert all(e["src_key"] for e in tm)                 # chave de TM computada


def test_build_voice_cards_parses_blocks_and_inline():
    md = (
        "### Ryu — `voice_criticality: high`\n"
        "- fala curta e direta\n"
        "- sem gíria moderna\n"
        "\n"
        "## Atualizacoes\n"
        "- **Nina** — `voice_criticality: medium`. tom leve.\n"
    )
    cards = si.build_voice_cards(md)
    assert "Ryu" in cards and cards["Ryu"]["criticality"] == "high"
    assert cards["Ryu"]["lines"]                          # bullets capturados
    assert "Nina" in cards                                # linha inline


def test_build_decision_index_splits_sections():
    md = (
        "# Decision Log\n"
        "## Ponteiros e opcode\n"
        "**Data:** 2026-01-01\n"
        "Preservar ponteiros ao reinserir.\n"
        "## Tom da Nina\n"
        "Manter registro informal.\n"
    )
    dec = si.build_decision_index(md)
    titles = {d["title"] for d in dec}
    assert "Ponteiros e opcode" in titles and "Tom da Nina" in titles
    # 'universal' liga por hint do conector (opcode/ponteiro)
    assert any(d["universal"] for d in dec if "opcode" in d["title"].lower())


def test_build_decision_index_extracts_reveal_tag():
    """#105: tag opcional '<!-- reveal: ... -->' na linha do titulo vira campo reveal, e e
    removida do titulo. Secao sem a tag -> reveal=None (default-deny decidido na migracao)."""
    md = (
        "# Decision Log\n"
        "## Nina e revelada dragao <!-- reveal: ch_12 -->\n"
        "Nina revela ser o dragao ancestral.\n"
        "## Tom da Nina\n"
        "Manter registro informal.\n"
    )
    dec = {d["title"]: d for d in si.build_decision_index(md)}
    assert dec["Nina e revelada dragao"]["reveal"] == "ch_12"
    assert dec["Tom da Nina"]["reveal"] is None


def _mini_project(root: Path, with_updated_date: bool):
    art = root / "artifacts"
    (art / "state").mkdir(parents=True)
    (root / "project.json").write_text('{"title":"T","media_type":"game"}', encoding="utf-8")
    # 1 plano com falante sem voice card -> dispara o warning de completude
    (art / "translation_plan_root.json").write_text(json.dumps({
        "scene_group": "root",
        "lines": [{"offset": "A:0:1", "text_source": "Hi", "base_translation": "Oi", "speaker": "Ghost"}]
    }), encoding="utf-8")
    hdr = "term,translation" + (",updated_date" if with_updated_date else "")
    row = "Dragon,Dragão" + (",2020-01-01" if with_updated_date else "")
    (art / "glossary.csv").write_text(hdr + "\n" + row + "\n", encoding="utf-8")


def test_build_warns_missing_voice_and_stale_glossary(tmp_path):
    _mini_project(tmp_path, with_updated_date=True)
    r = si.build(tmp_path, sync_db=False)
    joined = " ".join(r["warnings"])
    assert "voice card" in joined                        # Ghost sem card
    assert "updated_date" in joined or "revis" in joined  # glossário com data antiga
    assert (paths.state_dir(tmp_path) / "voice_cards.json").is_file()


def test_build_warns_glossary_without_updated_date(tmp_path):
    _mini_project(tmp_path, with_updated_date=False)
    r = si.build(tmp_path, sync_db=False)
    assert any("updated_date" in w for w in r["warnings"])


def test_check_sync_reports_no_version(tmp_path, capsys):
    """_check_sync: TM sem doctrine_version -> lista como 'sem doctrine_version'."""
    art = tmp_path / "artifacts"
    (art / "state").mkdir(parents=True)
    (tmp_path / "project.json").write_text('{"title":"T","media_type":"game"}', encoding="utf-8")
    tm_path = paths.translation_memory(tmp_path)
    tm_path.write_text(json.dumps({"scene": "S1", "offset": "A:0:1", "source": "Hi",
                                   "target": "Oi", "src_key": "k", "doctrine_version": ""}) + "\n",
                       encoding="utf-8")
    si._check_sync(tmp_path)
    out = capsys.readouterr().out.lower()
    assert "doctrine" in out
