#!/usr/bin/env python3
"""
model.py — INTERFACE de modelo do harness (agnosticismo de modelo).

Desacopla o run_scene do "como" a IA e chamada. Dois papeis de IA (so o que exige IA):
  - translate(...)      : traduz a cena a partir do pacote limitado (context_pack).
  - back_translate(...) : verifica linhas de alto risco (pt-BR -> EN -> confere sentido/voz).

Dois backends, mesmo contrato:
  (a) "in-session" (ASSINATURA): NAO chama rede. Garante o scene_prompt.md (auto-contido e limitado)
      e checa se o modelo do chat ja produziu o translations_<sfx>.json. Como o prompt e limitado,
      da p/ responder UMA cena por sessao limpa -> o contexto nunca acumula (mata o estouro), sem
      conta de API. Resumivel: rode de novo apos o arquivo aparecer.
  (b) "api" (ESCALA HEADLESS): Anthropic SDK. Model-mix do cost_model — Sonnet traduz, Opus faz a
      back-translation; doutrina (Carta) cacheada via cache_control (cobrada ~1x). Import preguicoso
      e com erro claro se faltar SDK/chave. (Endurecimento contra o SDK vivo = P1; ver docs/MODEL_INTERFACE.)

GOVERNANCA: sem work-text hardcoded. O conteudo vem do pacote/artefatos. Determinismo do harness vem
do context_pack; a chamada de IA e a unica parte nao-determinista (por isso isolada aqui).
"""
from __future__ import annotations
import json
import os
import sys
import time
import unicodedata
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import state_index   # noqa: E402  (sibling; _key p/ dedup por TM)

# --- model-mix (defaults; cost_model cenario 'mix'): Sonnet traduz, Opus verifica alto risco ---
MODEL_TRANSLATE = "claude-sonnet-4-6"
MODEL_BACK = "claude-opus-4-8"

# Saida pode ser grande (ate ~500 linhas x speaker/tone/intent/risk/t). Streaming evita timeout;
# este teto cobre a maior cena do corpus com folga (Sonnet/Opus 4.x suportam ate 64k de saida).
MAX_OUTPUT_TOKENS = 64000
_MAX_TRIES = 3        # tentativas p/ corrigir saida invalida (cobertura / token de quebra)
_MAX_BACKOFF = 4      # tentativas de rede com backoff exponencial

# Tuning de custo da TRADUCAO (medido: effort:high + thinking estourou ~5x o cost_model — o thinking
# conta como saida a $15/M). Traducao com contexto curado nao precisa de raciocinio profundo:
# default sem thinking + effort baixo. back_translate (alto risco) mantem thinking (raciocinio importa).
EFFORT_TRANSLATE = "low"
THINK_TRANSLATE = False

# Disciplina de orcamento: a traducao TRANSLITERADA (sem acentos — como vai p/ os bytes) nao deve
# estourar MUITO o byte_budget. E SOFT (best-effort): linhas acima de budget*tol recebem um nudge de
# encurtamento nas retries, mas sao aceitas (o conector absorve crescimento; a VERIFY e o juiz real).
# 1.40 = DEFAULT (alinhado ao build_plan; traducoes naturais, menos retries = mais barato). Cenas de
# binario APERTADO (multi-BIN) podem nao caber a 1.40 -> o run_scene ESCALA o aperto (1.40->1.15->1.0)
# e re-traduz so quando a VERIFY falha por fitting (out-of-file/residuo). Ver BUDGET_ESCALATION.
BUDGET_TOLERANCE = 1.40
BUDGET_ESCALATION = (1.15, 1.0)   # tolerancias mais apertadas tentadas, em ordem, na falha de fitting

AWAITING = "awaiting"   # o operador/modelo do chat precisa produzir a saida
READY = "ready"         # a saida ja existe
DONE = "done"           # chamada de IA concluida (backend api)


# ------------------------------- TRANSLATE ------------------------------------

