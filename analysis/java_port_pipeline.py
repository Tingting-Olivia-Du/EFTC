"""
Faithful Python port of the original Java word-list-leveling pipeline
(archive/java_source/hyponym/{LevelList,AffixLevel,AffixLevelHandler,
LevelListHandler,Coverage}.java), generalized to run for HSWL, CET-4, and
CET-6 (the Java source, as provided, only has the HighSchool code path
live -- cet4/cet6 are present but commented out) and wired up to data this
repository actually has, in place of the external files the Java code
expected on disk but that were never provided:

  Java expected file                          | What we use instead
  ---------------------------------------------|--------------------------------
  ./data/wordlist/{X}_origin.txt (Level 1)      | data/wordlists/{X}_level1.json
  ./data/wordlist/{X}_family_horizontal.txt     | rebuilt from the real BNC/COCA
    (Level 6 -- headword + all family members)  | family database (basewrd1-25,
                                                 | data/wordlists/bnc_coca_family_
                                                 | database.json) -- see Finding
                                                 | in report/level_reconstruction_
                                                 | attempt.md for how that was
                                                 | itself recovered
  ./data/wordlist/{X}_lemmas_horizontal.txt     | data/wordlists/antbnc_lemma_
    (Level 2 -- headword + inflectional forms)  | database.json -- the real
                                                 | AntBNC lemma list (Laurence
                                                 | Anthony), the same resource
                                                 | Tom Cobb's Familizer/
                                                 | Lemmatizer tool uses for
                                                 | English under the hood (see
                                                 | build_antbnc_lemma_db.py).
                                                 | Falls back to a regular-
                                                 | inflection regex for the ~4%
                                                 | of words it doesn't cover.

BUGS FOUND WHILE PORTING (see report/level_reconstruction_attempt.md
sections 7-9 for the full writeup). As of this version, BOTH are FIXED by
default (AffixLevelHandlerFixed, used unless you explicitly pass
AffixLevelHandlerAsFound()) -- the original report initially replicated
bug #1 faithfully to validate against the paper's published numbers, but
per-request this module's default configuration now applies every known
fix and reruns the whole pipeline through Table 9/10 (report section 9):

  1. AffixLevelHandler.java sets level3prefixes = {} (empty) and puts
     "non"/"un" into level3suffixes -- i.e. the real code checks
     word.endsWith("un"), not word.startsWith("un"), for Level 3, unlike
     what Table 1 in the paper describes. FIXED by default
     (AffixLevelHandlerFixed moves non-/un- to prefixes); the original,
     literal Java behavior is still available as AffixLevelHandlerAsFound
     for comparison. Fixing this turned out to only marginally change the
     accuracy vs. the paper (report section 9) -- it was not the dominant
     error source.

  2. LevelListHandler.buildLevel() has a hardcoded reference to
     `HighSchool_levelList6.entrySet()` regardless of which list's Levels
     3-5 are being built. This is clearly a copy-paste artifact: with only
     the HighSchool code path live, it happens to be correct (HighSchool
     building from HighSchool's own Level 6), but reusing this exact method
     unmodified for CET-4/CET-6 would build their Levels 3-5 by scanning
     HighSchool's (much smaller) family list instead of their own. Since
     data/wordlists/leveled_ground_truth/{CET4,CET6}/level{3,4,5}.json
     (the recovered near-final real output) match the paper closely, the
     actual production run did NOT have this bug active -- so it is FIXED
     here (each list's buildLevel scans its own Level 6), not replicated.

Run (from repo root): python3 analysis/java_port_pipeline.py
"""
import json
import re
from pathlib import Path

from coverage_lib import Corpus, coverage_stats

ROOT = Path(__file__).resolve().parent.parent
WL = ROOT / "data" / "wordlists"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# LevelList.java port: TreeMap<String, HashSet<String>> -> dict[str, set[str]]
# ---------------------------------------------------------------------------
class LevelList(dict):
    """headword -> set of member word forms (self included, matching how
    the Java code's mergeMaps/addMembers accumulate members onto a
    headword key)."""

    def add_members(self, headword, members):
        self.setdefault(headword, set()).update(members)

    def merge(self, other: "LevelList"):
        for headword, members in other.items():
            self.setdefault(headword, set()).update(members)

    def all_words(self) -> set:
        """Flatten to a plain word list (headwords + all their members) --
        this is the form Table 3/6/7/8/9/10's 'Size' column counts."""
        words = set(self.keys())
        for members in self.values():
            words |= members
        return words


