# Biblos Tenebraes Treasure

The Morningstar library of A Elite Estrangeira, turned into a searchable
engine: **17,927 entries** across seven sectors, with **626 PDFs** (551 with
a native text layer, 74 scanned/image, 1 unreadable). Book names are not
published — only the totals and the sector structure. See
[LIBRARY_SECTORS.md](LIBRARY_SECTORS.md).

The library is read one book at a time, smallest first. Each book becomes a
set of technique cards in `corpus.json`, and the engine ranks those cards
against a plain-words question. Ten books are in: 141 techniques.

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
  two tables: `techniques` (all 141 derived technique cards) and `book_chunks`
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

## Techniques from books 3 to 10 — Maçonaria and 1995 - Iluminattis

The six Maçonaria text PDFs (five in Luciferianism, one in Traditional
Satanism) and the two remaining 1995 - Iluminattis books were read whole,
smallest first, and converted into sentence-level chunks
(`data/book3_chunks.json` … `data/book10_chunks.json`). Their cases are
catalogued in `data/maconaria_cases.json` (40 cases) and
`data/illuminati_cases.json` (28 cases) — claims in derived words, with
evidence gaps kept visible.

- **Book 3** — Luciferianism / Maçonaria, 11 pages, 312 chunks, 8
  techniques: Federation by Assembly, Archival Codification, Regularity
  as Exported Standard, Temple Symbolism as Moral Template, Lodge as
  Workshop, Admission Testing by Greeting, Degree Ladder, Founding-Date
  Challenge by Minutes.
- **Book 4** — Traditional Satanism / Maçonaria, 20 pages, 746 chunks, 10
  techniques: Source-Trail Argument, Original-versus-Interpolation
  Reading, Initiatory Equivalence Mapping, Sacrificed-God Genealogy,
  Symbol Decoding, Egregore Formation, Absorption and Demonization,
  Creed as Political Code, Catechism Conditioning Audit, Fruit Test.
- **Book 5** — Luciferianism / Maçonaria, 86 pages, 2,481 chunks, 12
  techniques: Zero as Latent Field, Point in Circle Manifestation,
  Involution and Evolution, Polarity as Instruction, Third-Term Triangle
  Formation, Triangle Equality Test, Grade-Staged Symbol Disclosure,
  Four as Materialization, Five as Anti-Equilibrium, Septenary
  Correspondence, Eightfold Conduct Audit, Decalogue as Lodge Ethics.
- **Book 6** — Luciferianism / Maçonaria, 287 pages, 4,247 chunks, 12
  techniques: Evidence Taxonomy First, Chronology as Falsification,
  Plagiarism Fingerprinting, Witness Credibility Audit, Motive Audit,
  Language Forensics, Invented Geography Test, List Falsification by
  Denial, Place and Jurisdiction Verification, Source-Subtraction Audit,
  Authority Laundering, Denial-Proof Design.
- **Book 7** — Luciferianism / 1995 - Iluminattis, 304 pages, 13,222
  chunks, 12 techniques, all catalogued as claimed patterns with their
  evidence gaps: Assessment Before Structuring, Hidden Core with Decoy
  Fronts, Double-Bind Split Model, Layered Access Codes, Story-Script
  Mapping, Esoteric Dual Language, Gatekeeper Layering, Internal-World
  Structuring, Defense in Depth and Backups, Milieu Control, Media
  Trigger Catalog, Disbelief Barrier.
- **Book 8** — Luciferianism / Maçonaria, 304 pages, 5,380 chunks, 17
  techniques: Cross-Cultural Genealogy of Angelology, Fall as Deliberate
  Incarnation, Planetary Correspondence Mapping, Hierarchical Ascent
  through Spheres, Threefold Spiritual Typology, Sacred-Center Axis
  Construction, Preservation through Catastrophe, Liminal Crossing,
  Twin-Pillar Polarity Framing, Graded Recognition System,
  Death-and-Raising Pattern, Serpent as Teacher, Inner Outer Teaching
  Split, Lineage Preservation through Exile, Durable-Media Preservation,
  Charter-Based Transmission, Archangel Correspondence Table.
- **Book 9** — Luciferianism / 1995 - Iluminattis, 588 pages, 6,350
  chunks, 12 techniques, claimed patterns catalogued with gaps:
  Visual-Evidence Accumulation, Secrecy Architecture, Plain-Sight
  Signaling, Handshake Recognition Test, Penal Signs and Due Guards,
  X as Transformation Marker, Double-Headed Eagle Duality, Great Seal
  Decoding, Oath-Penalty Secrecy System, Triangle Polarity System,
  Photo-Caption Case Method, Star Talisman System.