def translate(root, scene, *, backend="api", model=None, budget_tolerance=None):
    root = Path(root)
    pack = context_pack.write_pack(root, scene)            # (re)gera prompt+pack (determinista)
    sfx = pack["sfx"]
    out = root / "artifacts" / scene / f"translations_{sfx}.json"
    if backend == "in-session":
        if out.is_file():
            return {"status": READY, "path": str(out), "sfx": sfx, "n_lines": pack["n_lines"]}
        return {"status": AWAITING, "sfx": sfx, "n_lines": pack["n_lines"],
                "prompt": str(root / "artifacts" / scene / "scene_prompt.md"),
                "expected_output": str(out)}
    if backend == "api":
        m = model or MODEL_TRANSLATE
        data, usage, meta = _api_translate(root, scene, pack, m, budget_tolerance=budget_tolerance)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": DONE, "path": str(out), "sfx": sfx, "n_lines": pack["n_lines"],
                "model": m, "usage": usage, "reused": meta["reused"], "novel": meta["novel"]}
    raise ValueError(f"backend desconhecido: {backend}")


# ----------------------------- BACK-TRANSLATE ---------------------------------

def back_translate(root, scene, high_lines, *, backend="api", model=None):
    """high_lines: lista de {offset, source, target, speaker, risk_notes}."""
    root = Path(root)
    sfx = context_pack.sfx_of(scene)
    out = root / "artifacts" / scene / f"back_translation_{sfx}.json"
    if not high_lines:
        return {"status": DONE, "reviewed": 0, "path": None}
    if backend == "in-session":
        _write_back_prompt(root, scene, sfx, high_lines)
        if out.is_file():
            return {"status": READY, "path": str(out), "reviewed": len(high_lines)}
        return {"status": AWAITING, "reviewed": len(high_lines),
                "prompt": str(root / "artifacts" / scene / f"back_prompt_{sfx}.md"),
                "expected_output": str(out)}
    if backend == "api":
        m = model or MODEL_BACK
        data, usage = _api_back_translate(root, scene, high_lines, m)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": DONE, "path": str(out), "reviewed": len(high_lines),
                "model": m, "usage": usage}
    raise ValueError(f"backend desconhecido: {backend}")


def _write_back_prompt(root, scene, sfx, high_lines):
    L = [f"# Back-translation — cena {scene} ({len(high_lines)} linhas de alto risco)", "",
         "> Para cada linha: traduza o pt-BR de volta p/ EN, compare com o source, e confirme que",
         "> SENTIDO, ambiguidade, voz e timing foram preservados. Divergencia -> revisar a traducao.",
         f"> Saida: `back_translation_{sfx}.json` = {{\"reviewed\": N, \"entries\": [",
         ">   {{offset, source, target, back_en, verdict: pass|revise, note}} ]}}.", ""]
    for h in high_lines:
        L.append(f"## {h['offset']} ({h.get('speaker','')})")
        L.append(f"- source : {h['source']}")
        L.append(f"- target : {h['target']}")
        if h.get("risk_notes"):
            L.append(f"- notas  : {h['risk_notes']}")
        L.append("")
    (root / "artifacts" / scene / f"back_prompt_{sfx}.md").write_text("\n".join(L), encoding="utf-8")


# ------------------------------- API backend ----------------------------------
# Implementacao fiel ao skill claude-api; import preguicoso, sem rede em import/teste.
# Endurecido p/ producao: streaming (.get_final_message) p/ saidas longas, output_config json_schema,
# backoff em erro transitorio, e guard do token de quebra + cobertura com retry (ver _api_translate).

# Structured output ESTRITO exige additionalProperties:false em todo objeto -> nao da p/ usar mapa
# {offset: {...}} (chaves dinamicas). Logo: ARRAY de entradas com 'offset' por item; convertido p/ o
# mapa {offset: {...}} (formato canonico do translations_<sfx>.json) apos parsear (ver _api_translate).
_LINE_PROPS = {
    "offset": {"type": "string"}, "speaker": {"type": "string"},
    "tone_register": {"type": "string"}, "intent": {"type": "string"},
    "risk_level": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
    "risk_notes": {"type": "string"}, "t": {"type": "string"},
}
_TRANSLATION_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["lines"],
    "properties": {"lines": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "properties": _LINE_PROPS,
        "required": ["offset", "speaker", "tone_register", "intent",
                     "risk_level", "risk_notes", "t"],
    }}},
}