# ---------------------------------------------------------------------------
# AffixLevel / AffixLevelHandler.java port. Two variants:
#   AffixLevelHandlerAsFound  -- verbatim from the real Java source, quirk
#                                 and all (bug #1: level3prefixes = [], with
#                                 non-/un- checked as SUFFIXES via endsWith).
#   AffixLevelHandlerFixed    -- bug #1 corrected: non-/un- moved to
#                                 level3prefixes, checked via startswith,
#                                 matching Table 1's documented design.
#                                 This is now the DEFAULT used by
#                                 LevelListHandler (see main()).
# ---------------------------------------------------------------------------
class AffixLevelHandlerAsFound:
    level3prefixes = []
    level3suffixes = ["able", "er", "ish", "less", "ly", "ness", "th", "y", "non", "un"]
    level4prefixes = ["in"]
    level4suffixes = ["al", "ation", "ess", "ful", "ism", "ist", "ity", "ize", "ment", "ous"]
    level5prefixes = ["anti", "ante", "arch", "bi", "circum", "counter", "en", "ex", "fore",
                       "hyper", "inter", "mid", "mis", "neo", "post", "pro", "semi", "sub", "un"]
    level5suffixes = ["age", "al", "ally", "an", "ance", "ant", "ary", "atory", "dom", "eer", "en",
                       "en", "ence", "ent", "ery", "ese", "esque", "ette", "hood", "i", "ian",
                       "ite", "let", "ling", "ly", "most", "ory", "ship", "ward", "ways", "wise"]

    def matches(self, word: str, level: int) -> bool:
        prefixes = getattr(self, f"level{level}prefixes")
        suffixes = getattr(self, f"level{level}suffixes")
        return any(word.startswith(p) for p in prefixes) or any(word.endswith(s) for s in suffixes)


class AffixLevelHandlerFixed(AffixLevelHandlerAsFound):
    level3prefixes = ["non", "un"]
    level3suffixes = ["able", "er", "ish", "less", "ly", "ness", "th", "y"]


# Backwards-compatible alias -- older code / callers importing AffixLevelHandler
# get the as-found (buggy) behavior unless they ask for the fixed one explicitly.
AffixLevelHandler = AffixLevelHandlerAsFound


# ---------------------------------------------------------------------------
# Approximates the external *_lemmas_horizontal.txt (Level 2) that the real
# Cobb Familizer/Lemmatizer tool produced but that isn't available to us.
# ---------------------------------------------------------------------------
def regular_inflections(headword: str, family_members: set) -> set:
    h = headword
    candidates = {h + "s", h + "es"}
    if h.endswith("y") and len(h) > 1 and h[-2] not in "aeiou":
        candidates.add(h[:-1] + "ies")
    if h.endswith("e"):
        candidates |= {h + "d", h[:-1] + "ed", h[:-1] + "ing", h[:-1] + "er", h[:-1] + "est"}
    else:
        candidates |= {h + "ed", h + "ing"}
        if h.endswith("y") and len(h) > 1 and h[-2] not in "aeiou":
            candidates.add(h[:-1] + "ied")
    candidates |= {h + "er", h + "est"}
    if h.endswith("y") and len(h) > 1 and h[-2] not in "aeiou":
        candidates |= {h[:-1] + "ier", h[:-1] + "iest"}
    if len(h) >= 3 and h[-1] not in "aeiouwxy" and h[-2] in "aeiou" and h[-3] not in "aeiou":
        candidates |= {h + h[-1] + "ed", h + h[-1] + "ing", h + h[-1] + "er", h + h[-1] + "est"}
    return family_members & candidates


