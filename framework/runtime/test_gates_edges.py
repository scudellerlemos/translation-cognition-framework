"""test_gates_edges.py — ramos de falha dos gates de KB e do lint de glossário: arquivo corrompido/ilegível
vira problema explícito (nunca passa calado), e o filtro de termos do glossário só audita o que deve.
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import glossary_lint  # noqa: E402
import kb_gate  # noqa: E402
import paths  # noqa: E402


def _res():
    return {"hard_problems": [], "problems": [], "warnings": [], "pending_decisions": []}


def _put(path: Path, data) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    (path.write_bytes if isinstance(data, bytes) else path.write_text)(data)
    return path


# --- kb_gate ----------------------------------------------------------------------------------------
def test_pending_decisions_stop_at_next_heading():
    txt = "## Decisões pendentes\n1. **Chamar Kuon de X?**\n2. Outro\n## Proxima secao\n3. nao entra\n"
    assert kb_gate._parse_pending_decisions(txt) == ["Chamar Kuon de X?", "Outro"]


def test_corrupt_project_json_is_a_hard_problem(tmp_path):
    _put(tmp_path / "project.json", "{nao e json")
    res = _res()
    assert kb_gate._load_cfg(tmp_path, res) == {}
    assert "project.json corrompido" in res["hard_problems"][0]


def test_empty_db_glossary_is_a_problem():
    res = _res()
    kb_gate._check_glossary_present(Path("."), "db.sqlite", [], res)
    assert "glossario vazio no DB" in res["problems"][0]


def test_invalid_voice_cards_json_is_a_problem(tmp_path):
    _put(paths.voice_cards(tmp_path), "{nao e json")
    res = _res()
    kb_gate._check_voice_cards(tmp_path, res)
    assert "voice_cards.json invalido" in res["problems"][0]


def test_unreadable_glossary_csv_is_a_problem_not_a_crash(tmp_path):
    _put(paths.glossary(tmp_path), b"\xff\xfe\x80 nao e utf-8\n")
    res = _res()
    kb_gate._check_glossary_dated(tmp_path, None, [], res)
    assert "glossary.csv ilegivel" in res["problems"][0]


def test_ratified_csv_header_only_is_ignored_and_unreadable_only_warns(tmp_path):
    kr = _put(paths.kb_ratified(tmp_path), "name,date_ratified\n")     # so cabecalho: nada a checar
    res = _res()
    kb_gate._check_ratified_dates(tmp_path, res)
    assert res["warnings"] == []
    kr.write_bytes(b"\xff\xfe\x80 lixo\n")
    kb_gate._check_ratified_dates(tmp_path, res)
    assert "kb_ratified.csv ilegivel" in res["warnings"][0]


# --- glossary_lint ----------------------------------------------------------------------------------

def test_glossary_lint_has_form_accepts_inflection_and_abbreviation():
    def has(expected, target):
        return glossary_lint._has_form(expected, target.split())
    assert has("imperial", "as tropas imperiais")           # plural
    assert has("eternos", "uma eterna")                     # genero
    assert has("selecionar", "selecione um topico")         # verbo
    assert has("penhasco", "penhas")                        # abreviacao
    assert has("planicies douradas", "nas planicies douradas")
    assert not has("mausoleu", "a tumba")
    assert not has("ponto de oceano", "ponto de mar")


def test_glossary_lint_skips_term_that_only_opens_a_sentence():
    skip = glossary_lint._only_sentence_initial
    assert skip("Try", '"Did you see him? Try looking north."')      # maiuscula da frase
    assert skip("Select", "Setas: Select um item")              # apos ':'
    assert skip("Love", "Gatos[0B]Love[0B]Viagens")             # codigo de controle separa opcoes
    assert not skip("Select", '[14]"Select"')                       # a linha e o rotulo
    assert not skip("Endless", "Behold the Endless!")               # meio da frase
    assert not skip("Ocean Spot", "Ocean Spot 1")                   # termo composto: sempre audita
    assert not skip("village", "Village of the wind")               # termo minusculo: sempre audita


def test_load_glossary_flat_filters_what_is_not_auditable(tmp_path):
    _put(paths.glossary(tmp_path),
         "term,handling_rule,target_translation,aliases\n"
         "Ab,traduzir,X,\n"                             # termo curto demais
         "man,traduzir,homem,\n"                        # palavra-comum: traducao por contexto
         "Foo,traduzir,,\n"                             # sem alvo definido
         "Kuon,manter_original,,alias1;alias2\n"        # nome proprio: verbatim + aliases
         "Warmaster,traduzir,Mestre de Guerra,\n")
    assert glossary_lint._load_glossary(tmp_path, cfg={}) == [
        ("Kuon", ["Kuon", "alias1", "alias2"], "manter_original"),
        ("Warmaster", ["Mestre de Guerra"], "traduzir"),
    ]


def test_lint_kept_name_hides_the_common_word_inside_it(tmp_path, monkeypatch):
    _put(paths.glossary(tmp_path),
         "term,handling_rule,target_translation,aliases\n"
         "Ice,traduzir,Gelo,\n"
         "Ring of Ice,manter_original,,\n")
    lines = {"a": {"source": "Ring of Ice", "target": "Ring of Ice"},          # nome preservado: ok
             "b": {"source": "Two Ring of Ices.", "target": "Dois Ring of Ice."},   # plural do nome: ok
             "c": {"source": "The Ice melts.", "target": "O frio derrete."},    # termo solto: acusa
             "d": {"source": "Ring of Ice", "target": "Anel de Gelo"}}          # nome traduzido: acusa
    monkeypatch.setattr(glossary_lint.context_pack, "load_translated_scenes", lambda root: [("s", "s", lines)])
    assert [(f["offset"], f["term"]) for f in glossary_lint.lint(tmp_path)] == [("c", "Ice"), ("d", "Ring of Ice")]


def test_lint_without_glossary_is_empty(tmp_path):
    assert glossary_lint._load_glossary(tmp_path, cfg={}) == []
    assert glossary_lint.lint(tmp_path) == []


def test_lint_scope_blocks_only_requested_scenes_and_warns_about_the_rest():
    found = [{"scene": "a", "offset": "a:1"}, {"scene": "b", "offset": "b:1"}]
    assert glossary_lint.split_scope(found, None) == (found, [])          # sem --scenes: tudo bloqueia
    assert glossary_lint.split_scope(found, []) == (found, [])
    assert glossary_lint.split_scope(found, ["a"]) == ([found[0]], [found[1]])
    assert glossary_lint.split_scope(found, ["c"]) == ([], found)          # cena limpa fecha com aviso


def test_quality_gate_scope_blocks_only_requested_scenes():
    import quality_gate
    items = [{"scene": "a", "offset": "a:1"}, {"scene": "b", "offset": "b:1"}]
    assert quality_gate.split_scope(items, None) == (items, [])
    assert quality_gate.split_scope(items, ["a"]) == ([items[0]], [items[1]])
