"""translation_rules.py — regras de traducao compartilhadas pelos DOIS caminhos (ADR 0019).

Paridade do token de quebra, tokens de formatacao, orcamento de bytes, guarda de blow-up, rotulo de engine (passthrough)
e dedup por memoria de traducao. Funcoes puras sobre o pacote e as linhas: sem rede, sem I/O de cena, sem dependencia do
caminho de sessao nem do de API. `model` reexporta todos os nomes (compat com chamadores e monkeypatch de testes).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import budget as _bud  # noqa: E402  (budget.py: fonte unica da conta de bytes)
import context_pack  # noqa: E402
import paths  # noqa: E402
import state_index  # noqa: E402  (_key p/ dedup por TM)

_FRAMEWORK_CONNECTORS = _HERE.parent / "connectors"
if str(_FRAMEWORK_CONNECTORS) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK_CONNECTORS))
import connector_io  # noqa: E402  (structural_token_rx/structural_tokens_match compartilhados com o conector)


def _check_translation(data, offsets):
    """Retorna (offsets_com_quebra_real, offsets_faltando). Guard do bug do token \\n + cobertura."""
    lines = data.get("lines", {}) if isinstance(data, dict) else {}
    bad_nl = [off for off, v in lines.items() if "\n" in ((v or {}).get("t", "") or "")]
    missing = [o for o in offsets if o not in lines]
    return bad_nl, missing


def _translit_len(t) -> int:
    """Comprimento em bytes da forma TRANSLITERADA — o que o reinsert grava (conta em budget.py)."""
    return _bud.translit_len(t)


def _budget_len(t, pc: dict | None) -> int:
    """Metrica de orcamento do projeto (fonte unica: budget.py; espelha o que verify_chapter.py confere)."""
    return _bud.budget_len(t, pc)


def _over_budget(t, budget_, pc, tol) -> bool:
    """True se `t` excede budget*tol pela metrica do projeto, com a reserva do terminador (ver budget.py)."""
    return _bud.over_budget(t, budget_, pc, tol)


def _norm_t(t):
    """Normaliza o campo: CR/LF real -> token literal `\\n` (o modelo as vezes colapsa o token numa
    quebra real). Deterministico/idempotente. A PARIDADE com a fonte e ajustada em _parity_fit."""
    if not isinstance(t, str):
        return t
    tok = context_pack.TOKEN
    return t.replace("\r\n", tok).replace("\n", tok).replace("\r", tok)


def _parity_fit(source, t):
    """Ciente da fonte: se a FONTE nao tem token de quebra, o ALVO tambem nao pode ter (o modelo as
    vezes adiciona uma quebra espuria -> build_plan reprova por paridade). Troca token por espaco e
    colapsa. Se a fonte TEM quebra(s), mantem (o modelo costuma casar; mismatch multi-token -> retry)."""
    if not isinstance(t, str):
        return t
    tok = context_pack.TOKEN
    if tok not in (source or ""):
        out = t.replace(tok, " ")
        while "  " in out:
            out = out.replace("  ", " ")
        return out.strip()
    return t


def _structural_rx(pc: dict) -> re.Pattern:
    """Regex dos tokens de formatacao do engine (<C1>/<P2>/etc., de project.json via pc['formatting_tokens']
    + pc['formatting_token_patterns']). MESMA checagem que o build_plan_chapter do conector faz depois —
    feita AQUI tambem (dentro do retry de traducao) pra pegar token perdido/trocado ANTES de persistir,
    em vez de so falhar num gate sem auto-reparo rio abaixo (bug real: 7/447 linhas em mp0010_01,
    2026-08-24, o LLM as vezes derruba ou corrompe <C1>/<P2> e o retry existente so checava `\\n`).
    Constroi via connector_io.structural_token_rx (compartilhada com build_plan_chapter.py)."""
    pc = pc or {}
    return connector_io.structural_token_rx(
        pc.get("formatting_tokens", []), pc.get("formatting_token_patterns", []))


def _struct_ok(rx: re.Pattern, source: str, t: str) -> bool:
    """True se `t` preserva o MESMO multiset de tokens de formatacao que `source` (conta E tipo)."""
    return connector_io.structural_tokens_match(rx, source, t)


# Guarda contra BLOW-UP patologico de comprimento: o modelo (raro) emite centenas/milhares de chars de
# lixo p/ uma linha curta (medido: um grito de ~17 chars virou 5872 chars de ruido num batch -> passou o
# fitting so porque AQUELA linha tinha byte_budget; uma sem budget escaparia). Rejeitamos a traducao cuja
# forma TRANSLITERADA passa de _BLOWUP_FACTOR x a fonte (piso _BLOWUP_FLOOR p/ nao punir linha curta
# legitima) -> a linha conta como NAO retornada (re-roda / fica 'missing' -> coverage a pega), nunca aceita.
_BLOWUP_FACTOR = 8


_BLOWUP_FLOOR = 200


def _is_blowup(source, t) -> bool:
    """True se `t` e patologicamente mais longa que `source` (lixo provavel do modelo)."""
    if not isinstance(t, str):
        return False
    return _translit_len(t) > max(_translit_len(source or "") * _BLOWUP_FACTOR, _BLOWUP_FLOOR)


# RÓTULO DE ENGINE: identificadores internos de rig/asset que NAO sao dialogo — body, face,
# hair, mask, Leg_2_B_L, ch120_01, env_bone, lightA02. O LLM os TRADUZIA, estourava o byte_budget e
# disparava o retighten (re-traducao = 58% do custo medido no ledger). Solucao: PASSTHROUGH
# deterministico (t = fonte), fora do lote do LLM.
#
# ALLOWLIST EXPLICITA: labels conhecidos que NUNCA sao dialogo (qualquer um desses => passthrough imediato).
# Adicionar aqui quando aparecer um novo label traduzido indevidamente no ledger.
_ENGINE_LABELS = frozenset({
    "body", "face", "hair", "mask", "env_bone", "bone",
    "light", "lightA", "lightB", "lightC",
})


_ENGINE_LABEL_RX = re.compile(
    r"^(body|face|hair|mask|env_bone|bone|light[A-Za-z0-9]*"
    r"|ch\d+_\d+|Leg_\d+_[A-Z]_[LR]|Spine\d*|Root|Hips"
    r"|[A-Z][a-z]+(?:[A-Z][a-z]+)+\d*"   # CamelCase strict (LeftFoot, RightArm...)
    r"|[a-z]+[A-Z]\w+\d*"                # camelCase (lightA02)
    r")\Z"
)


# Deteccao HEURISTICA de bloco de rotulos (corrida de tokens-unicos com >=1 STRICT_ID):
# detecta casos nao cobertos pela allowlist — nao substitui, complementa.
_TOKISH = re.compile(r"[A-Za-z][\w]*\Z")


_STRICT_ID = re.compile(r"[A-Za-z]\w*_\w+\Z|[A-Za-z]+\d\w*\Z|[A-Z][a-z]+(?:[A-Z][a-z]+)+\Z")


def _is_tokish(s: str) -> bool:
    s = (s or "").strip()
    return bool(s) and len(s) <= 16 and bool(_TOKISH.match(s))


def _label_passthrough(pack) -> dict:
    """Mapa {offset: entry} das linhas que sao rotulo de engine (t = fonte, sem ir ao LLM).
    Prioridade: allowlist explicita (_ENGINE_LABELS / _ENGINE_LABEL_RX) -> heuristica de bloco."""
    lines = pack.get("lines", [])
    out, i, n = {}, 0, len(lines)

    def _passthrough(r):
        return {"speaker": "", "tone_register": "", "intent": "rotulo_engine",
                "risk_level": "low", "risk_notes": "", "t": r.get("source", "") or ""}

    while i < n:
        s = (lines[i].get("source", "") or "").strip()
        # Allowlist explicita: passthrough imediato, sem precisar de bloco vizinho
        if s.lower() in _ENGINE_LABELS or _ENGINE_LABEL_RX.match(s):
            out[lines[i]["offset"]] = _passthrough(lines[i])
            i += 1
            continue
        # Heuristica de bloco: corrida de tokens-unicos com >=1 STRICT_ID
        if not _is_tokish(s):
            i += 1
            continue
        j = i
        while j < n and _is_tokish((lines[j].get("source", "") or "").strip()):
            j += 1
        run = lines[i:j]
        if any(_STRICT_ID.match((r.get("source", "") or "").strip()) for r in run):
            for r in run:
                rs = (r.get("source", "") or "").strip()
                if _STRICT_ID.match(rs) or rs.islower():   # capitalizada (Sim/OK) fica no LLM
                    out[r["offset"]] = _passthrough(r)
        i = j
    return out


def _prefilled(pack, *, enabled=True) -> dict:
    """Linhas que NUNCA vao ao LLM: reuso de TM (se enabled) + rotulo de engine (passthrough sempre).
    Fonte unica -- cada call site que montava os dois a mao podia esquecer um (bug do rotulo sobrescrito)."""
    out = _select_reuse(pack, enabled=enabled)
    out.update(_label_passthrough(pack))
    return out


def _select_reuse(pack, *, enabled):
    """DEDUP por TM: linhas cuja fonte JA foi traduzida em OUTRA cena -> reusa a traducao estabelecida
    em vez de re-gerar (corta tokens de SAIDA, 5x o custo de entrada; e a consistencia ja vem de graca).
    Guards: (1) nunca reusa a PROPRIA cena — a TM e reconstruida apos cada cena, entao re-rodar a poria
    na TM e a dedup reusaria a saida velha, sabotando o escalonamento de fitting (que quer ENCURTAR);
    (2) paridade de quebra: a chave de TM normaliza ignorando `\\n`, entao so reusa se a contagem do token
    na traducao casar a da fonte ATUAL (senao o build_plan reprova por paridade), idem tokens de formatacao. Desligado (vazio) no
    escalonamento (enabled=False) p/ re-traduzir fresco e mais curto. Determinista (testavel sem rede)."""
    if not enabled:
        return {}
    rx = _structural_rx(pack.get("project_constraints", {}))
    scene_id_here = pack.get("scene_id", "")
    by_key: dict[str, dict] = {}
    for e in pack.get("tm_exact", []):
        if context_pack.scene_id_of(str(e.get("from_scene", ""))) == scene_id_here:
            continue                                  # nunca reusar a propria cena
        by_key.setdefault(state_index._key(e.get("source", "")), e)
    reuse = {}
    for r in pack.get("lines", []):
        e = by_key.get(state_index._key(r.get("source", "")))
        if not e:
            continue
        tgt = e.get("target", "")
        if not tgt or not _line_ok(r.get("source", "") or "", tgt, rx):
            continue                                  # paridade de quebra/tokens com a fonte ATUAL
        reuse[r["offset"]] = {"speaker": e.get("speaker", ""), "tone_register": "",
                              "intent": "reuso_tm", "risk_level": "low", "risk_notes": "",
                              "t": _norm_t(tgt)}
    return reuse


def _line_ok(src, t, rx=None):
    """Paridade de `\\n` E (com rx) de tokens de formatacao -- o mesmo par que o _api_translate retenta."""
    tok = context_pack.TOKEN
    return t.count(tok) == src.count(tok) and (rx is None or _struct_ok(rx, src, t))


def saved_pack(root, scene) -> dict | None:
    """RECONFERENCIA (so caminho de sessao): o pack.json ja gravado, se a cena ja tem traducao e nada do que
    alimenta o pack mudou desde entao (falas da cena, project.json, doutrina = carta+glossario+decisoes+tom).
    Remontar o pack de uma cena pronta so para reconferir um conserto custava minutos em cena grande.
    None = nao da para reaproveitar -> quem chama remonta.
    So vale com a traducao COMPLETA: faltando fala, a TM que cresceu no banco depois do pack pode preenche-la,
    entao remonta. Com todas as falas presentes a TM nao e consultada e o pack gravado basta."""
    root = Path(root)
    pk = paths.pack(root, scene)
    if not pk.is_file():
        return None
    try:
        pack = json.loads(pk.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    out = paths.translations(root, scene, pack.get("scene_id", ""))
    try:
        have = json.loads(out.read_text(encoding="utf-8")).get("lines", {})
    except (OSError, ValueError):
        return None
    if any(r["offset"] not in have for r in pack.get("lines", [])):
        return None
    if pack.get("doctrine_hash", "") != context_pack._doctrine_hash(root):
        return None
    made = pk.stat().st_mtime
    deps = [paths.dialogs(root, scene), root / "project.json"]
    if any(d.is_file() and d.stat().st_mtime > made for d in deps):
        return None
    return pack


def _over_offsets(budgets: dict, lines: dict, tolerance: float = 1.0, pc: dict | None = None) -> list:
    """Offsets cuja traducao excede byte_budget*tolerance pela metrica correta do projeto (ver
    _budget_len). Puro/deterministico (testavel sem rede)."""
    over = []
    for off, b in budgets.items():
        if b is None:            # None = sem budget declarado; 0 = orcamento ZERO real (deve ENFORCAR)
            continue
        v = lines.get(off)
        if v and _over_budget((v or {}).get("t", ""), b, pc, tolerance):
            over.append(off)
    return sorted(over)


def over_budget_offsets(root, scene, *, tolerance: float = 1.0, detail: bool = False,
                        reuse_pack: bool = False) -> list:
    """Le o translations_<scene_id>.json atual e devolve os offsets acima do budget (candidatos a
    estouro). `detail=True` devolve [{offset, byte_budget, actual, source, t}, ...] em vez da lista
    nua de offsets (diagnostico persistivel, ver run_scene._persist_fitting_diagnostics)."""
    root = Path(root)
    pack = (saved_pack(root, scene) if reuse_pack else None) or context_pack.build_pack(root, scene)
    out = paths.translations(root, scene, pack['scene_id'])
    if not out.is_file():
        return []
    data = json.loads(out.read_text(encoding="utf-8"))
    lines = data.get("lines", {})
    budgets = {r["offset"]: r.get("byte_budget") for r in pack["lines"]}
    pc = pack.get("project_constraints")
    offsets = _over_offsets(budgets, lines, tolerance, pc=pc)
    if not detail:
        return offsets
    srcmap = {r["offset"]: r.get("source", "") for r in pack["lines"]}
    return [{"offset": o, "byte_budget": budgets[o],
             "actual": _budget_len(lines[o].get("t", ""), pc),
             "source": srcmap.get(o, ""), "t": lines[o].get("t", "")} for o in offsets]


def fix_newlines(root, scene, *, reuse_pack: bool = False) -> int:
    """Conserta o que e mecanico: quebra de linha REAL no `t` vira o token literal (_norm_t) e o token que a fonte
    nao tem sai (_parity_fit) -- o mesmo que o caminho api faz ao gravar. Devolve quantas falas mudou."""
    root = Path(root)
    pack = (saved_pack(root, scene) if reuse_pack else None) or context_pack.build_pack(root, scene)
    out = paths.translations(root, scene, pack["scene_id"])
    if not out.is_file():
        return 0
    data = json.loads(out.read_text(encoding="utf-8"))
    n = 0
    for r in pack["lines"]:
        v = data.get("lines", {}).get(r["offset"])
        if isinstance(v, dict) and isinstance(v.get("t"), str):
            new = _parity_fit(r.get("source"), _norm_t(v["t"]))
            if new != v["t"]:
                v["t"], n = new, n + 1
    if n:
        paths.atomic_write(out, json.dumps(data, ensure_ascii=False, indent=2))
    return n


def precheck(root, scene, *, reuse_pack: bool = False) -> list:
    """Pre-checagem barata ANTES do build_plan (so le): [(offset, problema)] para quebra de linha real no JSON,
    contagem do token `\n` diferente da fonte. Estouro de byte_budget NAO entra: no utawarerumono 7 de 26 cenas
    verified tem fala acima do budget por linha (o conector nao o impoe por fala), entao seria falso positivo; o
    `_fitting_loop` reage ao exit 3 do verify. Nao bloqueia: quem decide e o build_plan/verify."""
    root = Path(root)
    pack = (saved_pack(root, scene) if reuse_pack else None) or context_pack.build_pack(root, scene)
    out = paths.translations(root, scene, pack["scene_id"])
    if not out.is_file():
        return []
    lines = json.loads(out.read_text(encoding="utf-8")).get("lines", {})
    tok, found = context_pack.TOKEN, {}
    for r in pack["lines"]:
        t = (lines.get(r["offset"]) or {}).get("t")
        if not isinstance(t, str):
            continue
        if chr(10) in t or chr(13) in t:
            found[r["offset"]] = "quebra de linha real (use o token literal)"
        elif t.count(tok) != (r.get("source") or "").count(tok) and (r.get("source") or "").count(tok):
            found[r["offset"]] = f"{t.count(tok)} token(s) de quebra, a fonte tem {r['source'].count(tok)}"
    return sorted(found.items())
