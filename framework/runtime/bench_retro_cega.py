#!/usr/bin/env python3
"""
bench_retro_cega.py — BENCHMARK (dev) da retrotraducao cega (ADR 0025). NAO faz parte do pipeline.

Mede se o juiz que primeiro traduz de volta SEM ver o source (cega) pega mais defeitos que o juiz que ve
o source (padrao), com verdade conhecida: metade dos casos recebe um defeito rotulado, metade fica intacta.
Tudo vive em uma pasta de trabalho FORA do repo (ela guarda fala do jogo).

Passos (cada um grava na pasta de trabalho):
  sorteio  <projeto> <pasta> [--n 60] [--seed 1] [--por-cena 10]   casos.json + defeitos_prompt.md
  montar   <pasta>                                                 2 projetos sinteticos (padrao/ e cega/) com os prompts
  placar   <pasta>                                                 recall, falso alarme e criterio de adocao

Entre `sorteio` e `montar`, um agente le `defeitos_prompt.md` e grava `defeitos.json`.
Criterio fixado antes da medicao: adotar a cega so se recall_cega >= recall_padrao + 0.10 e
falso_alarme_cega <= falso_alarme_padrao + 0.10.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import artifact_io  # noqa: E402
import back_translate  # noqa: E402

TIPOS = ("sentido_invertido", "omissao", "tom", "nome_errado", "adicao")
MARGEM = 0.10


def sorteio(root, n: int = 60, seed: int = 1, por_cena: int = 10) -> list[dict]:
    """n casos {id, scene, offset, source, target, speaker} de falas ja traduzidas; metade marcada 'defeito'."""
    root = Path(root)
    rng = random.Random(seed)
    pool = []
    for scene in artifact_io.scenes(root):
        tr = artifact_io.translations_map(root, scene)
        sc_dir = root / "artifacts" / "scenes" / scene
        with (sc_dir / "dialogs.csv").open(encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh):
                e = tr.get(r.get("offset", ""))
                if e and len(r.get("text_en", "")) > 20 and e.get("t"):
                    pool.append({"scene": scene, "offset": r["offset"], "source": r["text_en"],
                                 "target": e["t"], "speaker": e.get("speaker", "")})
    por: dict[str, list[dict]] = {}
    for p in pool:
        por.setdefault(p["scene"], []).append(p)
    cenas = [s for s, v in por.items() if len(v) >= por_cena]    # so cenas que enchem a cota: poucos prompts por braco
    rng.shuffle(cenas)
    casos: list[dict] = []
    for s in cenas:
        casos += rng.sample(por[s], por_cena)
        if len(casos) >= n:
            break
    casos = casos[:n]
    casos.sort(key=lambda c: (c["scene"], c["offset"]))
    com_defeito = set(rng.sample(range(len(casos)), len(casos) // 2))
    for i, c in enumerate(casos):
        c["id"] = f"C{i:03d}"
        c["defeito"] = i in com_defeito
    return casos


def defeitos_prompt(casos: list[dict]) -> str:
    out = ["# Defeitos rotulados (benchmark de retrotraducao)", "",
           "Para cada caso abaixo, reescreva o `target` (pt-BR) introduzindo EXATAMENTE UM defeito plausivel e sutil,",
           "de um destes tipos: " + ", ".join(f"`{t}`" for t in TIPOS) + ".",
           "O resultado ainda deve parecer uma fala natural de pt-BR; mantenha tokens `[xx]` e quebras como estao.",
           "Grave com Write `defeitos.json` = {\"<id>\": {\"target\": \"...\", \"tipo\": \"<tipo>\"}} so para estes casos.", ""]
    for c in casos:
        if c["defeito"]:
            out += [f"## {c['id']}", f"- source: {c['source']}", f"- target: {c['target']}", ""]
    return "\n".join(out)


def montar(pasta, casos: list[dict], defeitos: dict) -> None:
    """Cria padrao/ e cega/ (projetos sinteticos) com os prompts da retrotraducao; mesmo conteudo nos dois."""
    pasta = Path(pasta)
    por_cena: dict[str, list[dict]] = {}
    for c in casos:
        alvo = defeitos[c["id"]]["target"] if c["defeito"] else c["target"]
        por_cena.setdefault(c["scene"], []).append({
            "offset": f"{c['scene']}:{c['id']}", "source": c["source"], "target": alvo,
            "speaker": c["speaker"], "risk_notes": ""})
    for braco, cega in (("padrao", False), ("cega", True)):
        proj = pasta / braco
        proj.mkdir(parents=True, exist_ok=True)
        (proj / "project.json").write_text(
            json.dumps({"title": "bench", "back_translation_cega": cega}), encoding="utf-8")
        for scene, highs in por_cena.items():
            (proj / "artifacts" / "scenes" / scene).mkdir(parents=True, exist_ok=True)
            back_translate.back_translate(proj, scene, highs, backend="in-session")


def _veredictos(proj: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for f in (proj / "artifacts" / "scenes").glob("*/back_translation_*.json"):
        for e in json.loads(f.read_text(encoding="utf-8")).get("entries", []):
            out[str(e.get("offset", "")).split(":")[-1]] = e.get("verdict", "")
    return out


def placar(pasta) -> dict:
    pasta = Path(pasta)
    casos = json.loads((pasta / "casos.json").read_text(encoding="utf-8"))
    defeitos = json.loads((pasta / "defeitos.json").read_text(encoding="utf-8"))
    res: dict = {}
    for braco in ("padrao", "cega"):
        v = _veredictos(pasta / braco)
        com = [c for c in casos if c["defeito"]]
        sem = [c for c in casos if not c["defeito"]]
        pegou = [c for c in com if v.get(c["id"]) == "revise"]
        alarme = [c for c in sem if v.get(c["id"]) == "revise"]
        por_tipo: dict[str, list[int]] = {}
        for c in com:
            t = defeitos[c["id"]]["tipo"]
            por_tipo.setdefault(t, [0, 0])
            por_tipo[t][1] += 1
            por_tipo[t][0] += c in pegou
        res[braco] = {"recall": len(pegou) / len(com) if com else 0.0,
                      "falso_alarme": len(alarme) / len(sem) if sem else 0.0,
                      "sem_veredito": sum(1 for c in casos if c["id"] not in v),
                      "por_tipo": {t: f"{a}/{b}" for t, (a, b) in sorted(por_tipo.items())}}
    p, c = res["padrao"], res["cega"]
    res["adotar_cega"] = (c["recall"] >= p["recall"] + MARGEM and c["falso_alarme"] <= p["falso_alarme"] + MARGEM
                          and p["sem_veredito"] == 0 and c["sem_veredito"] == 0)
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sorteio")
    s.add_argument("projeto")
    s.add_argument("pasta")
    s.add_argument("--n", type=int, default=60)
    s.add_argument("--seed", type=int, default=1)
    s.add_argument("--por-cena", type=int, default=10)
    sub.add_parser("montar").add_argument("pasta")
    sub.add_parser("placar").add_argument("pasta")
    a = ap.parse_args(argv)
    if a.cmd == "sorteio":
        pasta = Path(a.pasta)
        pasta.mkdir(parents=True, exist_ok=True)
        casos = sorteio(a.projeto, a.n, a.seed, a.por_cena)
        (pasta / "casos.json").write_text(json.dumps(casos, ensure_ascii=False, indent=1), encoding="utf-8")
        (pasta / "defeitos_prompt.md").write_text(defeitos_prompt(casos), encoding="utf-8")
        print(f"{len(casos)} casos ({sum(c['defeito'] for c in casos)} com defeito) em {pasta}")
    elif a.cmd == "montar":
        pasta = Path(a.pasta)
        montar(pasta, json.loads((pasta / "casos.json").read_text(encoding="utf-8")),
               json.loads((pasta / "defeitos.json").read_text(encoding="utf-8")))
        print("prompts gerados em padrao/ e cega/")
    else:
        print(json.dumps(placar(a.pasta), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
