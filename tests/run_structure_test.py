"""Structure checks: provenance, phase order, and whole-book coverage."""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    corpus = json.load(open(os.path.join(ROOT, "corpus.json")))
    practices = json.load(open(os.path.join(ROOT, "practices.json")))
    chunks = json.load(open(os.path.join(ROOT, "data", "book_chunks.json")))
    chunk_sets = {1: {c["id"] for c in chunks}}
    for n in range(2, 11):
        path = os.path.join(ROOT, "data", f"book{n}_chunks.json")
        if os.path.exists(path):
            chunk_sets[n] = {c["id"] for c in json.load(open(path))}
    sector_tree = json.load(open(os.path.join(ROOT, "data", "sector_tree.json")))
    library_metrics = json.load(open(os.path.join(ROOT, "data", "library_metrics.json")))
    failures = 0

    def check(name, ok):
        nonlocal failures
        failures += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'} {name}")

    check("every card has provenance inside the book", all(
        set(c["provenance"]["chunks"]) <= chunk_sets[c["book"]] and c["provenance"]["pages"]
        for c in corpus
    ))
    check("every card names book and sector", all(
        (c["book"], c["sector"]) in {
            (1, "01-traditional-satanism"), (2, "02-luciferianism"),
            (3, "02-luciferianism"), (4, "01-traditional-satanism"),
            (5, "02-luciferianism"), (6, "02-luciferianism"),
            (7, "02-luciferianism"), (8, "02-luciferianism"),
            (9, "02-luciferianism"), (10, "02-luciferianism"),
        }
        for c in corpus
    ))
    orders = [p["order"] for p in practices["phases"]]
    check("phase order is 1..N without gaps", orders == list(range(1, len(orders) + 1)))
    card_ids = {c["id"] for c in corpus}
    check("every phase binds a real technique", all(
        p["technique"] in card_ids for p in practices["phases"]
    ))
    mapped = set()
    for p in practices["phases"]:
        mapped |= set(p["chunks"])
    chunk_ids = chunk_sets[1]
    check("every chunk is mapped or declared", mapped | set(practices["coverage"]["chunks_language_layer"]) == chunk_ids)
    check("exercises are marked derived", all(e["derived"] for e in practices["exercises"]))
    check("gaps registry is non-empty", len(practices["gaps"]) >= 1)

    tree_paths = []
    def collect(node):
        for child in node.get("subfolders", []):
            tree_paths.append(child["repo_path"])
            collect(child)
    for sector in sector_tree["sectors"]:
        collect(sector)
    check("sector tree folders exist", all(
        os.path.isdir(os.path.join(ROOT, path)) for path in tree_paths
    ))
    check("every card path folder exists", all(
        os.path.isdir(os.path.join(ROOT, "sectors", c["sector"], *c["subfolder"].split("/")))
        for c in corpus
    ))
    check("book 1 leaf folder is in the sector tree",
          "sectors/01-traditional-satanism/Demonologia/Lilith" in tree_paths)
    totals = library_metrics["totals"]
    check("library metrics totals reconcile", (
        totals["entries"] == 17927 and totals["pdfs"] == 626
        and totals["pdf_text"] + totals["pdf_scanned"] + totals["pdf_unreadable"] == 626
        and sum(s["entries"] for s in library_metrics["sectors"].values()) + 2 == 17927
    ))
    check("directory accounting reconciles", (
        totals["directories"] == 7 + totals["materialized_subfolders"]
        + library_metrics["kinds"]["mirror"]["dirs"]
        + library_metrics["kinds"]["generated"]["dirs"]
    ))
    check("service levels are measured", (
        library_metrics["service_levels"]["availability_target_percent"] == 99.9
        and library_metrics["service_levels"]["measured_baseline"]["engine_test_result"] == "30/30"
    ))
    def cases_ok(fname):
        data = json.load(open(os.path.join(ROOT, "data", fname)))
        book_pages = {int(k): v for k, v in data["book_pages"].items()}
        return (
            data["cases"] and data["gaps"]
            and all(set(case["techniques"]) <= card_ids for case in data["cases"])
            and all(case["book"] in book_pages for case in data["cases"])
            and all(1 <= case["pages"][0] <= case["pages"][1] <= book_pages[case["book"]]
                    for case in data["cases"])
        )

    check("illuminati cases bind real techniques and pages", cases_ok("illuminati_cases.json"))
    check("maconaria cases bind real techniques and pages", cases_ok("maconaria_cases.json"))
    crossing = json.load(open(os.path.join(ROOT, "data", "crossing.json")))
    books = sorted({c["book"] for c in corpus})
    expected_pairs = sum(
        1 for i, a in enumerate(corpus) for b in corpus[i + 1:] if a["book"] != b["book"]
    )
    check("crossing pairs bind real techniques across books", (
        crossing["books_crossed"] == books and crossing["pairs_measured"] == expected_pairs
        and all(p["a"] in card_ids and p["b"] in card_ids and p["a_book"] != p["b_book"]
                for p in crossing["strongest_pairs"])
        and all(a in card_ids and b in card_ids
                for bridge in crossing["bridges"] for a, b in bridge["pairs"])
    ))
    sys.path.insert(0, ROOT)
    from engine import MODELS, embed_cached, load_session  # noqa: E402
    import numpy as np  # noqa: E402

    session = load_session(MODELS["e5"])
    vecs = embed_cached(session, "e5", [f"{c['title']}. {c['text']}" for c in corpus])
    vecs = vecs / np.linalg.norm(vecs, axis=1, keepdims=True)
    sims = vecs @ vecs.T
    np.fill_diagonal(sims, 0.0)
    check("no duplicated card fingerprint", float(sims.max()) < 0.95)

    print(f"{17 - failures}/17 structure checks pass")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
