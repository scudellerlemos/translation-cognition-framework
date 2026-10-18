#!/usr/bin/env python3
"""
risk_triage.py — TRIAGEM DE RISCO (passo 4.4a): um juiz barato reclassifica o risco das falas que o tradutor
deixou como low/medium. So caminho de sessao (nao chama API); a saida do juiz e curta — so o id de quem sobe.

O tradutor marca pouco risco alto, e so risco alto passa pela retrotraducao. A triagem fecha esse ponto cego
sem retrotraduzir o jogo inteiro: fala repetida entra UMA vez (par fonte+traducao unico), o juiz devolve so
os ids que merecem um segundo olhar, e o `apply` sobe o risco dessas falas para `high` — a retrotraducao que
ja existe (run_scene --require-back) e a revisao humana (quality_review export) cuidam do resto.

  export  grava lotes `lote_NNN.tsv` (id, fonte, traducao) + `triagem_prompt.md` em qa_revisao/para_revisar/triagem/
  apply   le `veredito_NNN.tsv` (id<TAB>motivo curto; so quem sobe) e marca risk_level=high nas cenas

Uso:
  python risk_triage.py export <projeto> [--batch 400]
  python risk_triage.py apply  <projeto>
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import artifact_io  # noqa: E402
import context_pack  # noqa: E402
import paths  # noqa: E402

_TOKEN = re.compile(r"\[[0-9A-Fa-f]{2}\]")
MIN_WORDS = 4      # rotulo de menu/nome solto nao tem o que o juiz avaliar (a consistencia e do glossary_lint)

PROMPT = """# Triagem de risco de traducao

Cada linha de `lote_NNN.tsv` e: id, fala original, traducao. Voce NAO corrige nada e NAO retraduz.
Aponte so as falas em que a traducao pode estar ERRADA ou ter perdido algo que importa:

- sentido trocado, negacao perdida, sujeito/objeto invertido, numero ou nome diferente;
- expressao idiomatica, trocadilho, ironia ou ambiguidade traduzida ao pe da letra;
- informacao cortada ou acrescentada; genero/tratamento que contradiz a fala;
- frase que nao faz sentido em portugues.

Traducao correta e natural NAO entra, mesmo que voce escrevesse diferente. Na duvida real, entra.

Para cada lote escreva `veredito_NNN.tsv` (mesmo numero, mesma pasta) com UMA linha por fala apontada:

    id<TAB>motivo em ate 8 palavras

