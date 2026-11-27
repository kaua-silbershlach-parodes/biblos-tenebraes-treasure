# Biblos Tenebraes Treasure

The Morningstar library of A Elite Estrangeira, turned into a searchable
engine: **17,927 entries** across seven sectors, with **626 PDFs** (551 with
a native text layer, 74 scanned/image, 1 unreadable). Book names are not
published — only the totals and the sector structure. See
[LIBRARY_SECTORS.md](LIBRARY_SECTORS.md).

The library is read one book at a time, smallest first. Each book becomes a
set of technique cards in `corpus.json`, and the engine ranks those cards
against a plain-words question. The first book is in: 12 techniques.

## The engine

The same Oracle-powered engine used across A Elite Estrangeira projects:

- `engine.py` — local semantic search over `corpus.json` with two ONNX
  embedding models (multilingual-e5-small and all-MiniLM-L12-v2, augmented
  builds), served from `models/` through Git LFS.
- `db_engine.py` — the database modes: vector search, approximate search,
  hybrid search, model provider, RAG, and REST, against an Oracle AI
  Database.
- `data/techniques.dmp` — the Oracle Data Pump dump with the embedding
  vectors already populated, so an import queries immediately. It carries
  two tables: `techniques` (the derived technique cards) and `book_chunks`
  (**the whole first book converted**: every chunk of its 3 pages, 22
  chunks, each with both model vectors), so the complete source is in the
  dump, not only the derived cards.
- `tests/run_engine_test.py` — known questions that must rank their
  technique first, under both models.

## Techniques from the first book — sector: Traditional Satanism

The first book read comes from the **Traditional Satanism** sector:
**177 entries in this sector, of 17,927 in the whole library (0.99%)**.
Its 12 techniques:

**Frame the work**

- Banishing Frame — open and close every working with a banishing.
- Spoken Intention — state the intention aloud before any invocation.
- Thanksgiving and Closure — gratitude first, then the final banishing.

**Hold the circle**

- Circle Formation — participants equidistant around the officiant.
- Alternating Mantra — two voices exchanging the chant.
- Sound as Trance Driver — drum, music, and chant carrying the state.

**Call the deity**

- Shared Visualization — one concrete image held by the whole group.
- Dual-Aspect Invocation — the terrible and the beautiful together.
- Sacred Language — words set apart for the central invocation.
- Incorporation Signal — a clear mark for the moment of transition.
- Cast Offering — a physical act repeated by each participant.
- Myth Study First — names, aspects, and history known beforehand.

## Verified

- Local engine: 24/24 known questions rank their technique first, under
  both models.
- Full Oracle suite (`tests/run_full_suite_linux.py`, the same suite that
  verifies the writing engine): **14 PASS + 2 BLOCKED** on Oracle AI
  Database 26ai — exact and approximate search agree with the local engine
  (8/8 top-1), HNSW and IVF indexes, hybrid search, external table, five
  distance metrics, Private AI container embeddings, CLIP text encoder,
  chunking, RAG retrieval, and ORDS REST all pass. The 2 BLOCKED are text
  generation: the running Private AI container serves no LLM.
- The dump round-trips: import restores 12 rows with 12/12 non-null vector
  pairs.
- Whole-book search: over the 22 chunks of the complete first book, the
  in-database top-10 equals the local engine's top-10 exactly under
  MiniLM (4/4 reference queries). Under e5 the top-10 sets agree with
  small order differences in the middle ranks, from runtime precision.

Copyright (c) A Elite Estrangeira.
