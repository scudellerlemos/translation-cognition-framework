#!/usr/bin/env python3
"""
model.py — INTERFACE de modelo do harness (agnosticismo de modelo).

Desacopla o run_scene do "como" a IA e chamada. Dois papeis de IA (so o que exige IA):
  - translate(...)      : traduz a cena a partir do pacote limitado (context_pack).
  - back_translate(...) : verifica linhas de alto risco (pt-BR -> EN -> confere sentido/voz).

Dois backends, mesmo contrato:
  (a) "in-session" (ASSINATURA): NAO chama rede. Garante o scene_prompt.md (auto-contido e limitado)
      e checa se o modelo do chat ja produziu o translations_<scene_id>.json. Como o prompt e limitado,
      da p/ responder UMA cena por sessao limpa -> o contexto nunca acumula (mata o estouro), sem
      conta de API. Resumivel: rode de novo apos o arquivo aparecer.
  (b) "api" (ESCALA HEADLESS): Anthropic SDK. Model-mix do cost_model — Sonnet traduz, Opus faz a
      back-translation; doutrina (Carta) cacheada via cache_control (cobrada ~1x). Import preguicoso
      e com erro claro se faltar SDK/chave. (Endurecimento contra o SDK vivo = P1; ver docs/MODEL_INTERFACE.)

GOVERNANCA: sem work-text hardcoded. O conteudo vem do pacote/artefatos. Determinismo do harness vem
do context_pack; a chamada de IA e a unica parte nao-determinista (por isso isolada aqui).
"""
from __future__ import annotations
import hashlib
import json
import os
import sys
import time
import unicodedata
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import artifact_io   # noqa: E402  (camada de leitura compartilhada de artefatos)
import context_pack  # noqa: E402
import paths          # noqa: E402  (H2: fonte unica de paths)
import state_index   # noqa: E402  (sibling; _key p/ dedup por TM)

# --- model-mix (defaults; cost_model cenario 'mix'): Sonnet traduz, Opus verifica alto risco ---
MODEL_TRANSLATE = "claude-sonnet-4-6"
MODEL_BACK = "claude-opus-4-8"
# TIERING por complexidade (so no caminho BATCH): linhas SEM token de quebra (single-line, maioria) vao
# p/ o Haiku (-67%/linha; benchmark: voz no nivel do Sonnet, inclusive registro arcaico); linhas COM `\n`
# (multi-linha) ficam no Sonnet (Haiku derrapa na disciplina de \n em escala — paridade so falha onde HA
# \n, entao o split DRIBLA a fraqueza). O caminho interativo (fallback/escalonamento) fica Sonnet (casos
# dificeis = confiabilidade). MODEL_TRANSLATE_CHEAP=None desliga o tiering (tudo Sonnet no batch).
MODEL_TRANSLATE_CHEAP = "claude-haiku-4-5"
# Amostragem de QUALIDADE do tier barato: a back-translation so cobre high/critical, deixando as
# low/medium (boa parte single-line -> Haiku) SEM crivo de qualidade (round-trip so prova bytes). Uma
# fracao DETERMINISTICA das low/medium entra na back-batch -> piso de qualidade medido p/ o Haiku.
BACK_SAMPLE_RATE = 0.05

# Saida pode ser grande (ate ~500 linhas x speaker/tone/intent/risk/t). Streaming evita timeout;
# este teto cobre a maior cena do corpus com folga (Sonnet/Opus 4.x suportam ate 64k de saida).
MAX_OUTPUT_TOKENS = 64000
# CHUNKING do batch: o endpoint de batch TRUNCA a saida estruturada longa (~100 linhas/resposta,
# DETERMINISTICO — medido no 15_06: 120/221 linhas sempre faltando, identico nas 3 rodadas; re-mandar
# nao adianta, volta o mesmo prefixo). Quebrar a cena em pedacos pequenos faz cada request voltar
# COMPLETO; a cobertura acumula entre os chunks. (O interativo/streaming escapa pq trunca em pontos
# variaveis a cada retry -> a uniao das 3 cobre; o batch trunca igual -> a uniao nao cresce.)
_BATCH_CHUNK = 60     # linhas por requisicao de batch (folga sob o teto ~100 medido)
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


def _no_effort_model(model: str) -> bool:
    """Modelos que NAO aceitam output_config.effort nem adaptive thinking (400): Haiku 4.5 e Sonnet 4.5.
    Opus 4.x e Sonnet 4.6 aceitam. Usado p/ montar params validos por modelo (tiering de custo)."""
    return model.startswith("claude-haiku") or model == "claude-sonnet-4-5"


# ------------------------------- TRANSLATE ------------------------------------