Lote sem nada a apontar: arquivo vazio. Nao escreva mais nada alem desses arquivos.
"""


def _dir(root: Path) -> Path:
    return paths.qa_outbox(root) / "triagem"


def _clean(s: str) -> str:
    return " ".join(_TOKEN.sub(" ", s or "").split())


def pairs(root: Path, everything: bool = False) -> dict[str, dict]:
    """{id: {source, target, where: [(cena, offset)]}} dos pares unicos ainda nao marcados como alto risco.
    everything=True: todo par traduzido (alto risco e rotulo curto inclusive) — a populacao da amostra de qualidade."""
    out: dict[str, dict] = {}
    for scene in artifact_io.scenes(root):
        for ln in artifact_io.plan_lines(root, scene):
            if not everything and ln.get("risk_level") in ("high", "critical"):
                continue
            src, tgt = _clean(ln.get("text_source", "")), _clean(ln.get("base_translation", ""))
            if not tgt or (not everything and (len(src.split()) < MIN_WORDS or src == tgt)):
                continue
            pid = hashlib.sha1(f"{src}\t{tgt}".encode(), usedforsecurity=False).hexdigest()[:10]
            out.setdefault(pid, {"source": src, "target": tgt, "where": []})["where"].append(
                (scene, ln.get("offset", "")))
    return out


def judged(root: Path) -> tuple[set, set]:
    """(ids que o juiz ja leu, ids que ele apontou) — so lotes que ja tem veredito."""
    seen, flagged = set(), set()
    for vf in sorted(_dir(root).glob("veredito_*.tsv")):
        lot = vf.with_name(vf.name.replace("veredito_", "lote_"))
        if lot.is_file():
            seen |= {r.split("\t")[0] for r in lot.read_text(encoding="utf-8").splitlines() if r.strip()}
        flagged |= {r.split("\t")[0].strip() for r in vf.read_text(encoding="utf-8").splitlines() if r.strip()}
    return seen, flagged & seen if seen else flagged


def export(root, batch: int = 400) -> dict:
    root = Path(root)
    d = _dir(root)
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("lote_*.tsv"):
        old.unlink()
    items = sorted(pairs(root).items(), key=lambda kv: kv[1]["where"][0])     # ordem do jogo: contexto vizinho
    n = 0
    for n, i in enumerate(range(0, len(items), batch), 1):
        paths.atomic_write(d / f"lote_{n:03}.tsv", "".join(f"{pid}\t{v['source']}\t{v['target']}\n" for pid, v in items[i:i + batch]))
    paths.atomic_write(d / "triagem_prompt.md", PROMPT)
    return {"pairs": len(items), "lines": sum(len(v["where"]) for _, v in items), "batches": n, "dir": str(d)}


def apply(root) -> dict:
    """Sobe para `high` toda fala cujo par foi apontado. Idempotente; id desconhecido e ignorado e contado."""
    root = Path(root)
    idx = pairs(root)
    raised, unknown, by_scene = 0, 0, {}
    for vf in sorted(_dir(root).glob("veredito_*.tsv")):
        for row in vf.read_text(encoding="utf-8").splitlines():
            pid, _, reason = row.strip().partition("\t")
            if not pid:
                continue
            if pid not in idx:
                unknown += 1        # ja subiu numa rodada anterior, ou id inventado pelo juiz
                continue
            for scene, off in idx[pid]["where"]:
                by_scene.setdefault(scene, {})[off] = reason.strip()[:80]
    for scene, offs in by_scene.items():
        tf = paths.translations(root, scene, context_pack.scene_id_of(scene))
        if not tf.is_file():
            continue
        data = json.loads(tf.read_text(encoding="utf-8"))
        for off, reason in offs.items():
            e = data.get("lines", {}).get(off)
            if isinstance(e, dict):
                e["risk_level"] = "high"
                e["risk_notes"] = f"triagem: {reason}" if reason else "triagem"
                raised += 1
        paths.atomic_write(tf, json.dumps(data, ensure_ascii=False, indent=1))
    return {"raised": raised, "unknown_ids": unknown, "scenes": sorted(by_scene)}


def main():
    with contextlib.suppress(AttributeError, ValueError, OSError):
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    ap = argparse.ArgumentParser(description="Triagem de risco por juiz barato (so caminho de sessao).")
    ap.add_argument("cmd", choices=["export", "apply"])
    ap.add_argument("project")
    ap.add_argument("--batch", type=int, default=400)
    a = ap.parse_args()
    if a.cmd == "export":
        r = export(a.project, a.batch)
        print(f"triagem: {r['pairs']} par(es) unico(s) cobrindo {r['lines']} fala(s) em {r['batches']} lote(s) -> {r['dir']}")
        print("  juiz: leia triagem_prompt.md e escreva veredito_NNN.tsv por lote; depois: risk_triage.py apply")
    else:
        r = apply(a.project)
        print(f"triagem: {r['raised']} fala(s) subiram para risco alto em {len(r['scenes'])} cena(s)"
              + (f" | {r['unknown_ids']} id(s) ignorado(s)" if r["unknown_ids"] else ""))
        if r["scenes"]:
            print("  re-rode com retrotraducao: run_scene.py <projeto> " + " ".join(r["scenes"])
                  + " --backend in-session --require-back")


if __name__ == "__main__":
    main()
