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
  FRONTEIRA: project.json `kb_frontier` = scene_id max coberto pela pesquisa (ex.: "12_17"). Cena
    alem disso -> a KB nao cobre este ponto narrativo -> rode a Fase 0 ate aqui. `kb_frontier` NAO
    declarado tambem e HARD (sem ele o gate nao tem como validar posicao de cena — tradução as cegas).
  PROFUNDIDADE (soft, reforco de coesao de codigo): 'reconciled' sozinho e so um marcador -- toda entidade com
    conteudo afirmado (nao-UNSOURCED) no universe_knowledge_base.md precisa de ratificacao humana
    em kb_ratified.csv (mesmo mecanismo que kb_reconcile.py ja usa pro caminho draft_ollama, aqui
    generalizado pro caminho manual/skill-03). Bypassavel via --skip-kb-gate como qualquer problem.

Uso (CLI):  python kb_gate.py <projeto> <scene>
"""
from __future__ import annotations

import contextlib
import csv
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


_pos = context_pack._pos   # fonte unica do parser de posicao narrativa (evitava divergencia:
                            # este split("_") dava () p/ ids alfanumericos sem "_", ex. "AREAD050")


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


# Cada _check_* abaixo acrescenta em `res` ({hard_problems, problems, warnings, pending_decisions});
# a ORDEM das chamadas em check() e a ordem das mensagens.

def _load_cfg(root: Path, res: dict) -> dict:
    cfg_path = root / "project.json"
    try:
        return json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.is_file() else {}
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
        # cfg={} faria _db_path() tratar um projeto DB-backed como flat-file calado -- os checks de
        # KB/glossario cairiam pro caminho de arquivo (sempre "ausente") em vez de acusar o
        # project.json quebrado. Vira hard_problem em vez de mascarar.
        res["hard_problems"].append(
            f"project.json corrompido/ilegivel ({e}) — corrija antes de continuar "
            f"(deteccao de DB vs. artefatos flat fica incerta enquanto isso).")
        return {}


def _fetch_db_rows(db_path, db_pid) -> tuple[list, list]:
    """Fetch 1x p/ os 3 checks DB-aware (KB, glossario-presenca, glossario-updated_at) reusarem --
    evita abrir Store/rodar get_glossary() de novo em cada check."""
    _db_dir = str(Path(__file__).resolve().parent.parent / "db")
    if _db_dir not in sys.path:
        sys.path.insert(0, _db_dir)
    from store import Store
    with Store(db_path) as db:
        return db.get_kb(db_pid), db.get_glossary(db_pid)


def _check_kb_present(art: Path, db_path, kb_rows, res: dict) -> None:
    """universe_knowledge_base.md: HARD — nao passa nem com --skip-kb-gate. #85: DB-aware (mesma
    lacuna do check de glossario) -- projeto com `db` populado nao tem o .md em disco."""
    if db_path:
        if not any((r.get("content") or "").strip() for r in kb_rows):
            res["hard_problems"].append(
                "KB vazia no DB (tabela kb) — sintetize a KB (skill 03/04) antes de traduzir. "
                "Este gate nao pode ser pulado."
            )
        return
    for name in _KB_HARD:
        f = art / name
        if not f.is_file() or not f.read_text(encoding="utf-8").strip():
            res["hard_problems"].append(
                f"{name} ausente/vazio — sintetize a KB (skill 03/04) antes de traduzir. "
                f"Este gate nao pode ser pulado."
            )


def _check_ratification_depth(root: Path, res: dict) -> None:
    """PROFUNDIDADE DA FASE 0 (reforco de coesao de codigo — generalizado do kb_reconcile.py, que so
    cobria o caminho draft_ollama do kb_build_ollama.py): 'reconciled' sozinho e so um MARCADOR,
    nao garante que a reconciliacao teve profundidade de verdade. Exige tambem ratificacao
    humana por entidade (kb_ratified.csv) — seja o research_log.md escrito a mao (skill 03)
    ou promovido por kb_reconcile.py. NAO generalizamos o tripwire de "Conflitos Resolvidos"
    do kb_reconcile.py pra ca: la faz sentido pq o placeholder e um texto EXATO e conhecido
    (gerado por kb_build_ollama.py); aqui, um research_log.md sem NENHUM conflito de verdade
    (fonte unica, sem divergencia) e um caso legitimo — nao da pra distinguir isso de "nao
    revisado" so pelo tamanho do texto sem o placeholder conhecido como ancora."""
    import kb_reconcile  # noqa: E402  (import tardio: so precisa apos 'reconciled' confirmado)
    found = kb_reconcile._kb_entities_found(root)
    ratified = kb_reconcile._ratified_set(root)
    pending = [n for n in found if n.lower() not in ratified]
    if pending:
        res["problems"].append(
            f"{len(pending)} entidade(s) com conteudo na KB sem ratificacao humana "
            f"(kb_ratified.csv): {pending[:5]}{' ...' if len(pending) > 5 else ''}"
        )


