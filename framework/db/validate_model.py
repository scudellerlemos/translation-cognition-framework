"""validate_model.py — Revalidação de modelo de embedding por par de idiomas (#170).

Antes de habilitar RAG semântico em produção para um projeto novo, mede a qualidade de
retrieval do modelo (embedder._MODEL_NAME por default, ou --model) contra o par de idiomas
do projeto:
  - exact_match: query = source verbatim -> o próprio hit deve voltar em 1º lugar.
  - vocab_variation: query = paráfrase curada manualmente do source (--paraphrases) ->
    score do hit esperado. Não há gerador automático de paráfrase de qualidade em stdlib/dep
    já instalada (exigiria um LLM externo) — curadoria humana por par de idiomas, como foi
    feito para EN->pt-BR.

Baseline de referência (EN->pt-BR, translation_software, medido no #170):
    exact_match_avg      = 1.0
    vocab_variation_avg  = 0.944
Não é threshold universal (qualidade de embedding varia por par de idiomas) — serve de régua
de comparação manual antes de confiar no retrieval em produção.

Uso:
    python validate_model.py <db_path> <project_id> [--model NOME] [--sample-size N]
                              [--seed N] [--paraphrases paraphrases.json]

Formato de paraphrases.json: lista de {"query": "...", "source": "..."}, onde "source" casa
exatamente com translations.source de uma linha aprovada do projeto.

Amostragem (#185): aleatória sobre TODAS as linhas aprovadas do projeto, via `random.Random`
(não `ORDER BY RANDOM()` do SQLite — evita registrar função seedável na conexão só pra isso).
--seed fixa a amostra pra reprodutibilidade (CI/comparação antes-depois); sem --seed, usa
entropia do SO (amostra diferente a cada rodada, mais representativa em validação manual).
"""
from __future__ import annotations

import random
import sqlite3


def validate_model(con: sqlite3.Connection, project_id: str, model_name: str | None = None,
                    sample_size: int = 20, paraphrases: list[dict] | None = None,
                    seed: int | None = None) -> dict:
    from embedder import Embedder
    emb = Embedder(model_name) if model_name else Embedder()
    emb.index_project(con, project_id, force=True)  # reindexa com o modelo em validação

    all_rows = con.execute(
        "SELECT id, source FROM translations WHERE project_id=? AND approved=1",
        (project_id,),
    ).fetchall()
    if not all_rows:
        raise ValueError(f"nenhuma tradução aprovada em '{project_id}' — nada pra validar")
    rows = random.Random(seed).sample(all_rows, min(sample_size, len(all_rows)))

    exact_scores = []
    for tid, source in rows:
        hits = emb.search(con, source, project_id=project_id, k=1)
        exact_scores.append(hits[0]["score"] if hits and hits[0]["translation_id"] == tid else 0.0)

    vocab_scores = []
    for pair in (paraphrases or []):
        hits = emb.search(con, pair["query"], project_id=project_id, k=5)
        match = next((h for h in hits if h["source"] == pair["source"]), None)
        vocab_scores.append(match["score"] if match else 0.0)

    return {
        "model_name": emb.model_name,
        "project_id": project_id,
        "n_samples": len(rows),
        "seed": seed,
        "exact_match_avg": round(sum(exact_scores) / len(exact_scores), 4),
        "exact_match_min": round(min(exact_scores), 4),
        "n_paraphrases": len(vocab_scores),
        "vocab_variation_avg": round(sum(vocab_scores) / len(vocab_scores), 4) if vocab_scores else None,
    }


if __name__ == "__main__":
    import argparse
    import json
    import sys
    from pathlib import Path
    try:                                              # Windows cp1252: permitir acentos no stdout
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("db_path")
    p.add_argument("project_id")
    p.add_argument("--model", default=None, help="default: modelo pinado em embedder._MODEL_NAME")
    p.add_argument("--sample-size", type=int, default=20)
    p.add_argument("--seed", type=int, default=None,
                    help="fixa a amostra aleatória (reprodutibilidade); default: entropia do SO")
    p.add_argument("--paraphrases", default=None, help="JSON com [{query, source}, ...]")
    args = p.parse_args()

    paraphrases = (json.loads(Path(args.paraphrases).read_text(encoding="utf-8"))
                   if args.paraphrases else None)

    con = sqlite3.connect(args.db_path)
    result = validate_model(con, args.project_id, model_name=args.model,
                             sample_size=args.sample_size, paraphrases=paraphrases,
                             seed=args.seed)
    con.close()

    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("\nBaseline de referência (EN->pt-BR, translation_software, #170): "
          "exact_match_avg=1.0, vocab_variation_avg=0.944.")
    if result["vocab_variation_avg"] is None:
        print("Sem --paraphrases: curar um JSON com paráfrases do par de idiomas antes de "
              "confiar no retrieval em produção.")