def translate(root, scene, *, backend="api", model=None, budget_tolerance=None):
    root = Path(root)
    pack = context_pack.write_pack(root, scene)            # (re)gera prompt+pack (determinista)
    scene_id = pack["scene_id"]
    out = paths.translations(root, scene, scene_id)
    if backend == "in-session":
        if out.is_file():
            return {"status": READY, "path": str(out), "scene_id": scene_id, "n_lines": pack["n_lines"]}
        return {"status": AWAITING, "scene_id": scene_id, "n_lines": pack["n_lines"],
                "prompt": str(paths.scene_prompt(root, scene)),
                "expected_output": str(out)}
    if backend == "api":
        m = model or MODEL_TRANSLATE
        data, usage, meta = _api_translate(root, scene, pack, m, budget_tolerance=budget_tolerance)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": DONE, "path": str(out), "scene_id": scene_id, "n_lines": pack["n_lines"],
                "model": m, "usage": usage, "reused": meta["reused"], "novel": meta["novel"]}
    raise ValueError(f"backend desconhecido: {backend}")


# ----------------------------- BACK-TRANSLATE ---------------------------------

def back_translate(root, scene, high_lines, *, backend="api", model=None):
    """high_lines: lista de {offset, source, target, speaker, risk_notes}."""
    root = Path(root)
    scene_id = context_pack.scene_id_of(scene)
    out = paths.back_translation(root, scene, scene_id)
    if not high_lines:
        return {"status": DONE, "reviewed": 0, "path": None}
    if backend == "in-session":
        _write_back_prompt(root, scene, scene_id, high_lines)
        if out.is_file():
            return {"status": READY, "path": str(out), "reviewed": len(high_lines)}
        return {"status": AWAITING, "reviewed": len(high_lines),
                "prompt": str(paths.back_prompt(root, scene, scene_id)),
                "expected_output": str(out)}
    if backend == "api":
        m = model or MODEL_BACK
        data, usage = _api_back_translate(root, scene, high_lines, m)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": DONE, "path": str(out), "reviewed": len(high_lines),
                "model": m, "usage": usage}
    raise ValueError(f"backend desconhecido: {backend}")


def _write_back_prompt(root, scene, scene_id, high_lines):
    L = [f"# Back-translation — cena {scene} ({len(high_lines)} linhas de alto risco)", "",
         "> Para cada linha: traduza o pt-BR de volta p/ EN, compare com o source, e confirme que",
         "> SENTIDO, ambiguidade, voz e timing foram preservados. Divergencia -> revisar a traducao.",
         f"> Saida: `back_translation_{scene_id}.json` = {{\"reviewed\": N, \"entries\": [",
         ">   {{offset, source, target, back_en, verdict: pass|revise, note}} ]}}.", ""]
    for h in high_lines:
        L.append(f"## {h['offset']} ({h.get('speaker','')})")
        L.append(f"- source : {h['source']}")
        L.append(f"- target : {h['target']}")
        if h.get("risk_notes"):
            L.append(f"- notas  : {h['risk_notes']}")
        L.append("")
    (paths.back_prompt(root, scene, scene_id)).write_text("\n".join(L), encoding="utf-8")


# ------------------------------- API backend ----------------------------------
# Implementacao fiel ao skill claude-api; import preguicoso, sem rede em import/teste.
# Endurecido p/ producao: streaming (.get_final_message) p/ saidas longas, output_config json_schema,
# backoff em erro transitorio, e guard do token de quebra + cobertura com retry (ver _api_translate).

# Structured output ESTRITO exige additionalProperties:false em todo objeto -> nao da p/ usar mapa
# {offset: {...}} (chaves dinamicas). Logo: ARRAY de entradas com 'offset' por item; convertido p/ o
# mapa {offset: {...}} (formato canonico do translations_<scene_id>.json) apos parsear (ver _api_translate).
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
    # timeout generoso (fetch de resultados de batch grande) + retries do PROPRIO SDK (1a linha de
    # defesa em 429/500/timeout/conexao); o _with_backoff por cima cobre o que escapar (2a linha).
    return anthropic.Anthropic(timeout=900.0, max_retries=5)


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


def cost_of(model: str, u: dict, *, batch: bool = False) -> float:
    """Custo US$ de uma chamada a partir do usage (in/out/cache_read/cache_write). A Batch API tem
    desconto de 50% sobre TODO o uso (batch=True -> 0.5x)."""
    p = _PRICE.get(model)
    if not p or not u:
        return 0.0
    base = (u.get("in", 0) * p["in"] + u.get("cache_read", 0) * p["in"] * 0.10
            + u.get("cache_write", 0) * p["in"] * 1.25 + u.get("out", 0) * p["out"])
    return base * (0.5 if batch else 1.0)


