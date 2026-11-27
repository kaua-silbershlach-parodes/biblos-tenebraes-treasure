"""Practice progress: sessions, completions, and mastery per technique.

Mastery levels, from recorded sessions only (never assumed):
  0 untouched · 1 practiced (1+ session) · 2 steady (3+ completions)
  3 mastered (7+ completions across 3+ distinct days)

Usage:
  python tools/progress.py log bt-04 --completed
  python tools/progress.py report
"""

import argparse
import json
import os
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "progress.json")


def load():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"sessions": []}


def save(state):
    json.dump(state, open(STATE, "w"), ensure_ascii=False, indent=1)


def mastery(sessions, tid):
    mine = [s for s in sessions if s["technique"] == tid]
    done = [s for s in mine if s["completed"]]
    days = {s["date"] for s in done}
    if len(done) >= 7 and len(days) >= 3:
        return 3
    if len(done) >= 3:
        return 2
    if mine:
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    log = sub.add_parser("log")
    log.add_argument("technique")
    log.add_argument("--completed", action="store_true")
    log.add_argument("--date", default=date.today().isoformat())
    sub.add_parser("report")
    args = parser.parse_args()

    corpus = json.load(open(os.path.join(ROOT, "corpus.json")))
    ids = {c["id"] for c in corpus}
    state = load()

    if args.cmd == "log":
        if args.technique not in ids:
            print(f"unknown technique {args.technique}")
            return 1
        state["sessions"].append(
            {"technique": args.technique, "date": args.date, "completed": bool(args.completed)}
        )
        save(state)
        print(f"logged {args.technique} completed={bool(args.completed)} "
              f"mastery={mastery(state['sessions'], args.technique)}")
        return 0

    names = {0: "untouched", 1: "practiced", 2: "steady", 3: "mastered"}
    for c in corpus:
        m = mastery(state["sessions"], c["id"])
        n = sum(1 for s in state["sessions"] if s["technique"] == c["id"])
        print(f"[{c['id']}] {c['title']}: {names[m]} ({n} sessions)")
    total = sum(mastery(state["sessions"], c["id"]) for c in corpus)
    print(f"formation: {total}/{3 * len(corpus)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