# ---------------------------------------------------------------------------
# LevelListHandler.java port, generalized (see module docstring, bug #2 fix)
# ---------------------------------------------------------------------------
class LevelListHandler:
    def __init__(self, level1_words: set, family_db: dict, family_reverse: dict,
                 lemma_db: dict = None, affix_handler: "AffixLevelHandlerAsFound" = None):
        self.affix = affix_handler if affix_handler is not None else AffixLevelHandlerFixed()

        # Level 1: original word list, no members yet
        self.level1 = LevelList()
        for w in level1_words:
            self.level1.setdefault(w, set())

        # Level 6: family_horizontal equivalent -- each Level-1 word's full
        # BNC/COCA family (headword + all members), keyed by the Level-1
        # word itself so LevelList.all_words() reproduces "headword +
        # members" the same way the Java process_file() would have.
        self.level6 = LevelList()
        for w in level1_words:
            hw = family_reverse.get(w)
            members = set(family_db.get(hw, [])) | ({hw} if hw else set())
            members.discard(w)
            self.level6.add_members(w, members)

        # Level 2: lemmas_horizontal equivalent. Uses the real AntBNC lemma
        # database (data/wordlists/antbnc_lemma_database.json, recovered
        # from Laurence Anthony's site -- see report §9) when available,
        # since it's a genuine lemma-vs-family distinction (same POS only),
        # not an approximation. Falls back to the regex heuristic for the
        # ~4% of words the lemma database doesn't have an entry for.
        self.level2 = LevelList()
        for w in level1_words:
            if lemma_db is not None and w in lemma_db:
                forms = set(lemma_db[w]) - {w}
            else:
                hw = family_reverse.get(w, w)
                fam_members = set(family_db.get(hw, []))
                forms = regular_inflections(hw, fam_members) - {w}
            self.level2.add_members(w, forms)
        self.level2.merge(self.level1)

        # Levels 3-5: iteratively add Level-6 members matching that level's
        # affix rules (bug #2 fix: scan THIS list's own level6, not a
        # hardcoded other list's)
        self.level3 = self._build_level(3, self.level6)
        self.level3.merge(self.level2)

        self.level4 = self._build_level(4, self.level6)
        self.level4.merge(self.level3)

        self.level5 = self._build_level(5, self.level6)
        self.level5.merge(self.level4)

    def _build_level(self, level: int, level6: LevelList) -> LevelList:
        """Direct port of LevelListHandler.buildLevel()."""
        out = LevelList()
        for headword, members in level6.items():
            for member in members:
                if self.affix.matches(member, level):
                    out.add_members(headword, {member})
        return out


def build_family_lookup():
    family_db = json.load(open(WL / "bnc_coca_family_database.json", encoding="utf-8"))
    family_db = {hw.lower(): [m.lower() for m in members] for hw, members in family_db.items()}
    reverse = {}
    for hw, members in family_db.items():
        reverse.setdefault(hw, hw)
        for m in members:
            reverse.setdefault(m, hw)
    return family_db, reverse


PAPER_TABLE3 = {
    "HSWL": {1: 3448, 2: 9854, 3: 12792, 4: 13750, 5: 14951, 6: 18023},
    "CET4": {1: 4543, 2: 12885, 3: 16359, 4: 17595, 5: 18991, 6: 22664},
    "CET6": {1: 8074, 2: 16390, 3: 19572, 4: 20478, 5: 21762, 6: 25243},
}
PAPER_TOKEN = {
    "HSWL": [60.63, 62.84, 65.97, 67.90, 68.36, 69.70],
    "CET4": [72.26, 74.63, 76.92, 78.26, 78.76, 80.10],
    "CET6": [82.32, 84.00, 85.49, 85.72, 86.03, 86.72],
}
FILES = {"HSWL": "HSWL_level1.json", "CET4": "CET4_level1.json", "CET6": "CET6_level1.json"}