def _check_research_log(root: Path, art: Path, res: dict) -> None:
    rl = art / "research_log.md"
    if not rl.is_file():
        res["problems"].append("research_log.md ausente — rode a Fase 0 (skill 03, pesquisa IA+humano).")
        return
    txt = rl.read_text(encoding="utf-8")
    # tolera markdown: "**Status:** reconciled", "status : reconciled", etc.
    if not re.search(r"status[:*\s]+reconciled", txt, re.I):
        res["problems"].append("research_log.md sem 'status: reconciled' — reconcilie a pesquisa IA+humano.")
    else:
        if re.search(r"human_input\s*:\s*pending", txt, re.I):
            res["warnings"].append("research_log.md: status=reconciled mas human_input=pending — "
                                   "atualize para 'confirmed' ou 'declined' (proveniência incompleta).")
        _check_ratification_depth(root, res)
    # Decisoes pendentes: sempre extraidas e reportadas ao usuario (nao bloqueiam)
    res["pending_decisions"] = _parse_pending_decisions(txt)


def _check_glossary_present(art: Path, db_path, g_rows, res: dict) -> None:
    """glossary.csv: #85 DB-aware -- projeto com `db` populado nao tem o CSV em disco."""
    if db_path:
        if not g_rows:
            res["problems"].append("glossario vazio no DB (tabela glossary) — KB incompleta (skills 03/04).")
        return
    for name in _KB_ARTIFACTS:
        f = art / name
        if not f.is_file() or not f.read_text(encoding="utf-8").strip():
            res["problems"].append(f"{name} ausente/vazio — KB incompleta (skills 03/04).")


def _check_voice_cards(root: Path, res: dict) -> None:
    vc = paths.voice_cards(root)
    if not vc.is_file():
        res["problems"].append("voice_cards.json ausente — rode state_index (deriva do tone_analysis.md).")
        return
    try:
        vc_data = json.loads(vc.read_text(encoding="utf-8"))
        if not vc_data:
            res["problems"].append(
                "voice_cards.json vazio ({}) — tone_analysis.md precisa de perfis de personagem "
                "no formato '### Nome — `voice_criticality: X`'. Rode state_index apos criar."
            )
    except (json.JSONDecodeError, OSError):
        res["problems"].append("voice_cards.json invalido — rode state_index apos corrigir tone_analysis.md.")


def _check_glossary_dated(root: Path, db_path, g_rows, res: dict) -> None:
    """Glossario: updated_date/updated_at e gate obrigatorio (nao so aviso de state_index).
    #85: DB-aware -- projeto com `db` populado nao tem glossary.csv (o CSV e so o modelo flat),
    entao o check precisa ler a coluna equivalente (updated_at) do banco em vez de grepar header."""
    if db_path:
        undated = [r.get("term", "?") for r in g_rows if not r.get("updated_at")]
        if undated:
            res["problems"].append(
                f"{len(undated)} termo(s) do glossario sem 'updated_at' no DB — grave a data da "
                f"ultima revisao antes de traduzir: {undated[:5]}{' ...' if len(undated) > 5 else ''}"
            )
        return
    gp = paths.glossary(root)
    if not gp.is_file():
        return
    try:
        with gp.open(encoding="utf-8-sig", newline="") as fh:
            hdr = next(csv.reader(fh), [])
        if "updated_date" not in [h.strip() for h in hdr]:
            res["problems"].append(
                "glossary.csv sem coluna 'updated_date' — adicione a coluna com a data da "
                "ultima revisao de cada termo antes de traduzir."
            )
    except Exception as exc:
        res["problems"].append(f"glossary.csv ilegivel ({exc!r}) — nao foi possivel checar 'updated_date'.")


