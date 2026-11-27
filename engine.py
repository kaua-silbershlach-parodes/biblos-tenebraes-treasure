#!/usr/bin/env python3
"""Semantic search over the hardening techniques in corpus.json.

The engine is Oracle's own augmented ONNX embedding models, run
unchanged: the tokenizer and the pre/post-processing are baked into
each model file by Oracle, so the input is raw text and the output is
a 384-dimension embedding. Ranking is cosine similarity between the
query embedding and each technique's embedding.

Models (in models/, Oracle's prebuilt augmented exports):
  minilm  all_MiniLM_L12_v2.onnx   - English-first, 384 dimensions
  e5      multilingual_e5_small.onnx - 100 languages, 384 dimensions

Usage:
  python engine.py "how do I refuse unknown routes by default"
  python engine.py "como limitar permissoes de um componente" --model e5 --top 3

Requires: onnxruntime, onnxruntime-extensions, numpy
(see requirements.txt). The augmented graphs use a custom tokenizer
operator from the ONNX Runtime extensions library; without it the
model files do not load.
"""

import argparse
import hashlib
import json
import os
import sys

import numpy as np
import onnxruntime as ort
from onnxruntime_extensions import get_library_path

ROOT = os.path.dirname(os.path.abspath(__file__))
MODELS = {
    "minilm": os.path.join(ROOT, "models", "all_MiniLM_L12_v2.onnx"),
    "e5": os.path.join(ROOT, "models", "multilingual_e5_small.onnx"),
}
DIMS = 384


def load_session(model_path):
    opts = ort.SessionOptions()
    opts.register_custom_ops_library(get_library_path())
    return ort.InferenceSession(
        model_path, sess_options=opts, providers=["CPUExecutionProvider"]
    )


def embed(session, texts):
    inp = session.get_inputs()[0]
    parts = []
    for start in range(0, len(texts), 16):
        batch = texts[start:start + 16]
        outs = session.run(None, {inp.name: np.array(batch, dtype=object)})
        for out in outs:
            arr = np.asarray(out, dtype=np.float64)
            if arr.ndim == 2 and arr.shape[1] == DIMS:
                parts.append(arr)
                break
        else:
            raise RuntimeError("model produced no 384-dimension embedding output")
    return np.concatenate(parts, axis=0)


def embed_cached(session, model_name, texts):
    """Embed documents once, then reuse: keyed by model + exact texts.

    Book 2's Private Intelligence Advantage applied to the engine itself:
    repeated searches must not pay the full embedding cost again.
    """
    key = hashlib.sha256(
        (model_name + "\n" + "\n".join(texts)).encode("utf-8")
    ).hexdigest()
    cache_dir = os.path.join(ROOT, "data", ".embedding-cache")
    cache_file = os.path.join(cache_dir, key + ".npy")
    if os.path.exists(cache_file):
        vecs = np.load(cache_file)
        if vecs.shape == (len(texts), DIMS):
            return vecs
    vecs = embed(session, texts)
    os.makedirs(cache_dir, exist_ok=True)
    np.save(cache_file, vecs)
    return vecs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="the question to match against the techniques")
    parser.add_argument(
        "--model",
        choices=sorted(MODELS),
        default="e5",
        help="e5 (multilingual, default) or minilm (English-first)",
    )
    parser.add_argument("--top", type=int, default=3, help="how many results to print")
    parser.add_argument(
        "--book",
        action="store_true",
        help="search the whole book chunks (data/book_chunks.json) instead of the technique cards",
    )
    parser.add_argument(
        "--book2",
        action="store_true",
        help="search the second book chunks (data/book2_chunks.json) instead of the technique cards",
    )
    parser.add_argument(
        "--sector",
        default=None,
        help="route the search to one sector (e.g. 01-traditional-satanism)",
    )
    args = parser.parse_args()

    session = load_session(MODELS[args.model])
    query_vec = embed(session, [args.query])[0]
    query_vec = query_vec / np.linalg.norm(query_vec)

    if args.book or args.book2:
        chunk_file = "book2_chunks.json" if args.book2 else "book_chunks.json"
        chunk_path = "02-luciferianism/1995 - Iluminattis/book-2" if args.book2 else "01-traditional-satanism/Demonologia/Lilith/book-1"
        with open(os.path.join(ROOT, "data", chunk_file), encoding="utf-8") as f:
            chunks = json.load(f)
        doc_vecs = embed_cached(session, args.model, [c["text"] for c in chunks])
        doc_vecs = doc_vecs / np.linalg.norm(doc_vecs, axis=1, keepdims=True)
        scores = doc_vecs @ query_vec
        order = np.argsort(-scores)[: args.top]
        for rank, idx in enumerate(order, 1):
            c = chunks[idx]
            print(f"{rank}. [chunk {c['id']} · page {c['page']} · {chunk_path}] {scores[idx]:.3f}")
        if scores[order[0]] < 0.35:
            print("Weak match: the best passage is only loosely related to the question.")
        return 0

    with open(os.path.join(ROOT, "corpus.json"), encoding="utf-8") as f:
        corpus = json.load(f)
    if args.sector:
        corpus = [c for c in corpus if c.get("sector") == args.sector]
        if not corpus:
            print(f"no techniques routed to sector {args.sector}")
            return 1

    docs = [f"{item['title']}. {item['text']}" for item in corpus]
    doc_vecs = embed_cached(session, args.model, docs)
    doc_vecs = doc_vecs / np.linalg.norm(doc_vecs, axis=1, keepdims=True)
    scores = doc_vecs @ query_vec

    order = np.argsort(-scores)[: args.top]
    for rank, idx in enumerate(order, 1):
        item = corpus[idx]
        print(f"{rank}. [{item['id']}] {item['title']} — {scores[idx]:.3f} · {item['path']}")
    if scores[order[0]] < 0.35:
        print("Weak match: the best technique is only loosely related to the question.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
