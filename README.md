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
- `data/techniques.dmp` — the techniques table as an Oracle Data Pump dump,
  exported with the embedding vectors already populated, so an import
  queries immediately.
- `tests/run_engine_test.py` — known questions that must rank their
  technique first, under both models.

## Techniques from the first book

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
- Oracle AI Database 26ai (lab): both models loaded in-database, 12/12
  vector pairs populated, in-database search returns the same top technique
  as the local engine.
- The dump round-trips: import restores 12 rows with 12/12 non-null vector
  pairs.

Copyright (c) A Elite Estrangeira.