def log_api_call(root, scene, kind, model, usage, *, batch=False):
    """Anexa 1 linha a artifacts/api_ledger.jsonl por chamada de API CONCLUIDA (cada tentativa de
    cobertura e cada escalonamento de fitting). E a VERDADE de gasto: registra TODA chamada cobrada,
    INCLUSIVE as de cenas que depois falham (cobertura/verify) ou retries — exatamente o que o
    metrics.jsonl (resumo so-de-sucesso) perde. Sem isso o saldo surpreende (estimado << real).
    Best-effort (nunca derruba a traducao por falha de log). Ver cost_report.py p/ o agregado."""
    if not usage:
        return None
    rec = {"t": round(time.time(), 3), "scene": scene, "kind": kind, "model": model,
           "batch": bool(batch), "usage": dict(usage),
           "cost_usd": round(cost_of(model, usage, batch=batch), 5)}
    try:
        p = paths.ledger(root)
        with p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass
    return rec


def _transient_errors():
    """Erros de rede TRANSITORIOS (curam com retry): 429/500/timeout + quedas de conexao httpx. NAO
    inclui 400 BadRequest (esse nao 'cura'). Lazy import (anthropic/httpx so quando o backend api roda)."""
    import anthropic
    import httpx
    return (anthropic.RateLimitError, anthropic.InternalServerError,
            anthropic.APITimeoutError, anthropic.APIConnectionError,
            httpx.RemoteProtocolError, httpx.ReadError, httpx.ReadTimeout,
            httpx.ConnectError, httpx.ConnectTimeout)


def _with_backoff(fn):
    """Executa fn() com backoff exponencial em erro transitorio de rede (mesma classe do _stream_final).
    Para chamadas de BATCH (create/retrieve/results) que nao usam streaming — sem isso, um timeout de
    rede num unico GET/POST derrubava todo o batch (ex.: back-batch do cap.18 morreu por timeout)."""
    transient = _transient_errors()
    delay = 2.0
    for i in range(_MAX_BACKOFF):
        try:
            return fn()
        except transient:
            if i == _MAX_BACKOFF - 1:
                raise
            time.sleep(delay)
            delay *= 2


def _stream_final(client, **kwargs):
    """Streaming + backoff. Streaming evita timeout em saidas longas; backoff cobre 429/500/timeout E
    quedas de conexao no meio do stream (httpx RemoteProtocolError/'incomplete chunked read'), comuns
    em cenas grandes (output longo). NAO retenta erros de request (400 BadRequest) — esses nao 'curam'."""
    def _do():
        with client.messages.stream(**kwargs) as s:
            return s.get_final_message()
    return _with_backoff(_do)


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
    scene_id_here = pack.get("scene_id", "")
    by_key = {}
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
                   budget_tolerance=None, quality_note=""):
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
    base_user += quality_note   # feedback de qualidade da back-translation (quality_fix); "" no fluxo normal
    offsets = [r["offset"] for r in novel]
    offset_set = set(offsets)
    budgets = {r["offset"]: r.get("byte_budget") for r in novel}
    srcmap = {r["offset"]: r.get("source", "") for r in novel}
    note, last, usage = "", None, {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}
    merged = {}        # ACUMULA linhas entre tentativas: cada retry preenche lacunas -> cobertura converge
    # thinking custa como saida ($15/M). Traducao com contexto curado raramente exige raciocinio
    # profundo -> default sem thinking + effort baixo (medido: corta ~5x o custo; ver OBSERVABILITY).
    # Haiku 4.5 / Sonnet 4.5 NAO aceitam output_config.effort nem adaptive thinking (400) -> omitir.
    no_effort = _no_effort_model(model)
    thinking = {"type": "adaptive"} if (think and not no_effort) else {"type": "disabled"}
    out_cfg = {"format": {"type": "json_schema", "schema": _TRANSLATION_SCHEMA}}
    if not no_effort:
        out_cfg["effort"] = effort

    def _over(off, v):
        b = budgets.get(off)
        return b and _translit_len((v or {}).get("t", "")) > b * tol

    for attempt in range(_MAX_TRIES):
        msg = _stream_final(
            client, model=model, max_tokens=MAX_OUTPUT_TOKENS,
            system=system,
            messages=[{"role": "user", "content": base_user + note}],
            thinking=thinking,
            output_config=out_cfg,
        )
        u_attempt = _usage_of(msg)
        _add_usage(usage, u_attempt)
        log_api_call(root, scene, "translate", model, u_attempt)   # registra ANTES de qualquer parse/gate
        data = _to_map(json.loads(_text_of(msg)))   # array -> mapa {offset:{...}}; CR/LF real -> token
        for off, v in data.get("lines", {}).items():
            if off not in offset_set or not isinstance(v, dict):
                continue
            v["t"] = _parity_fit(srcmap.get(off, ""), v.get("t", ""))   # quebra espuria -> espaco
            if _is_blowup(srcmap.get(off, ""), v["t"]):
                continue                                 # lixo patologico -> descarta (vira 'missing' -> retry)
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