def _check_frontier(cfg: dict, scene, res: dict) -> None:
    """fronteira: declarada em project.json (machine-readable) tem prioridade; senao, so reporta a do log."""
    frontier = cfg.get("kb_frontier")
    scene_id = context_pack.scene_id_of(scene)
    if not frontier:
        # kb_frontier ausente = gate nao tem fronteira machine-readable para validar posicao de cena.
        # HARD BLOCK (nunca bypassavel, nem com --skip-kb-gate): sem declaracao explicita nao e possivel
        # garantir que a KB cobre a cena sendo traduzida — mesma severidade de "sem sei se e seguro
        # avancar" que os demais hard_problems deste gate. Declare "kb_frontier": "<scene_id>" em project.json.
        res["hard_problems"].append(
            "kb_frontier nao declarada em project.json — declare a scene_id maxima coberta "
            "pela pesquisa (ex.: \"kb_frontier\": \"12_17\"). Sem isso o gate nao pode "
            "validar fronteira e qualquer cena alem da pesquisa seria traduzida as cegas. "
            "Este gate nao pode ser pulado.")
        return
    frontier_pos = _pos(frontier)
    # frontier_pos vazio => kb_frontier NAO e um scene_id parseavel (ex.: convencao de projeto
    # flat "artifacts/kb_phase_worklist.md" — sem ordem narrativa, ver BoF4/Souldiers). Nesse
    # caso nao ha posicao numerica p/ comparar — pular a checagem em vez de comparar contra
    # tupla vazia. Bug real descoberto no Souldiers 2026-07-02: _pos() acha digito em QUALQUER
    # segmento "_"-separado do scene_id (ex. "CAVE_00" -> (0,), "1_5" -> (1,5)), entao
    # `_pos(scene_id) > _pos(frontier vazio)` dava True p/ quase toda cena com numero no nome —
    # bloqueava 500+ cenas por engano. So funcionava por coincidencia no BoF4 (nomes de cena
    # sem segmento puramente numerico).
    scene_pos = _pos(scene_id)
    # scene_pos vazio (scene_id sem digito) e INCOMPARAVEL, nao "antes da fronteira" -- default-deny
    # (mesma convencao de _pos()/select_spoiler_guards): sem como provar que a KB cobre esta cena,
    # trata como alem da fronteira em vez de deixar passar por `() > frontier_pos` dar False.
    if frontier_pos and (not scene_pos or scene_pos > frontier_pos):
        res["problems"].append(f"cena {scene_id} ALEM da fronteira de KB pesquisada (kb_frontier={frontier}) — "
                               f"estenda a Fase 0 ate aqui antes de traduzir.")


def _check_ratified_dates(root: Path, res: dict) -> None:
    """kb_ratified: se existe, checar coluna de data de ratificacao."""
    kr = paths.kb_ratified(root)
    if not kr.is_file():
        return
    try:
        with kr.open(encoding="utf-8-sig", newline="") as fh:
            ratified_rows = list(csv.DictReader(fh))
        if not ratified_rows:
            return
        date_cols = [c for c in ratified_rows[0].keys() if "date" in c.lower() or "data" in c.lower()]
        if not date_cols:
            res["warnings"].append("kb_ratified.csv sem coluna de data — adicione 'date_ratified' "
                                   "p/ rastrear quando cada entidade foi ratificada.")
            return
        undated = sum(1 for r in ratified_rows if not any(r.get(c, "").strip() for c in date_cols))
        if undated:
            res["warnings"].append(f"{undated} entidade(s) em kb_ratified.csv sem data de "
                                   f"ratificacao (coluna '{date_cols[0]}').")
    except Exception as exc:
        res["warnings"].append(f"kb_ratified.csv ilegivel ({exc!r}) — data de ratificacao nao checada.")


def check(root, scene) -> dict:
    """Retorna {hard_problems: [...], problems: [...], warnings: [...], pending_decisions: [...]}.
    hard_problems != []    => bloquear sempre (nao bypassavel).
    problems != []         => bloquear salvo --skip-kb-gate.
    pending_decisions != [] => sempre exibido ao usuario (nao bloqueia, mas obrigatorio informar).
    """
    root = Path(root)
    art = paths.artifacts(root)
    res: dict = {"hard_problems": [], "problems": [], "warnings": [], "pending_decisions": []}
    cfg = _load_cfg(root, res)
    db_path, db_pid = context_pack._db_path(root, cfg)
    kb_rows, g_rows = _fetch_db_rows(db_path, db_pid) if db_path else (None, None)

    _check_kb_present(art, db_path, kb_rows, res)
    _check_research_log(root, art, res)
    _check_glossary_present(art, db_path, g_rows, res)
    _check_voice_cards(root, res)
    _check_glossary_dated(root, db_path, g_rows, res)
    _check_frontier(cfg, scene, res)
    _check_ratified_dates(root, res)
    return res


def main():
    with contextlib.suppress(AttributeError, ValueError, OSError):  # Windows cp1252: permitir setas/acentos no stdout
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
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
