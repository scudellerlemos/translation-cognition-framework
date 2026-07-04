#!/usr/bin/env python3
"""
run_chapter.py — DRIVER de capitulo (tira o loop de cenas do chat).

Roda todas as cenas de um capitulo como jobs stateless, em sequencia, via run_scene. Cada cena e uma
requisicao isolada (backend api -> 1 chamada HTTP por cena); o chat so LANCA este driver e LE o resumo,
entao o footprint de sessao e constante, independente do nº de cenas/capitulos.

Propriedades:
  - RESUMIVEL: pula cenas ja `verified` em run_state.json (a menos de --redo).
  - PARA NA 1ª FALHA: build_plan/verify/api falhou -> interrompe e reporta (nao mascara erro).
  - Determinista: descobre as cenas por glob de artifacts/scenes/ch_<cap>_*/dialogs.csv (ordem por scene_id).
  - Reusa run_scene + state_index; nada de logica de IA aqui.

Uso:  python run_chapter.py <projeto> <cap> [--backend api|in-session] [--require-back] [--redo] [--no-verify]
      <cap> = "12" roda ch_12_01, ch_12_02, ... na ordem.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import connector_gate  # noqa: E402  (gate de completude de conector, roda ANTES do kb_gate)
import context_pack  # noqa: E402
import cost_report  # noqa: E402
import kb_gate  # noqa: E402
import model as M  # noqa: E402
import paths  # noqa: E402  (paths.py: fonte unica do contrato de caminhos de artefato)
import quality_gate  # noqa: E402  (piso de qualidade obrigatorio: verdicts de back-translation)
import quality_review  # noqa: E402  (QA obrigatorio: export do XLSX de revisao humana ao fim do cap.)
import run_scene as RS  # noqa: E402
import spoiler_check  # noqa: E402  (auditoria obrigatoria de spoiler/genero ao fim do cap.)
import state_index  # noqa: E402  (rebuild 1x/capitulo em modo batch, ver _rebuild_index_phase)

_OK = ("verified", "planned")          # estados que permitem seguir p/ a proxima cena
_DONE = ("verified",)                  # estados que contam como "ja feito" (skip em modo resumivel)

# PREVISIBILIDADE — estimativa pre-voo: custo esperado ANTES de gastar, derivado do nº de linhas.
# Faixa medida (batch -50% + back-translation; com recuperacao-por-linha do model._api_translate):
# ~$0.0007 (otimista, muito reuso de TM) a ~$0.0014 (pessimista, pouco reuso) por linha. O reuso de TM
# (dedup) puxa o real p/ BAIXO -> trate o topo como teto-ish, nao piso. Game-agnostico.
_USD_PER_LINE_LO = 0.0007
_USD_PER_LINE_HI = 0.0014


def _count_lines(root: Path, scenes) -> int:
    """Soma as linhas (dialogs.csv) das cenas dadas — base da estimativa de custo."""
    import csv
    n = 0
    for s in scenes:
        d = paths.artifacts(root) / "scenes" / s / "dialogs.csv"   # cenas vivem em artifacts/scenes/
        if d.is_file():
            with d.open(encoding="utf-8") as f:
                n += sum(1 for _ in csv.DictReader(f))
    return n


def _estimate(root: Path, scenes) -> dict:
    n = _count_lines(root, scenes)
    return {"lines": n, "lo": n * _USD_PER_LINE_LO, "hi": n * _USD_PER_LINE_HI}


def _fit_budget(root: Path, scenes, max_usd):
    """Subconjunto de `scenes` (preservando a ordem) cujo custo estimado PESSIMISTA acumulado cabe em
    max_usd, + as que sobraram. Usa _USD_PER_LINE_HI -> garante TETO: mesmo no pior caso o trabalho
    comprometido fica <= max_usd (o reuso de TM so melhora). max_usd None -> tudo cabe (sem teto)."""
    if max_usd is None:
        return list(scenes), []
    fit, dropped, acc = [], [], 0.0
    for s in scenes:
        c = _count_lines(root, [s]) * _USD_PER_LINE_HI
        if acc + c <= max_usd:
            fit.append(s)
            acc += c
        else:
            dropped.append(s)
    return fit, dropped


def _validate_chapter_arg(root: Path, chap: str) -> None:
    """Garante que chap nao resulta em path fora de artifacts/ (path traversal guard).

    O chap e interpolado como 'ch_{chap}_*' no glob. Separadores de path (/ ou barra-invertida)
    inserem segmentos '..' navegaveis pelo glob e causam traversal. Bloqueamos na raiz:
    qualquer separador no chap e proibido antes de qualquer I/O.
    """
    if not chap:
        raise ValueError("chapter nao pode ser vazio")
    if "/" in chap or "\\" in chap:
        raise ValueError(f"chapter {chap!r} contem separador de path — bloqueado")
    # defesa adicional: verifica que o path composto nao escapa de artifacts/
    candidate = (paths.artifacts(root) / f"ch_{chap}_00").resolve()
    if not candidate.is_relative_to(paths.artifacts(root).resolve()):
        raise ValueError(f"chapter {chap!r} resultaria em path fora de artifacts/ — bloqueado")


def _scenes_of(root: Path, chap: str) -> list[str]:
    art = paths.artifacts(root)
    names = [p.parent.name for p in (art / "scenes").glob(f"ch_{chap}_*/dialogs.csv")]
    return sorted(set(names), key=context_pack.scene_id_of)


def _scenes_of_glob(root: Path, globs: str) -> list[str]:
    """Discovery via glob(s) customizados (ex: 'AREAD*,AREAS*') para projetos com estrutura flat.
    Aceita multiplos padroes separados por virgula. Alternativa a ch_<chap>_* do Utawarerumono."""
    art = paths.artifacts(root)
    names: set[str] = set()
    for pat in globs.split(","):
        pat = pat.strip()
        if pat:
            for p in (art / "scenes").glob(f"{pat}/dialogs.csv"):
                names.add(p.parent.name)
    return sorted(names)


def _verified(root: Path, scene: str) -> bool:
    p = paths.run_state(root)
    if not p.is_file():
        return False
    st = json.loads(p.read_text(encoding="utf-8")).get("scenes", {}).get(scene, {})
    return st.get("status") in _DONE and st.get("verified") is True


def _batch_phase(root, pending, *, skip_kb_gate):
    """FASE 1 do modo batch: submete as cenas pendentes (que passam o KB-gate) num unico batch (50% off,
    Carta cacheada compartilhada). Retorna {scene: status} do batch_translate. Cenas KB-bloqueadas ou
    que falham cobertura caem p/ o caminho interativo na fase 2 (run_scene normal). Best-effort: se o
    batch em si falhar (rede), retorna {} e tudo vira caminho interativo."""
    submit = []
    for s in pending:
        kb = kb_gate.check(root, s)
        if kb["problems"] and not skip_kb_gate:
            print(f"[batch] {s} pulado do batch (KB-gate): {kb['problems'][0]}")
            continue
        submit.append(s)
    if not submit:
        return {}
    print(f"[batch] submetendo {len(submit)} cena(s) em 1 batch (50% off; pode levar minutos) ...")
    try:
        st = M.batch_translate(root, submit)
    except Exception as e:
        print(f"[batch] falhou ({e}) -> caindo p/ caminho interativo em todas as cenas.")
        return {}
    for s in submit:
        print(f"[batch] {s}: {st.get(s, '?')}")
    return st


def _rebuild_index_phase(root):
    """POS-PASSE do modo batch: 1 rebuild de state_index cobrindo o capitulo INTEIRO, em vez de 1
    por cena (redundante no batch -- roda depois que todas as cenas ja fecharam translation_plan,
    entao ja reflete tudo de uma vez). Barato/idempotente mesmo sem cena nova verified."""
    si = state_index.build(root, sync_db=False)
    print(f"\n[state_index] TM: {si['tm']} entradas | cards: {si['cards']} | decisoes: {si['decisions']}")
    for w in si.get("warnings", []):
        print(f"      [state_index] AVISO: {w}")


def _back_batch_phase(root, scenes):
    """POS-PASSE do modo batch: back-translation de todas as cenas verificadas num UNICO batch (-50%
    Opus). Roda DEPOIS do loop (cada cena ja produziu seu translation_plan); report-only (nao bloqueia).
    Resume idempotente dentro do batch_back_translate (cena ja revisada nao re-cobra)."""
    if not scenes:
        return
    print(f"\n[back-batch] back-translation de {len(scenes)} cena(s) em 1 batch (50% off, Opus) ...")
    try:
        st = M.batch_back_translate(root, scenes)
    except Exception as e:
        print(f"[back-batch] falhou ({e}) — back-translation segue pendente (report-only, nao bloqueia).")
        return
    rev = sum(1 for v in st.values() if v == "reviewed")
    noh = sum(1 for v in st.values() if v == "no_high")
    print(f"[back-batch] {rev} revisada(s), {noh} sem alto risco; detalhe: "
          f"{ {s: v for s, v in st.items() if v not in ('no_high',)} }")


def _chapter_cost(root, chap) -> float:
    """Gasto REAL ja contabilizado neste capitulo (delta do ledger, so cenas ch_<chap>_*)."""
    try:
        return cost_report.report(root, chapter=chap).get("total_usd", 0.0)
    except Exception:
        return 0.0


def run_chapter(root, chap, *, backend="api", require_back=False, redo=False, do_verify=True,
                skip_kb_gate=False, batch=False, max_usd=None, scenes_glob=None,
                skip_connector_gate=False, no_back=False):
    root = Path(root)
    # GATE DE COMPLETUDE DE CONECTOR: checa 1x pro CAPITULO INTEIRO (completude de conector nao
    # depende de cena) -- ANTES de qualquer descoberta/estimativa. Sem conector, nada aqui tem sentido.
    cg = connector_gate.check(root)
    for w in cg["warnings"]:
        print(f"[connector] aviso: {w}")
    if cg["hard_problems"] or (cg["problems"] and not skip_connector_gate):
        blockers = cg["hard_problems"] + (cg["problems"] if not skip_connector_gate else [])
        print(f"BLOQUEADO por completude de conector ({len(blockers)}):")
        for p in blockers:
            print(f"  - {p}")
        if cg["problems"] and not cg["hard_problems"]:
            print("  -> use --skip-connector-gate p/ ignorar (nao recomendado).")
        return {"chapter": chap, "scenes": [], "status": "connector_incomplete"}
    if scenes_glob:
        scenes = _scenes_of_glob(root, scenes_glob)
        cost_chap = None   # sem filtro ch_* — reporta ledger completo do projeto
    else:
        _validate_chapter_arg(root, chap)
        scenes = _scenes_of(root, chap)
        cost_chap = chap
    if not scenes:
        hint = f"artifacts/scenes/<glob>/dialogs.csv (glob: {scenes_glob})" if scenes_glob else f"artifacts/scenes/ch_{chap}_*/dialogs.csv"
        print(f"nenhuma cena encontrada p/ {chap} (esperado {hint})")
        return {"chapter": chap, "scenes": [], "status": "empty"}
    print(f"capitulo {chap}: {len(scenes)} cena(s) -> {', '.join(scenes)}"
          + (f" | teto de gasto: ${max_usd:.2f}" if max_usd is not None else ""))

    # PREVISIBILIDADE: estima o custo das cenas PENDENTES (nao-verified) ANTES de gastar 1 centavo.
    pend_est = [s for s in scenes if redo or not _verified(root, s)]
    est = _estimate(root, pend_est)
    print(f"estimativa pre-voo: {est['lines']} linha(s) pendente(s) -> ~${est['lo']:.2f}-${est['hi']:.2f}"
          f" (reuso de TM puxa p/ baixo)"
          + (f" | teto --max-usd ${max_usd:.2f}" if max_usd is not None else ""))

    # TETO DURO PREVISIVEL: comete ao batch SO as cenas cujo custo pessimista acumulado cabe no teto;
    # as que nao cabem sao ADIADAS (skipped_budget), nunca traduzidas caro no interativo. Sem gasto-
    # surpresa: o trabalho iniciado tem custo de pior-caso <= max_usd. Resto resumivel apos recarga.
    affordable, budget_excluded = _fit_budget(root, pend_est, max_usd)
    budget_excluded = set(budget_excluded)
    if budget_excluded:
        print(f"[teto ${max_usd:.2f}] {len(budget_excluded)} cena(s) adiada(s) por orcamento "
              f"(resumiveis apos recarga): {', '.join(sorted(budget_excluded, key=context_pack.scene_id_of))}")
    if max_usd is not None and not affordable and pend_est:
        print(f"\nABORTADO ANTES DE GASTAR: nem a 1a cena pendente cabe em --max-usd ${max_usd:.2f} "
              f"(estimativa ~${est['lo']:.2f}-${est['hi']:.2f}). Aumente o teto ou recarregue. Nada foi gasto.")
        return {"chapter": chap, "scenes": [], "status": "stopped_budget_preflight"}

    # MODO BATCH: traduz as pendentes QUE CABEM num batch (fase 1); a fase 2 so finaliza (build_plan/verify).
    batch_status = {}
    if batch and backend == "api":
        pending = [s for s in scenes if (redo or not _verified(root, s)) and s not in budget_excluded]
        if pending:
            batch_status = _batch_phase(root, pending, skip_kb_gate=skip_kb_gate)

    results = []
    for scene in scenes:
        if not redo and _verified(root, scene):
            print(f"[skip] {scene} ja verified")
            results.append({"scene": scene, "status": "skipped"})
            continue
        if scene in budget_excluded:                  # adiada no pre-voo por orcamento — nao gasta
            print(f"[teto] {scene} adiada por orcamento (rode de novo apos recarga)")
            results.append({"scene": scene, "status": "skipped_budget"})
            continue
        # TETO DE GASTO: checa o custo do capitulo ANTES de cada cena (a granularidade e por-cena —
        # uma cena ja iniciada pode estourar um pouco; o teto barra a PROXIMA). Cenas verified ja
        # salvas; rode de novo p/ continuar de onde parou.
        if max_usd is not None:
            spent = _chapter_cost(root, cost_chap)
            if spent >= max_usd:
                print(f"\nABORTADO por teto de gasto: {chap} ja custou ${spent:.2f} >= "
                      f"--max-usd ${max_usd:.2f} (parado ANTES de {scene}; cenas verified seguem "
                      f"salvas — rode de novo p/ continuar).")
                _print_cost(root, cost_chap)
                return {"chapter": chap, "scenes": results, "status": "stopped_budget",
                        "stopped_at": scene}
        pre = batch_status.get(scene) in ("written", "all_reused")
        # MODO BATCH: difere a back-translation p/ o pos-passe (1 batch -50% Opus ao fim do capitulo)
        # E o rebuild do state_index (1x pro capitulo inteiro em _rebuild_index_phase, nao por cena
        # -- redundante no batch, a rodada de traducao ja terminou antes do rebuild ser util).
        defer_back = bool(batch and backend == "api")
        rebuild_index = not defer_back
        print(f"\n=== {scene} ({backend}{', batch' if pre else ''}) ===")
        r = RS.run_scene(root, scene, backend=backend, require_back=require_back,
                         do_verify=do_verify, skip_kb_gate=skip_kb_gate, pretranslated=pre,
                         defer_back=defer_back, rebuild_index=rebuild_index,
                         skip_connector_gate=skip_connector_gate, no_back=no_back)
        results.append({"scene": scene, "status": r["status"]})
        if r["status"] not in _OK:
            print(f"\nPAROU em {scene}: status = {r['status']} "
                  f"(corrija e rode de novo; cenas verified serao puladas)")
            _print_cost(root, cost_chap)
            return {"chapter": chap, "scenes": results, "status": "stopped", "stopped_at": scene}
    # POS-PASSE: back-translation em batch (-50% Opus) + rebuild do state_index, 1x pro capitulo
    # inteiro, se modo batch (cada cena deferiu os dois pra cá — ver rebuild_index/defer_back acima).
    if batch and backend == "api":
        _rebuild_index_phase(root)
        if no_back:
            print("[back-batch] pulado (--no-back).")
        elif max_usd is not None and _chapter_cost(root, cost_chap) >= max_usd:
            print(f"[back-batch] pulado: teto de gasto atingido "
                  f"(${_chapter_cost(root, cost_chap):.2f} >= ${max_usd:.2f}).")
        else:
            _back_batch_phase(root, [s for s in scenes if _verified(root, s)])
    done = sum(1 for x in results if x["status"] in ("verified", "skipped"))
    print(f"\nOK {chap}: {done}/{len(scenes)} cena(s) prontas."
          + (f" ({len(budget_excluded)} adiada(s) por orcamento — rode de novo apos recarga)"
             if budget_excluded else ""))
    _print_cost(root, cost_chap)
    _export_qa(root, cost_chap)   # QA OBRIGATORIO: gera o XLSX de revisao humana SEMPRE (piso de qualidade)
    _audit_spoiler(root)          # AUDITORIA OBRIGATORIA: spoiler de nome/titulo + genero pt-BR, projeto inteiro
    _audit_quality(root, cost_chap)  # OBRIGATORIO: piso de qualidade (verdicts de back-translation)
    # parcial-por-orcamento NAO e "complete" (honestidade do status); mas tb nao e erro de pipeline.
    status = "stopped_budget" if budget_excluded else "complete"
    return {"chapter": chap, "scenes": results, "status": status}


def _export_qa(root: Path, chap: str):
    """OBRIGATORIO: ao fim do capitulo, disponibiliza o XLSX de revisao HUMANA no outbox — SEMPRE, mesmo
    que a IA nao tenha marcado nada (o piso de qualidade e o humano ler). Best-effort: nao derruba um
    capitulo ja traduzido se o export falhar (ex.: openpyxl ausente) — so avisa em alto e bom som."""
    try:
        rows = quality_review.export(root, chap)
        outbox = paths.qa_outbox(root)
        outbox.mkdir(parents=True, exist_ok=True)
        paths.qa_inbox(root).mkdir(parents=True, exist_ok=True)
        out = outbox / f"review_cap_{chap}.xlsx"
        quality_review.write_xlsx(rows, str(out))
        marked = sum(1 for r in rows if r.get("revisar"))
        print(f"[QA obrigatorio] revisao humana disponibilizada: {out}")
        print(f"                 {len(rows)} linha(s), {marked} marcada(s) p/ ler. Devolva preenchido em "
              f"{paths.qa_inbox(root)} e rode: quality_review.py apply <projeto>")
    except Exception as e:
        print(f"[QA obrigatorio] AVISO: falha ao gerar o XLSX de revisao ({e}). "
              f"Gere a mao: python quality_review.py export <projeto> {chap}")


def _audit_spoiler(root: Path):
    """OBRIGATORIO: audita vazamento de NOME/TITULO pos-reveal (alta confianca, determinista) e de
    GENERO pt-BR (heuristica, pode ter falso-positivo) sobre o PROJETO INTEIRO -- sempre, mesmo que o
    capitulo atual nao tenha nada marcado no ledger. Nunca bloqueia o capitulo (report-only, mesma
    filosofia do QA); a garantia e a auditoria RODAR e o resultado FICAR em artifacts/spoiler_audit.json
    (nao se perder no scroll do terminal nem depender de alguem lembrar de rodar o CLI a mao)."""
    try:
        rep = spoiler_check.audit_and_persist(root)
    except Exception as e:
        print(f"[spoiler-audit obrigatorio] AVISO: falha ao auditar ({e}).")
        return
    if rep["name_leaks"]:
        print(f"[spoiler-audit] ALERTA: {len(rep['name_leaks'])} vazamento(s) de NOME/TITULO "
              f"pos-reveal -- ver {paths.spoiler_audit(root)}")
    if rep["gender_flags"]:
        print(f"[spoiler-audit] {len(rep['gender_flags'])} linha(s) a revisar por GENERO pt-BR "
              f"(heuristico, pode ter falso-positivo) -- ver {paths.spoiler_audit(root)}")
    if rep["clean"]:
        print("[spoiler-audit] OK: nenhum vazamento nem marcador de genero suspeito.")


def _audit_quality(root: Path, chap: str | None):
    """OBRIGATORIO: torna o veredito da back-translation OBSERVAVEL (mesma logica ja aplicada ao
    spoiler_check) -- sem isso, uma linha high/critical marcada 'revise' pelo modelo passava
    silenciosa. Report-only (nunca bloqueia o capitulo); chap=None varre o projeto inteiro."""
    try:
        r = quality_gate.check(root, chap)
    except Exception as e:
        print(f"[quality-gate obrigatorio] AVISO: falha ao auditar ({e}).")
        return
    if r["revise"]:
        print(f"[quality-gate] ALERTA: {len(r['revise'])} linha(s) high/critical com verdict "
              f"'revise' (o modelo apontou divergencia) -- rode quality_gate.py p/ detalhe.")
    if r["uncovered"]:
        print(f"[quality-gate] {len(r['uncovered'])} linha(s) high/critical sem cobertura de "
              f"back-translation -- rode quality_gate.py p/ detalhe.")
    if not r["revise"] and not r["uncovered"]:
        print("[quality-gate] OK: nenhuma linha high/critical com verdict 'revise' nem sem cobertura.")


def _print_cost(root: Path, chap: str | None = None):
    """Resumo de gasto REAL (api_ledger.jsonl) ao fim do capitulo — protege o saldo (toda chamada
    cobrada conta, inclusive cenas que falharam/escalaram, nao so as que o metrics.jsonl registrou).
    Mostra o DELTA do capitulo (so cenas ch_<chap>_*), nao o acumulado de todo o ledger."""
    try:
        rep = cost_report.report(root, chapter=chap)
        if rep["n_calls"]:
            print(f"\n{cost_report._fmt(rep, by_scene=False)}")
    except Exception:
        pass


def main():
    ap = argparse.ArgumentParser(description="Driver determinista de capitulo (loop de cenas).")
    ap.add_argument("project")
    ap.add_argument("chapter", help='prefixo do capitulo, ex.: "12"')
    ap.add_argument("--backend", default="api", choices=["in-session", "api"])
    ap.add_argument("--require-back", action="store_true")
    ap.add_argument("--redo", action="store_true", help="reprocessa mesmo cenas ja verified")
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--skip-kb-gate", action="store_true", help="ignora o gate de cobertura de KB")
    ap.add_argument("--skip-connector-gate", action="store_true",
                    help="ignora o gate de completude de conector (nao recomendado)")
    ap.add_argument("--batch", action="store_true",
                    help="traduz todas as cenas pendentes num unico batch (50%% off, assincrono)")
    ap.add_argument("--max-usd", type=float, default=None,
                    help="teto de gasto: aborta antes da proxima cena se o custo do capitulo passar deste "
                         "valor (cenas verified seguem salvas; rode de novo p/ continuar)")
    ap.add_argument("--scenes-glob", default=None,
                    help="glob(s) customizados para projetos com estrutura flat (ex: 'AREAD*,AREAS*'). "
                         "Substitui o padrao ch_<chapter>_*. <chapter> vira so um rotulo de display.")
    ap.add_argument("--no-back", action="store_true",
                    help="pula a back-translation (Opus) inteiramente (economia de custo)")
    a = ap.parse_args()
    r = run_chapter(a.project, a.chapter, backend=a.backend, require_back=a.require_back,
                    redo=a.redo, do_verify=not a.no_verify, skip_kb_gate=a.skip_kb_gate, batch=a.batch,
                    max_usd=a.max_usd, scenes_glob=a.scenes_glob,
                    skip_connector_gate=a.skip_connector_gate, no_back=a.no_back)
    sys.exit(0 if r["status"] in ("complete", "empty") else 1)


if __name__ == "__main__":
    main()
