"""End-to-end check: known questions must rank their technique first."""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import MODELS, embed, load_session  # noqa: E402

CASES = [
    ("how do I open and close a rite with a banishing", "bt-01"),
    ("should the intention be spoken aloud before the invocation", "bt-02"),
    ("how should participants be seated around the officiant", "bt-03"),
    ("how do two groups alternate a chant without breaking rhythm", "bt-04"),
    ("how does the group hold one image of the deity together", "bt-05"),
    ("what role do drum and music play in the trance", "bt-06"),
    ("how does the group know the moment of incorporation", "bt-07"),
    ("why cast a physical offering into a vessel", "bt-08"),
    ("should both the terrible and beautiful aspects be invoked", "bt-09"),
    ("what should be studied before the rite begins", "bt-10"),
    ("why use a sacred language for the central invocation", "bt-11"),
    ("how does the rite close with gratitude", "bt-12"),
]


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "corpus.json"), encoding="utf-8") as f:
        corpus = json.load(f)
    failures = 0
    for name in ("e5", "minilm"):
        session = load_session(MODELS[name])
        docs = [f"{item['title']}. {item['text']}" for item in corpus]
        doc_vecs = embed(session, docs)
        doc_vecs = doc_vecs / np.linalg.norm(doc_vecs, axis=1, keepdims=True)
        for question, expected in CASES:
            qv = embed(session, [question])[0]
            qv = qv / np.linalg.norm(qv)
            top = corpus[int(np.argmax(doc_vecs @ qv))]["id"]
            ok = top == expected
            failures += 0 if ok else 1
            print(f"{name} {'PASS' if ok else 'FAIL'} {expected} -> {top} | {question}")
    total = len(CASES) * 2
    print(f"{total - failures}/{total} top-1 correct")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
