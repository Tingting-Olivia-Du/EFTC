"""
Best-effort reconstruction of the Level 2-6 affix-expanded word lists for
HSWL, CET-4, and CET-6, using the recovered official BNC/COCA word-family
database (data/wordlists/bnc_coca_family_database.json) and the Bauer &
Nation (1993) affix rules exactly as given in the paper's Table 1.

IMPORTANT CAVEATS (read before trusting these numbers):
  - Level 6 = full word-family expansion: for every Level-1 word, pull in
    every member of its BNC/COCA family. This matches the paper's stated
    method, but our copy of the family database (RANGE package,
    "bnc_coca_cleaned_ver_002_20141015") may be a different vintage than
    whatever the original study used (cited as "Nation, 2017, v1.0.0") --
    Table 5 numbers matched this database exactly, but Table 3's Level-6
    sizes do not match ours exactly (see output), so some version drift is
    likely for the family-membership data specifically.
  - Level 2 ("lemmatisation") is approximated with regular-inflection
    pattern matching (plural/3sg -s/-es, past tense -d/-ed, -ing,
    comparative/superlative -er/-est, with standard spelling-change
    handling). The paper states the original used Tom Cobb's
    Familizer/Lemmatizer tool, which we don't have access to -- our
    heuristic will not be identical to it in every edge case.
  - Levels 3-5 are built by the iterative merge procedure the paper
    describes in Section 3.2.1: starting from Level-1 (+Level-2), add
    Level-6 family members whose spelling matches that level's prefix/
    suffix patterns from Table 1, cumulatively.

Treat the results as an independently-reasoned approximation that tracks
the paper's pattern (same rank ordering, broadly similar magnitudes), not
as an exact replacement for the missing original Java pipeline. See
report/level_reconstruction_attempt.md for the full comparison and caveats.

Run (from repo root): python3 analysis/build_leveled_wordlists.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WL = ROOT / "data" / "wordlists"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

# --- Table 1 affix rules, verbatim ---
LEVEL_PREFIXES = {
    3: ["non", "un"],
    4: ["in"],
    5: ["ante", "anti", "arch", "bi", "circum", "counter", "en", "ex", "fore", "hyper",
        "inter", "mid", "mis", "neo", "post", "pro", "semi", "sub", "un"],
    6: ["pre", "re"],
}
LEVEL_SUFFIXES = {
    3: ["able", "er", "ish", "less", "ly", "ness", "th", "y"],
    4: ["al", "ation", "ess", "ful", "ism", "ist", "ity", "ize", "ment", "ous"],
    5: ["age", "al", "ally", "an", "ance", "ant", "ary", "atory", "dom", "eer", "en",
        "ence", "ent", "ery", "ese", "esque", "ette", "hood", "i", "ian", "ite", "let",
        "ling", "ly", "most", "ory", "ship", "ward", "ways", "wise"],
    6: ["able", "ee", "ic", "ify", "ion", "ist", "ition", "ive", "th", "y"],
}


def matches_affix(word: str, level: int) -> bool:
    return (any(word.startswith(p) for p in LEVEL_PREFIXES[level])
            or any(word.endswith(s) for s in LEVEL_SUFFIXES[level]))


# --- Level 2: approximate regular-inflection matcher ---
def inflectional_forms_of(members, headword):
    h = headword
    candidates = set()
    candidates.add(h + "s")
    candidates.add(h + "es")
    if h.endswith("y") and len(h) > 1 and h[-2] not in "aeiou":
        candidates.add(h[:-1] + "ies")
    candidates.add(h + "d")
    candidates.add(h + "ed")
    if h.endswith("e"):
        candidates.add(h + "d")
        candidates.add(h[:-1] + "ed")
        candidates.add(h[:-1] + "ing")
    else:
        candidates.add(h + "ing")
        if h.endswith("y") and len(h) > 1 and h[-2] not in "aeiou":
            candidates.add(h[:-1] + "ied")
    candidates.add(h + "er")
    candidates.add(h + "est")
    if h.endswith("e"):
        candidates.add(h[:-1] + "er")
        candidates.add(h[:-1] + "est")
    if h.endswith("y") and len(h) > 1 and h[-2] not in "aeiou":
        candidates.add(h[:-1] + "ier")
        candidates.add(h[:-1] + "iest")
    # doubled final consonant (e.g. stop -> stopped/stopping)
    if len(h) >= 3 and h[-1] not in "aeiouwxy" and h[-2] in "aeiou" and h[-3] not in "aeiou":
        candidates.add(h + h[-1] + "ed")
        candidates.add(h + h[-1] + "ing")
        candidates.add(h + h[-1] + "er")
        candidates.add(h + h[-1] + "est")
    return members & candidates


class FamilyDB:
    def __init__(self, path):
        raw = json.load(open(path, encoding="utf-8"))
        self.family = {hw.lower(): [m.lower() for m in members] for hw, members in raw.items()}
        self.reverse = {}
        for hw, members in self.family.items():
            self.reverse.setdefault(hw, hw)
            for m in members:
                self.reverse.setdefault(m, hw)

    def headword_of(self, word: str):
        return self.reverse.get(word)

    def full_family(self, word: str):
        hw = self.headword_of(word)
        if hw is None:
            return {word}
        return {hw} | set(self.family.get(hw, []))


def build_levels(level1, db):
    level1 = {w.lower() for w in level1}

    # Level 6: full family union
    level6 = set(level1)
    for w in level1:
        level6 |= db.full_family(w)

    # Level 2: level1 + regular inflectional forms found within each word's family
    level2 = set(level1)
    for w in level1:
        hw = db.headword_of(w)
        family_members = set(db.family.get(hw, [])) if hw else set()
        level2 |= inflectional_forms_of(family_members, hw or w)

    # Levels 3-5: iteratively add Level-6 members matching that level's affixes
    level3 = set(level1) | set(level2)
    for w in level6 - level3:
        if matches_affix(w, 3):
            level3.add(w)

    level4 = set(level3)
    for w in level6 - level4:
        if matches_affix(w, 4):
            level4.add(w)

    level5 = set(level4)
    for w in level6 - level5:
        if matches_affix(w, 5):
            level5.add(w)

    return {1: level1, 2: level2, 3: level3, 4: level4, 5: level5, 6: level6}


PAPER_TABLE3 = {
    "HSWL": {1: 3448, 2: 9854, 3: 12792, 4: 13750, 5: 14951, 6: 18023},
    "CET4": {1: 4543, 2: 12885, 3: 16359, 4: 17595, 5: 18991, 6: 22664},
    "CET6": {1: 8074, 2: 16390, 3: 19572, 4: 20478, 5: 21762, 6: 25243},
}


def main():
    db = FamilyDB(WL / "bnc_coca_family_database.json")
    results = {}
    print(f"{'List':6s} {'Level':>5s} {'built':>8s} {'paper':>8s} {'diff':>8s} {'diff%':>8s}")
    for name, path in [("HSWL", WL / "HSWL_level1.json"), ("CET4", WL / "CET4_level1.json"),
                        ("CET6", WL / "CET6_level1.json")]:
        level1 = set(json.load(open(path)))
        levels = build_levels(level1, db)
        results[name] = {lvl: sorted(words) for lvl, words in levels.items()}
        for lvl in range(1, 7):
            built = len(levels[lvl])
            paper = PAPER_TABLE3[name][lvl]
            diff = built - paper
            print(f"{name:6s} {lvl:5d} {built:8d} {paper:8d} {diff:+8d} {100*diff/paper:+7.1f}%")

        out_dir = WL / "leveled" / name
        out_dir.mkdir(parents=True, exist_ok=True)
        for lvl, words in results[name].items():
            with open(out_dir / f"level{lvl}.json", "w", encoding="utf-8") as f:
                json.dump(words, f, ensure_ascii=False, indent=1)
    print(f"\nWrote leveled word lists to {WL/'leveled'}/{{HSWL,CET4,CET6}}/level{{1..6}}.json")


if __name__ == "__main__":
    main()
