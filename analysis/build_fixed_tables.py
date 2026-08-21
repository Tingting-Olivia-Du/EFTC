"""
Computes Tables 3, 6, 7, 8, 9, and 10's starred rows entirely from the
bug-fixed pipeline (java_port_pipeline.py's default AffixLevelHandlerFixed
+ real AntBNC lemma database for Level 2 + the buildLevel bug fix) --
i.e. the "correct" Level 1-6 construction per Table 1's documented design,
resolving the open question in report/level_reconstruction_attempt.md §1
finding #1 in favor of "the code should match Table 1" rather than
"Table 1 should be revised to match the code".

This supersedes both (a) the paper's original published numbers, which we
now know depended on a Level-3 implementation that didn't match Table 1,
and (b) the from-scratch reconstructions in earlier scripts, by using the
most accurate Level-2 source available (real AntBNC lemma data) combined
with the corrected Level-3 rule.

Run (from repo root): python3 analysis/build_fixed_tables.py
"""
import csv
import json
from pathlib import Path

from coverage_lib import Corpus, load_wordlist, coverage_stats
from java_port_pipeline import LevelListHandler, AffixLevelHandlerFixed, build_family_lookup

ROOT = Path(__file__).resolve().parent.parent
WL = ROOT / "data" / "wordlists"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

FILES = {"HSWL": "HSWL_level1.json", "CET4": "CET4_level1.json", "CET6": "CET6_level1.json"}
LABELS = {"HSWL": "HSWL", "CET4": "CET-4 WL", "CET6": "CET-6 WL"}

PAPER_TABLE3 = {
    "HSWL": {1: 3448, 2: 9854, 3: 12792, 4: 13750, 5: 14951, 6: 18023},
    "CET4": {1: 4543, 2: 12885, 3: 16359, 4: 17595, 5: 18991, 6: 22664},
    "CET6": {1: 8074, 2: 16390, 3: 19572, 4: 20478, 5: 21762, 6: 25243},
}
PAPER_LEVEL_TABLE = {
    "HSWL": {1: (3448, 92.98, 2.65, 60.63), 2: (9854, 51.79, 4.22, 62.84), 3: (12792, 53.60, 5.67, 65.97),
             4: (13750, 54.47, 6.20, 67.90), 5: (14951, 53.92, 6.67, 68.36), 6: (18023, 48.73, 7.27, 69.70)},
    "CET4": {1: (4543, 93.92, 3.53, 72.26), 2: (12885, 51.46, 5.49, 74.63), 3: (16359, 52.60, 7.12, 76.92),
             4: (17595, 53.27, 7.76, 78.26), 5: (18991, 52.73, 8.29, 78.76), 6: (22664, 47.82, 8.97, 80.10)},
    "CET6": {1: (8074, 93.88, 6.27, 82.32), 2: (16390, 60.52, 8.21, 84.00), 3: (19572, 59.39, 9.62, 85.49),
             4: (20478, 58.99, 9.99, 85.72), 5: (21762, 57.97, 10.44, 86.03), 6: (25243, 52.58, 10.98, 86.72)},
}
PAPER_LEVEL_PLUS_TABLE = {
    "HSWL": {1: (33138, 45.04, 12.35, 65.93), 2: (39413, 42.61, 13.90, 68.02), 3: (42351, 43.79, 15.35, 71.15),
             4: (43309, 44.29, 15.87, 73.08), 5: (44510, 44.38, 16.35, 73.54), 6: (47582, 43.03, 16.94, 74.89)},
    "CET4": {1: (34257, 46.71, 13.24, 77.44), 2: (42477, 43.14, 15.17, 79.69), 3: (45951, 44.18, 16.80, 81.99),
             4: (47187, 44.65, 17.44, 83.32), 5: (48583, 44.68, 17.97, 83.83), 6: (52256, 43.12, 18.65, 85.17)},
    "CET6": {1: (37719, 51.04, 15.93, 87.48), 2: (45895, 46.92, 17.82, 88.96), 3: (49077, 47.35, 19.23, 90.45),
             4: (49983, 47.40, 19.61, 90.68), 5: (51267, 47.26, 20.05, 90.99), 6: (54748, 45.45, 20.59, 91.67)},
}


