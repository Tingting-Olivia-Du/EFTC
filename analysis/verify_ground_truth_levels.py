"""
Uses the REAL Level 1-6 word lists recovered from the original researcher's
Java project working files (java_source/research_file/FAWL_Python/
wordlist/gen_leveled/, not tracked in git -- see archive/java_source/ for
the Java code itself and data/wordlists/leveled_ground_truth/ for these
parsed lists) to:

  1. Verify Tables 3, 6, 7, 8 far more precisely than the from-scratch
     reconstruction in build_leveled_wordlists.py could.
  2. Rebuild Table 9 (General Composite Word List) and Table 10's starred
     rows, including a high-confidence corrected AVL* estimate.

These gen_leveled files are a slightly earlier snapshot than whatever
produced the final published numbers (sizes are ~0.1-0.5% larger, missing
one last small cleanup pass) but are otherwise strong ground truth: a
sanity check re-deriving Table 10's AVL* using the paper's own (wrong) AVL
data reproduces 94.09% EXACTLY.

Run (from repo root): python3 analysis/verify_ground_truth_levels.py
"""
import csv
import json
from pathlib import Path

from coverage_lib import Corpus, load_wordlist, coverage_stats

ROOT = Path(__file__).resolve().parent.parent
WL = ROOT / "data" / "wordlists"
GT = WL / "leveled_ground_truth"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

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


def main():
    corpus = Corpus(WL / "eftc_corpus.json")
    supplement = set(w.lower() for w in json.load(open(WL / "bnc_coca_supplement_combined.json")))

    rows = []
    diffs = []
    print(f"{'List':6s}{'Lvl':>4s} {'size(GT)':>9s} {'size(paper)':>12s} {'token%(GT)':>11s} {'token%(paper)':>14s} {'diff':>7s}")
    level6 = {}
    for name in ["HSWL", "CET4", "CET6"]:
        for lvl in range(1, 7):
            words = set(json.load(open(GT / name / f"level{lvl}.json")))
            s = coverage_stats(words, corpus)
            paper_size = PAPER_TABLE3[name][lvl]
            paper_token = PAPER_TOKEN[name][lvl - 1]
            d = s["token_coverage_pct"] - paper_token
            diffs.append(d)
            rows.append({"list": name, "level": lvl, **s, "paper_size": paper_size, "paper_token_pct": paper_token})
            print(f"{name:6s}{lvl:4d} {s['wordlist_size']:9d} {paper_size:12d} "
                  f"{s['token_coverage_pct']:11.2f} {paper_token:14.2f} {d:+7.2f}")
            if lvl == 6:
                level6[name] = words

    import statistics
    print(f"\nToken coverage vs. paper: mean diff {statistics.mean(diffs):+.3f}pp, "
          f"max |diff| {max(abs(d) for d in diffs):.3f}pp, stdev {statistics.stdev(diffs):.3f}pp "
          f"(n={len(diffs)})")

    general_composite = level6["HSWL"] | level6["CET4"] | level6["CET6"]
    general_composite_plus = general_composite | supplement
    s9a = coverage_stats(general_composite, corpus)
    s9b = coverage_stats(general_composite_plus, corpus)
    print(f"\nTable 9 General Composite:  size={s9a['wordlist_size']} token={s9a['token_coverage_pct']:.2f}  "
          f"(paper: size=26,411 token=86.88)")
    print(f"Table 9 General Composite+: size={s9b['wordlist_size']} token={s9b['token_coverage_pct']:.2f}  "
          f"(paper: size=55,801 token=91.78)")

    awl = load_wordlist(WL / "AWL.json")
    nawl = load_wordlist(WL / "NAWL.json")
    avl_correct = load_wordlist(WL / "AVL_correct.json")
    avl_wrong = load_wordlist(WL / "AVL_old_wrong.json")

    print(f"\n{'':45s} {'size':>7s} {'attest%':>8s} {'type%':>7s} {'token%':>7s}")
    table10_rows = []
    for label, wl, paper in [
        ("AWL*", awl, (56254, 45.07, 20.98, 91.93)),
        ("NAWL*", nawl, (56775, 44.75, 21.03, 92.50)),
        ("AVL* -- SANITY CHECK (paper's wrong AVL)", avl_wrong, (63153, 47.37, 24.76, 94.09)),
        ("AVL* -- CORRECTED (high-confidence estimate)", avl_correct, None),
    ]:
        combined = general_composite_plus | wl
        s = coverage_stats(combined, corpus)
        table10_rows.append({"row": label, **s})
        paper_str = f"  (paper: {paper[0]:,} / {paper[1]:.2f} / {paper[2]:.2f} / {paper[3]:.2f})" if paper else "  (no paper value -- this is the correction)"
        print(f"{label:45s} {s['wordlist_size']:7d} {s['attestation_rate_pct']:8.2f} "
              f"{s['type_coverage_pct']:7.2f} {s['token_coverage_pct']:7.2f}{paper_str}")

    with open(OUT / "ground_truth_level_verification.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(OUT / "ground_truth_table10_starred.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(table10_rows[0].keys()))
        w.writeheader()
        w.writerows(table10_rows)
    print(f"\nWrote {OUT/'ground_truth_level_verification.csv'} and {OUT/'ground_truth_table10_starred.csv'}")


if __name__ == "__main__":
    main()