# --------------------------- escalonamento CIRURGICO --------------------------
# Quando a verify falha por fitting, NAO re-traduzir a cena inteira: so as linhas que ESTOURAM o budget.
# Numa cena de 500 linhas com 2 estouros, re-traduz 2 (nao 500) -> corte de custo grande no caminho caro
# (medido na run viva do cap.13: o re-translate full custou ~$3,4 em 2 cenas).

def _over_offsets(budgets: dict, lines: dict, tolerance: float = 1.0) -> list:
    """Offsets cuja traducao TRANSLITERADA (sem acentos — o que vai p/ os bytes) excede
    byte_budget*tolerance. Puro/deterministico (testavel sem rede)."""
    over = []
    for off, b in budgets.items():
        if not b:
            continue
        v = lines.get(off)
        if v and _translit_len((v or {}).get("t", "")) > b * tolerance:
            over.append(off)
    return sorted(over)


def over_budget_offsets(root, scene, *, tolerance: float = 1.0) -> list:
    """Le o translations_<scene_id>.json atual e devolve os offsets acima do budget (candidatos a estouro)."""
    root = Path(root)
    pack = context_pack.build_pack(root, scene)
    out = paths.translations(root, scene, pack['scene_id'])
    if not out.is_file():
        return []
    data = json.loads(out.read_text(encoding="utf-8"))
    budgets = {r["offset"]: r.get("byte_budget") for r in pack["lines"]}
    return _over_offsets(budgets, data.get("lines", {}), tolerance)