def main():
    corpus = Corpus(WL / "eftc_corpus.json")
    family_db, family_reverse = build_family_lookup()
    lemma_db = json.load(open(WL / "antbnc_lemma_database.json", encoding="utf-8"))
    affix_handler = AffixLevelHandlerFixed()
    supplement = set(w.lower() for w in json.load(open(WL / "bnc_coca_supplement_combined.json")))

    all_levels = {}
    table_rows = []  # for Tables 6/7/8
    print(f"{'List':6s}{'Lvl':>4s} {'size':>8s} {'attest%':>8s} {'type%':>7s} {'token%':>7s}  "
          f"vs paper (size/attest/type/token)")
    for name, fname in FILES.items():
        level1_words = {w.lower() for w in json.load(open(WL / fname))}
        handler = LevelListHandler(level1_words, family_db, family_reverse, lemma_db, affix_handler)
        levels = {1: handler.level1, 2: handler.level2, 3: handler.level3,
                  4: handler.level4, 5: handler.level5, 6: handler.level6}
        all_levels[name] = {lvl: ll.all_words() for lvl, ll in levels.items()}

        for lvl in range(1, 7):
            words = all_levels[name][lvl]
            s = coverage_stats(words, corpus)
            s_plus = coverage_stats(words | supplement, corpus)
            pv = PAPER_LEVEL_TABLE[name][lvl]
            pvp = PAPER_LEVEL_PLUS_TABLE[name][lvl]
            table_rows.append({"list": LABELS[name], "level": f"Level {lvl}", "size": s["wordlist_size"],
                                "attestation_pct": round(s["attestation_rate_pct"], 2),
                                "type_pct": round(s["type_coverage_pct"], 2),
                                "token_pct": round(s["token_coverage_pct"], 2)})
            table_rows.append({"list": LABELS[name], "level": f"Level {lvl}+", "size": s_plus["wordlist_size"],
                                "attestation_pct": round(s_plus["attestation_rate_pct"], 2),
                                "type_pct": round(s_plus["type_coverage_pct"], 2),
                                "token_pct": round(s_plus["token_coverage_pct"], 2)})
            print(f"{name:6s}{lvl:4d} {s['wordlist_size']:8d} {s['attestation_rate_pct']:8.2f} "
                  f"{s['type_coverage_pct']:7.2f} {s['token_coverage_pct']:7.2f}  vs paper "
                  f"({pv[0]}/{pv[1]:.2f}/{pv[2]:.2f}/{pv[3]:.2f})")
            print(f"{'':6s}{'+':>4s} {s_plus['wordlist_size']:8d} {s_plus['attestation_rate_pct']:8.2f} "
                  f"{s_plus['type_coverage_pct']:7.2f} {s_plus['token_coverage_pct']:7.2f}  vs paper "
                  f"({pvp[0]}/{pvp[1]:.2f}/{pvp[2]:.2f}/{pvp[3]:.2f})")

    # Table 9: General Composite
    general_composite = all_levels["HSWL"][6] | all_levels["CET4"][6] | all_levels["CET6"][6]
    general_composite_plus = general_composite | supplement
    s9 = coverage_stats(general_composite, corpus)
    s9p = coverage_stats(general_composite_plus, corpus)
    print(f"\nTable 9 General Composite:  size={s9['wordlist_size']} attest={s9['attestation_rate_pct']:.2f} "
          f"type={s9['type_coverage_pct']:.2f} token={s9['token_coverage_pct']:.2f}  (paper: 26,411/51.49/11.25/86.88)")
    print(f"Table 9 General Composite+: size={s9p['wordlist_size']} attest={s9p['attestation_rate_pct']:.2f} "
          f"type={s9p['type_coverage_pct']:.2f} token={s9p['token_coverage_pct']:.2f}  (paper: 55,801/45.09/20.82/91.78)")

    # Table 10 starred rows
    awl = load_wordlist(WL / "AWL.json")
    nawl = load_wordlist(WL / "NAWL.json")
    avl_correct = load_wordlist(WL / "AVL_correct.json")
    table10 = {}
    print()
    for label, wl, paper in [
        ("AWL*", awl, (56254, 45.07, 20.98, 91.93)),
        ("NAWL*", nawl, (56775, 44.75, 21.03, 92.50)),
        ("AVL*", avl_correct, None),
    ]:
        s = coverage_stats(general_composite_plus | wl, corpus)
        table10[label] = s
        ref = f"  (paper: {paper[0]:,}/{paper[1]:.2f}/{paper[2]:.2f}/{paper[3]:.2f})" if paper else "  (corrected AVL, no paper value)"
        print(f"{label:6s} size={s['wordlist_size']:6d} attest={s['attestation_rate_pct']:6.2f} "
              f"type={s['type_coverage_pct']:6.2f} token={s['token_coverage_pct']:6.2f}{ref}")

    with open(OUT / "fixed_pipeline_table6_7_8.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(table_rows[0].keys()))
        w.writeheader()
        w.writerows(table_rows)
    with open(OUT / "fixed_pipeline_table3_9_10.json", "w", encoding="utf-8") as f:
        json.dump({
            "table3": {name: {lvl: len(all_levels[name][lvl]) for lvl in range(1, 7)} for name in FILES},
            "table9": {"general_composite": s9, "general_composite_plus": s9p},
            "table10_starred": table10,
        }, f, indent=2, default=lambda o: round(o, 2) if isinstance(o, float) else o)
    print(f"\nWrote {OUT/'fixed_pipeline_table6_7_8.csv'} and {OUT/'fixed_pipeline_table3_9_10.json'}")


if __name__ == "__main__":
    main()