- **Book 10** — Luciferianism / Maçonaria, 592 pages, 19,185 chunks, 31
  techniques: Mystery-School Transmission, Mediated Oracle Pipeline,
  Cave-Descent Incubation, Graded Initiation with Delayed Access,
  Aphorism as Compressed Instruction, Letter-Value Analysis, Body-as-Map
  Teaching, Graded Custody of Words and Signs, Ratio-Based Harmony,
  Emblem Selection by Observed Habit, Tree as Systems Diagram,
  Protective-Circle Construction, Two-Layer Encoding, Trial-Gated
  Admission, Architecture as Curriculum, Fragment Inventory and
  Reassembly, Descent Stripping and Return, Correspondence-Table Method,
  Gate and Ring Ascent, Encoded-Text Reading, Temple-Body
  Internalization, Hidden-Order Operating Model, Alchemical Process
  Ladders, Operator-Qualification Rule, Color-Sequence Reading,
  Seven-Stage Initiation Journey, Cipher Taxonomy Before Decoding,
  Three-Temple Mapping, Sevenfold Ascent Mapping, Guardian-Spirit Quest,
  Pictographic Degree Records.

## The crossing — what forms between the books

`tools/cross_books.py` embeds every technique card and measures the 8,761
cross-book pairs (`data/crossing.json`). Six bridges form:

- **The sealed boundary** — the rite opens and closes with a banishing;
  the order binds vows with seals and oaths. One operation at two scales:
  a protected space whose edge is marked and guarded.
- **Two sides held in one frame** — the terrible and the beautiful
  invoked together; thesis steered against antithesis. The discipline of
  holding opposed forces inside a single frame.
- **The circle and the front** — participants equidistant around a
  center; institutions as a visible ring with direction at the hidden
  middle. A public circumference, a directing center.
- **The correspondence table** — planets, metals, organs, letters, and
  seasons bound into one table in book after book. One reading
  instrument: balance and polarity judged through the table.
- **Secrecy as architecture** — compartmentation, oath penalties, graded
  custody of words, and plain-sight signaling recur as one design:
  layers, locks, and decoy surfaces.
- **Reading the corrupted text** — original against interpolation,
  encoded reading, and the audit of witnesses converge on one discipline:
  never trust the surface until the text survives its own audit.

## The engine applied to itself

The second book's techniques, turned on the engine that carries them:

- **Private Intelligence Advantage** → document embeddings are cached
  (`data/.embedding-cache/`, keyed by model and exact texts), so repeated
  searches do not pay the full embedding cost again.
- **Bloodline Mapping** → provenance is checked as a graph: every case
  binds real technique cards and real pages, every crossing pair binds
  real cards across books (structure test).
- **Two sides held in one frame** → results hold their own weakness:
  a top score under 0.35 is printed as a weak match instead of passing
  as a finding.

The ten books, turned on the engine again:

- **Myth Study First / Source-Trail Argument** → routing before
  retrieval: `--only-book N` narrows the technique search to one book
  before ranking, and fails closed when nothing is routed there.
- **Evidence Taxonomy First** → every result carries its evidence tier
  (strong ≥ 0.80, moderate ≥ 0.50, weak below), not only a weak flag.
- **Source-Subtraction Audit** → the structure test fingerprints the
  corpus: no two cards may be near-duplicates (max pair 0.921, gate
  0.95).
- **Fragment Inventory and Reassembly** → a missing piece is named, not
  hidden: a missing chunk file or corpus stops the engine with the
  missing path printed.
- **Encoded-Text Reading / Original-versus-Interpolation** → `--both`
  takes a second reading with the other model and reports whether the
  two readings agree on the top technique.

## Verified

- Local engine: 282/282 known questions rank their technique first, under
  both models.
- Reading control (`tools/reading_control.py`): every one of the first
  book's 46 chunks is mapped to a phase or declared, every one of the 141
  cards is supported by its own provenance chunks in its own book, and
  every named tool appears in the chunks its phase cites — PASS.
- Full Oracle suite (`tests/run_full_suite_linux.py`, the same suite that
  verifies the writing engine): **14 PASS + 2 BLOCKED** on Oracle AI
  Database 26ai — exact and approximate search agree with the local engine
  (8/8 top-1), HNSW and IVF indexes, hybrid search, external table, five
  distance metrics, Private AI container embeddings, CLIP text encoder,
  chunking, RAG retrieval, and ORDS REST all pass. The 2 BLOCKED are text
  generation: the running Private AI container serves no LLM.
- The dump round-trips: import restores all 141 technique rows and all 46
  book chunks with their vector pairs (942,080 bytes).
- Whole-book search: over the 46 chunks of the complete first book, the
  engine returns the exact passage with its chunk and page, and every
  result carries the full path
  `01-traditional-satanism/Demonologia/Lilith/book-1`. Every book searches
  the same way (`--bookN N`): 65,148 chunks across the ten books, each
  result carrying its sector, subfolder, and book path.

Copyright (c) A Elite Estrangeira.