def invalidate_back_translation(root, scene, offsets) -> int:
    """Marca como STALE as entries de back_translation dos `offsets` re-traduzidos: o verdict julgou o
    TEXTO ANTIGO, entao nao vale mais como crivo de qualidade. NAO apaga (preserva historico + permite
    re-julgar). O quality_gate trata entry stale como SEM cobertura. Retorna nº de entries marcadas."""
    root = Path(root)
    scene_id = context_pack.scene_id_of(scene)
    bt = paths.back_translation(root, scene, scene_id)
    if not bt.is_file():
        return 0
    try:
        data = json.loads(bt.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return 0
    offset_set = set(offsets)
    n = 0
    for e in data.get("entries", []):
        if e.get("offset") in offset_set and not e.get("stale"):
            e["stale"] = True
            n += 1
    if n:
        bt.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return n


def retranslate_offsets(root, scene, offsets, *, model=None, budget_tolerance, quality_note=""):
    """Re-traduz APENAS `offsets` (apertado por budget_tolerance) e MESCLA no translations_<scene_id>.json,
    preservando todas as outras linhas. Caminho cirurgico do escalonamento de fitting (e do quality_fix).
    Reusa _api_translate sobre um pack reduzido (dedup ja vem OFF com budget_tolerance != None -> traduz
    fresco e mais curto). `quality_note` opcional anexa feedback de revisao da back-translation ao prompt."""
    root = Path(root)
    pack = context_pack.build_pack(root, scene)
    scene_id = pack["scene_id"]
    out = paths.translations(root, scene, scene_id)
    full = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else {"lines": {}}
    offset_set = set(offsets)
    sub = dict(pack)
    sub["lines"] = [r for r in pack["lines"] if r["offset"] in offset_set]
    sub["n_lines"] = len(sub["lines"])
    if not sub["lines"]:
        return {"status": DONE, "model": model or MODEL_TRANSLATE, "usage": None,
                "n_lines": 0, "reused": 0, "novel": 0}
    m = model or MODEL_TRANSLATE
    data, usage, meta = _api_translate(root, scene, sub, m, budget_tolerance=budget_tolerance,
                                       quality_note=quality_note)
    full.setdefault("lines", {}).update(data.get("lines", {}))   # merge: so os offsets re-traduzidos
    out.write_text(json.dumps(full, ensure_ascii=False, indent=2), encoding="utf-8")
    invalidate_back_translation(root, scene, offset_set)         # o verdict antigo nao vale mais
    return {"status": DONE, "model": m, "usage": usage, "n_lines": sub["n_lines"],
            "reused": meta["reused"], "novel": meta["novel"]}


# ------------------------------- BATCH backend --------------------------------
# Batch API: 50% de desconto, assincrono (1 requisicao por cena num unico batch). Usa o MESMO system
# cacheado (Carta) -> cache compartilhado entre todas as cenas do batch, alem do desconto. Pre-passe de
# baixo custo: cenas que passam cobertura/paridade na 1a (sem retry) seguem; as que falham caem p/ o
# caminho interativo (streaming, com retry/escalonamento). Quem faz fitting (verify) continua sendo cada
# cena no run_scene. Determinismo da montagem do request isolado em _translate_params (testavel sem rede).

def _coverage_note(missing, bad_par) -> str:
    """Nota CORRETIVA p/ a re-rodada: quais offsets faltam (incluir TODOS) e quais tem paridade de `\\n`
    errada (casar EXATO). Vazia se nada a corrigir. Mesma redacao da retry interativa (_api_translate) —
    e o que faz a cena de narracao CONVERGIR no batch em vez de cair pro interativo full-price."""
    if not missing and not bad_par:
        return ""
    note = "\n\n## CORRECAO NECESSARIA (gere a cena COMPLETA de novo; vamos MESCLAR com o anterior)\n"
    if missing:
        note += f"- Faltam estes offsets — INCLUA todos: {sorted(missing)[:40]}\n"
    if bad_par:
        note += ("- Estes offsets tem nº de quebras `\\n` DIFERENTE da fonte — case EXATO (mesma "
                 f"quantidade e posicao do token): {sorted(bad_par)[:30]}\n")
    return note


def _translate_params(pack, model, note=""):
    """Params de UMA requisicao de traducao (compartilhado por batch). Aplica dedup; retorna
    (params|None, reuse, novel). params=None quando a cena e 100% reaproveitada da TM (sem chamada).
    `note`: feedback corretivo (ver _coverage_note) anexado ao prompt nas re-rodadas do batch."""
    reuse = _select_reuse(pack, enabled=True)
    novel = [r for r in pack["lines"] if r["offset"] not in reuse]
    if not novel:
        return None, reuse, novel
    system = [{"type": "text", "text": _carta_text(), "cache_control": {"type": "ephemeral"}}]
    red = dict(pack); red["lines"] = novel; red["n_lines"] = len(novel)
    base_user = context_pack.render_prompt(red, carta="") + _NL_RULE + note
    # Haiku 4.5 / Sonnet 4.5 NAO aceitam output_config.effort (400) — igual ao _api_translate, OMITE o
    # effort nesses modelos. BUG MEDIDO (cap.15): o batch sempre mandava effort -> todo request do tier
    # cheap (Haiku) dava 400 -> as linhas single-line nunca voltavam (MISSING) -> coverage_failed.
    out_cfg = {"format": {"type": "json_schema", "schema": _TRANSLATION_SCHEMA}}
    if not _no_effort_model(model):
        out_cfg["effort"] = EFFORT_TRANSLATE
    params = {
        "model": model, "max_tokens": MAX_OUTPUT_TOKENS, "system": system,
        "messages": [{"role": "user", "content": base_user}],
        "thinking": {"type": "disabled"},
        "output_config": out_cfg,
    }
    return params, reuse, novel


def _write_translations(root, scene, data):
    out = paths.translations(root, scene, context_pack.scene_id_of(scene))
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _tier_of(source: str) -> str:
    """Tier de modelo por COMPLEXIDADE: 'main' (Sonnet) p/ linha com token de quebra (multi-linha);
    'cheap' (Haiku) p/ single-line. Driblar a fraqueza medida do Haiku (paridade de \\n so falha onde
    HA \\n)."""
    return "main" if context_pack.TOKEN in (source or "") else "cheap"


def _parse_batch_lines(pack, text):
    """Parseia UMA resposta de batch -> {offset: entry} so das linhas NOVAS validas (parity-fitted).
    Tolera incompletude (devolve o que veio); {} se o JSON quebrar. Usado p/ ACUMULAR entre rodadas."""
    reuse = _select_reuse(pack, enabled=True)
    novel_offsets = {r["offset"] for r in pack["lines"]} - set(reuse)
    srcmap = {r["offset"]: r.get("source", "") for r in pack["lines"]}
    try:
        parsed = _to_map(json.loads(text))
    except Exception:
        return {}
    out = {}
    for off, v in parsed.get("lines", {}).items():
        if off in novel_offsets and isinstance(v, dict):
            v["t"] = _parity_fit(srcmap.get(off, ""), v.get("t", ""))
            if _is_blowup(srcmap.get(off, ""), v["t"]):
                continue                                 # lixo patologico -> descarta (re-roda / missing)
            out[off] = v
    return out


def _merge_best_parity(dest, new, srcmap):
    """Mescla `new` em `dest` ACUMULANDO entre rodadas, preferindo paridade de `\\n` correta — igual ao
    _api_translate (interativo). NUNCA troca uma linha de paridade BOA por uma RUIM: assim uma re-rodada
    que regride uma linha ja boa nao desfaz o ganho (o `dict.update` cego perdia isso e a cena nao
    convergia). Mesma paridade -> usa a mais nova (consistente com o comportamento anterior)."""
    tok = context_pack.TOKEN
    for off, v in new.items():
        src = srcmap.get(off, "")
        good = v.get("t", "").count(tok) == src.count(tok)
        old = dest.get(off)
        if old is None:
            dest[off] = v
            continue
        old_good = old.get("t", "").count(tok) == src.count(tok)
        if good or not old_good:        # melhora a paridade, ou ambas ruins -> aceita a nova
            dest[off] = v
    return dest


def _batch_coverage(pack, merged):
    """(missing, bad_parity) das linhas NOVAS, dado o acumulado `merged` (offset->entry)."""
    tok = context_pack.TOKEN
    reuse = _select_reuse(pack, enabled=True)
    novel = [r for r in pack["lines"] if r["offset"] not in reuse]
    srcmap = {r["offset"]: r.get("source", "") for r in novel}
    missing = [r["offset"] for r in novel if r["offset"] not in merged]
    bad_par = [o for o in srcmap if o in merged
               and merged[o].get("t", "").count(tok) != srcmap[o].count(tok)]
    return missing, bad_par


def _await_batch(client, batch_id, poll_seconds, max_wait_seconds):
    """Aguarda o batch terminar (processing_status='ended'). True=terminou; False=timeout."""
    waited = 0
    while True:
        b = _with_backoff(lambda: client.messages.batches.retrieve(batch_id))   # poll resiliente a timeout
        if getattr(b, "processing_status", None) == "ended":
            return True
        if waited >= max_wait_seconds:
            return False
        time.sleep(poll_seconds)
        waited += poll_seconds


def batch_translate(root, scenes, *, model=None, poll_seconds=30, max_wait_seconds=24 * 3600,
                    max_rounds=3, tiered=True):
    """Traduz VARIAS cenas em batches (50% off), ACUMULANDO cobertura entre RODADAS. O batch e 1-tiro
    por requisicao (sem retry interno) -> cenas grandes as vezes dropam linhas. Em vez de cair pro
    caminho interativo a preco CHEIO, cada rodada re-batcha SO o que falta (cena inteira na 1a; depois
    apenas os offsets faltantes/de paridade ruim) e mescla — convergindo a -50%.

    TIERING (tiered=True, default): por cena/rodada, as linhas SEM token de quebra vao num request Haiku
    (-67%/linha) e as COM `\\n` num request Sonnet (confiabilidade de paridade). custom_id = 'scene__tier'
    (separador `__` — a Batch API rejeita custom_id fora de ^[a-zA-Z0-9_-]{1,64}$, ex.: '@' dá 400).

    Grava translations_<scene_id>.json das cenas completas; retorna {scene: status} em
    {all_reused, written, coverage_failed, errored:<tipo>, timeout}. Cenas != (written|all_reused) ainda
    caem p/ o caminho interativo (run_scene). NAO roda build_plan/verify (isso e por-cena)."""
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    root = Path(root)
    m = model or MODEL_TRANSLATE
    cheap = MODEL_TRANSLATE_CHEAP if (tiered and MODEL_TRANSLATE_CHEAP) else m
    tiers = (("cheap", cheap), ("main", m))            # roteamento por complexidade
    client = _client()
    packs, merged, status = {}, {}, {}
    pending = []
    for scene in scenes:
        pack = context_pack.write_pack(root, scene)
        packs[scene] = pack
        reuse = _select_reuse(pack, enabled=True)
        merged[scene] = dict(reuse)                      # reuso pre-preenche o acumulado
        # RESUME (idempotente): se ja existe translations_<scene_id>.json, aproveita -> nao re-batcha o que ja
        # foi pago. Cobertura parcial: re-batcha SO o que falta (ver rodadas). Cobertura completa: pula.
        existing = paths.translations(root, scene, pack['scene_id'])
        if existing.is_file():
            try:
                ex = json.loads(existing.read_text(encoding="utf-8")).get("lines", {})
                merged[scene].update({o: v for o, v in ex.items() if isinstance(v, dict)})
            except Exception:
                pass
        miss, badpar = _batch_coverage(pack, merged[scene])
        if not miss and not badpar:
            _write_translations(root, scene, {"lines": merged[scene]})
            status[scene] = "all_reused" if all(r["offset"] in reuse for r in pack["lines"]) else "written"
        else:
            pending.append(scene)

    for rnd in range(max_rounds):
        if not pending:
            break
        reqs, req_model = [], {}                          # req_model[custom_id] = modelo (p/ custo no ledger)
        for scene in pending:
            miss, badpar = _batch_coverage(packs[scene], merged[scene])
            want = (set(miss) | set(badpar)) if rnd > 0 else None   # rnd0: tudo; depois: so o que falta
            for tier, tmodel in tiers:                    # split por COMPLEXIDADE (cheap=Haiku / main=Sonnet)
                tier_lines = [r for r in packs[scene]["lines"]
                              if _tier_of(r.get("source", "")) == tier
                              and (want is None or r["offset"] in want)]
                # CHUNKING: cada request = ate _BATCH_CHUNK linhas (o batch trunca saidas longas). Cada
                # chunk e auto-contido (render so das suas linhas) e volta completo; a cobertura acumula
                # entre chunks E rodadas via _merge_best_parity.
                for ci in range(0, len(tier_lines), _BATCH_CHUNK):
                    chunk = tier_lines[ci:ci + _BATCH_CHUNK]
                    sub = dict(packs[scene]); sub["lines"] = chunk
                    # FEEDBACK CORRETIVO na re-rodada (rnd>0): nota com os offsets faltando/paridade-errada
                    # DESTE chunk, como o _api_translate faz.
                    note = ""
                    if rnd > 0:
                        coffs = {r["offset"] for r in chunk}
                        note = _coverage_note([o for o in miss if o in coffs],
                                              [o for o in badpar if o in coffs])
                    params, _reuse, _novel = _translate_params(sub, tmodel, note=note)
                    if params is None:                    # tudo reuso nesse chunk -> sem request
                        continue
                    # custom_id 'scene__tier__chunk' — ^[a-zA-Z0-9_-]{1,64}$; split('__',1)[0] = scene
                    cid = f"{scene}__{tier}__{ci // _BATCH_CHUNK}"
                    req_model[cid] = tmodel
                    reqs.append(Request(custom_id=cid, params=MessageCreateParamsNonStreaming(**params)))
        if not reqs:
            break
        batch = _with_backoff(lambda: client.messages.batches.create(requests=reqs))
        if not _await_batch(client, batch.id, poll_seconds, max_wait_seconds):
            for scene in pending:
                status.setdefault(scene, "timeout")
            return status
        # materializa os resultados DENTRO do backoff (a iteracao faz I/O lazy -> timeout no meio)
        results = _with_backoff(lambda: list(client.messages.batches.results(batch.id)))
        for result in results:
            cid = result.custom_id
            scene = cid.split("__", 1)[0]
            if getattr(result.result, "type", None) != "succeeded":
                continue                                  # tier falho -> cobertura decide (re-batch/fallback)
            msg = result.result.message
            log_api_call(root, scene, "translate", req_model.get(cid, m), _usage_of(msg), batch=True)
            srcmap = {r["offset"]: r.get("source", "") for r in packs[scene]["lines"]}
            _merge_best_parity(merged[scene], _parse_batch_lines(packs[scene], _text_of(msg)), srcmap)
        still = []
        for scene in pending:
            if str(status.get(scene, "")).startswith("errored"):
                continue                                 # erro duro -> nao re-tenta; cai p/ interativo
            miss, badpar = _batch_coverage(packs[scene], merged[scene])
            if not miss and not badpar:
                _write_translations(root, scene, {"lines": merged[scene]})
                status[scene] = "written"
            else:
                still.append(scene)
        pending = still

    for scene in pending:
        status.setdefault(scene, "coverage_failed")      # nao convergiu apos as rodadas -> interativo
    return status


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


def _back_params(high_lines, model):
    """Params de UMA requisicao de back-translation (compartilhado pelo caminho streaming e pelo BATCH).
    Determinista (sem rede) -> montagem do request testavel sem SDK."""
    payload = [{"offset": h["offset"], "source": h["source"], "target": h["target"],
                "speaker": h.get("speaker", "")} for h in high_lines]
    instr = ("Para cada item, traduza o 'target' (pt-BR) de volta p/ EN ('back_en'), compare com "
             "'source', e de um 'verdict' (pass|revise) + 'note' curta. verdict=revise se "
             "sentido/ambiguidade/voz divergirem. Inclua o 'offset' de cada item.\n\n")
    return {
        "model": model, "max_tokens": MAX_OUTPUT_TOKENS,
        "messages": [{"role": "user", "content": instr + json.dumps(payload, ensure_ascii=False)}],
        "thinking": {"type": "adaptive"},
        "output_config": {"effort": "high",
                          "format": {"type": "json_schema", "schema": _BACK_SCHEMA}},
    }


def _api_back_translate(root, scene, high_lines, model):
    client = _client()
    msg = _stream_final(client, **_back_params(high_lines, model))
    usage = _usage_of(msg)
    log_api_call(root, scene, "back", model, usage)   # registra antes do parse (Opus cobra mesmo se quebrar)
    data = json.loads(_text_of(msg))
    data["reviewed"] = len(data.get("entries", []))
    return data, usage


def _plan_lines(root, scene):
    """Linhas brutas do translation_plan_<scene_id>.json (lista), ou [] se nao houver plano.
    Delega ao artifact_io (fonte unica do parse de plano)."""
    return artifact_io.plan_lines(root, scene)


def _ln_entry(ln):
    """Normaliza uma linha do plano p/ o shape de candidato de back-translation."""
    return {"offset": ln.get("offset", ""), "source": ln.get("text_source", ""),
            "target": ln.get("base_translation", ""), "speaker": ln.get("speaker", ""),
            "risk_notes": ln.get("risk_notes", "")}


def high_risk_lines(root, scene):
    """Linhas risco>=high/critical do translation_plan_<scene_id>.json (candidatas a back-translation).
    Le o plano do conector (existe apos build_plan). Fonte unica — run_scene e o batch leem daqui."""
    return [_ln_entry(ln) for ln in _plan_lines(root, scene)
            if ln.get("risk_level") in ("high", "critical")]


def sample_low_risk_lines(root, scene, rate=BACK_SAMPLE_RATE, *, seed="bt"):
    """Amostra DETERMINISTICA (~rate) das linhas low/medium — o piso de qualidade do tier barato.
    A inclusao depende so de sha1(seed|scene_id|offset): rodar 2x da o MESMO conjunto (idempotente,
    sem random). rate<=0 -> vazio. Retorna o mesmo shape de high_risk_lines."""
    if rate <= 0:
        return []
    scene_id = context_pack.scene_id_of(scene)
    out = []
    for ln in _plan_lines(root, scene):
        if ln.get("risk_level") in ("high", "critical"):
            continue
        h = hashlib.sha1(f"{seed}|{scene_id}|{ln.get('offset','')}".encode("utf-8")).hexdigest()
        if int(h[:8], 16) % 10000 < rate * 10000:
            out.append(_ln_entry(ln))
    return out


def back_translate_candidates(root, scene, sample_rate=BACK_SAMPLE_RATE):
    """Candidatos a back-translation = high/critical (sempre) UNIAO amostra ~sample_rate das low/medium.
    Dedup por offset (high vence). E a fonte de candidatos do batch_back_translate."""
    cands = high_risk_lines(root, scene)
    seen = {c["offset"] for c in cands}
    for c in sample_low_risk_lines(root, scene, sample_rate):
        if c["offset"] not in seen:
            cands.append(c)
            seen.add(c["offset"])
    return cands


def batch_back_translate(root, scenes, *, model=None, poll_seconds=30, max_wait_seconds=24 * 3600,
                         sample_rate=BACK_SAMPLE_RATE):
    """Back-translation de VARIAS cenas num UNICO batch (-50% sobre o Opus, o passo mais caro/linha).
    A back-translation e report-only e roda DEPOIS do verify (precisa do translation_plan) -> e um
    POS-PASSE natural: coleta os candidatos de cada cena (high/critical + amostra ~sample_rate das
    low/medium, p/ dar piso de qualidade ao tier barato), monta 1 request por cena e submete em batch.
    Grava back_translation_<scene_id>.json por cena. custom_id = scene.

    Resume idempotente: cena que ja tem back_translation_<scene_id>.json e pulada (nao re-cobra). Cena sem
    candidato -> 'no_high' (sem request). Retorna {scene: status} em
    {reviewed, no_high, errored, parse_failed, timeout}. NAO bloqueia o pipeline (o run_scene ja seguiu)."""
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    root = Path(root)
    m = model or MODEL_BACK
    status, highs, reqs = {}, {}, []
    for scene in scenes:
        scene_id = context_pack.scene_id_of(scene)
        out = paths.back_translation(root, scene, scene_id)
        hl = back_translate_candidates(root, scene, sample_rate)
        if not hl:
            status[scene] = "no_high"
            continue
        if out.is_file():                                # ja revisada (run anterior) -> nao re-cobra
            status[scene] = "reviewed"
            continue
        highs[scene] = hl
        reqs.append(Request(custom_id=scene,
                            params=MessageCreateParamsNonStreaming(**_back_params(hl, m))))
    if not reqs:
        return status
    client = _client()
    batch = _with_backoff(lambda: client.messages.batches.create(requests=reqs))
    if not _await_batch(client, batch.id, poll_seconds, max_wait_seconds):
        for scene in highs:
            status.setdefault(scene, "timeout")
        return status
    # materializa os resultados DENTRO do backoff (igual ao batch_translate; foi aqui que o cap.18 morreu)
    results = _with_backoff(lambda: list(client.messages.batches.results(batch.id)))
    for result in results:
        scene = result.custom_id
        if getattr(result.result, "type", None) != "succeeded":
            status[scene] = "errored"
            continue
        msg = result.result.message
        log_api_call(root, scene, "back", m, _usage_of(msg), batch=True)   # registra antes do parse
        try:
            data = json.loads(_text_of(msg))
            data["reviewed"] = len(data.get("entries", []))
            scene_id = context_pack.scene_id_of(scene)
            (paths.back_translation(root, scene, scene_id)).write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            status[scene] = "reviewed"
        except Exception:
            status[scene] = "parse_failed"                # cobrado (ledger), mas saida nao parseou
    return status


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