def _load_dotenv():
    """Carrega um `.env` (KEY=VALUE) p/ os.environ SEM dependencia externa. Nao sobrescreve
    variavel ja setada no ambiente (env real vence). Procura na raiz do framework e no CWD."""
    roots = [_HERE.parent.parent, Path.cwd()]   # framework/ (raiz do repo) e diretorio de execucao
    for base in roots:
        f = base / ".env"
        if not f.is_file():
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, _, v = s.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _client():
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError("backend 'api' requer o pacote 'anthropic' (pip install anthropic). "
                           "Use backend 'in-session' p/ o caminho assinatura.") from e
    _load_dotenv()
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key or "cole-sua-chave" in key:
        raise RuntimeError("backend 'api' requer ANTHROPIC_API_KEY: edite o `.env` na raiz do "
                           "framework e troque o placeholder pela sua chave real (veja .env.example).")
    return anthropic.Anthropic()


def _carta_text() -> str:
    return context_pack._read(context_pack.CARTA_PATH)


# Regra do token de quebra reforcada na borda da API: em JSON, o literal barra+n e escrito `\\n`.
# O modelo as vezes colapsa isso numa quebra de linha REAL (o bug recorrente) — instruimos e validamos.
_NL_RULE = (
    "\n\n## FORMATO DE SAIDA (sobrepoe a secao 8)\n"
    "Responda um objeto JSON com a chave \"lines\" = ARRAY de entradas; cada entrada tem os campos "
    "`offset, speaker, tone_register, intent, risk_level, risk_notes, t` (preencha todos; `risk_notes` "
    "pode ser \"\" quando risco baixo). Uma entrada por offset da secao 7 — cubra TODOS, sem excecao.\n"
    "## REGRA CRITICA (token de quebra)\n"
    "Onde o source contem o token literal de quebra de linha, o campo \"t\" deve conte-lo como os DOIS "
    "caracteres literais barra-invertida + n (no JSON: escreva `\\\\n`), NUNCA uma quebra de linha real."
)


def _text_of(msg) -> str:
    return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")


def _usage_of(msg) -> dict:
    u = getattr(msg, "usage", None)
    if not u:
        return {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}
    return {"in": getattr(u, "input_tokens", 0) or 0,
            "out": getattr(u, "output_tokens", 0) or 0,
            "cache_read": getattr(u, "cache_read_input_tokens", 0) or 0,
            "cache_write": getattr(u, "cache_creation_input_tokens", 0) or 0}


def _add_usage(acc: dict, u: dict) -> dict:
    for k in ("in", "out", "cache_read", "cache_write"):
        acc[k] = acc.get(k, 0) + u.get(k, 0)
    return acc


# precos US$/token (skill claude-api 2026-05-26); cache_read=0.1x in, cache_write=1.25x in.
# Fonte unica de verdade de custo (run_scene/cost_report importam daqui — sem drift de preco).
_PRICE = {"claude-opus-4-8":   {"in": 5.00e-6, "out": 25.00e-6},
          "claude-sonnet-4-6": {"in": 3.00e-6, "out": 15.00e-6},
          "claude-haiku-4-5":  {"in": 1.00e-6, "out":  5.00e-6}}


def cost_of(model: str, u: dict) -> float:
    """Custo US$ de uma chamada a partir do usage (in/out/cache_read/cache_write)."""
    p = _PRICE.get(model)
    if not p or not u:
        return 0.0
    return (u.get("in", 0) * p["in"] + u.get("cache_read", 0) * p["in"] * 0.10
            + u.get("cache_write", 0) * p["in"] * 1.25 + u.get("out", 0) * p["out"])