def main():
    corpus = Corpus(WL / "eftc_corpus.json")
    family_db, family_reverse = build_family_lookup()
    lemma_db_path = WL / "antbnc_lemma_database.json"
    lemma_db = json.load(open(lemma_db_path, encoding="utf-8")) if lemma_db_path.exists() else None
    affix_handler = AffixLevelHandlerFixed()
    print(f"Level 2 source: {'real AntBNC lemma database' if lemma_db else 'regex heuristic (AntBNC not found)'}")
    print(f"Level 3 affix rule: FIXED (non-/un- as prefixes, matching Table 1) "
          f"-- bug #1 from report section 7 corrected, not replicated\n")

    print(f"{'List':6s}{'Lvl':>4s} {'size(ported)':>12s} {'size(GT)':>9s} {'size(paper)':>12s} "
          f"{'token%(ported)':>15s} {'token%(paper)':>14s} {'diff':>7s}")
    all_levels = {}
    diffs = []
    for name, fname in FILES.items():
        level1_words = set(json.load(open(WL / fname)))
        level1_words = {w.lower() for w in level1_words}
        handler = LevelListHandler(level1_words, family_db, family_reverse, lemma_db, affix_handler)
        levels = {1: handler.level1, 2: handler.level2, 3: handler.level3,
                  4: handler.level4, 5: handler.level5, 6: handler.level6}
        all_levels[name] = {lvl: ll.all_words() for lvl, ll in levels.items()}

        gt_dir = WL / "leveled_ground_truth" / name
        for lvl in range(1, 7):
            words = all_levels[name][lvl]
            s = coverage_stats(words, corpus)
            paper_size = PAPER_TABLE3[name][lvl]
            paper_token = PAPER_TOKEN[name][lvl - 1]
            gt_size = None
            if (gt_dir / f"level{lvl}.json").exists():
                gt_size = len(json.load(open(gt_dir / f"level{lvl}.json")))
            d = s["token_coverage_pct"] - paper_token
            diffs.append(d)
            print(f"{name:6s}{lvl:4d} {s['wordlist_size']:12d} {gt_size if gt_size else 0:9d} "
                  f"{paper_size:12d} {s['token_coverage_pct']:15.2f} {paper_token:14.2f} {d:+7.2f}")

        out_dir = WL / "leveled_java_port" / name
        out_dir.mkdir(parents=True, exist_ok=True)
        for lvl, words in all_levels[name].items():
            json.dump(sorted(words), open(out_dir / f"level{lvl}.json", "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)

    import statistics
    print(f"\nToken coverage vs. paper: mean {statistics.mean(diffs):+.3f}pp, "
          f"max|diff| {max(abs(d) for d in diffs):.3f}pp, stdev {statistics.stdev(diffs):.3f}pp (n={len(diffs)})")
    print(f"\nWrote leveled word lists to {WL/'leveled_java_port'}/{{HSWL,CET4,CET6}}/level{{1..6}}.json")

    # --- Downstream: Table 9 (General Composite) and Table 10 starred rows,
    # rebuilt from THIS run's Level 6 (bug-fixed pipeline output), for a full
    # "rerun everything from level construction onward" result. ---
    print("\n=== Downstream: Table 9 / Table 10 rebuilt from this (bug-fixed) run ===")
    from coverage_lib import load_wordlist
    supplement = set(w.lower() for w in json.load(open(WL / "bnc_coca_supplement_combined.json")))
    general_composite = all_levels["HSWL"][6] | all_levels["CET4"][6] | all_levels["CET6"][6]
    general_composite_plus = general_composite | supplement
    s9 = coverage_stats(general_composite, corpus)
    s9p = coverage_stats(general_composite_plus, corpus)
    print(f"Table 9 General Composite:  size={s9['wordlist_size']:6d} token={s9['token_coverage_pct']:6.2f}  "
          f"(paper: 26,411 / 86.88)")
    print(f"Table 9 General Composite+: size={s9p['wordlist_size']:6d} token={s9p['token_coverage_pct']:6.2f}  "
          f"(paper: 55,801 / 91.78)")

    awl = load_wordlist(WL / "AWL.json")
    nawl = load_wordlist(WL / "NAWL.json")
    avl_correct = load_wordlist(WL / "AVL_correct.json")
    avl_wrong = load_wordlist(WL / "AVL_old_wrong.json")
    paper10 = {
        "AWL*": (56254, 91.93), "NAWL*": (56775, 92.50),
        "AVL* (sanity check, wrong AVL)": (63153, 94.09),
    }
    for label, wl in [("AWL*", awl), ("NAWL*", nawl),
                       ("AVL* (sanity check, wrong AVL)", avl_wrong),
                       ("AVL* (CORRECTED)", avl_correct)]:
        s = coverage_stats(general_composite_plus | wl, corpus)
        ref = paper10.get(label)
        ref_str = f"  (paper: {ref[0]:,} / {ref[1]:.2f})" if ref else "  (no paper value -- this is the correction)"
        print(f"{label:32s} size={s['wordlist_size']:6d} token={s['token_coverage_pct']:6.2f}{ref_str}")


if __name__ == "__main__":
    main()
