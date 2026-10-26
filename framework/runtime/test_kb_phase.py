"""test_kb_phase.py — cobre o driver de Fase 0 (descoberta de gap de KB + validação de cobertura).

Usa o modo flat ("all", lê artifacts/dialogs.csv). Testa os helpers determinísticos de limpeza de
candidato + discover/coverage/apply_frontier/write_worklist. kb_review.blocking é mockado (outro módulo).
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import kb_phase as kp  # noqa: E402
import paths  # noqa: E402


def test_clean_cand_variants():
    assert kp._clean_cand("Despite Maroro") == "Maroro"             # stopword de borda
    assert kp._clean_cand("CARRY") == ""                            # ALL-CAPS = grito
    assert kp._clean_cand("M-Maroro") == "Maroro"                   # gagueira
    assert kp._clean_cand("Oshtor's") == "Oshtor"                   # possessivo


def test_norm_tok_and_covered():
    assert kp._norm_tok("Haku!") == "Haku"
    kb = kp._kb_blob_from(["Haku"], ["Ukon"])
    assert kp._covered("Master Haku", kb) is True                   # núcleo 'Haku' na KB
    assert kp._covered("Oshtor", kb) is False


def test_midsentence():
    assert kp._midsentence("Oshtor", "then, Oshtor spoke") is True
    assert kp._midsentence("What", "What is that?") is False


def _flat_project(root: Path, source_lines, glossary="term,aliases\nHaku,\n", frontier="0"):
    (root / "artifacts").mkdir(parents=True, exist_ok=True)
    body = "offset,text_source,byte_budget\n" + "".join(
        f'X:0:{i},"{s}",40\n' for i, s in enumerate(source_lines))
    paths.dialogs_flat(root).write_text(body, encoding="utf-8")
    paths.glossary(root).write_text(glossary, encoding="utf-8")
    (root / "project.json").write_text(
        f'{{"title":"T","media_type":"game","kb_frontier":"{frontier}"}}', encoding="utf-8")


def test_discover_flat_gap_and_covered(tmp_path):
    _flat_project(tmp_path, ["When Oshtor arrived, Oshtor bowed.", "Master Haku smiled."])
    d = kp.discover(tmp_path, "all")
    assert "Oshtor" in {r["cand"] for r in d["gap"]}                # não coberto
    assert any("Haku" in r["cand"] for r in d["covered"])          # 'Master Haku' -> núcleo Haku coberto


def test_coverage_ok_and_apply_frontier(tmp_path, monkeypatch):
    _flat_project(tmp_path, ["Haku spoke softly."])
    paths.research_log(tmp_path).write_text("**Status:** reconciled\n", encoding="utf-8")
    monkeypatch.setattr(kp.kb_review, "blocking", lambda r, c, strict=False: [])
    cov = kp.coverage(tmp_path, "all")
    assert cov["problems"] == []                                    # tudo coberto + reconciliado
    assert kp.apply_frontier(tmp_path, "all") == "all"
    assert '"kb_frontier":"all"' in (tmp_path / "project.json").read_text(encoding="utf-8")


def test_coverage_blocks_on_uncovered_recurrent(tmp_path, monkeypatch):
    # 'Oshtor' recorre >=3x, não coberto -> bloqueia; sem research reconciliada -> +1 problema
    _flat_project(tmp_path, ["Oshtor came.", "Then Oshtor spoke, Oshtor left.", "Oshtor again."])
    monkeypatch.setattr(kp.kb_review, "blocking", lambda r, c, strict=False: [])
    cov = kp.coverage(tmp_path, "all")
    assert cov["problems"]                                          # block + sem reconciled


def test_write_worklist(tmp_path):
    _flat_project(tmp_path, ["When Oshtor came, Oshtor left."])
    out = kp.write_worklist(tmp_path, "all")
    assert out.is_file() and "worklist" in out.read_text(encoding="utf-8").lower()


# --- ramos de borda ---------------------------------------------------------------------------------
def test_kb_blob_includes_entities_csv(tmp_path):
    _flat_project(tmp_path, ["x"])
    paths.entities(tmp_path).write_text("canonical_name,aliases\nUkon,Ukon-sama\n", encoding="utf-8")
    blob = kp._kb_blob(tmp_path)
    assert kp._covered("Ukon", blob) is True and kp._covered("Haku", blob) is True


def test_clean_cand_drops_empty_tokens_and_trailing_stopword():
    assert kp._clean_cand("- Oshtor") == "Oshtor"                   # token so de pontuacao some
    assert kp._clean_cand("Oshtor The") == "Oshtor"                 # stopword na borda final


def test_scan_skips_scene_without_dialogs(tmp_path):
    assert kp._scan(tmp_path, ["ch_99_01"]) == []


def test_scan_does_not_glue_break_token_nor_join_rows(tmp_path):
    _flat_project(tmp_path, ["Oh no\\nbecause so.", "Gran--", "Tuskur came."])
    text = kp._scan(tmp_path, [kp._FLAT_SCENE])[0][1]
    assert "nbecause" not in text and "no because" in text
    assert "Gran-- Tuskur" not in kp._CAP_RUN.findall(text)


def test_scan_skips_bracketed_interface_headings(tmp_path):
    _flat_project(tmp_path, ["[About Battle Results]", "Oshtor spoke."])
    text = kp._scan(tmp_path, [kp._FLAT_SCENE])[0][1]
    assert "Battle" not in text and "Oshtor" in text


def test_truecasing_trim_company_and_laughter():
    vocab = {"guide", "eight", "pillar", "generals"}
    assert kp._trim_common_lead("Guide Mutikapa", vocab) == "Mutikapa"            # resto nunca em minuscula
    assert kp._trim_common_lead("Eight Pillar Generals", vocab) == "Eight Pillar Generals"
    corpus = "Plop!" + chr(10) + "Flinch." + chr(10) + "Kwese came home. Then Kwese left."
    assert kp._company("Plop", corpus) == 0 and kp._company("Kwese", corpus) == 2
    assert kp._interj("Nyahaha") and kp._interj("Hohoho") and not kp._interj("Kwese")


def test_capitalization_alone_is_not_evidence_of_a_name():
    assert kp._clean_cand("Tsetse Grass'll") == "Tsetse Grass"      # contracao nao e parte do nome
    assert kp._clean_cand("Wha--") == "" and kp._clean_cand("Gran--") == ""   # palavra cortada
    corpus = "Battle Results" + chr(10) + "Then Oshtor Haku spoke, Oshtor Haku left."
    assert kp._strong({"cand": "Battle Results", "multi": True, "count": 1}, corpus) is False
    assert kp._midsentence("Battle Results", "so far" + chr(10) + "Battle Results") is False   # linha nova nao e meio de frase
    assert kp._strong({"cand": "Oshtor Haku", "multi": True, "count": 2}, corpus) is True


def test_strong_rejects_adverbs_and_contractions():
    assert kp._strong({"cand": "Really", "multi": False, "count": 9}, "x Really y") is False
    assert kp._strong({"cand": "Couldn't", "multi": False, "count": 9}, "x") is False


def test_coverage_reports_unanchored_entities_and_one_off_warning(tmp_path, monkeypatch):
    _flat_project(tmp_path, ["Then Oshtor spoke, Oshtor left."])    # 2x na mesma cena: gap, mas nao bloqueia
    paths.research_log(tmp_path).write_text("**Status:** reconciled\n", encoding="utf-8")
    monkeypatch.setattr(kp.kb_review, "blocking",
                        lambda r, c, strict=False: [{"name": "Haku", "blockers": ["fonte", "ratificacao"]}])
    cov = kp.coverage(tmp_path, "all", strict=True)
    assert any("Haku (fonte/ratificacao)" in p and "kb_ratified.csv" in p for p in cov["problems"])
    assert any("baixa confianca" in w for w in cov["warnings"])


def test_apply_frontier_without_scenes_or_field_is_noop(tmp_path):
    _flat_project(tmp_path, ["Haku spoke."])
    assert kp.apply_frontier(tmp_path, "ch_99") is None             # capitulo sem cenas
    (tmp_path / "project.json").write_text('{"title":"T"}', encoding="utf-8")
    assert kp.apply_frontier(tmp_path, "all") is None               # sem campo kb_frontier: nao insere


def test_worklist_says_so_when_nothing_is_uncovered(tmp_path):
    _flat_project(tmp_path, ["Haku spoke."])
    txt = kp.write_worklist(tmp_path, "all").read_text(encoding="utf-8")
    assert "nenhum — todos os nomes proprios fortes" in txt


def test_worklist_lists_weak_candidates_and_truncates_at_40(tmp_path):
    names = [f"Kq{chr(97 + i // 26)}{chr(97 + i % 26)}" for i in range(45)]
    _flat_project(tmp_path, [f"{n} came." for n in names])
    txt = kp.write_worklist(tmp_path, "all").read_text(encoding="utf-8")
    assert "Candidatos FRACOS" in txt and "(+5 mais)" in txt


def test_onda_lists_one_off_and_respects_cap(tmp_path):
    _flat_project(tmp_path, ["When Oshtor arrived, Zarkul bowed.", "Then Qwerin left."])
    got = [r["cand"] for r in kp.onda(tmp_path, ["_flat"], max_n=2)]
    assert len(got) == 2 and set(got) <= {"Oshtor", "Zarkul", "Qwerin"}


def test_onda_drops_interjections():
    assert kp._interj("Uhhh") and kp._interj("Mmm") and kp._interj("Nrgh") and not kp._interj("Potum")


def test_kind_separates_names_from_common_labels_by_frequency():
    vocab = {"voice"}
    zipf = {"barricade": 3.09, "dummy": 3.64, "enemy": 4.5, "rank": 4.4, "saraana": 0.0, "uruuru": 0.0, "sahara": 3.4, "ability": 4.96}.get
    z = lambda w: zipf(w, 0.0)  # noqa: E731
    k = lambda cand, rotulo=True, f=z: kp._kind({"cand": cand, "rotulo": rotulo}, vocab, f)  # noqa: E731
    assert k("Voice") == "ui" and k("Barricade") == "ui" and k("Dummy") == "ui" and k("Enemy Rank") == "ui"
    assert k("Saraana") == "nome" and k("Uruuru") == "nome" and k("Oshtor Cohort") == "nome"
    assert k("Sahara", rotulo=False) == "nome" and k("Dummy", rotulo=False) == "nome"   # comum, mas em fala corrida
    assert k("Ability", rotulo=False) == "ui"                                                  # corrente demais para ser nome
    assert k("Barricade", f=None) == "nome" and k("Voice", f=None) == "ui"                    # sem wordfreq: so o vocabulario


def test_so_rotulo_looks_at_every_occurrence():
    assert kp._so_rotulo("Dummy", ["Dummy", "Training Dummy", "Hit the wall"])
    assert not kp._so_rotulo("Sahara", ["Sahara", "He is confined in a prison on Sahara Island"])
    assert not kp._so_rotulo("Ghost", ["nothing here"])


def test_zipf_fn_uses_the_projects_source_language_and_degrades(tmp_path):
    (tmp_path / "project.json").write_text('{"source_language": "en"}', encoding="utf-8")
    z = kp._zipf_fn(tmp_path)
    if z is not None:                                # wordfreq e opcional
        assert z("dummy") >= kp._ZIPF_COMUM > z("saraana")
    (tmp_path / "project.json").write_text('{"source_language": "xx"}', encoding="utf-8")
    assert kp._zipf_fn(tmp_path) is None             # lingua sem dados: cai no vocabulario do jogo


def test_onda_tags_every_candidate_with_a_kind(tmp_path):
    _flat_project(tmp_path, ["When Oshtor arrived, Barricade fell.", "Then Oshtor left, Barricade rose."])
    got = {r["cand"]: r["kind"] for r in kp.onda(tmp_path, ["_flat"])}
    assert got.get("Oshtor") == "nome" and got.get("Barricade") in ("ui", "nome")
