#!/usr/bin/env python3
"""
kb_gate.py — GATE DE COBERTURA DE CONHECIMENTO (cabeia a doutrina no runtime).

A doutrina (skills 01-04 + invariante #9 do _index) exige KB reconciliada ANTES de traduzir. O harness
de escala consumia os artefatos sem exigir isso -> arco novo podia ser traduzido "as cegas". Este gate
fecha a lacuna: o run_scene chama check() ANTES de traduzir e bloqueia se a cobertura falhar.

Checagens (deterministas, sem rede):
  HARD (bloqueiam):
    - research_log.md existe e tem `status: reconciled` (pesquisa IA+humano conciliada).
    - artefatos de KB presentes e nao-vazios: glossary.csv, universe_knowledge_base.md, voice_cards.json.
  FRONTEIRA (bloqueia se declarada): project.json `kb_frontier` = scene_id max coberto pela pesquisa
    (ex.: "12_17"). Cena alem disso -> a KB nao cobre este ponto narrativo -> rode a Fase 0 ate aqui.
    Se `kb_frontier` nao for declarado, a fronteira do research_log e so REPORTADA (warning), nao bloqueia.
  PROFUNDIDADE (soft, reforco de coesao de codigo): 'reconciled' sozinho e so um marcador -- toda entidade com
    conteudo afirmado (nao-UNSOURCED) no universe_knowledge_base.md precisa de ratificacao humana
    em kb_ratified.csv (mesmo mecanismo que kb_reconcile.py ja usa pro caminho draft_ollama, aqui
    generalizado pro caminho manual/skill-03). Bypassavel via --skip-kb-gate como qualquer problem.

Uso (CLI):  python kb_gate.py <projeto> <scene>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import paths  # noqa: E402  (paths.py: fonte unica do contrato de caminhos de artefato)

# Artefatos de KB: hard = NUNCA bypassavel (nem com --skip-kb-gate); skip = bypassavel
_KB_HARD = ("universe_knowledge_base.md",)
_KB_ARTIFACTS = ("glossary.csv",)


def _pos(scene_id: str):
    """scene_id '12_03' -> (12, 3) p/ comparacao numerica robusta (evita pegadinha lexicografica 9 vs 12)."""
    return tuple(int(p) for p in str(scene_id).split("_") if p.isdigit())


def _parse_pending_decisions(txt: str) -> list[str]:
    """Extrai itens numerados da secao 'Decisoes pendentes' do research_log.md."""
    # Localiza a secao pelo heading (tolerante a acentos e parenteticos)
    m = re.search(r"^#{1,4}\s+Decis[oõ]es? pendentes[^\n]*$", txt, re.I | re.M)
    if not m:
        return []
    block = txt[m.end():]
    # Corta no proximo heading de mesmo nivel ou superior
    next_head = re.search(r"^#{1,4}\s", block, re.M)
    if next_head:
        block = block[: next_head.start()]
    items = []
    for line in block.splitlines():
        # Linha numerada: "1. **texto**" ou "1. texto"
        lm = re.match(r"^\s*\d+\.\s+(.+)", line)
        if lm:
            # Remove marcadores de negrito e limpa espacos
            item = re.sub(r"\*+", "", lm.group(1)).strip()
            items.append(item)
    return items


def check(root, scene) -> dict:
    """Retorna {hard_problems: [...], problems: [...], warnings: [...], pending_decisions: [...]}.
    hard_problems != []    => bloquear sempre (nao bypassavel).
    problems != []         => bloquear salvo --skip-kb-gate.
    pending_decisions != [] => sempre exibido ao usuario (nao bloqueia, mas obrigatorio informar).
    """
    root = Path(root)
    art = paths.artifacts(root)
    hard_problems, problems, warnings = [], [], []

    # universe_knowledge_base.md: HARD — nao passa nem com --skip-kb-gate
    for name in _KB_HARD:
        f = art / name
        if not f.is_file() or not f.read_text(encoding="utf-8").strip():
            hard_problems.append(
                f"{name} ausente/vazio — sintetize a KB (skill 03/04) antes de traduzir. "
                f"Este gate nao pode ser pulado."
            )

    pending_decisions: list[str] = []
    rl = art / "research_log.md"
    if not rl.is_file():
        problems.append("research_log.md ausente — rode a Fase 0 (skill 03, pesquisa IA+humano).")
    else:
        txt = rl.read_text(encoding="utf-8")
        # tolera markdown: "**Status:** reconciled", "status : reconciled", etc.
        if not re.search(r"status[:*\s]+reconciled", txt, re.I):
            problems.append("research_log.md sem 'status: reconciled' — reconcilie a pesquisa IA+humano.")
        else:
            if re.search(r"human_input\s*:\s*pending", txt, re.I):
                warnings.append("research_log.md: status=reconciled mas human_input=pending — "
                                "atualize para 'confirmed' ou 'declined' (proveniência incompleta).")
            # PROFUNDIDADE DA FASE 0 (reforco de coesao de codigo — generalizado do kb_reconcile.py, que so cobria
            # o caminho draft_ollama do kb_build_ollama.py): 'reconciled' sozinho e so um MARCADOR,
            # nao garante que a reconciliacao teve profundidade de verdade. Exige tambem ratificacao
            # humana por entidade (kb_ratified.csv) — seja o research_log.md escrito a mao (skill 03)
            # ou promovido por kb_reconcile.py. NAO generalizamos o tripwire de "Conflitos Resolvidos"
            # do kb_reconcile.py pra ca: la faz sentido pq o placeholder e um texto EXATO e conhecido
            # (gerado por kb_build_ollama.py); aqui, um research_log.md sem NENHUM conflito de verdade
            # (fonte unica, sem divergencia) e um caso legitimo — nao da pra distinguir isso de "nao
            # revisado" so pelo tamanho do texto sem o placeholder conhecido como ancora.
            import kb_reconcile  # noqa: E402  (import tardio: so precisa apos 'reconciled' confirmado)
            found = kb_reconcile._kb_entities_found(root)
            ratified = kb_reconcile._ratified_set(root)
            pending = [n for n in found if n.lower() not in ratified]
            if pending:
                problems.append(
                    f"{len(pending)} entidade(s) com conteudo na KB sem ratificacao humana "
                    f"(kb_ratified.csv): {pending[:5]}{' ...' if len(pending) > 5 else ''}"
                )
        # Decisoes pendentes: sempre extraidas e reportadas ao usuario (nao bloqueiam)
        pending_decisions = _parse_pending_decisions(txt)

    for name in _KB_ARTIFACTS:
        f = art / name
        if not f.is_file() or not f.read_text(encoding="utf-8").strip():
            problems.append(f"{name} ausente/vazio — KB incompleta (skills 03/04).")
    vc = paths.voice_cards(root)
    if not vc.is_file():
        problems.append("voice_cards.json ausente — rode state_index (deriva do tone_analysis.md).")
    else:
        try:
            vc_data = json.loads(vc.read_text(encoding="utf-8"))
            if not vc_data:
                problems.append(
                    "voice_cards.json vazio ({}) — tone_analysis.md precisa de perfis de personagem "
                    "no formato '### Nome — `voice_criticality: X`'. Rode state_index apos criar."
                )
        except (json.JSONDecodeError, OSError):
            problems.append("voice_cards.json invalido — rode state_index apos corrigir tone_analysis.md.")

    # Glossario: updated_date e gate obrigatorio (nao so aviso de state_index)
    gp = paths.glossary(root)
    if gp.is_file():
        import csv as _csv
        try:
            with gp.open(encoding="utf-8-sig", newline="") as fh:
                hdr = next(_csv.reader(fh), [])
            if "updated_date" not in [h.strip() for h in hdr]:
                problems.append(
                    "glossary.csv sem coluna 'updated_date' — adicione a coluna com a data da "
                    "ultima revisao de cada termo antes de traduzir."
                )
        except Exception:
            pass

    # fronteira: declarada em project.json (machine-readable) tem prioridade; senao, so reporta a do log
    cfg = json.loads((root / "project.json").read_text(encoding="utf-8"))
    frontier = cfg.get("kb_frontier")
    scene_id = context_pack.scene_id_of(scene)
    if frontier:
        frontier_pos = _pos(frontier)
        # frontier_pos vazio => kb_frontier NAO e um scene_id parseavel (ex.: convencao de projeto
        # flat "artifacts/kb_phase_worklist.md" — sem ordem narrativa, ver BoF4/Souldiers). Nesse
        # caso nao ha posicao numerica p/ comparar — pular a checagem em vez de comparar contra
        # tupla vazia. Bug real descoberto no Souldiers 2026-07-02: _pos() acha digito em QUALQUER
        # segmento "_"-separado do scene_id (ex. "CAVE_00" -> (0,), "1_5" -> (1,5)), entao
        # `_pos(scene_id) > _pos(frontier vazio)` dava True p/ quase toda cena com numero no nome —
        # bloqueava 500+ cenas por engano. So funcionava por coincidencia no BoF4 (nomes de cena
        # sem segmento puramente numerico).
        if frontier_pos and _pos(scene_id) > frontier_pos:
            problems.append(f"cena {scene_id} ALEM da fronteira de KB pesquisada (kb_frontier={frontier}) — "
                            f"estenda a Fase 0 ate aqui antes de traduzir.")
    else:
        # kb_frontier ausente = gate nao tem fronteira machine-readable para validar posicao de cena.
        # Promovido para problema (hard block): sem declaracao explicita nao e possivel garantir que
        # a KB cobre a cena sendo traduzida — declare "kb_frontier": "<scene_id>" em project.json.
        problems.append("kb_frontier nao declarada em project.json — declare a scene_id maxima coberta "
                        "pela pesquisa (ex.: \"kb_frontier\": \"12_17\"). Sem isso o gate nao pode "
                        "validar fronteira e qualquer cena alem da pesquisa seria traduzida as cegas.")
    # kb_ratified: se existe, checar coluna de data de ratificacao
    kr = paths.kb_ratified(root)
    if kr.is_file():
        import csv as _csv
        try:
            with kr.open(encoding="utf-8-sig", newline="") as fh:
                ratified_rows = list(_csv.DictReader(fh))
            if ratified_rows:
                date_cols = [c for c in ratified_rows[0].keys()
                             if "date" in c.lower() or "data" in c.lower()]
                if not date_cols:
                    warnings.append("kb_ratified.csv sem coluna de data — adicione 'date_ratified' "
                                    "p/ rastrear quando cada entidade foi ratificada.")
                else:
                    undated = sum(1 for r in ratified_rows
                                  if not any(r.get(c, "").strip() for c in date_cols))
                    if undated:
                        warnings.append(f"{undated} entidade(s) em kb_ratified.csv sem data de "
                                        f"ratificacao (coluna '{date_cols[0]}').")
        except Exception:
            pass

    return {
        "hard_problems": hard_problems,
        "problems": problems,
        "warnings": warnings,
        "pending_decisions": pending_decisions,
    }


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Gate de cobertura de KB (pre-traducao).")
    ap.add_argument("project")
    ap.add_argument("scene")
    a = ap.parse_args()
    r = check(a.project, a.scene)
    for w in r["warnings"]:
        print(f"[warn] {w}")
    for p in r.get("hard_problems", []):
        print(f"[HARD-BLOCK] {p}")
    for p in r["problems"]:
        print(f"[BLOCK] {p}")
    if r.get("pending_decisions"):
        print(f"\n[DECISOES PENDENTES — {len(r['pending_decisions'])} item(ns) aguardam revisao humana]")
        for i, d in enumerate(r["pending_decisions"], 1):
            print(f"  {i}. {d}")
    all_problems = r.get("hard_problems", []) + r["problems"]
    print("\nOK: cobertura de KB suficiente." if not all_problems else
          f"\nBLOQUEADO: {len(all_problems)} problema(s) de cobertura.")
    sys.exit(1 if all_problems else 0)


if __name__ == "__main__":
    main()
