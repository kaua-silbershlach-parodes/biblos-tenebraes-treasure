"""Structure checks: provenance, phase order, and whole-book coverage."""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    corpus = json.load(open(os.path.join(ROOT, "corpus.json")))
    practices = json.load(open(os.path.join(ROOT, "practices.json")))
    chunks = json.load(open(os.path.join(ROOT, "data", "book_chunks.json")))
    chunks2 = json.load(open(os.path.join(ROOT, "data", "book2_chunks.json")))
    chunk_sets = {1: {c["id"] for c in chunks}, 2: {c["id"] for c in chunks2}}
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
        (c["book"], c["sector"]) in {(1, "01-traditional-satanism"), (2, "02-luciferianism")}
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
    cases = json.load(open(os.path.join(ROOT, "data", "illuminati_cases.json")))
    check("illuminati cases bind real techniques and pages", (
        cases["book"] == 2 and len(cases["cases"]) == 14 and cases["gaps"]
        and all(set(case["techniques"]) <= card_ids for case in cases["cases"])
        and all(1 <= case["pages"][0] <= case["pages"][1] <= cases["pages"] for case in cases["cases"])
    ))
    crossing = json.load(open(os.path.join(ROOT, "data", "crossing.json")))
    check("crossing pairs bind real techniques across books", (
        crossing["books_crossed"] == [1, 2] and crossing["pairs_measured"] == 180
        and all(p["a"] in card_ids and p["b"] in card_ids and p["a_book"] != p["b_book"]
                for p in crossing["strongest_pairs"])
        and all(a in card_ids and b in card_ids
                for bridge in crossing["bridges"] for a, b in bridge["pairs"])
    ))
    print(f"{15 - failures}/15 structure checks pass")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
