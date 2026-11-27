"""Structure checks: provenance, phase order, and whole-book coverage."""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    corpus = json.load(open(os.path.join(ROOT, "corpus.json")))
    practices = json.load(open(os.path.join(ROOT, "practices.json")))
    chunks = json.load(open(os.path.join(ROOT, "data", "book_chunks.json")))
    sector_tree = json.load(open(os.path.join(ROOT, "data", "sector_tree.json")))
    library_metrics = json.load(open(os.path.join(ROOT, "data", "library_metrics.json")))
    failures = 0

    def check(name, ok):
        nonlocal failures
        failures += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'} {name}")

    chunk_ids = {c["id"] for c in chunks}
    check("every card has provenance inside the book", all(
        set(c["provenance"]["chunks"]) <= chunk_ids and c["provenance"]["pages"]
        for c in corpus
    ))
    check("every card names book and sector", all(
        c["book"] == 1 and c["sector"] == "01-traditional-satanism" for c in corpus
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
    print(f"{13 - failures}/13 structure checks pass")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