def log_api_call(root, scene, kind, model, usage):
    """Anexa 1 linha a artifacts/api_ledger.jsonl por chamada de API CONCLUIDA (cada tentativa de
    cobertura e cada escalonamento de fitting). E a VERDADE de gasto: registra TODA chamada cobrada,
    INCLUSIVE as de cenas que depois falham (cobertura/verify) ou retries — exatamente o que o
    metrics.jsonl (resumo so-de-sucesso) perde. Sem isso o saldo surpreende (estimado << real).
    Best-effort (nunca derruba a traducao por falha de log). Ver cost_report.py p/ o agregado."""
    if not usage:
        return None
    rec = {"t": round(time.time(), 3), "scene": scene, "kind": kind, "model": model,
           "usage": dict(usage), "cost_usd": round(cost_of(model, usage), 5)}
    try:
        p = Path(root) / "artifacts" / "api_ledger.jsonl"
        with p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass
    return rec


def _stream_final(client, **kwargs):
    """Streaming + backoff. Streaming evita timeout em saidas longas; backoff cobre 429/500/timeout E
    quedas de conexao no meio do stream (httpx RemoteProtocolError/'incomplete chunked read'), comuns
    em cenas grandes (output longo). NAO retenta erros de request (400 BadRequest) — esses nao 'curam'."""
    import anthropic
    import httpx
    transient = (anthropic.RateLimitError, anthropic.InternalServerError,
                 anthropic.APITimeoutError, anthropic.APIConnectionError,
                 httpx.RemoteProtocolError, httpx.ReadError, httpx.ReadTimeout,
                 httpx.ConnectError, httpx.ConnectTimeout)
    delay = 2.0
    for i in range(_MAX_BACKOFF):
        try:
            with client.messages.stream(**kwargs) as s:
                return s.get_final_message()
        except transient:
            if i == _MAX_BACKOFF - 1:
                raise
            time.sleep(delay)
            delay *= 2


def _check_translation(data, offsets):
    """Retorna (offsets_com_quebra_real, offsets_faltando). Guard do bug do token \\n + cobertura."""
    lines = data.get("lines", {}) if isinstance(data, dict) else {}
    bad_nl = [off for off, v in lines.items() if "\n" in ((v or {}).get("t", "") or "")]
    missing = [o for o in offsets if o not in lines]
    return bad_nl, missing


def _translit_len(t) -> int:
    """Comprimento em bytes da forma TRANSLITERADA (NFKD + drop combining) — o que o reinsert grava."""
    s = unicodedata.normalize("NFKD", t or "")
    return len("".join(c for c in s if not unicodedata.combining(c)))


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


def _select_reuse(pack, *, enabled):
    """DEDUP por TM: linhas cuja fonte JA foi traduzida em OUTRA cena -> reusa a traducao estabelecida
    em vez de re-gerar (corta tokens de SAIDA, 5x o custo de entrada; e a consistencia ja vem de graca).
    Guards: (1) nunca reusa a PROPRIA cena — a TM e reconstruida apos cada cena, entao re-rodar a poria
    na TM e a dedup reusaria a saida velha, sabotando o escalonamento de fitting (que quer ENCURTAR);
    (2) paridade de quebra: a chave de TM normaliza ignorando `\\n`, entao so reusa se a contagem do token
    na traducao casar a da fonte ATUAL (senao o build_plan reprova por paridade). Desligado (vazio) no
    escalonamento (enabled=False) p/ re-traduzir fresco e mais curto. Determinista (testavel sem rede)."""
    if not enabled:
        return {}
    tok = context_pack.TOKEN
    sfx_here = pack.get("sfx", "")
    by_key = {}
    for e in pack.get("tm_exact", []):
        if context_pack.sfx_of(str(e.get("from_scene", ""))) == sfx_here:
            continue                                  # nunca reusar a propria cena
        by_key.setdefault(state_index._key(e.get("source", "")), e)
    reuse = {}
    for r in pack.get("lines", []):
        e = by_key.get(state_index._key(r.get("source", "")))
        if not e:
            continue
        tgt = e.get("target", "")
        if not tgt or tgt.count(tok) != (r.get("source", "") or "").count(tok):
            continue                                  # paridade de quebra com a fonte ATUAL
        reuse[r["offset"]] = {"speaker": e.get("speaker", ""), "tone_register": "",
                              "intent": "reuso_tm", "risk_level": "low", "risk_notes": "",
                              "t": _norm_t(tgt)}
    return reuse


