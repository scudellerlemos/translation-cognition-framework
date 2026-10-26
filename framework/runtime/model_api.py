"""model_api.py — caminho de API do translate (ADR 0019): cliente, streaming, retry, lote (batch).

Implementacao fiel ao skill claude-api; import preguicoso do SDK, sem rede em import/teste. Nao importa o caminho de
sessao. `model` reexporta estes nomes (compat com chamadores e monkeypatch de testes: o alvo do patch das
dependencias de rede e este modulo, `model_api._client` etc.).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import paths  # noqa: E402
import translate_checkpoint as ckpt  # noqa: E402
from back_translate import invalidate_back_translation  # noqa: E402
from config import (  # noqa: E402
    _BATCH_CHUNK,
    _MAX_TRIES,
    _TRANSLATE_SUBMIT_CHUNK,
    BUDGET_TOLERANCE,
    DONE,
    EFFORT_TRANSLATE,
    MAX_OUTPUT_TOKENS,
    MODEL_TRANSLATE,
    MODEL_TRANSLATE_CHEAP,
    THINK_TRANSLATE,
)
from cost import log_api_call  # noqa: E402
from llm_client import (  # noqa: E402
    _add_usage,
    _await_batch,
    _carta_text,
    _client,
    _stream_final,
    _text_of,
    _usage_of,
    _with_backoff,
)
from translation_rules import (  # noqa: E402
    _budget_len,
    _is_blowup,
    _line_ok,
    _norm_t,
    _over_budget,
    _parity_fit,
    _prefilled,
    _struct_ok,
    _structural_rx,
)


def _no_effort_model(model: str) -> bool:
    """Modelos que NAO aceitam output_config.effort nem adaptive thinking (400): Haiku 4.5 e Sonnet 4.5.
    Opus 4.x e Sonnet 4.6 aceitam. Usado p/ montar params validos por modelo (tiering de custo)."""
    return model.startswith("claude-haiku") or model == "claude-sonnet-4-5"


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


def _budget_note(over: list, pc: dict) -> str:
    """Texto de correcao de retry p/ offsets acima do budget — usado por _api_translate."""
    metric = ("bytes UTF-8 reais — cada acento custa byte extra, NAO e removido na gravacao"
              if (pc or {}).get("target_charset_supported") is True
              else "TRANSLITERADO, sem acentos")
    if (pc or {}).get("budget_reserves_terminator"):
        metric += "; o byte_budget ja reserva 1 byte pro terminador, o texto precisa caber em budget-1"
    note = (f"- Estes offsets passam do byte_budget ({metric}); ENCURTE preservando o sentido "
            "(corte redundancia; ex.: 'adicionado ao'->'no'):\n")
    for off, b, cur in over[:25]:
        note += f"  - {off}: budget {b}, atual {cur}\n"
    return note


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
    pc = pack.get("project_constraints", {})
    struct_rx = _structural_rx(pc)
    # DEDUP por TM (so no 1o passe; desligado no escalonamento de fitting p/ re-traduzir mais curto):
    # linhas com fonte ja traduzida em OUTRA cena nao vao ao modelo (corta tokens de saida).
    reuse = _prefilled(pack, enabled=(budget_tolerance is None))   # rotulo: passthrough SEMPRE (ate no retighten)
    novel = [r for r in pack["lines"] if r["offset"] not in reuse]
    meta = {"reused": len(reuse), "novel": len(novel), "n_lines": len(pack["lines"])}
    if not novel:                                     # cena 100% reaproveitada -> zero chamada de API
        return {"lines": dict(reuse)}, {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}, meta

    client = _client()
    # system = doutrina estavel (cacheada ~1x via cache_control); user = pacote da cena (so as novas)
    system = [{"type": "text", "text": _carta_text(), "cache_control": {"type": "ephemeral"}}]
    novel_by_off = {r["offset"]: r for r in novel}
    offsets = [r["offset"] for r in novel]
    offset_set = set(offsets)
    budgets = {r["offset"]: r.get("byte_budget") for r in novel}
    srcmap = {r["offset"]: r.get("source", "") for r in novel}
    last, usage = None, {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}
    # L01: so o 1o passe usa checkpoint (no escalonamento de fitting a traducao e mais curta de proposito)
    sid, use_ckpt, dh = context_pack.scene_id_of(scene), budget_tolerance is None, pack.get("doctrine_hash", "")
    seed = ckpt.load(root, scene, sid, dh, srcmap, enabled=use_ckpt)   # linhas ja pagas de uma rodada que esgotou
    merged = dict(seed)  # ACUMULA linhas entre tentativas: cada retry preenche lacunas -> cobertura converge
    # thinking custa como saida ($15/M). Traducao com contexto curado raramente exige raciocinio
    # profundo -> default sem thinking + effort baixo (medido: corta ~5x o custo; ver OBSERVABILITY).
    # Haiku 4.5 / Sonnet 4.5 NAO aceitam output_config.effort nem adaptive thinking (400) -> omitir.
    no_effort = _no_effort_model(model)
    thinking = {"type": "adaptive"} if (think and not no_effort) else {"type": "disabled"}
    out_cfg: dict = {"format": {"type": "json_schema", "schema": _TRANSLATION_SCHEMA}}
    if not no_effort:
        out_cfg["effort"] = effort

    def _over(off, v):
        return _over_budget((v or {}).get("t", ""), budgets.get(off), pc, tol)

    def _render(target, note):
        # PREVISIBILIDADE (recuperacao por-linha): o 1o passe manda TODAS as linhas novas; a re-rodada manda
        # SO as quebradas (faltantes/paridade-ruim/acima-do-budget), nunca a cena inteira de novo. O
        # context_pack (glossario/vozes/decisoes/TM) vai junto em qualquer caso -> a coerencia de cena se
        # preserva; muda so a LISTA de linhas a traduzir -> custo de retry ∝ linhas quebradas, nao ∝ cena.
        red = dict(pack); red["lines"] = target; red["n_lines"] = len(target)
        return context_pack.render_prompt(red, carta="") + _NL_RULE + quality_note + note

    target, note = [r for r in novel if r["offset"] not in seed], ""   # quality_note (back-translation/quality_fix) entra via _render; "" no fluxo normal
    for attempt in range(_MAX_TRIES):
        msg = _stream_final(
            client, model=model, max_tokens=MAX_OUTPUT_TOKENS,
            system=system,
            messages=[{"role": "user", "content": _render(target, note)}],
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
            good_parity = _line_ok(srcmap.get(off, ""), v["t"], struct_rx)
            if off not in merged:
                merged[off] = v                      # preenche lacuna
            else:
                old = merged[off]
                old_parity = _line_ok(srcmap.get(off, ""), old.get("t", ""), struct_rx)
                if good_parity and not old_parity:
                    merged[off] = v                  # prioriza paridade correta
                elif good_parity == old_parity and _over(off, old) and \
                        _budget_len(v.get("t", ""), pc) < _budget_len(old.get("t", ""), pc):
                    merged[off] = v                  # mesma paridade: prefere a mais curta (budget)
        missing = [o for o in offsets if o not in merged]
        bad_par = [o for o in merged if merged[o].get("t", "").count(tok) != srcmap.get(o, "").count(tok)]
        bad_struct = [o for o in merged if not _struct_ok(struct_rx, srcmap.get(o, ""), merged[o].get("t", ""))]
        over = [(o, budgets[o], _budget_len(merged[o].get("t", ""), pc))
                for o in merged if _over(o, merged[o])]
        last = {"missing": missing, "bad_parity": bad_par, "bad_structural": bad_struct, "over_budget": over}
        # HARD (bloqueia): cobertura + paridade de quebra + tokens de formatacao do engine (build_plan
        # reprova ambos). SOFT (best-effort): byte_budget — o conector absorve via head-reloc; a VERIFY
        # (round-trip) e o juiz de residuo.
        if not missing and not bad_par and not bad_struct and (not over or attempt == _MAX_TRIES - 1):
            merged.update(reuse)                      # reanexa as linhas reaproveitadas da TM
            ckpt.clear(root, scene, sid, enabled=use_ckpt)
            return {"lines": merged}, usage, meta
        # PROXIMA RODADA = SO as linhas quebradas (recuperacao por-linha, nao re-traduz a cena inteira)
        broken = set(missing) | set(bad_par) | set(bad_struct) | {o for o, _b, _c in over}
        target = [novel_by_off[o] for o in offsets if o in broken]
        note = "\n\n## CORRECAO NECESSARIA (traduza SO as linhas acima; vamos MESCLAR com o resto ja pronto)\n"
        if missing:
            note += f"- Faltam estes offsets — INCLUA todos: {missing[:40]}\n"
        if bad_par:
            note += (f"- Estes offsets tem nº de quebras `\\n` DIFERENTE da fonte — case EXATO (mesma "
                     f"quantidade e posicao do token): {bad_par[:30]}\n")
        if bad_struct:
            note += (f"- Estes offsets perderam ou trocaram tokens de formatacao do engine (ex.: <C1>, "
                     f"<P2>) — preserve EXATAMENTE os mesmos tokens da fonte, na mesma quantidade e sem "
                     f"remover os `<>`: {bad_struct[:30]}\n")
        if over:
            note += _budget_note(over, pc)
    assert last is not None  # _MAX_TRIES > 0 -> loop roda >=1x -> last sempre atribuido aqui
    kept = ckpt.save(root, scene, sid, dh, merged, srcmap,
                     set(last["bad_parity"]) | set(last["bad_structural"]), enabled=use_ckpt)
    ckpt.log_exhausted(root, scene, model, usage, last, kept, stage="first" if use_ckpt else "retighten")
    raise RuntimeError(f"_api_translate: cobertura/paridade incompletas apos {_MAX_TRIES} tentativas: "
                       f"faltam={last['missing']} paridade={last['bad_parity']} "
                       f"formatacao={last['bad_structural']}"
                       + (f" | {kept} linha(s) boa(s) salvas em checkpoint: rode de novo p/ retomar" if kept else ""))


def retranslate_offsets(root, scene, offsets, *, model=None, budget_tolerance, quality_note="",
                        backend: str = "api"):
    """Re-traduz APENAS `offsets` (apertado por budget_tolerance) e MESCLA no translations_<scene_id>.json,
    preservando todas as outras linhas. Caminho cirurgico do escalonamento de fitting (e do quality_fix).
    Reusa _api_translate sobre um pack reduzido (dedup ja vem OFF com
    budget_tolerance != None -> traduz fresco e mais curto). `backend` despacha igual translate()
    (default "api" preserva o comportamento de todo caller anterior). `quality_note` opcional anexa
    feedback de revisao da back-translation ao prompt (so suportado no backend api; quality_fix so
    roda nesse caminho hoje)."""
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
    if backend == "api":
        m = model or MODEL_TRANSLATE
        data, usage, meta = _api_translate(root, scene, sub, m, budget_tolerance=budget_tolerance,
                                           quality_note=quality_note)
    else:
        raise ValueError(f"backend desconhecido: {backend}")
    full.setdefault("lines", {}).update(data.get("lines", {}))   # merge: so os offsets re-traduzidos
    paths.atomic_write(out, json.dumps(full, ensure_ascii=False, indent=2))
    invalidate_back_translation(root, scene, offset_set)         # o verdict antigo nao vale mais
    return {"status": DONE, "model": m, "usage": usage, "n_lines": sub["n_lines"],
            "reused": meta["reused"], "novel": meta["novel"]}


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
        note += ("- Estes offsets tem nº de quebras `\\n` ou tokens de formatacao DIFERENTES da fonte — case EXATO (mesma "
                 f"quantidade e posicao do token): {sorted(bad_par)[:30]}\n")
    return note


def _translate_params(pack, model, note=""):
    """Params de UMA requisicao de traducao (compartilhado por batch). Aplica dedup; retorna
    (params|None, reuse, novel). params=None quando a cena e 100% reaproveitada da TM (sem chamada).
    `note`: feedback corretivo (ver _coverage_note) anexado ao prompt nas re-rodadas do batch."""
    reuse = _prefilled(pack)
    novel = [r for r in pack["lines"] if r["offset"] not in reuse]
    if not novel:
        return None, reuse, novel
    system = [{"type": "text", "text": _carta_text(), "cache_control": {"type": "ephemeral"}}]
    red = dict(pack); red["lines"] = novel; red["n_lines"] = len(novel)
    base_user = context_pack.render_prompt(red, carta="") + _NL_RULE + note
    # Haiku 4.5 / Sonnet 4.5 NAO aceitam output_config.effort (400) — igual ao _api_translate, OMITE o
    # effort nesses modelos. BUG MEDIDO (cap.15): o batch sempre mandava effort -> todo request do tier
    # cheap (Haiku) dava 400 -> as linhas single-line nunca voltavam (MISSING) -> coverage_failed.
    out_cfg: dict = {"format": {"type": "json_schema", "schema": _TRANSLATION_SCHEMA}}
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
    paths.atomic_write(out, json.dumps(data, ensure_ascii=False, indent=2))


def _tier_of(source: str) -> str:
    """Tier de modelo por COMPLEXIDADE: 'main' (Sonnet) p/ linha com token de quebra (multi-linha);
    'cheap' (Haiku) p/ single-line. Driblar a fraqueza medida do Haiku (paridade de \\n so falha onde
    HA \\n)."""
    return "main" if context_pack.TOKEN in (source or "") else "cheap"


def _parse_batch_lines(pack, text):
    """Parseia UMA resposta de batch -> {offset: entry} so das linhas NOVAS validas (parity-fitted).
    Tolera incompletude (devolve o que veio); {} se o JSON quebrar. Usado p/ ACUMULAR entre rodadas."""
    reuse = _prefilled(pack)                          # rotulo tambem: resposta que o ecoe nao sobrescreve o passthrough
    novel_offsets = {r["offset"] for r in pack["lines"]} - set(reuse)
    srcmap = {r["offset"]: r.get("source", "") for r in pack["lines"]}
    struct_rx = _structural_rx(pack.get("project_constraints", {}))
    try:
        parsed = _to_map(json.loads(text))
    except Exception as exc:
        print(f"[batch] AVISO: resposta de batch ilegivel ({type(exc).__name__}) -- rodada sem linhas novas.")
        return {}
    out = {}
    for off, v in parsed.get("lines", {}).items():
        if off in novel_offsets and isinstance(v, dict):
            v["t"] = _parity_fit(srcmap.get(off, ""), v.get("t", ""))
            if _is_blowup(srcmap.get(off, ""), v["t"]):
                continue                                 # lixo patologico -> descarta (re-roda / missing)
            if not _struct_ok(struct_rx, srcmap.get(off, ""), v["t"]):
                continue                                 # token de formatacao perdido/trocado (paridade com o caminho interativo)
            out[off] = v
    return out


def _merge_best_parity(dest, new, srcmap, rx=None):
    """Mescla `new` em `dest` ACUMULANDO entre rodadas, preferindo paridade de `\\n` correta — igual ao
    _api_translate (interativo). NUNCA troca uma linha de paridade BOA por uma RUIM: assim uma re-rodada
    que regride uma linha ja boa nao desfaz o ganho (o `dict.update` cego perdia isso e a cena nao
    convergia). Mesma paridade -> usa a mais nova (consistente com o comportamento anterior)."""
    for off, v in new.items():
        src = srcmap.get(off, "")
        good = _line_ok(src, v.get("t", ""), rx)
        old = dest.get(off)
        if old is None:
            dest[off] = v
            continue
        old_good = _line_ok(src, old.get("t", ""), rx)
        if good or not old_good:        # melhora a paridade, ou ambas ruins -> aceita a nova
            dest[off] = v
    return dest


def _batch_coverage(pack, merged):
    """(missing, bad_parity) das linhas NOVAS, dado o acumulado `merged` (offset->entry). bad_parity =
    `\\n` OU tokens de formatacao divergentes (batch sem isso deixava <C1> perdido ir pro build_plan)."""
    rx = _structural_rx(pack.get("project_constraints", {}))
    reuse = _prefilled(pack)                          # rotulo de engine nunca vai ao lote (_translate_params)
    novel = [r for r in pack["lines"] if r["offset"] not in reuse]
    srcmap = {r["offset"]: r.get("source", "") for r in novel}
    missing = [r["offset"] for r in novel if r["offset"] not in merged]
    bad_par = [o for o in srcmap if o in merged and not _line_ok(srcmap[o], merged[o].get("t", ""), rx)]
    return missing, bad_par


def _submit_translate_chunk(client, chunk_reqs, poll_seconds, max_wait_seconds, req_model, req_offsets,
                            packs, merged, root, default_model):
    """Submete e mescla UM chunk de requests de traducao (ate _TRANSLATE_SUBMIT_CHUNK requests por
    batch). Isola a rodada inteira de virar tudo-ou-nada: um chunk que trava/estoura o timeout so fica
    SEM cobertura dele agora -- a rodada seguinte (ou o coverage_failed final, se acabarem as rodadas)
    trata o que faltar, exatamente como qualquer request perdido hoje (mesmo caminho do
    _batch_coverage/_merge_best_parity). Ver feedback-segment-large-batches / _TRANSLATE_SUBMIT_CHUNK.

    req_offsets[cid] = offsets REALMENTE pedidos NESTE chunk/tier -- restringe o merge a eles, pra uma
    resposta que "vaze" um offset de OUTRO chunk da mesma cena (alucinado/duplicado) nao ser aceita sem
    nunca ter sido validada no contexto/orcamento do chunk a que aquele offset pertence de verdade."""
    batch = _with_backoff(lambda: client.messages.batches.create(requests=chunk_reqs))  # noqa: B023  (_with_backoff invoca na hora)
    if not _await_batch(client, batch.id, poll_seconds, max_wait_seconds):
        print(f"  [translate-batch] chunk {batch.id} nao concluiu em {max_wait_seconds}s "
              f"({len(chunk_reqs)} requisicao(oes)) -- segue sem essa cobertura agora; "
              f"a rodada seguinte re-tenta o que faltar.")
        return
    # materializa os resultados DENTRO do backoff (a iteracao faz I/O lazy -> timeout no meio)
    results = _with_backoff(lambda: list(client.messages.batches.results(batch.id)))  # noqa: B023  (_with_backoff invoca na hora)
    for result in results:
        cid = result.custom_id
        scene = cid.split("__", 1)[0]
        if getattr(result.result, "type", None) != "succeeded":
            continue                                  # tier falho -> cobertura decide (re-batch/fallback)
        msg = result.result.message
        log_api_call(root, scene, "translate", req_model.get(cid, default_model), _usage_of(msg), batch=True)
        srcmap = {r["offset"]: r.get("source", "") for r in packs[scene]["lines"]}
        parsed = _parse_batch_lines(packs[scene], _text_of(msg))
        wanted = req_offsets.get(cid)
        if wanted is not None:
            parsed = {off: v for off, v in parsed.items() if off in wanted}
        _merge_best_parity(merged[scene], parsed, srcmap,
                           _structural_rx(packs[scene].get("project_constraints", {})))


def batch_translate(root, scenes, *, model=None, poll_seconds=30, max_wait_seconds=24 * 3600,
                    max_rounds=3, tiered=True):
    """Traduz VARIAS cenas em batches (50% off), ACUMULANDO cobertura entre RODADAS. O batch e 1-tiro
    por requisicao (sem retry interno) -> cenas grandes as vezes dropam linhas. Em vez de cair pro
    caminho interativo a preco CHEIO, cada rodada re-batcha SO o que falta (cena inteira na 1a; depois
    apenas os offsets faltantes/de paridade ruim) e mescla — convergindo a -50%.

    TIERING (tiered=True, default): por cena/rodada, as linhas SEM token de quebra vao num request Haiku
    (-67%/linha) e as COM `\\n` num request Sonnet (confiabilidade de paridade). custom_id = 'scene__tier'
    (separador `__` — a Batch API rejeita custom_id fora de ^[a-zA-Z0-9_-]{1,64}$, ex.: '@' dá 400).

    SEGMENTACAO (`_TRANSLATE_SUBMIT_CHUNK`, ver _submit_translate_chunk): as requisicoes de CADA rodada
    sao submetidas em chunks (nao 1 batch gigante) — um chunk que trava so fica sem cobertura dele,
    a rodada seguinte re-tenta o que faltar (ou vira coverage_failed apos max_rounds).

    Grava translations_<scene_id>.json das cenas completas; retorna {scene: status} em
    {all_reused, written, coverage_failed, errored:<tipo>}. Cenas != (written|all_reused) ainda
    caem p/ o caminho interativo (run_scene). NAO roda build_plan/verify (isso e por-cena)."""
    from typing import cast

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
        reuse = _prefilled(pack)
        merged[scene] = dict(reuse)                      # reuso pre-preenche o acumulado
        # RESUME (idempotente): se ja existe translations_<scene_id>.json, aproveita -> nao re-batcha o que ja
        # foi pago. Cobertura parcial: re-batcha SO o que falta (ver rodadas). Cobertura completa: pula.
        existing = paths.translations(root, scene, pack['scene_id'])
        if existing.is_file():
            try:
                ex = json.loads(existing.read_text(encoding="utf-8")).get("lines", {})
                merged[scene].update({o: v for o, v in ex.items() if isinstance(v, dict)})
            except Exception as exc:
                print(f"[batch] AVISO: {existing.name} ilegivel ({exc!r}) -- as linhas ja pagas desse "
                      f"arquivo serao re-traduzidas e o arquivo sobrescrito.")
        miss, badpar = _batch_coverage(pack, merged[scene])
        if not miss and not badpar:
            _write_translations(root, scene, {"lines": merged[scene]})
            status[scene] = "all_reused" if all(r["offset"] in reuse for r in pack["lines"]) else "written"
        else:
            pending.append(scene)

    for rnd in range(max_rounds):
        if not pending:
            break
        reqs, req_model, req_offsets = [], {}, {}         # req_model/req_offsets[custom_id] = modelo/offsets pedidos
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
                    req_offsets[cid] = {r["offset"] for r in chunk}
                    reqs.append(Request(custom_id=cid, params=cast(MessageCreateParamsNonStreaming, params)))
        if not reqs:
            break
        # SEGMENTACAO: nao submete tudo num batch so -- fatia em chunks de _TRANSLATE_SUBMIT_CHUNK
        # requests, cada 1 um batch SEPARADO (ver _submit_translate_chunk). Blast radius menor: um
        # chunk lento/travado nao afeta os demais nem aborta a rodada inteira.
        for i in range(0, len(reqs), _TRANSLATE_SUBMIT_CHUNK):
            chunk = reqs[i:i + _TRANSLATE_SUBMIT_CHUNK]
            _submit_translate_chunk(client, chunk, poll_seconds, max_wait_seconds, req_model, req_offsets,
                                    packs, merged, root, m)
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
