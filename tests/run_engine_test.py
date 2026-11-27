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
    ("should participants enter the space one at a time", "bt-13"),
    ("why separate the participants before the closing", "bt-14"),
    ("how should the working space be lit", "bt-15"),
    ("how is power traced through descent intermarriage and surname changes", "bt-16"),
    ("how does influence move through foundations banks and cover bodies", "bt-17"),
    ("how are two managed sides staged so conflict produces a chosen outcome", "bt-18"),
    ("how are history education press and reputation controlled", "bt-19"),
    ("why place advisers and gatekeepers beside decision makers", "bt-20"),
    ("how do privilege cartels and state contracts become monopoly control", "bt-21"),
    ("how do compartmentation oral orders and cover lives protect secrecy", "bt-22"),
    ("why do private couriers and coded correspondence give an intelligence advantage", "bt-23"),
    ("how does grant dependence capture universities churches and media", "bt-24"),
    ("how do banking panics justify new central authorities", "bt-25"),
    ("how are vows sealed with exchanged objects and oaths", "bt-26"),
    ("how does a trusted family brand lower the audience guard", "bt-27"),
    ('how do separate lodges federate by electing a grand master', 'bt-28'),
    ('how does writing constitutions shift control from oral custom to the archive', 'bt-29'),
    ('how does regularity work as an exported standard certified by a grand lodge', 'bt-30'),
    ('how is temple symbolism used as a moral template for conduct', 'bt-31'),
    ('why is the lodge described as a workshop with graded craft classes', 'bt-32'),
    ('how is admission tested by greeting and handshake without writing the teaching', 'bt-33'),
    ('how does the degree ladder disclose more at each grade', 'bt-34'),
    ('how do dated minutes challenge a founding legend', 'bt-35'),
    ('how is a claim traced back along its source trail before being believed', 'bt-36'),
    ('how are original text layers separated from later interpolations', 'bt-37'),
    ('how are figures from different traditions mapped by initiatory function', 'bt-38'),
    ('how is the sacrificed god traced through a genealogy of dying deities', 'bt-39'),
    ('how are symbols decoded by their place in a system', 'bt-40'),
    ('how does a group form an egregore through shared focus', 'bt-41'),
    ('how does a rising order absorb and demonize older gods', 'bt-42'),
    ('how is a creed read as a political code of rule and exclusion', 'bt-43'),
    ('how is catechism drilling audited as conditioning', 'bt-44'),
    ('how is a teaching judged by the fruits it produces', 'bt-45'),
    ('what is zero as the latent field before manifestation', 'bt-46'),
    ('how does the point in the circle picture manifestation', 'bt-47'),
    ('how do involution and evolution form one cycle in opposite directions', 'bt-48'),
    ('how does polarity instruct by opposition between poles', 'bt-49'),
    ('how does a third term mediate two opposed terms into a triangle', 'bt-50'),
    ('how is triangle equality used as a diagnostic test', 'bt-51'),
    ('how are symbols disclosed by grade as capacity grows', 'bt-52'),
    ('why does four mark materialization through the elements', 'bt-53'),
    ('why is five the anti-equilibrium of senses and action', 'bt-54'),
    ('how does the septenary system align planets notes and stages of ascent', 'bt-55'),
    ('how is conduct audited against an eightfold rubric', 'bt-56'),
    ('how is the decalogue re-read as a lodge ethics code', 'bt-57'),
    ('why sort evidence into kinds before arguing from it', 'bt-58'),
    ('how do dates falsify an impossible narrative of travels and offices', 'bt-59'),
    ('how are copied rituals fingerprinted back to earlier authors', 'bt-60'),
    ('how is a witness audited for purchased degrees and contradictions', 'bt-61'),
    ('how does motive explain conversion testimony better than doctrine', 'bt-62'),
    ('how does syntax prove which language a document was written in first', 'bt-63'),
    ('how does invented geography collapse when officeholders deny the office', 'bt-64'),
    ('how is a list of inspectors falsified by writing to the named men', 'bt-65'),
    ('how are claimed temples checked against real geography and jurisdiction', 'bt-66'),
    ('what remains when every borrowed source is subtracted from a compilation', 'bt-67'),
    ('how does a hoax launder authority through borrowed endorsements', 'bt-68'),
    ('why is a claim that no evidence could refute a design feature', 'bt-69'),
    ('what screening does the book claim happens before structuring', 'bt-70'),
    ('how does the book describe a hidden core behind decoy fronts', 'bt-71'),
    ('how does the double bind model explain amnesia walled parts', 'bt-72'),
    ('what layered access codes does the book describe at pattern level', 'bt-73'),
    ('how are narrative works mapped scene by scene onto internal structures', 'bt-74'),
    ('how does dual language give terms a second insider meaning', 'bt-75'),
    ('how are gatekeeper personas layered at successive depths', 'bt-76'),
    ('how are internal worlds structured with grids maps and color codes', 'bt-77'),
    ('what layered defenses and backups does the book claim protect the system', 'bt-78'),
    ('how does milieu control keep a subject inside a managed social world', 'bt-79'),
    ('what media does the book catalog as alleged cue carriers', 'bt-80'),
    ('how does the disbelief barrier stop listeners crediting disclosures', 'bt-81'),
    ('how is angelic magic traced across Egyptian Persian and Greek traditions', 'bt-82'),
    ('how is the fall reframed as deliberate incarnation into matter', 'bt-83'),
    ('how are angelic teachers mapped to planets metals and plants', 'bt-84'),
    ('how does ascent climb through planetary spheres toward unity', 'bt-85'),
    ('what are the three spiritual states tied to salt sulfur and mercury', 'bt-86'),
    ('how do towers and temples link underworld earth and heaven as an axis', 'bt-87'),
    ('how does sacred knowledge survive catastrophe through lineages and arks', 'bt-88'),
    ('how does liminal crossing at borders loosen fixed divisions', 'bt-89'),
    ('how do twin pillars frame polarity as an engine of tension', 'bt-90'),
    ('how do degrees signs and passwords organize recognition without speech', 'bt-91'),
    ('how does the death search and raising pattern enact renewal', 'bt-92'),
    ('how is the serpent read as teacher and healing key on the tree', 'bt-93'),
    ('how is the case built by accumulating many visual exhibits until the pattern holds', 'bt-94'),
    ('how does an outer fraternity conceal an inner elect', 'bt-95'),
    ('how are public gestures read as plain sight recognition signals', 'bt-96'),
    ('how are hand grips presented as a recognition test for rank', 'bt-97'),
    ('what do the penal signs and due guards show the body owes', 'bt-98'),
    ('how is the X mark interpreted as union of opposites', 'bt-99'),
    ('how is the double headed eagle read as managed duality', 'bt-100'),
    ('how is the great seal decoded as a builder hierarchy', 'bt-101'),
    ('how do oath penalties and silence guards enforce secrecy', 'bt-102'),
    ('how do upward and downward triangles form a polarity system', 'bt-103'),
    ('how are dated magazine photos treated as staged messages', 'bt-104'),
    ('how are stars classified by orientation and use', 'bt-105'),
    ('how did ancient mystery schools transmit symbolic teaching to modern forms', 'bt-106'),
    ('how does the oracle pipeline separate scribes interpreters and poets', 'bt-107'),
    ('how does cave descent incubation use waters of forgetting and memory', 'bt-108'),
    ('how does graded initiation delay access to the teacher', 'bt-109'),
    ('how do aphorisms compress discipline into short symbolic rules', 'bt-110'),
    ('how are letter values summed and reduced to a numeric signature', 'bt-111'),
    ('how is the body mapped onto temple chambers as a teaching diagram', 'bt-112'),
    ('how are passwords graded by work class to limit the master word', 'bt-113'),
    ('how are octave fifth and fourth derived from string ratios', 'bt-114'),
    ('how are animal emblems derived from observed habits', 'bt-115'),
    ('how does the tree diagram one source producing many effects', 'bt-116'),
    ('how is the protective circle constructed with three concentric circles', 'bt-117'),
    ('how do myths carry an outer story and a restricted inner reading', 'bt-118'),
    ('how is access earned through staged tests and purification', 'bt-119'),
    ('how do passages and chambers encode the sequence of learning', 'bt-120'),
    ('how is a scattered whole recovered piece by piece with the missing piece marked', 'bt-121'),
    ('how does return surrender accretions level by level after descent', 'bt-122'),
    ('how are letters planets metals and organs bound into correspondence tables', 'bt-123'),
    ('how does ascent move sequentially through gates and rings without skipping', 'bt-124'),
    ('how are texts read through numerical equivalence and letter permutation', 'bt-125'),
    ('how does the tabernacle map temple cosmos and human constitution', 'bt-126'),
    ('what rules govern the hidden order core and its succession', 'bt-127'),
    ('how do alchemical ladders stage transformation operation by operation', 'bt-128'),
    ('why do the same operations fail for an unprepared operator', 'bt-129'),
    ('how are black white and red stages read as process states', 'bt-130'),
    ('what stages form the seven stage initiation journey', 'bt-131'),
    ('why classify the cipher system before attempting extraction', 'bt-132'),
    ('how are universe body and soul mapped as nested temples', 'bt-133'),
    ('how are churches planets and seals aligned into one ascent ladder', 'bt-134'),
    ('how does the forest quest earn a lifelong guardian spirit', 'bt-135'),
    ('how do birch bark charts preserve degrees without exposing secrets', 'bt-136'),
    ('how are mysteries split between inner circle and outsiders receiving parables', 'bt-137'),
    ('how does a sacred lineage survive through exile and migration', 'bt-138'),
    ('why is forbidden knowledge engraved on metal or stone', 'bt-139'),
    ('how does a written charter transmit authority to found lodges', 'bt-140'),
    ('how are archangels organized by sefirah tarot element and color', 'bt-141'),
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
