"""rag_eval.py — conjunto de avaliacao SINTETICO do RAG (busca semantica na TM) com recall@k e MRR.

Cada caso e (frase indexada, consulta parafraseada com outras palavras): o RAG acerta se a frase indexada
volta no top-k da consulta. O corpus e inventado (nada de jogo, nada de wiki). Roda com o modelo real no
workflow ML (`ml-coverage-optional.yml`); `test_rag_eval.py` compara o resultado com o piso e com o baseline
(`rag_eval_baseline.json`): queda do recall abaixo do piso, ou mais de MARGEM abaixo do baseline, falha o CI.

Uso: python rag_eval.py [--write-baseline]
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
for _p in (_HERE, _HERE.parent / "runtime"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import paths  # noqa: E402

BASELINE = _HERE / "rag_eval_baseline.json"
KS = (1, 3, 5)
PISO = {"recall@1": 0.85, "recall@3": 0.95, "recall@5": 0.95}     # medido: 0,95 / 1,0 / 1,0
MARGEM = 0.05                                                       # queda tolerada em relacao ao baseline

# (frase indexada, consulta com palavras diferentes)
CASOS: list[tuple[str, str]] = [
    ("The old man walked slowly to the market.", "An elderly gentleman strolled to the bazaar."),
    ("She opened the heavy wooden door.", "The woman pushed open a thick door made of timber."),
    ("We must leave the village before sunrise.", "We have to depart from the town prior to dawn."),
    ("The sword was sharper than any blade he had seen.", "He had never seen a weapon so keen."),
    ("Rain fell on the quiet harbor all night.", "It poured over the silent port throughout the evening."),
    ("Please bring me a cup of hot tea.", "Could you fetch a warm mug of tea for me?"),
    ("The king refused to listen to his advisors.", "The monarch would not heed his counselors."),
    ("A cold wind blew across the empty field.", "A chilly breeze swept over the barren meadow."),
    ("He promised to return before the festival began.", "He swore he would come back ahead of the celebration."),
    ("The children laughed and ran through the garden.", "Kids giggled while sprinting across the yard."),
    ("Nobody knew where the traveler had come from.", "The wanderer's origin was a mystery to everyone."),
    ("The bridge collapsed under the weight of the cart.", "The wagon was too heavy and the span gave way."),
    ("I am afraid we have lost the way.", "Unfortunately, we no longer know the right path."),
    ("The healer mixed herbs into a bitter drink.", "The medic blended plants into an unpleasant potion."),
    ("Thunder shook the walls of the castle.", "The fortress trembled from the roar of the storm."),
    ("She kept the letter hidden in her sleeve.", "The note was concealed inside her cuff."),
    ("The soldiers marched toward the northern pass.", "Troops advanced on the mountain gap to the north."),
    ("He could not forgive what his brother had done.", "What his sibling did was beyond his pardon."),
    ("The fire burned low in the empty hall.", "The flames were dying in the deserted chamber."),
    ("Tell me the truth, and I will help you.", "Be honest with me and I shall assist you."),
    ("A single candle lit the narrow stairway.", "Only one taper illuminated the tight staircase."),
    ("The merchant counted his coins twice.", "The trader tallied his money two times."),
    ("They shared bread and stories by the river.", "Beside the stream they split a loaf and told tales."),
    ("The boy was too proud to ask for help.", "Pride kept the lad from requesting assistance."),
    ("A bell rang somewhere in the distance.", "Far away, a chime sounded."),
    ("The map showed a hidden path through the forest.", "The chart revealed a secret trail among the trees."),
    ("He woke up with a terrible headache.", "He got out of bed with a pounding skull."),
    ("The queen smiled but her eyes stayed cold.", "Her majesty grinned, yet her gaze was icy."),
    ("We will meet again when the snow melts.", "We shall see each other once the ice thaws."),
    ("The ship disappeared into the fog.", "The vessel vanished in the mist."),
    ("Do not touch anything in this room.", "Leave every object in this chamber alone."),
    ("The teacher praised her for the careful work.", "The instructor complimented her on the meticulous effort."),
    ("An owl watched them from the high branch.", "From atop a tall bough, a night bird stared at them."),
    ("The price of bread has doubled this winter.", "A loaf costs twice as much during this cold season."),
    ("He swore an oath on his mother's grave.", "On his mother's tomb he made a vow."),
    ("The river was too wide to cross on foot.", "You could not wade over that broad stream."),
    ("Someone had been here before us.", "Another person had already visited this place."),
    ("The old clock stopped at midnight.", "At twelve o'clock the ancient timepiece ceased ticking."),
    ("She sang softly to calm the frightened horse.", "She hummed quietly so the scared stallion would settle."),
    ("Everything changed after the accident.", "Nothing was the same following the mishap."),
]


def avaliar(emb, con, project_id: str = "rag") -> dict:
    """recall@k e MRR: a frase indexada de cada caso volta no top-k da consulta parafraseada?"""
    ranks = []
    for fonte, consulta in CASOS:
        hits = emb.search(con, consulta, project_id=project_id, k=max(KS))
        srcs = [h["source"] for h in hits]
        ranks.append(srcs.index(fonte) + 1 if fonte in srcs else None)
    n = len(ranks)
    out = {f"recall@{k}": round(sum(r is not None and r <= k for r in ranks) / n, 3) for k in KS}
    out["mrr"] = round(sum(1 / r for r in ranks if r) / n, 3)
    out["n_casos"] = n
    return out


def executar() -> dict:
    """Indexa o corpus sintetico num banco temporario com o modelo REAL e avalia."""
    import embedder
    from store import Store
    emb = embedder.Embedder()
    with tempfile.TemporaryDirectory() as d, Store(Path(d) / "rag.db") as db:
        db.upsert_project("rag", "RAG eval")
        for i, (fonte, _) in enumerate(CASOS):
            db.upsert_translation("rag", "s", f"o{i}", source=fonte, target=f"alvo {i}", approved=True)
        emb.index_project(db._con, "rag")
        return avaliar(emb, db._con)


def problemas(res: dict, baseline: dict | None) -> list[str]:
    """Piso absoluto + queda em relacao ao baseline. Vazio = ok."""
    out = [f"{k} = {res[k]} abaixo do piso {v}" for k, v in PISO.items() if res[k] < v]
    if baseline:
        out += [f"{k} caiu de {baseline[k]} para {res[k]} (margem {MARGEM})"
                for k in PISO if k in baseline and res[k] < baseline[k] - MARGEM]
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Avalia o RAG (recall@k/MRR) num corpus sintetico.")
    ap.add_argument("--write-baseline", action="store_true")
    a = ap.parse_args()
    res = executar()
    print(json.dumps(res, indent=2))
    if a.write_baseline:
        paths.atomic_write(BASELINE, json.dumps(res, indent=2) + "\n")
        return 0
    base = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.is_file() else None
    probs = problemas(res, base)
    for p in probs:
        print(f"RAG REGREDIU: {p}")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
