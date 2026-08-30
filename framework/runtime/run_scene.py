#!/usr/bin/env python3
"""
run_scene.py — ORQUESTRADOR DETERMINISTA de UMA cena (tira a orquestracao do chat).

Encadeia o pipeline de 1 cena como um job limitado e resumivel:
  1. context_pack  -> scene_prompt.md + pack.json (contexto O(cena), nao O(historico))
  2. translate     -> model.translate (in-session: espera o translations_<scene_id>.json; api: gera)
  3. build_plan    -> connector/build_plan_chapter.py (valida cobertura/tokens/risk_notes; gera approved)
  4. back-translate-> linhas risco>=high (model.back_translate; REPORTA por padrao, --require-back exige)
  5. verify        -> connector/verify_chapter.py (round-trip byte-identico + ponteiros within-file)
  6. checkpoint    -> artifacts/run_state.json (status por cena) + reconstroi o state_index (TM cresce)

O chat deixa de ser runtime/memoria: o estado vive em run_state.json + artifacts. Crash/parada ->
rode de novo; cada etapa e idempotente e o checkpoint diz onde retomar.

GOVERNANCA: sem work-text. Os scripts do conector sao por-projeto (convencao <projeto>/connector/,
override em project.json connector.{build_plan_script,verify_script}). A unica parte nao-determinista
e a chamada de IA (isolada em model.py). Sob CONGELAMENTO de traducao: nao gera traducao nova; roda
as gates sobre cenas ja traduzidas (dry-run/dogfood).

Uso:  python run_scene.py <dir-do-projeto> <scene> [--backend in-session|api] [--require-back] [--no-verify]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import connector_gate  # noqa: E402  (gate de completude de conector, roda ANTES do kb_gate)
import context_pack  # noqa: E402
import kb_gate  # noqa: E402
import model as M  # noqa: E402
import paths  # noqa: E402  (paths.py: fonte unica do contrato de caminhos de artefato)
import state_index  # noqa: E402
from config import (  # noqa: E402
    CONNECTOR_KNOWN_KEYS,
    CONNECTOR_REGISTRY,
    RunSceneOptions,
    RunSceneResult,
    validate_connector_types,
)
from connector_mgr import (  # noqa: E402
    _connector_hash,
    _connector_script,
    _run,
    _verify_status,
    _warn_if_connector_stale,
)

# Housekeeping/diagnostico (reforco de coesao de codigo: extraido p/ scene_lifecycle.py quando cruzou o limiar de
# leitura) — reimportado aqui p/ rs.clean_failed_scene(...)/etc. continuarem funcionando sem mudar
# nenhum caller (mesmo padrao de re-export usado em model.py/back_translate.py).
from scene_lifecycle import (  # noqa: E402,F401
    _check_stale,
    clean_failed_scene,
    prune_discontinued,
)


def _validate_scene_arg(root: Path, scene: str) -> None:
    """Garante que scene nao resulta em path fora de artifacts/ (path traversal guard)."""
    if not scene:
        raise ValueError("scene nao pode ser vazia")
    resolved = paths.scene_dir(root, scene).resolve()
    if not resolved.is_relative_to(paths.scenes_dir(root).resolve()):
        raise ValueError(f"scene {scene!r} resultaria em path fora de artifacts/scenes/ — bloqueado")


def _validate_connector_cfg(cfg: dict) -> list:
    """Retorna lista de avisos sobre chaves desconhecidas em project.json connector.{}."""
    known = CONNECTOR_KNOWN_KEYS | {s.key for s in CONNECTOR_REGISTRY}
    return [f"connector.{k!r} desconhecida — chaves validas: {sorted(known)}"
            for k in sorted(cfg.get("connector", {})) if k not in known]


def _checkpoint(root: Path, scene: str, patch: dict):
    import time as _time
    p = paths.run_state(root)
    state = {}
    if p.is_file():
        state = json.loads(p.read_text(encoding="utf-8"))
    scenes = state.setdefault("scenes", {})
    # S4: _ts = epoch do último checkpoint desta cena (audit trail temporal)
    scenes[scene] = {**scenes.get(scene, {}), **patch, "_ts": round(_time.time(), 3)}
    state["scenes"] = dict(sorted(scenes.items()))
    state["managed_by"] = "framework/runtime/run_scene.py"
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _ledger_scene_cost(root: Path, scene: str) -> float:
    """Custo-VERDADE da cena = soma de TODAS as chamadas no api_ledger.jsonl (cada retry de cobertura e
    cada escalonamento de fitting), nao so a ultima translate/back. E o numero que casa com o saldo."""
    p = paths.ledger(root)
    if not p.is_file():
        return 0.0
    tot = 0.0
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("scene") == scene:
            tot += r.get("cost_usd", 0.0)
    return round(tot, 5)


def _metrics(root: Path, scene: str, scene_id: str, *, n_lines, tr, bt, n_high, verified):
    """Anexa 1 linha a artifacts/metrics.jsonl: RESUMO por cena (tokens/custo segmentados da ultima
    translate/back, pass-rate). O custo-verdade (`cost_usd`) vem do api_ledger.jsonl — soma TODAS as
    chamadas cobradas da cena (retries + escalonamento), nao so a ultima. O metrics.jsonl segue sendo
    resumo so-de-sucesso; a contabilidade completa (inclusive cenas que falharam) e o ledger."""
    tu = tr.get("usage") if isinstance(tr, dict) else None
    bu = bt.get("usage") if isinstance(bt, dict) else None
    tmodel = tr.get("model", "") if isinstance(tr, dict) else ""
    bmodel = bt.get("model", "") if isinstance(bt, dict) else ""
    # back-translation pass-rate (se houve saida)
    bt_pass = None
    bpath = paths.back_translation(root, scene, scene_id)
    if bpath.is_file():
        try:
            ents = json.loads(bpath.read_text(encoding="utf-8")).get("entries", [])
            if ents:
                bt_pass = sum(1 for e in ents if e.get("verdict") == "pass") / len(ents)
        except Exception:
            pass
    rec = {"scene": scene, "n_lines": n_lines, "n_high": n_high, "verified": verified,
           "reused": tr.get("reused", 0) if isinstance(tr, dict) else 0,
           "translate": {"model": tmodel, "usage": tu, "cost_usd": round(M.cost_of(tmodel, tu or {}), 5)},
           "back": {"model": bmodel, "usage": bu, "cost_usd": round(M.cost_of(bmodel, bu or {}), 5)},
           "back_pass_rate": bt_pass,
           "cost_usd_last": round(M.cost_of(tmodel, tu or {}) + M.cost_of(bmodel, bu or {}), 5)}
    rec["cost_usd"] = _ledger_scene_cost(root, scene)   # VERDADE: soma o ledger (retries + escalonamento)
    p = paths.metrics(root)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def _high_lines(root: Path, scene: str, scene_id: str):
    return M.high_risk_lines(root, scene)               # fonte unica (model.high_risk_lines)


def _pack_and_translate(root: Path, scene: str, scene_id: str, backend: str,
                        pretranslated: bool) -> tuple:
    """FASE 1/2: monta o contexto (context_pack) e obtém a tradução (batch preexistente ou M.translate).

    Retorna (tr, early_return): se early_return não é None, run_scene() deve retorná-lo imediatamente.
    """
    tr: M.TranslateResult | dict | None = None
    if pretranslated:                                       # batch ja produziu o translations_<scene_id>.json
        pack = context_pack.write_pack(root, scene)
        outp = paths.translations(root, scene, scene_id)
        if outp.is_file():
            tr = {"status": M.DONE, "n_lines": pack["n_lines"], "model": M.MODEL_TRANSLATE,
                  "usage": None, "reused": None, "novel": None}
            print("      traducao do batch reaproveitada (sem nova chamada).")
        else:
            print("      batch nao produziu a traducao; traduzindo agora (fallback).")
    if tr is None:
        try:
            tr = M.translate(root, scene, backend=backend)
        except Exception as e:                              # backend api: erro de rede/saida invalida
            print(f"      ERRO na traducao ({backend}): {e}")
            _checkpoint(root, scene, {"scene_id": scene_id, "status": "api_translate_failed"})
            return None, {"status": "api_translate_failed", "scene": scene, "error": str(e)}
    print(f"      glossario/vozes/decisoes/TM montados; status traducao = {tr['status']}")
    if isinstance(tr, dict) and tr.get("reused"):
        tr_done = cast(M.TranslateDone, tr)
        print(f"      dedup: {tr_done['reused']}/{tr_done['n_lines']} linha(s) reaproveitadas da TM "
              f"(nao re-traduzidas; {tr_done.get('novel', 0)} novas ao modelo)")
    _checkpoint(root, scene, {"scene_id": scene_id, "n_lines": tr["n_lines"], "status": "packed"})

    # V2/V3: registra doctrine_hash e prompt_hash no checkpoint — computados direto das fontes
    import hashlib as _hl
    _cp_hash = context_pack._doctrine_hash(root)
    _sp = paths.scene_prompt(root, scene)
    _pr_hash = _hl.sha1(_sp.read_bytes(), usedforsecurity=False).hexdigest()[:16] if _sp.is_file() else ""
    if _cp_hash or _pr_hash:
        _checkpoint(root, scene, {"doctrine_hash": _cp_hash, "prompt_hash": _pr_hash})

    if tr["status"] == M.AWAITING:
        tr = cast(M.TranslateAwaiting, tr)
        print("[2/6] AGUARDANDO traducao (caminho assinatura): responda o prompt limitado")
        print(f"      prompt : {tr['prompt']}")
        print(f"      saida  : {tr['expected_output']}")
        print("      -> rode novamente apos o arquivo aparecer. (checkpoint: 'packed')")
        return None, {"status": "awaiting_translation", "scene": scene}
    print(f"[2/6] traducao presente ({tr['status']}).")
    return tr, None


def _persist_fitting_diagnostics(root: Path, scene: str, scene_id: str) -> None:
    """Na falha final de verify (fitting exaurido OU falha dura), persiste os offsets acima do
    byte_budget em disco — diagnostico backend-agnostico e PASSIVO (so le arquivos ja gravados;
    nao pede nenhum trabalho extra de nenhum backend/modelo)."""
    try:
        over = M.over_budget_offsets(root, scene, tolerance=1.0, detail=True)
    except Exception as e:
        print(f"      AVISO: diagnostico de fitting falhou: {e}")
        return
    if not over:
        return
    print(f"[diag] {len(over)} linha(s) acima do byte_budget -> "
          f"{paths.verify_diagnostics(root, scene, scene_id).name}")
    paths.verify_diagnostics(root, scene, scene_id).write_text(
        json.dumps({"tolerance": 1.0, "over_budget": over}, ensure_ascii=False, indent=2),
        encoding="utf-8")


def _fitting_loop(root: Path, scene: str, scene_id: str, cfg: dict, backend: str,
                  do_verify: bool, tr: M.TranslateResult | dict) -> tuple:
    """FASE 3/5: build_plan + verify com escalonamento de fitting.

    Re-traduz apenas as linhas acima do budget quando a verify falha por fitting (exit 3), escalando
    BUDGET_ESCALATION em sequência. Retorna (tr, verified, early_return): se early_return não é None,
    run_scene() deve retorná-lo imediatamente.
    """
    build_plan_script = _connector_script(root, cfg, "build_plan_script", "build_plan_chapter.py")
    verify_script = _connector_script(root, cfg, "verify_script", "verify_chapter.py")
    _warn_if_connector_stale(root, scene, cfg)   # S3: integridade pre-execução
    # ESCALONAMENTO DE FITTING: budget 1.40 (natural) por padrao; se a verify falha por fitting
    # (out-of-file/residuo) e o backend e AUTOMATIZAVEL (api — chama modelo real, sem intervencao
    # manual), re-traduz mais apertado (BUDGET_ESCALATION) e repete. in-session fica
    # de fora (depende de humano+Claude no chat p/ cada retighten). Cenas normais passam de primeira
    # (sem custo extra); so as apertadas escalam.
    tolerances = [None] + (list(M.BUDGET_ESCALATION) if backend == "api" else [])
    verified = None
    for ti, tol in enumerate(tolerances):
        if ti > 0:
            # CIRURGICO: re-traduzir SO as linhas acima do budget (nao a cena inteira). Numa cena grande
            # com poucos estouros isso troca centenas de re-traducoes por umas poucas (medido: ~$3,4
            # economizados em 2 cenas do cap.13). Fallback p/ cena inteira so se nada estiver acima.
            # ESCALONAMENTO DE MODELO (so backend "api"): pareado por indice com BUDGET_ESCALATION —
            # tol=1.15 (folga maior) tenta o modelo barato; tol=1.0 (residuo que nem 1.15 resolveu,
            # sinal real de dificuldade) escala pro caro.
            model = (M.MODEL_ESCALATION[ti - 1]
                     if backend == "api" and ti - 1 < len(M.MODEL_ESCALATION) else None)
            try:
                over = M.over_budget_offsets(root, scene, tolerance=1.0)
                if over:
                    print(f"[retighten] verify falhou por fitting -> re-traduzindo SO {len(over)} "
                          f"linha(s) acima do budget (tol={tol}, model={model or 'default'}) ...")
                    tr = M.retranslate_offsets(root, scene, over, budget_tolerance=tol, backend=backend,
                                               model=model)
                else:
                    print(f"[retighten] verify falhou por fitting (nenhuma linha acima do budget) -> "
                          f"re-traduzindo a cena (tol={tol}, model={model or 'default'}) ...")
                    tr = M.translate(root, scene, backend=backend, budget_tolerance=tol, model=model)
            except Exception as e:
                print(f"      ERRO na re-traducao ({backend}): {e}")
                _checkpoint(root, scene, {"status": "api_translate_failed"})
                return tr, None, {"status": "api_translate_failed", "scene": scene, "error": str(e)}

        print(f"[3/6] build_plan_chapter {scene} ...")
        code, out = _run([sys.executable, str(build_plan_script), scene])
        print(_indent(out))
        if code != 0:
            _checkpoint(root, scene, {"status": "build_plan_failed"})
            return tr, None, {"status": "build_plan_failed", "scene": scene}
        _checkpoint(root, scene, {"status": "planned"})

        if not do_verify:
            print("[5/6] verify pulado (--no-verify).")
            break
        print(f"[5/6] verify_chapter {scene} (round-trip) ...")
        code, out = _run([sys.executable, str(verify_script), scene])
        print(_indent(out))
        if code == 0:
            verified = True
            _checkpoint(root, scene, {"status": "verified", "verified": True,
                                      "connector_hash": _connector_hash(root, cfg)})
            break
        # PROTOCOLO ESTRUTURADO DE SAIDA: exit-code do conector decide, NAO grep de prosa. exit 3 = falha
        # SO de fitting (escalonavel); 1 = falha dura. Fallback (conector legado sem o exit 3): le a linha
        # VERIFY_STATUS; se nem isso, conservadoramente NAO escala (falha dura). Acabou com o grep fragil
        # que procurava "fora do arquivo" (espacos) — texto real e "fora-do-arquivo" (hifens) -> nunca casava.
        fitting = (code == 3) or _verify_status(out).get("fitting_failure") is True
        if fitting and ti < len(tolerances) - 1:
            print("      verify falhou por FITTING (cena apertada); escalando aperto de budget ...")
            continue
        _persist_fitting_diagnostics(root, scene, scene_id)
        _checkpoint(root, scene, {"status": "verify_failed", "verified": False})
        return tr, None, {"status": "verify_failed", "scene": scene}

    return tr, verified, None


def _back_phase(root: Path, scene: str, scene_id: str, highs: list, backend: str,
                require_back: bool, defer_back: bool, no_back: bool = False) -> tuple:
    """FASE 4/6: back-translation das linhas de alto risco (report-only por padrao).

    Retorna (bt, early_return): se early_return nao e None, run_scene() deve retorna-lo imediatamente.
    No modo defer_back, apenas registra o checkpoint de deferimento; state_index/metrics ficam em run_scene.
    `no_back`: pula a back-translation inteiramente (economia de custo; usuario confia no 1o passe).
    """
    if no_back and require_back:
        print(f"[4/6] AVISO: --no-back ignorado (--require-back tem precedencia) — "
              f"back-translation vai rodar para {len(highs)} linha(s) risco>=high")
    elif no_back:
        print(f"[4/6] back-translation: PULADA (--no-back) para {len(highs)} linha(s) risco>=high")
        _checkpoint(root, scene, {"high": len(highs), "back_skipped": True})
        return {"status": M.DONE, "reviewed": 0, "path": None}, None
    if defer_back:
        print(f"[4/6] back-translation: {len(highs)} linha(s) risco>=high -> DEFERIDA p/ batch do capitulo")
        _checkpoint(root, scene, {"high": len(highs), "back_deferred": True})
        return {"status": M.DONE, "reviewed": 0, "path": None}, None
    print(f"[4/6] back-translation: {len(highs)} linha(s) risco>=high")
    bt: M.BackTranslateResult | dict
    try:
        bt = M.back_translate(root, scene, highs, backend=backend)
    except Exception as e:
        print(f"      AVISO: back-translation falhou ({backend}): {e} — seguindo (report-only).")
        bt = {"status": M.DONE, "reviewed": 0, "path": None}
        if require_back:
            _checkpoint(root, scene, {"status": "back_translation_failed", "high": len(highs)})
            return bt, {"status": "back_translation_failed", "scene": scene, "error": str(e)}
    if bt["status"] == M.AWAITING:
        bt = cast(M.BackTranslateAwaiting, bt)
        msg = f"      AGUARDANDO back-translation: {bt['prompt']}"
        if require_back:
            print(msg + "  (--require-back: bloqueia)")
            _checkpoint(root, scene, {"status": "awaiting_back_translation", "high": len(highs)})
            return bt, {"status": "awaiting_back_translation", "scene": scene}
        print(msg + "  (apenas reportado; use --require-back p/ bloquear)")
    elif bt["status"] == M.READY:
        bt = cast(M.BackTranslateReady, bt)
        print(f"      back-translation presente: {bt['path']}")
    else:
        print(f"      back-translation: {bt.get('reviewed',0)} revisada(s)")
    _checkpoint(root, scene, {"high": len(highs)})
    return bt, None


def run_scene(root, scene, *, backend="api", require_back=False, do_verify=True, skip_kb_gate=False,
              pretranslated=False, defer_back=False, rebuild_index=True, skip_connector_gate=False,
              no_back=False, opts: RunSceneOptions | None = None) -> RunSceneResult:
    if opts is not None:
        backend, require_back, do_verify = opts.backend, opts.require_back, opts.do_verify
        skip_kb_gate, pretranslated, defer_back = opts.skip_kb_gate, opts.pretranslated, opts.defer_back
        rebuild_index = opts.rebuild_index
        skip_connector_gate = opts.skip_connector_gate
        no_back = opts.no_back
    root = Path(root)
    _validate_scene_arg(root, scene)
    cfg = json.loads((root / "project.json").read_text(encoding="utf-8"))
    type_errors = validate_connector_types(cfg)
    if type_errors:
        raise ValueError("project.json connector{} mal configurado:\n" +
                          "\n".join(f"  - {e}" for e in type_errors))
    for w in _validate_connector_cfg(cfg):
        print(f"[cfg] AVISO: {w}")
    scene_id = context_pack.scene_id_of(scene)
    bypassed: list = []   # #79: rastro de todo gate soft ignorado via --skip-* — nunca invisivel no checkpoint

    # GATE DE COMPLETUDE DE CONECTOR: roda ANTES do kb_gate -- sem conector completo (scripts
    # existentes + ao menos 1 round-trip verde ja registrado), uma KB reconciliada nao serve de nada.
    cg = connector_gate.check(root)
    for w in cg["warnings"]:
        print(f"[connector] aviso: {w}")
    if cg["hard_problems"]:
        print(f"[0/6] BLOQUEADO (conector, hard) — {len(cg['hard_problems'])} problema(s) sem bypass possivel:")
        for p in cg["hard_problems"]:
            print(f"      - {p}")
        _checkpoint(root, scene, {"scene_id": scene_id, "status": "connector_incomplete"})
        return {"status": "connector_incomplete", "scene": scene, "problems": cg["hard_problems"]}
    if cg["problems"]:
        if not skip_connector_gate:
            print(f"[0/6] BLOQUEADO por completude de conector ({len(cg['problems'])}):")
            for p in cg["problems"]:
                print(f"      - {p}")
            print("      -> rode build_plan+verify de 1 cena manualmente, ou use --skip-connector-gate p/ ignorar (nao recomendado).")
            _checkpoint(root, scene, {"scene_id": scene_id, "status": "connector_incomplete"})
            return {"status": "connector_incomplete", "scene": scene, "problems": cg["problems"]}
        bypassed.append("connector")

    # GATE DE COBERTURA DE KB (cabeia a doutrina: pesquisa reconciliada ANTES de traduzir)
    kb = kb_gate.check(root, scene)
    for w in kb["warnings"]:
        print(f"[kb] aviso: {w}")
    # hard_problems: nunca bypassavel (nem com --skip-kb-gate)
    if kb.get("hard_problems"):
        print(f"[0/6] BLOQUEADO (hard) — {len(kb['hard_problems'])} problema(s) sem bypass possivel:")
        for p in kb["hard_problems"]:
            print(f"      - {p}")
        _checkpoint(root, scene, {"scene_id": scene_id, "status": "kb_coverage_failed"})
        return {"status": "kb_coverage_failed", "scene": scene, "problems": kb["hard_problems"]}
    if kb["problems"]:
        if not skip_kb_gate:
            print(f"[0/6] BLOQUEADO por cobertura de KB ({len(kb['problems'])}):")
            for p in kb["problems"]:
                print(f"      - {p}")
            print("      -> rode a Fase 0 (skill 03) ou use --skip-kb-gate p/ ignorar (nao recomendado).")
            _checkpoint(root, scene, {"scene_id": scene_id, "status": "kb_coverage_failed"})
            return {"status": "kb_coverage_failed", "scene": scene, "problems": kb["problems"]}
        bypassed.append("kb")

    # Decisoes pendentes: sempre exibidas ao usuario antes de traduzir (nao bloqueia, mas obrigatorio)
    if kb.get("pending_decisions"):
        pd = kb["pending_decisions"]
        print(f"[kb] DECISOES PENDENTES ({len(pd)}) — requerem revisao humana antes do merge final:")
        for i, d in enumerate(pd, 1):
            print(f"      {i}. {d}")

    print(f"[1/6] context_pack {scene} ...")
    tr, early = _pack_and_translate(root, scene, scene_id, backend, pretranslated)
    if early is not None:
        return early

    # [3+5] build_plan + verify com escalonamento de fitting (ver _fitting_loop)
    tr, verified, early = _fitting_loop(root, scene, scene_id, cfg, backend, do_verify, tr)
    if early is not None:
        return early

    # [4/6] back-translation (apos fitting OK; report-only; roda 1x — nao re-roda no escalonamento)
    highs = _high_lines(root, scene, scene_id)
    bt, early = _back_phase(root, scene, scene_id, highs, backend, require_back, defer_back, no_back)
    if early is not None:
        return early

    if rebuild_index:
        print("[6/6] reconstruindo state_index (TM cresce com esta cena) ...")
        # sync_db=False: o checkpoint por-cena reconstroi os indices flat (barato), mas NAO espelha
        # o corpus inteiro no DB a cada cena. O mirror roda no rebuild deliberado (CLI state_index).
        si = state_index.build(root, sync_db=False)
        print(f"      TM: {si['tm']} entradas | cards: {si['cards']} | decisoes: {si['decisions']}")
        for w in si.get("warnings", []):
            print(f"      [state_index] AVISO: {w}")
    else:
        # BATCH: o rebuild por-cena e redundante (a rodada de traducao ja terminou; TM so importa
        # pra proxima cena/capitulo) -- run_chapter faz 1 rebuild p/ o capitulo inteiro apos o loop.
        print("[6/6] state_index: rebuild deferido p/ pos-capitulo (modo batch).")
    _checkpoint(root, scene, {"status": "verified" if verified else "planned", "bypassed_gates": bypassed})
    mr = _metrics(root, scene, scene_id, n_lines=tr.get("n_lines"), tr=tr, bt=bt,
                  n_high=len(highs), verified=bool(verified))
    cost_note = "(back-translation deferida p/ batch)" if defer_back else f"| back_pass_rate={mr['back_pass_rate']}"
    print(f"      metrics: custo ~${mr['cost_usd']:.4f} {cost_note}")
    print(f"OK run_scene {scene}: status final = {'verified' if verified else 'planned'}")
    return {"status": "verified" if verified else "planned", "scene": scene,
            "high": len(highs), "verified": verified}


def _indent(s: str) -> str:
    return "\n".join("      " + ln for ln in s.strip().splitlines() if ln.strip())


def main():
    ap = argparse.ArgumentParser(description="Orquestrador determinista de 1 cena.")
    ap.add_argument("project")
    ap.add_argument("scene", nargs="?", default=None)
    ap.add_argument("--backend", default="api", choices=["in-session", "api"])
    ap.add_argument("--require-back", action="store_true",
                    help="bloqueia se a back-translation de alto risco faltar")
    ap.add_argument("--no-verify", action="store_true", help="pula o round-trip (verify_chapter)")
    ap.add_argument("--skip-kb-gate", action="store_true",
                    help="ignora o gate de cobertura de KB (nao recomendado)")
    ap.add_argument("--skip-connector-gate", action="store_true",
                    help="ignora o gate de completude de conector (nao recomendado)")
    ap.add_argument("--no-back", action="store_true",
                    help="pula a back-translation (Opus) inteiramente (economia de custo)")
    ap.add_argument("--clean", action="store_true",
                    help="remove artefatos de run anterior antes de rodar (retry limpo)")
    ap.add_argument("--check-stale", action="store_true",
                    help="V3: lista cenas com doctrine_hash diferente do atual (sem rodar traducao)")
    ap.add_argument("--purge-discontinued", type=int, metavar="DAYS",
                    help="G4: remove dirs de artifacts/discontinued/ mais antigos que DAYS dias")
    a = ap.parse_args()
    if a.check_stale:
        if not a.project:
            ap.error("--check-stale requer <project>")
        _check_stale(a.project)
        return
    if a.purge_discontinued is not None:
        removed = prune_discontinued(Path(a.project), a.purge_discontinued)
        print(f"[prune] {len(removed)} dir(s) removido(s) de discontinued/.")
        return
    if not a.scene:
        ap.error("scene e obrigatorio (exceto com --check-stale)")
    if a.clean:
        removed = clean_failed_scene(a.project, a.scene)
        print(f"[clean] {len(removed)} artefato(s) removido(s).")
    r = run_scene(a.project, a.scene, backend=a.backend, require_back=a.require_back,
                  do_verify=not a.no_verify, skip_kb_gate=a.skip_kb_gate,
                  skip_connector_gate=a.skip_connector_gate, no_back=a.no_back)
    sys.exit(0 if r["status"] in ("verified", "planned", "awaiting_translation",
                                  "awaiting_back_translation") else 1)


if __name__ == "__main__":
    main()
