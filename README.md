# Biblos Tenebraes Treasure

The Morningstar library of A Elite Estrangeira, turned into a searchable
engine: **17,927 entries** across seven sectors, with **626 PDFs** (551 with
a native text layer, 74 scanned/image, 1 unreadable). Book names are not
published — only the totals and the sector structure. See
[LIBRARY_SECTORS.md](LIBRARY_SECTORS.md).

The library is read one book at a time, smallest first. Each book becomes a
set of technique cards in `corpus.json`, and the engine ranks those cards
against a plain-words question. Two books are in: 27 techniques.

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
  (**the whole first book converted**: every chunk of its 3 pages, 46
  sentence-level chunks, each with both model vectors), so the complete
  source is in the dump, not only the derived cards.
- `tests/run_engine_test.py` — known questions that must rank their
  technique first, under both models.

## Techniques from the first book — Traditional Satanism / Demonologia / Lilith

The first book read sits at the full path **Traditional Satanism →
Demonologia → Lilith**
(`sectors/01-traditional-satanism/Demonologia/Lilith`): the sector holds
**177 entries of 17,927 in the whole library (0.99%)**, the Demonologia
subfolder holds 60, and the Lilith sub-subfolder holds 17. Its 15
techniques:

**Frame the work**

- Banishing Frame — open and close every working with a banishing.
- Candlelit Space — the working space lit and set apart first.
- Spoken Intention — state the intention aloud before any invocation.
- Thanksgiving and Closure — gratitude first, then the final banishing.

**Hold the circle**

- Circle Formation — participants equidistant around the officiant.
- Single Entry — each participant enters alone, one at a time.
- Alternating Mantra — two voices exchanging the chant.
- Sound as Trance Driver — drum, music, and chant carrying the state.

**Call the deity**

- Shared Visualization — one concrete image held by the whole group.
- Dual-Aspect Invocation — the terrible and the beautiful together.
- Sacred Language — words set apart for the central invocation.
- Incorporation Signal — a clear mark for the moment of transition.
- Cast Offering — a physical act repeated by each participant.
- Separation Before Closure — the group separates before the final thanks.
- Myth Study First — names, aspects, and history known beforehand.

## Techniques from the second book — Luciferianism / 1995 - Iluminattis

The second book read is the smallest of the three text PDFs in the
**1995 - Iluminattis** subfolder (292 pages, 204,330 words), at the full
path **Luciferianism → 1995 - Iluminattis**
(`sectors/02-luciferianism/1995 - Iluminattis`): the sector holds 107
entries, and the subfolder holds 3. Its whole text is converted into
13,179 sentence-level chunks (`data/book2_chunks.json`), and its 14
family cases are catalogued in `data/illuminati_cases.json` — the book's
claims in derived words, with their evidence gaps kept visible. Its 12
techniques:

- Bloodline Mapping — power traced through descent and intermarriage.
- Front Structures and Proxies — influence through respectable cover bodies.
- Controlled Opposition — managed conflict producing a chosen outcome.
- Information Control — history, press, and reputation as controlled channels.
- Advisor Placement — gatekeepers beside decision-makers.
- Monopoly Formation — privilege and cartels becoming durable control.
- Secrecy Discipline — compartmentation and cover lives.
- Private Intelligence Advantage — couriers and coded correspondence.
- Institutional Capture by Funding — grant dependence aligning institutions.
- Crisis-to-Institution Sequence — panics justifying central authorities.
- Sealing and Oath Binding — vows sealed through exchanged objects.
- Wholesome-Front Deception — a trusted brand lowering the guard.

## Verified

- Local engine: 54/54 known questions rank their technique first, under
  both models.
- Reading control (`tools/reading_control.py`): every one of the first
  book's 46 chunks is mapped to a phase or declared, every one of the 27
  cards is supported by its own provenance chunks in its own book, and
  every named tool appears in the chunks its phase cites — PASS.
- Full Oracle suite (`tests/run_full_suite_linux.py`, the same suite that
  verifies the writing engine): **14 PASS + 2 BLOCKED** on Oracle AI
  Database 26ai — exact and approximate search agree with the local engine
  (8/8 top-1), HNSW and IVF indexes, hybrid search, external table, five
  distance metrics, Private AI container embeddings, CLIP text encoder,
  chunking, RAG retrieval, and ORDS REST all pass. The 2 BLOCKED are text
  generation: the running Private AI container serves no LLM.
- The dump round-trips: import restores the technique rows and all 46
  book chunks with their vector pairs.
- Whole-book search: over the 46 chunks of the complete first book, the
  engine returns the exact passage with its chunk and page, and every
  result carries the full path
  `01-traditional-satanism/Demonologia/Lilith/book-1`. The second book's
  13,179 chunks search the same way under
  `02-luciferianism/1995 - Iluminattis/book-2` (`--book2`).

Copyright (c) A Elite Estrangeira.