def _to_map(data):
    """Converte a saida estruturada {lines:[{offset,...}]} no formato canonico {lines:{offset:{...}}}.
    Tolera ja vir em mapa (idempotente). Remove 'offset' do corpo da entrada e normaliza o `t`."""
    lines = (data or {}).get("lines")
    if isinstance(lines, dict):
        for v in lines.values():
            if isinstance(v, dict) and "t" in v:
                v["t"] = _norm_t(v["t"])
        return data
    out = {}
    for e in (lines or []):
        off = e.get("offset")
        if not off:
            continue
        body = {k: v for k, v in e.items() if k != "offset"}
        if "t" in body:
            body["t"] = _norm_t(body["t"])
        out[off] = body
    return {"lines": out}


def _api_translate(root, scene, pack, model, *, effort=EFFORT_TRANSLATE, think=THINK_TRANSLATE,
                   budget_tolerance=None):
    tol = budget_tolerance or BUDGET_TOLERANCE
    tok = context_pack.TOKEN
    # DEDUP por TM (so no 1o passe; desligado no escalonamento de fitting p/ re-traduzir mais curto):
    # linhas com fonte ja traduzida em OUTRA cena nao vao ao modelo (corta tokens de saida).
    reuse = _select_reuse(pack, enabled=(budget_tolerance is None))
    novel = [r for r in pack["lines"] if r["offset"] not in reuse]
    meta = {"reused": len(reuse), "novel": len(novel), "n_lines": len(pack["lines"])}
    if not novel:                                     # cena 100% reaproveitada -> zero chamada de API
        return {"lines": dict(reuse)}, {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}, meta

    client = _client()
    # system = doutrina estavel (cacheada ~1x via cache_control); user = pacote da cena (so as novas)
    system = [{"type": "text", "text": _carta_text(), "cache_control": {"type": "ephemeral"}}]
    red = dict(pack); red["lines"] = novel; red["n_lines"] = len(novel)   # render so as linhas novas
    base_user = context_pack.render_prompt(red, carta="") + _NL_RULE  # Carta ja no system
    offsets = [r["offset"] for r in novel]
    offset_set = set(offsets)
    budgets = {r["offset"]: r.get("byte_budget") for r in novel}
    srcmap = {r["offset"]: r.get("source", "") for r in novel}
    note, last, usage = "", None, {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}
    merged = {}        # ACUMULA linhas entre tentativas: cada retry preenche lacunas -> cobertura converge
    # thinking custa como saida ($15/M). Traducao com contexto curado raramente exige raciocinio
    # profundo -> default sem thinking + effort baixo (medido: corta ~5x o custo; ver OBSERVABILITY).
    thinking = {"type": "adaptive"} if think else {"type": "disabled"}

    def _over(off, v):
        b = budgets.get(off)
        return b and _translit_len((v or {}).get("t", "")) > b * tol

    for attempt in range(_MAX_TRIES):
        msg = _stream_final(
            client, model=model, max_tokens=MAX_OUTPUT_TOKENS,
            system=system,
            messages=[{"role": "user", "content": base_user + note}],
            thinking=thinking,
            output_config={"effort": effort,
                           "format": {"type": "json_schema", "schema": _TRANSLATION_SCHEMA}},
        )
        u_attempt = _usage_of(msg)
        _add_usage(usage, u_attempt)
        log_api_call(root, scene, "translate", model, u_attempt)   # registra ANTES de qualquer parse/gate
        data = _to_map(json.loads(_text_of(msg)))   # array -> mapa {offset:{...}}; CR/LF real -> token
        for off, v in data.get("lines", {}).items():
            if off not in offset_set or not isinstance(v, dict):
                continue
            v["t"] = _parity_fit(srcmap.get(off, ""), v.get("t", ""))   # quebra espuria -> espaco
            good_parity = (v["t"].count(tok) == srcmap.get(off, "").count(tok))
            if off not in merged:
                merged[off] = v                      # preenche lacuna
            else:
                old = merged[off]
                old_parity = (old.get("t", "").count(tok) == srcmap.get(off, "").count(tok))
                if good_parity and not old_parity:
                    merged[off] = v                  # prioriza paridade correta
                elif good_parity == old_parity and _over(off, old) and \
                        _translit_len(v.get("t", "")) < _translit_len(old.get("t", "")):
                    merged[off] = v                  # mesma paridade: prefere a mais curta (budget)
        missing = [o for o in offsets if o not in merged]
        bad_par = [o for o in merged if merged[o].get("t", "").count(tok) != srcmap.get(o, "").count(tok)]
        over = [(o, budgets[o], _translit_len(merged[o].get("t", "")))
                for o in merged if _over(o, merged[o])]
        last = {"missing": missing, "bad_parity": bad_par, "over_budget": over}
        # HARD (bloqueia): cobertura + paridade de quebra (build_plan reprova). SOFT (best-effort):
        # byte_budget — o conector absorve via head-reloc; a VERIFY (round-trip) e o juiz de residuo.
        if not missing and not bad_par and (not over or attempt == _MAX_TRIES - 1):
            merged.update(reuse)                      # reanexa as linhas reaproveitadas da TM
            return {"lines": merged}, usage, meta
        note = "\n\n## CORRECAO NECESSARIA (gere a cena COMPLETA de novo; vamos MESCLAR com o anterior)\n"
        if missing:
            note += f"- Faltam estes offsets — INCLUA todos: {missing[:40]}\n"
        if bad_par:
            note += (f"- Estes offsets tem nº de quebras `\\n` DIFERENTE da fonte — case EXATO (mesma "
                     f"quantidade e posicao do token): {bad_par[:30]}\n")
        if over:
            note += ("- Estes offsets passam do byte_budget (TRANSLITERADO, sem acentos); ENCURTE "
                     "preservando o sentido (corte redundancia; ex.: 'adicionado ao'->'no'):\n")
            for off, b, cur in over[:25]:
                note += f"  - {off}: budget {b}, atual {cur}\n"
    raise RuntimeError(f"_api_translate: cobertura/paridade incompletas apos {_MAX_TRIES} tentativas: "
                       f"faltam={last['missing']} paridade={last['bad_parity']}")


