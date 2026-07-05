#!/usr/bin/env python3
"""
kb_reconcile.py — promove o rascunho do kb_build_ollama.py (status: draft_ollama) pra reconciled,
SO depois de ratificacao humana explicita. Fecha o loop de governanca do onboarding de baixo custo (kb_fetch.py +
kb_build_ollama.py produzem so o insumo bruto; a Fase 1B da skill 03 continua sendo julgamento
humano, nao um script).

Reusa `kb_ratified.csv` (mesmo arquivo/coluna que kb_review.py --strict ja usa em outro ponto do
pipeline) em vez de inventar um formato novo: e o "segundo par de olhos" ja estabelecido no projeto
p/ impedir "a IA propoe E aprova sozinha" (ver kb_review.py, risco #5 documentado la). So o HUMANO
edita kb_ratified.csv -- a IA nunca se auto-ratifica.

`--promote` recusa (nao promove) se:
  - alguma entidade com conteudo afirmado (found=true no rascunho, ou seja, != UNSOURCED) no
    universe_knowledge_base.md ainda nao tem linha em kb_ratified.csv; OU
  - a secao "## Conflitos Resolvidos" do research_log.md ainda esta no placeholder literal que o
    kb_build_ollama.py escreve (tripwire barato contra "rodei --promote sem olhar pra nada").

UNSOURCED nunca bloqueia (nada foi afirmado, nada a ratificar). kb_gate.py NAO precisa mudar: a
regex que ja usa (status seguido de 'reconciled') so casa depois da promocao, exatamente como deveria.

Uso:  python kb_reconcile.py <projeto>              # --check (default, read-only)
      python kb_reconcile.py <projeto> --promote     # promove SE --check estiver limpo
      python kb_reconcile.py <projeto> --concordance # triagem alta/baixa concordancia (#67)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import paths  # noqa: E402  (paths.py: fonte unica do contrato de caminhos de artefato)
from kb_review import (
    _ratified_set,  # noqa: E402  (mesmo "segundo par de olhos" ja usado no projeto)
)

_STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(\S+)", re.M | re.I)
_ENTITY_BLOCK_RE = re.compile(r"^## (.+?)\n(.*?)(?=^## |\Z)", re.M | re.S)
_CONFLICTS_PLACEHOLDER = "(nenhum -- reconciliacao ainda nao rodou)"
_MIN_CONFLICTS_CHARS = 15   # tripwire minimo -- so remover o placeholder nao basta (ver _conflicts_section_untouched)


def _current_status(root: Path) -> str:
    """Ancorado em '**Status:**' no INICIO de linha (o mesmo formato exato que _write_research_log/
    promote() escrevem) -- nao um 'status' solto em qualquer lugar do documento. Uma regex frouxa
    aqui divergia do padrao ESTRITO usado pra escrever em promote(), abrindo espaco pra promote()
    reportar sucesso sem ter mudado nada (ver defesa extra em promote())."""
    rl = paths.research_log(root)
    if not rl.is_file():
        return ""
    m = _STATUS_RE.search(rl.read_text(encoding="utf-8"))
    return m.group(1) if m else ""


def _kb_entities_found(root: Path) -> list[str]:
    """Nomes das entidades no universe_knowledge_base.md com conteudo AFIRMADO (found=true no
    rascunho, != UNSOURCED) -- as que precisam de ratificacao humana antes de promover."""
    kb = paths.artifacts(root) / "universe_knowledge_base.md"
    if not kb.is_file():
        return []
    txt = kb.read_text(encoding="utf-8")
    names = []
    for m in _ENTITY_BLOCK_RE.finditer(txt):
        name, body = m.group(1).strip(), m.group(2)
        conf_m = re.search(r"\*\*Status de confian[çc]a:\*\*\s*\n(.+)", body)
        conf = conf_m.group(1).strip() if conf_m else ""
        if conf and not conf.upper().startswith("UNSOURCED"):
            names.append(name)
    return names


def _conflicts_section_body(root: Path) -> str:
    rl = paths.research_log(root)
    if not rl.is_file():
        return ""
    m = re.search(r"^## Conflitos Resolvidos\s*\n(.*?)(?=^## |\Z)", rl.read_text(encoding="utf-8"),
                  re.M | re.S)
    return m.group(1).strip() if m else ""


def _conflicts_section_untouched(root: Path) -> bool:
    """True se a secao ainda estiver no placeholder OU vazia/trivial demais pra contar como
    revisada. So tirar o placeholder nao basta (um "xxx" qualquer passava antes) -- exige um
    minimo de conteudo substantivo. Nao valida QUALIDADE semantica (isso exigiria um modelo,
    fora de escopo deste gate deterministico) -- so levanta a barra contra o caso mais preguicoso."""
    body = _conflicts_section_body(root)
    if _CONFLICTS_PLACEHOLDER in body:
        return True
    return len(body) < _MIN_CONFLICTS_CHARS


def check(root) -> dict:
    """Read-only. {status, pending_ratification, conflicts_untouched, ready, note?}. Se o
    research_log.md nao estiver em status draft_ollama, e um no-op informativo (nada a promover
    aqui -- ou ja esta reconciled, ou nunca rodou o kb_build_ollama.py)."""
    root = Path(root)
    status = _current_status(root)
    if status != "draft_ollama":
        return {"status": status, "pending_ratification": [], "conflicts_untouched": False,
                "ready": False, "note": f"status atual e {status!r}, nao 'draft_ollama' -- nada a "
                                        "fazer aqui (ou ja reconciliado, ou kb_build_ollama.py nunca rodou)."}
    ratified = _ratified_set(root)
    found = _kb_entities_found(root)
    pending = [n for n in found if n.lower() not in ratified]
    untouched = _conflicts_section_untouched(root)
    return {"status": status, "pending_ratification": pending,
            "conflicts_untouched": untouched, "ready": not pending and not untouched}


def promote(root) -> dict:
    """SO promove (draft_ollama -> reconciled, human_input: pending -> confirmed) se check()
    estiver ready=True. Caso contrario, recusa (promoted=False) sem tocar em nada -- reaproveita
    o mesmo dict de check() pra listar o que falta.

    Defesa extra: confirma que a substituicao REALMENTE aconteceu antes de reportar promoted=True.
    _current_status() e o re.sub aqui usam o MESMO padrao ancorado '**Status:**' agora (ver
    _STATUS_RE), entao nao deveriam divergir -- mas se o arquivo for editado a mao fora desse
    formato entre o check() e a escrita, ou algum drift futuro reintroduzir a divergencia, isso
    evita reportar sucesso falso (arquivo intocado, mensagem dizendo que promoveu)."""
    root = Path(root)
    c = check(root)
    if not c["ready"]:
        return {"promoted": False, **c}
    rl = paths.research_log(root)
    txt = rl.read_text(encoding="utf-8")
    new_txt = re.sub(r"(\*\*Status:\*\*\s*)draft_ollama", r"\1reconciled", txt, count=1)
    new_txt = re.sub(r"(\*\*human_input:\*\*\s*)pending", r"\1confirmed", new_txt, count=1)
    if new_txt == txt:
        return {"promoted": False, **c,
                "note": "research_log.md nao esta no formato esperado ('**Status:**'/'**human_input:**') "
                        "-- nao foi possivel promover automaticamente. Corrija o formato manualmente."}
    rl.write_text(new_txt, encoding="utf-8")
    return {"promoted": True, **c}


def _print_check(r: dict):
    if not r["pending_ratification"] and not r["conflicts_untouched"]:
        print("OK: todas as entidade(s) com conteudo estao ratificadas em kb_ratified.csv, e a "
              "secao 'Conflitos Resolvidos' foi revisada. Pronto para --promote.")
        return
    if r["pending_ratification"]:
        print(f"PENDENTE — {len(r['pending_ratification'])} entidade(s) ainda sem ratificacao "
              "humana (kb_ratified.csv):")
        for n in r["pending_ratification"]:
            print(f"  - {n}")
    if r["conflicts_untouched"]:
        print("AVISO: secao 'Conflitos Resolvidos' ainda no placeholder do rascunho — revise "
              "antes de promover.")


def main():
    import argparse
    ap = argparse.ArgumentParser(
        description="Promove draft_ollama -> reconciled apos ratificacao humana (kb_ratified.csv).")
    ap.add_argument("project")
    ap.add_argument("--promote", action="store_true",
                    help="promove SE o check estiver limpo; senao recusa (exit 1), nada e alterado")
    ap.add_argument("--concordance", action="store_true",
                    help="triagem alta/baixa concordancia rascunho x pesquisa humana (read-only, "
                         "nao substitui --promote; ver kb_concordance.py, #67)")
    a = ap.parse_args()

    if a.concordance:
        import kb_concordance
        kb_concordance._print_report(kb_concordance.concordance(a.project))
        return

    if a.promote:
        r = promote(a.project)
        if r["promoted"]:
            print("[kb_reconcile] status: draft_ollama -> reconciled (human_input: confirmed)")
            sys.exit(0)
        print(f"[kb_reconcile] status atual: {r['status'] or '(research_log.md ausente)'}")
        if r.get("note"):
            print(r["note"])
        else:
            print("[kb_reconcile] RECUSADO: ainda ha pendencia. Nao promovido.")
            _print_check(r)
        sys.exit(1)

    r = check(a.project)
    print(f"[kb_reconcile] status atual: {r['status'] or '(research_log.md ausente)'}")
    if r.get("note"):
        print(r["note"])
        sys.exit(0)
    _print_check(r)
    sys.exit(0 if r["ready"] else 1)


if __name__ == "__main__":
    main()
