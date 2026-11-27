"""Cross the books: measure which techniques of different books meet.

Embeds every technique card, computes cross-book cosine pairs, and writes
data/crossing.json with the strongest pairs and the bridges they form.
Interpretation stays in derived words; scores are the measurement.
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import MODELS, embed, load_session  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    corpus = json.load(open(os.path.join(ROOT, "corpus.json"), encoding="utf-8"))
    session = load_session(MODELS["e5"])
    docs = [f"{c['title']}. {c['text']}" for c in corpus]
    vecs = embed(session, docs)
    vecs = vecs / np.linalg.norm(vecs, axis=1, keepdims=True)

    pairs = []
    for i, a in enumerate(corpus):
        for j, b in enumerate(corpus):
            if j <= i or a["book"] == b["book"]:
                continue
            pairs.append({
                "score": round(float(vecs[i] @ vecs[j]), 3),
                "a": a["id"], "a_title": a["title"], "a_book": a["book"],
                "b": b["id"], "b_title": b["title"], "b_book": b["book"],
            })
    pairs.sort(key=lambda p: -p["score"])

    crossing = {
        "books_crossed": sorted({c["book"] for c in corpus}),
        "model": "e5",
        "pairs_measured": len(pairs),
        "strongest_pairs": pairs[:12],
        "bridges": [
            {
                "name": "The sealed boundary",
                "reading": "Both books seal a boundary before work begins: the rite opens and closes with a banishing, the order binds vows with seals and oaths. What forms is one operation at two scales — a protected space whose edge is marked and guarded.",
                "pairs": [["bt-01", "bt-26"], ["bt-03", "bt-22"], ["bt-14", "bt-22"]],
            },
            {
                "name": "Two sides held in one frame",
                "reading": "The rite invokes the terrible and the beautiful together; the power book steers thesis against antithesis toward a managed outcome. What forms is the discipline of holding opposed forces inside a single frame instead of choosing one side.",
                "pairs": [["bt-09", "bt-18"], ["bt-05", "bt-18"], ["bt-04", "bt-18"]],
            },
            {
                "name": "The circle and the front",
                "reading": "Participants sit equidistant around a center; institutions stand as a visible ring while direction sits at the hidden center. What forms is the same geometry: a public circumference, a directing middle.",
                "pairs": [["bt-03", "bt-17"], ["bt-05", "bt-17"], ["bt-01", "bt-17"]],
            },
        ],
        "note": "Scores are e5 cosine similarities between derived technique cards. Bridges are readings of the strongest measured pairs, in derived words; they assert structure, not historical fact.",
    }
    out = os.path.join(ROOT, "data", "crossing.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(crossing, f, ensure_ascii=False, indent=1)
    print(f"crossing written: {len(pairs)} pairs measured, top {pairs[0]['score']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