# Schema ESTRITO p/ a back-translation (garante JSON parseavel — sem ele o Opus as vezes devolvia
# texto vazio/markdown e o parse quebrava DEPOIS de ja cobrar a chamada: vazamento de Opus).
_BACK_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["entries"],
    "properties": {"entries": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "required": ["offset", "back_en", "verdict", "note"],
        "properties": {
            "offset": {"type": "string"}, "back_en": {"type": "string"},
            "verdict": {"type": "string", "enum": ["pass", "revise"]},
            "note": {"type": "string"},
        }}}},
}


def _api_back_translate(root, scene, high_lines, model):
    client = _client()
    payload = [{"offset": h["offset"], "source": h["source"], "target": h["target"],
                "speaker": h.get("speaker", "")} for h in high_lines]
    instr = ("Para cada item, traduza o 'target' (pt-BR) de volta p/ EN ('back_en'), compare com "
             "'source', e de um 'verdict' (pass|revise) + 'note' curta. verdict=revise se "
             "sentido/ambiguidade/voz divergirem. Inclua o 'offset' de cada item.\n\n")
    msg = _stream_final(
        client, model=model, max_tokens=MAX_OUTPUT_TOKENS,
        messages=[{"role": "user", "content": instr + json.dumps(payload, ensure_ascii=False)}],
        thinking={"type": "adaptive"},
        output_config={"effort": "high",
                       "format": {"type": "json_schema", "schema": _BACK_SCHEMA}},
    )
    usage = _usage_of(msg)
    log_api_call(root, scene, "back", model, usage)   # registra antes do parse (Opus cobra mesmo se quebrar)
    data = json.loads(_text_of(msg))
    data["reviewed"] = len(data.get("entries", []))
    return data, usage


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Interface de modelo do harness (translate).")
    ap.add_argument("project")
    ap.add_argument("scene")
    ap.add_argument("--backend", default="api", choices=["in-session", "api"])
    ap.add_argument("--model", default=None)
    a = ap.parse_args()
    r = translate(a.project, a.scene, backend=a.backend, model=a.model)
    print(json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
