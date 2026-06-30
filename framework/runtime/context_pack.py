#!/usr/bin/env python3
"""
context_pack.py — monta o CONTEXTO LIMITADO e AUTO-CONTIDO de UMA cena (a peca central do harness).

Em vez de carregar glossario inteiro + decision_log + capitulos anteriores na janela da LLM (contexto
O(historico) -> estoura a sessao), monta um pacote O(cena): so o que ESTA cena precisa.

Pacote = doutrina cacheavel (a Carta) + regras do conector (project.json) + SUBCONJUNTO do glossario
(so termos que aparecem) + voice cards dos falantes relevantes + decisoes relevantes (por tag/universal)
+ hits de memoria de traducao (TM) + as linhas-fonte + byte budgets.

Emite, no dir da cena (`<projeto>/artifacts/<scene>/`):
  - scene_prompt.md : auto-contido, pronto p/ o modelo responder em UM turno (caminho assinatura: da
                      p/ rodar 1 cena por sessao limpa -> contexto nunca acumula).
  - pack.json       : a mesma informacao, estruturada (consumida pelo run_scene / caminho API).

GOVERNANCA: determinista (rodar 2x -> byte-identico), sem rede, sem work-text hardcoded. Le os indices
de `state_index.py` (auto-constroi se faltarem).

Uso:  python context_pack.py <dir-do-projeto> <scene>     ex.: python context_pack.py projects/utawarerumono ch_12_01
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

import paths  # noqa: E402  (paths.py: fonte unica do contrato de caminhos de artefato)

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import state_index  # noqa: E402  (sibling no mesmo dir)

FRAMEWORK = _HERE.parent
CARTA_PATH = FRAMEWORK / "skills" / "translation_governance.md"
TOKEN = chr(92) + "n"

MAX_DECISIONS = 12          # universal + matched, teto p/ manter o pacote limitado
MAX_TM_VOICE_PER_SPEAKER = 3  # exemplos de "voz estabelecida" por falante presente


def _doctrine_hash(root: Path) -> str:
    """SHA1 curto dos artefatos de doutrina — detecta se a carta ou o KB mudou desde a última tradução."""
    h = hashlib.sha1(usedforsecurity=False)
    art = Path(root) / "artifacts"
    for p in [CARTA_PATH, art / "glossary.csv", art / "decision_log.md", art / "tone_analysis.md"]:
        if p.is_file():
            h.update(p.read_bytes())
    return h.hexdigest()[:16]


def _skills_revision() -> str:
    """SHA1 curto de todos os .md em framework/skills/ — versão das skills e da Carta."""
    h = hashlib.sha1(usedforsecurity=False)
    for p in sorted(FRAMEWORK.glob("skills/**/*.md")):
        h.update(p.read_bytes())
    return h.hexdigest()[:12]


def scene_id_of(scene: str) -> str:
    return scene[3:] if scene.startswith("ch_") else scene


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.is_file() else ""


_DIALOGS_TEXT_COLS = ("text_source", "text_en")


def validate_dialogs_csv(path: Path) -> list:
    """A4: valida schema do dialogs.csv — retorna lista de problemas (vazia = OK).
    Chamada em build_pack() antes de load_dialogs() para erros antecipados e legíveis."""
    problems = []
    try:
        with path.open(encoding="utf-8") as fh:
            rdr = csv.DictReader(fh)
            fields = frozenset(rdr.fieldnames or [])
            for col in ("offset", "byte_budget"):
                if col not in fields:
                    problems.append(f"coluna obrigatória ausente: '{col}'")
            if not any(c in fields for c in _DIALOGS_TEXT_COLS):
                problems.append(f"coluna de texto ausente — esperada uma de: {_DIALOGS_TEXT_COLS}")
            if problems:
                return problems
            for i, row in enumerate(rdr, start=2):
                if not (row.get("offset") or "").strip():
                    problems.append(f"linha {i}: offset vazio")
                bv = (row.get("byte_budget") or "").strip()
                if bv and not bv.lstrip("-").isdigit():
                    problems.append(f"linha {i}: byte_budget não-numérico: {bv!r}")
    except (OSError, csv.Error) as e:
        problems.append(f"erro ao ler: {e}")
    return problems


def load_dialogs(p: Path):
    rows = []
    with p.open(encoding="utf-8") as fh:
        rdr = csv.DictReader(fh)
        textcol = "text_source" if "text_source" in (rdr.fieldnames or []) else "text_en"
        for r in rdr:
            rows.append({"offset": r["offset"], "source": r.get(textcol, ""),
                         "byte_budget": int(r["byte_budget"])})
    return rows


def load_glossary(p: Path):
    out: list[dict] = []
    if not p.is_file():
        return out
    with p.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out.append(r)
    return out


def _present(needle: str, blob_low: str) -> bool:
    n = (needle or "").strip().lower()
    if not n:
        return False
    if n.isalnum():
        # tolera plural/inflexao inglesa (termo + s/es opcional): 'gigiri' casa 'gigiris', 'cohort' casa
        # 'cohorts', 'general' casa 'generals'. Possessivo ("ukon's") ja casa pelo \b no apostrofo.
        # Conservador (so sufixo plural) -> mais recall sem virar substring solta. Primitiva unica de
        # match: vale p/ glossario, vozes e gatilhos de spoiler de uma vez.
        return re.search(r"\b" + re.escape(n) + r"(?:e?s)?\b", blob_low) is not None
    return n in blob_low


_GLOSSARY_CAP = 60   # max entradas por pack; acima disso o contexto da IA começa a saturar

def select_glossary(glossary, blob_low):
    sub = []
    for g in glossary:
        terms = [g.get("term", "")] + [a for a in (g.get("aliases", "") or "").split(";") if a]
        if any(_present(t, blob_low) for t in terms):
            sub.append({"term": g.get("term", ""), "category": g.get("category", ""),
                        "target_translation": g.get("target_translation", ""),
                        "handling_rule": g.get("handling_rule", ""),
                        "spoiler_level": g.get("spoiler_level", ""),
                        "notes": g.get("notes", "")})
    sub = sorted(sub, key=lambda x: x["term"].lower())
    if len(sub) > _GLOSSARY_CAP:
        import warnings
        warnings.warn(
            f"select_glossary: {len(sub)} termos casaram na cena, truncando para {_GLOSSARY_CAP}. "
            "Glossario cresceu demais? Considere dividir por dominio ou aumentar _GLOSSARY_CAP.",
            stacklevel=3)
        sub = sub[:_GLOSSARY_CAP]
    return sub


def select_voices(voice_cards, blob_low):
    """Falantes relevantes = high-criticality (sempre, narracao/voz principal) ∪ os citados na cena."""
    sel = {}
    for name, card in voice_cards.items():
        names = [name] + card.get("aliases", [])
        matched = any(_present(x, blob_low) for x in names)
        if card.get("criticality") == "high" or matched:
            sel[name] = card
    return dict(sorted(sel.items()))


def select_decisions(decisions, present_terms, present_speakers):
    toks = {t.lower() for t in present_terms} | {s.lower() for s in present_speakers}
    chosen, seen = [], set()
    for d in decisions:                       # universais primeiro (regras do conector)
        if d.get("universal") and d["title"] not in seen:
            chosen.append(d); seen.add(d["title"])
    for d in decisions:                       # depois: casadas por TAG (titulo) OU pelo SUMMARY (conteudo)
        if d["title"] in seen:
            continue
        tags = {t.lower() for t in d.get("tags", [])}
        summ = (d.get("summary", "") or "").lower()
        # match por conteudo do summary aumenta o recall de decisoes relevantes que o tag de titulo nao
        # pega (ex.: decisao sobre um termo citado so no corpo). Continua bounded por MAX_DECISIONS.
        if (toks & tags) or any(_present(t, summ) for t in toks):
            chosen.append(d); seen.add(d["title"])
    return chosen[:MAX_DECISIONS]


def load_tm(p: Path):
    tm: list[dict] = []
    if not p.is_file():
        return tm
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            tm.append(json.loads(line))
    return tm


def select_tm(tm, scene_rows, present_speakers):
    """Hits exatos (mesma fala ja traduzida antes) + amostra de voz estabelecida por falante presente."""
    by_key: dict[str, dict] = {}
    for e in tm:
        by_key.setdefault(e["src_key"], e)
    exact = []
    seen_keys = set()
    for r in scene_rows:
        k = state_index._key(r["source"])
        if k in by_key and k not in seen_keys:
            h = by_key[k]
            exact.append({"source": h["source"], "target": h["target"],
                          "speaker": h["speaker"], "from_scene": h["scene"]})
            seen_keys.add(k)
    voice = []
    speakers_low = {s.lower() for s in present_speakers}
    per: dict[str, int] = {}
    for e in tm:                              # ordem estavel (TM ja vem ordenada)
        sp = (e.get("speaker") or "").lower()
        if sp in speakers_low and per.get(sp, 0) < MAX_TM_VOICE_PER_SPEAKER:
            voice.append({"speaker": e["speaker"], "source": e["source"], "target": e["target"]})
            per[sp] = per.get(sp, 0) + 1
    return exact, voice


def _pos(scene_id: str):
    """scene_id -> tupla numerica de posicao narrativa p/ comparacao. Extrai TODA sequencia de
    digitos (robusto a esquemas sem '_': '12_03'->(12,3), 'AREAD050'->(50,), 'AREAD001'->(1,)).
    Sem digito nenhum -> () (incomparavel); os callers tratam isso como default-SAFE/deny."""
    return tuple(int(m) for m in re.findall(r"\d+", str(scene_id)))


def select_spoiler_guards(ledger: dict, blob_low: str, scene_id: str) -> list:
    """FILTRO TEMPORAL: para os fatos cujo reveal e FUTURO em relacao a esta cena, retorna o guard de
    ambiguidade se a entidade aparece nesta cena. Disparo por (a) `scenes` explicitas (scene_id) ou (b)
    `triggers` casados por LIMITE DE PALAVRA (_present, evita 'system' em 'system of gears').
    reveal='beyond_frontier' = sempre futuro p/ cenas na fronteira; reveal=<scene_id> = futuro se > a cena."""
    out = []
    here = _pos(scene_id)
    for e in (ledger or {}).get("entries", []):
        rev = e.get("reveal", "beyond_frontier")
        rp = _pos(rev)
        # DEFAULT-SAFE: beyond_frontier, ou posicao incomparavel (reveal/cena sem numero), trata
        # como FUTURO -> guarda. Nunca PULA o guard por nao conseguir ordenar (evita vazamento;
        # espelha o default-deny da select_kb). So omite o guard quando PROVADAMENTE ja revelado.
        future = True if (rev == "beyond_frontier" or not rp or not here) else (rp > here)
        if not future:
            continue
        in_scenes = scene_id in {scene_id_of(s) for s in e.get("scenes", [])}
        by_trigger = any(_present(t, blob_low) for t in e.get("triggers", []))
        if in_scenes or by_trigger:
            out.append({"entity": e.get("entity", ""), "fact": e.get("fact", ""),
                        "spoiler_level": e.get("spoiler_level", ""), "guard": e.get("pre_reveal", "")})
    return out


def project_constraints(cfg: dict) -> dict:
    conn = cfg.get("connector", {})
    return {
        "formatting_tokens": cfg.get("formatting_tokens", []),
        "formatting_token_patterns": cfg.get("formatting_token_patterns", []),
        "system_line_convention": cfg.get("system_line_convention", ""),
        "length_constraints": cfg.get("length_constraints", {}),
        "newline_token": TOKEN,
        "target_charset_supported": conn.get("target_charset_supported", True),
        "charset_note": conn.get("charset_note", ""),
        "space_strategy": conn.get("space_strategy", ""),
    }


def _db_path(root: Path, cfg: dict):
    """(db_path, project_id) se o projeto declara um `db` populado; senão (None, None).
    Com DB presente, o context_pack lê as fontes do SQLite; senão, dos flat files (BoF4)."""
    db = cfg.get("db") or {}
    rel = db.get("path")
    if not rel:
        return None, None
    p = Path(root) / rel
    if not p.is_file():
        return None, None
    return p, db.get("project_id", "")


def _load_sources_db(db_path: Path, project_id: str):
    """Lê glossary/voice_cards/decisions/tm/ledger do SQLite e ADAPTA para a MESMA forma
    dos loaders flat (assim os select_* não precisam saber a origem)."""
    _db_dir = str(FRAMEWORK / "db")
    if _db_dir not in sys.path:
        sys.path.insert(0, _db_dir)
    from store import Store
    with Store(db_path) as db:
        g_rows = db.get_glossary(project_id)
        vc_rows = db.get_voice_cards(project_id)
        dec_rows = db.get_decisions(project_id)
        sp_rows = db.get_spoiler_entries(project_id)
        tm_rows = db.get_translations(project_id, approved_only=True)
    glossary = [{
        "term": r.get("term", ""), "aliases": r.get("aliases") or "",
        "category": r.get("category") or "", "target_translation": r.get("translation") or "",
        "handling_rule": r.get("handling_rule") or "", "spoiler_level": r.get("spoiler_level") or "",
        "notes": r.get("notes") or "",
    } for r in g_rows]
    voice_cards = {r["speaker"]: {
        "aliases": r.get("aliases") or [], "criticality": r.get("criticality") or "",
        "lines": r.get("lines") or [],
    } for r in vc_rows}
    decisions = [{
        "title": d.get("title", ""), "summary": d.get("summary") or "",
        "universal": bool(d.get("universal")), "tags": d.get("tags") or [],
    } for d in dec_rows]
    tm = [{
        "src_key": state_index._key(r.get("source", "")), "source": r.get("source", ""),
        "target": r.get("target") or "", "speaker": r.get("speaker") or "",
        "scene": r.get("scene_id") or "",
    } for r in tm_rows]
    ledger = {"entries": [{
        "entity": e.get("entity", ""), "fact": e.get("fact") or "",
        "spoiler_level": e.get("spoiler_level") or "", "reveal": e.get("reveal") or "beyond_frontier",
        "scenes": e.get("scenes") or [], "triggers": e.get("triggers") or [],
        "pre_reveal": e.get("pre_reveal") or "",
    } for e in sp_rows]}
    return glossary, voice_cards, decisions, tm, ledger


def _load_lines(root: Path, cfg: dict, scene: str):
    """Linhas da cena (offset/source/byte_budget). Do SQLite se o projeto tem `db`;
    senão de dialogs.csv (com a validação A4 original)."""
    db_path, db_pid = _db_path(root, cfg)
    if db_path:
        _db_dir = str(FRAMEWORK / "db")
        if _db_dir not in sys.path:
            sys.path.insert(0, _db_dir)
        from store import Store
        with Store(db_path) as db:
            rows = db.get_scene_lines(db_pid, scene_id_of(scene))
        if not rows:
            raise SystemExit(f"ERRO: cena {scene} sem linhas no DB ({db_path})")
        return rows
    scene_dir = paths.scene_dir(root, scene)
    if not (scene_dir / "dialogs.csv").is_file():
        raise SystemExit(f"ERRO: {scene_dir/'dialogs.csv'} nao encontrado")
    for prob in validate_dialogs_csv(scene_dir / "dialogs.csv"):
        print(f"[A4] AVISO dialogs.csv ({scene}): {prob}")
    return load_dialogs(scene_dir / "dialogs.csv")


def _load_sources(root: Path, cfg: dict):
    """(glossary, voice_cards, decisions, tm, ledger) — do SQLite se o projeto tem `db`
    populado; senão dos flat files (comportamento original; BoF4 intacto)."""
    db_path, db_pid = _db_path(root, cfg)
    if db_path:
        return _load_sources_db(db_path, db_pid)
    state = paths.state_dir(root)
    if not (paths.translation_memory(root)).is_file():
        state_index.build(root)               # auto-constroi os indices se faltarem
    glossary = load_glossary(paths.glossary(root))
    voice_cards = json.loads(_read(state / "voice_cards.json") or "{}")
    decisions = json.loads(_read(state / "decision_index.json") or "[]")
    tm = load_tm(paths.translation_memory(root))
    ledger_path = paths.spoiler_ledger(root)
    if not ledger_path.is_file():
        import warnings
        warnings.warn(
            f"spoiler_ledger.json nao encontrado em {ledger_path} — "
            "guards de spoiler DESATIVADOS para esta cena. Crie o ledger ou verifique se foi deletado.",
            stacklevel=3)
        ledger = {}
    else:
        ledger = json.loads(_read(ledger_path) or "{}")
    return glossary, voice_cards, decisions, tm, ledger


_EMBEDDER = None
_EMBEDDER_MISSING = False


def _get_embedder():
    """Embedder lazy + CACHEADO no módulo: o modelo (~470MB) é carregado UMA vez por processo,
    não a cada build_pack. Retorna None se o stack de ML não está instalado (fallback esperado,
    silencioso). Falha inesperada NA CONSTRUÇÃO propaga (não é o caso "sem deps")."""
    global _EMBEDDER, _EMBEDDER_MISSING
    if _EMBEDDER is not None or _EMBEDDER_MISSING:
        return _EMBEDDER
    _db_dir = str(FRAMEWORK / "db")
    if _db_dir not in sys.path:
        sys.path.insert(0, _db_dir)
    try:
        # sentence_transformers carrega lazy no Embedder.__init__ — o ImportError do stack
        # ausente estoura na CONSTRUÇÃO, não no import do módulo; por isso ambos no try.
        from embedder import Embedder
        _EMBEDDER = Embedder()
    except ImportError:
        _EMBEDDER_MISSING = True       # stack de ML ausente (caso da CI) — fallback esperado
        return None
    return _EMBEDDER


def _load_tm_semantic(db_path, project_id, rows, k: int = 3, max_hits: int = 8):
    """Vizinhos SEMÂNTICOS (similares, NÃO idênticos) das linhas da cena — p/ reuso de
    voz/fraseado em falas parecidas (RAG). Suplemento ROTULADO; nunca entra no match exato.
    Fallback: sem o stack de embeddings/sqlite-vec ou sem índice → [] (sem erro).
    Determinismo: ordem estável (score desc, source) sobre vetores pré-computados no DB."""
    if not db_path:
        return []
    try:
        emb = _get_embedder()
        if emb is None:
            return []                  # stack de ML ausente → fallback silencioso (esperado)
        from store import Store, strip_codes
        out, seen = [], set()
        with Store(db_path) as db:
            for r in rows:
                for hit in emb.search(db._con, r.get("source", ""), project_id=project_id, k=k):
                    if float(hit.get("score", 0)) >= 0.999:    # match exato já está em tm_exact
                        continue
                    key = (hit.get("source", ""), hit.get("target", ""))
                    if key in seen:
                        continue
                    seen.add(key)
                    # exibe a forma LIMPA (sem códigos do jogo) — fiel fica no banco
                    out.append({"source": strip_codes(hit.get("source", "")),
                                "target": strip_codes(hit.get("target", "")),
                                "speaker": hit.get("speaker", ""),
                                "score": round(float(hit.get("score", 0)), 3)})
        out.sort(key=lambda h: (-h["score"], h["source"]))     # ordem estável (determinismo)
        return out[:max_hits]
    except Exception as e:             # noqa: BLE001
        # falha INESPERADA com o stack PRESENTE (índice ausente, sqlite-vec não carregou, OOM):
        # NÃO mascarar como "sem vizinhos" — avisa (visível) e cai p/ [] sem derrubar o pacote.
        import warnings as _w
        _w.warn(f"TM semântica falhou (stack presente): {e!r} — pacote sem seção semântica.",
                stacklevel=2)
        return []


_KB_CAP = 5


def _load_kb(db_path, project_id):
    """Seções da KB do projeto (lore). Sem ML — SQL puro. [] se sem db/erro."""
    if not db_path:
        return []
    try:
        _db_dir = str(FRAMEWORK / "db")
        if _db_dir not in sys.path:
            sys.path.insert(0, _db_dir)
        from store import Store
        with Store(db_path) as db:
            return db.get_kb(project_id)
    except Exception:
        return []


_KB_SAFE = {"safe", "always", "sempre", "public", "publico"}


def select_kb(kb, blob_low, scene_id, cap=_KB_CAP):
    """Seções da KB relevantes à cena, com GATE de spoiler DEFAULT-DENY: uma seção só é injetada
    se PROVADAMENTE segura — ou `reveal` marcado 'safe', ou `reveal` = uma cena JÁ passada
    (≤ cena atual). Sem `reveal`, ou 'beyond_frontier', ou reveal FUTURO → EXCLUÍDA. A garantia
    de não-vazamento vem do dado explícito por seção (não de matching de texto EN↔PT).
    Relevância: o nome/tema da seção é citado nas falas. Determinístico, sem ML."""
    here = _pos(scene_id)
    out = []
    for sec in kb:
        reveal = (sec.get("reveal") or "").strip().lower()
        if reveal in _KB_SAFE:
            allowed = True
        elif reveal and reveal not in ("beyond_frontier", "bf"):
            rp = _pos(reveal)
            allowed = bool(rp) and rp <= here          # já revelado até esta cena
        else:
            allowed = False                            # sem tag / beyond_frontier → default-deny
        if not allowed:
            continue
        title = sec.get("section", "")
        toks = [w for w in re.split(r"[^\wçáàâãéêíóôõúü]+", title.lower()) if len(w) >= 4]
        if toks and any(_present(w, blob_low) for w in toks):  # relevância: tema citado na cena
            out.append({"section": title, "content": sec.get("content", "")})
        if len(out) >= cap:
            break
    return out


def build_pack(root: Path, scene: str) -> dict:
    root = Path(root)
    cfg = json.loads((root / "project.json").read_text(encoding="utf-8"))
    rows = _load_lines(root, cfg, scene)
    blob_low = "\n".join(r["source"] for r in rows).lower()

    glossary, voice_cards, decisions, tm, ledger = _load_sources(root, cfg)

    gsub = select_glossary(glossary, blob_low)
    voices = select_voices(voice_cards, blob_low)
    present_terms = [g["term"] for g in gsub]
    present_speakers = list(voices.keys())
    dsel = select_decisions(decisions, present_terms, present_speakers)
    tm_exact, tm_voice = select_tm(tm, rows, present_speakers)
    db_path, db_pid = _db_path(root, cfg)
    tm_semantic = _load_tm_semantic(db_path, db_pid, rows) if db_path else []
    # KB com gate default-deny por seção (só injeta reveal já-passado/safe). Seguro por construção.
    kb = select_kb(_load_kb(db_path, db_pid), blob_low, scene_id_of(scene)) if db_path else []

    spoiler_guards = select_spoiler_guards(ledger, blob_low, scene_id_of(scene))

    return {
        "scene": scene, "scene_id": scene_id_of(scene), "n_lines": len(rows),
        "doctrine": "framework/skills/translation_governance.md",
        "doctrine_hash": _doctrine_hash(root),
        "skills_revision": _skills_revision(),
        "project_constraints": project_constraints(cfg),
        "glossary_subset": gsub,
        "voice_cards": voices,
        "decisions": dsel,
        "tm_exact": tm_exact,
        "tm_voice": tm_voice,
        "tm_semantic": tm_semantic,
        "kb": kb,
        "spoiler_guards": spoiler_guards,
        "lines": rows,
    }


# ------------------------------ render scene_prompt ----------------------------

def render_prompt(pack: dict, carta: str) -> str:
    pc = pack["project_constraints"]
    L = []
    L.append(f"# Cena {pack['scene']} — pacote de traducao ({pack['n_lines']} linhas)")
    L.append("")
    L.append("> Pacote AUTO-CONTIDO e LIMITADO (so o que esta cena precisa). Traduza EN -> pt-BR")
    L.append("> seguindo a Carta abaixo. Saida exigida ao final. Nao precisa de contexto externo.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## 1. CARTA DE GOVERNANCA (contrato de qualidade)")
    L.append("")
    if carta.strip():
        L.append(carta.strip())
    else:
        L.append("> (Carta fornecida no system cacheado — `framework/skills/translation_governance.md`.)")
    L.append("")
    L.append("## 2. Regras do conector / projeto")
    L.append(f"- Token de quebra de linha: `{pc['newline_token']}` (literal; preservar EXATO, mesma posicao).")
    L.append(f"- Tokens de formatacao a preservar verbatim: {pc['formatting_tokens']} "
             f"+ padroes {pc['formatting_token_patterns']}.")
    L.append("- CRITICO — token `[02]` e QUEBRA DE PAGINA (page break do jogo): "
             "quando o source tem `[02]`, o campo `t` DEVE ter o mesmo numero de `[02]` "
             "na posicao equivalente. Omitir `[02]` causa falha de validacao e texto sem paginacao. "
             "Nao confunda com `[01]` (quebra de linha dentro da mesma pagina). "
             "Regra: contagem de `[02]` em `t` == contagem de `[02]` no texto source.")
    if pc.get("system_line_convention"):
        L.append(f"- Convencao de linha de sistema: {pc['system_line_convention']}.")
    lc = pc.get("length_constraints", {})
    if lc:
        L.append(f"- Restricao de comprimento: {lc} (orcamento em bytes por linha — ver coluna byte_budget).")
    if not pc.get("target_charset_supported", True):
        L.append(f"- ATENCAO charset: {pc['charset_note'][:200]}")
        L.append("  -> ESCREVA o campo `t` na forma canonica COM acentos/til normais (ex.: \"você\", "
                 "\"coração\"). A transliteracao p/ ASCII e feita DEPOIS pelo script de reinsercao — "
                 "nao remova acentos voce mesmo. Apenas nao dependa do acento para DISTINGUIR sentido "
                 "(ex.: evite pares que so diferem por acento), pois ele some no jogo.")
    L.append("")
    L.append("## 3. Glossario relevante (subconjunto desta cena)")
    if pack["glossary_subset"]:
        L.append("| termo | categoria | traducao | regra | spoiler |")
        L.append("|---|---|---|---|---|")
        for g in pack["glossary_subset"]:
            L.append(f"| {g['term']} | {g['category']} | {g['target_translation']} | "
                     f"{g['handling_rule']} | {g['spoiler_level']} |")
    else:
        L.append("_(nenhum termo do glossario aparece nesta cena)_")
    L.append("")
    L.append("## 4. Vozes presentes")
    for name, card in pack["voice_cards"].items():
        al = f" (aliases: {', '.join(card['aliases'])})" if card.get("aliases") else ""
        L.append(f"### {name} — criticality: {card.get('criticality','')}{al}")
        for b in card.get("lines", []):
            L.append(f"- {b}")
    L.append("")
    L.append("## 5. Decisoes relevantes (do decision_log)")
    for d in pack["decisions"]:
        flag = " [universal]" if d.get("universal") else ""
        L.append(f"- **{d['title']}**{flag}: {d['summary']}")
    L.append("")
    guards = pack.get("spoiler_guards", [])
    if guards:
        L.append("## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena")
        L.append("> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a")
        L.append("> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).")
        for g in guards:
            L.append(f"- **{g['entity']}** ({g['spoiler_level']}): {g['guard']}")
        L.append("")
    if pack.get("kb"):
        L.append("## 5c. Lore relevante (KB — apenas fatos JA revelados ate esta cena)")
        for s in pack["kb"]:
            L.append(f"### {s['section']}")
            L.append(s["content"])
        L.append("")
    L.append("## 6. Memoria de traducao (consistencia — nao reinventar)")
    if pack["tm_exact"]:
        L.append("**Falas identicas ja traduzidas (reusar):**")
        for e in pack["tm_exact"]:
            L.append(f"- `{e['source']}` -> `{e['target']}` ({e['speaker']}, {e['from_scene']})")
    if pack["tm_voice"]:
        L.append("**Voz estabelecida dos falantes (amostra):**")
        for e in pack["tm_voice"]:
            L.append(f"- {e['speaker']}: `{e['source']}` -> `{e['target']}`")
    if pack.get("tm_semantic"):
        L.append("**Falas SIMILARES (nao identicas) — use p/ voz/fraseado, ADAPTE ao contexto:**")
        for e in pack["tm_semantic"]:
            L.append(f"- (~{e['score']}) `{e['source']}` -> `{e['target']}`")
    if not pack["tm_exact"] and not pack["tm_voice"] and not pack.get("tm_semantic"):
        L.append("_(sem memoria previa para esta cena)_")
    L.append("")
    L.append("## 7. Linhas a traduzir")
    L.append("> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`")
    L.append("> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR")
    L.append("> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**")
    L.append("> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o")
    L.append("> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.")
    L.append("| offset | byte_budget | source |")
    L.append("|---|---|---|")
    for r in pack["lines"]:
        src = r["source"].replace("|", "\\|")
        L.append(f"| {r['offset']} | {r['byte_budget']} | {src} |")
    L.append("")
    L.append("## 8. Formato de saida EXIGIDO")
    L.append(f"Escreva `translations_{pack['scene_id']}.json` com a forma:")
    _known_voices = sorted(pack.get("voice_cards", {}).keys())
    _voice_hint = (", ".join(f"'{v}'" for v in _known_voices) + " ") if _known_voices else ""
    L.append(f"**Campo `speaker`:** use o nome EN exato da secao 4 para personagens conhecidos "
             f"({_voice_hint}); `'npc'` para NPCs sem perfil de voz; `'system'` para "
             f"narrador/sistema/tutorial; `'unknown'` se nao identificavel. "
             f"NAO use descricoes em portugues (ex.: NAO escreva 'Personagem' ou 'Vilao/NPC').")
    L.append("```json")
    L.append('{ "lines": {')
    L.append('  "<offset>": {"speaker": "<nome EN da sec4 | npc | system | unknown>", "tone_register": "...", "intent": "...",')
    L.append('    "risk_level": "low|medium|high|critical", "risk_notes": "(se >= medium)",')
    L.append('    "t": "<traducao pt-BR canonica, com acentos, com o token de quebra exato>"},')
    L.append("  ... 1 entrada por offset acima ...")
    L.append("} }")
    L.append("```")
    L.append("Regras: cobrir TODOS os offsets; preservar o token de quebra; risco >= medium exige")
    L.append("risk_notes; interjeicoes/onomatopeias = traducao (localizar, nao copiar). O build_plan")
    L.append("valida cobertura/tokens/risk_notes; linhas risco>=high passam por back-translation.")
    L.append("")
    return "\n".join(L)


def write_pack(root: Path, scene: str) -> dict:
    pack = build_pack(root, scene)
    scene_dir = paths.scene_dir(root, scene)
    carta = _read(CARTA_PATH)
    (scene_dir / "scene_prompt.md").write_text(render_prompt(pack, carta), encoding="utf-8")
    (scene_dir / "pack.json").write_text(
        json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
    return pack


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        sys.exit("uso: python context_pack.py <dir-do-projeto> <scene>")
    root, scene = Path(args[0]), args[1]
    pack = write_pack(root, scene)
    print(f"OK context_pack {scene}: {pack['n_lines']} linhas")
    print(f"  glossario: {len(pack['glossary_subset'])} termos | vozes: {len(pack['voice_cards'])} "
          f"| decisoes: {len(pack['decisions'])} | TM exato: {len(pack['tm_exact'])} "
          f"| TM voz: {len(pack['tm_voice'])}")
    print(f"  doctrine_hash: {pack['doctrine_hash']} | skills_revision: {pack['skills_revision']}")
    print(f"  -> artifacts/scenes/{scene}/scene_prompt.md + pack.json")


if __name__ == "__main__":
    main()
