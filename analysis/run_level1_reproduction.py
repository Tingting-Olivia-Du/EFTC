"""
Independently recomputes, from the raw word-list and corpus files that are
actually present in the original EFTC repository, every table cell in the
paper that does NOT depend on the (missing, see report) Level 2-6
word-family expansion or the BNC/COCA supplementary lists.

This covers:
  - Corpus totals (Table 2 grand total)
  - Standalone AWL / NAWL / AVL coverage (Table 10, unstarred rows)
  - HSWL / CET-4 / CET-6 Level-1 coverage (Table 6/7/8, "Level 1" rows)
  - Pairwise overlap of HSWL/CET-4/CET-6/AWL/NAWL/AVL (Table 4)

Run: python3 src/run_level1_reproduction.py
"""
import csv
import json
from pathlib import Path

from coverage_lib import Corpus, load_wordlist, coverage_stats, overlap_stats

ROOT = Path(__file__).resolve().parent.parent
WL = ROOT / "data" / "wordlists"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

# Values as printed in paper/paper.md, for direct diffing.
PAPER = {
    "AWL":    {"wordlist_size": 3107,  "attestation_rate_pct": 62.63, "type_coverage_pct": 1.61,  "token_coverage_pct": 20.19},
    "NAWL":   {"wordlist_size": 2598,  "attestation_rate_pct": 48.08, "type_coverage_pct": 1.03,  "token_coverage_pct": 5.15},
    "AVL":    {"wordlist_size": 18558, "attestation_rate_pct": 81.50, "type_coverage_pct": 12.52, "token_coverage_pct": 86.99},
    "HSWL_level1": {"wordlist_size": 3448, "attestation_rate_pct": 92.98, "type_coverage_pct": 2.65, "token_coverage_pct": 60.63},
    "CET4_level1": {"wordlist_size": 4543, "attestation_rate_pct": 93.92, "type_coverage_pct": 3.53, "token_coverage_pct": 72.26},
    "CET6_level1": {"wordlist_size": 8074, "attestation_rate_pct": 93.88, "type_coverage_pct": 6.27, "token_coverage_pct": 82.32},
}

PAPER_OVERLAP = {
    ("CET4_level1", "HSWL_level1"): {"rate": 55.80, "overlap": 2862, "union": 5129},
    ("CET6_level1", "HSWL_level1"): {"rate": 39.00, "overlap": 3233, "union": 8289},
    ("CET4_level1", "CET6_level1"): {"rate": 51.90, "overlap": 4311, "union": 8306},
    ("AWL", "CET6_level1"):         {"rate": 10.29, "overlap": 1043, "union": 10138},
    ("NAWL", "CET6_level1"):        {"rate": 7.78,  "overlap": 770,  "union": 9902},
    ("AVL", "CET6_level1"):         {"rate": 39.46, "overlap": 7536, "union": 19096},
    ("AVL", "AWL"):                 {"rate": 8.04,  "overlap": 1613, "union": 20052},
    ("AVL", "NAWL"):                {"rate": 5.31,  "overlap": 1067, "union": 20089},
    ("AWL", "NAWL"):                {"rate": 8.42,  "overlap": 443,  "union": 5262},
}

PAPER_CORPUS_TOTAL_TOKENS = 16_354_339
PAPER_CORPUS_TOTAL_BOOKS = 94


def main():
    corpus = Corpus(WL / "eftc_corpus.json")
    print(f"Loaded EFTC corpus: {corpus.total_types:,} types, {corpus.total_tokens:,} tokens")
    print(f"Paper reports: {PAPER_CORPUS_TOTAL_TOKENS:,} tokens (Table 2 grand total)")
    diff = corpus.total_tokens - PAPER_CORPUS_TOTAL_TOKENS
    print(f"  -> difference: {diff:+,} tokens ({100*diff/PAPER_CORPUS_TOTAL_TOKENS:+.3f}%)\n")

    lists = {
        "AWL": load_wordlist(WL / "AWL.json"),
        "NAWL": load_wordlist(WL / "NAWL.json"),
        "AVL": load_wordlist(WL / "AVL_old_wrong.json"),
        "HSWL_level1": load_wordlist(WL / "HSWL_level1.json"),
        "CET4_level1": load_wordlist(WL / "CET4_level1.json"),
        "CET6_level1": load_wordlist(WL / "CET6_level1.json"),
    }

    rows = []
    print(f"{'List':14s} {'size':>8s} {'attest%':>9s} {'type%':>8s} {'token%':>8s}   vs paper (attest/type/token)")
    for name, wl in lists.items():
        stats = coverage_stats(wl, corpus)
        p = PAPER[name]
        rows.append({"list": name, **stats, "paper_wordlist_size": p["wordlist_size"],
                      "paper_attestation_rate_pct": p["attestation_rate_pct"],
                      "paper_type_coverage_pct": p["type_coverage_pct"],
                      "paper_token_coverage_pct": p["token_coverage_pct"]})
        print(f"{name:14s} {stats['wordlist_size']:8d} {stats['attestation_rate_pct']:9.2f} "
              f"{stats['type_coverage_pct']:8.2f} {stats['token_coverage_pct']:8.2f}   "
              f"vs  {p['attestation_rate_pct']:.2f} / {p['type_coverage_pct']:.2f} / {p['token_coverage_pct']:.2f}"
              f"  (size in paper: {p['wordlist_size']})")

    with open(OUT / "level1_coverage_reproduction.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print("\n--- Pairwise overlap reproduction (Table 4) ---")
    print(f"{'Pair':30s} {'rate%':>8s}  {'overlap':>8s} {'union':>8s}   vs paper")
    overlap_rows = []
    for (a, b), pv in PAPER_OVERLAP.items():
        stats = overlap_stats(lists[a], lists[b])
        overlap_rows.append({"list_a": a, "list_b": b, **stats,
                              "paper_overlap_rate_pct": pv["rate"],
                              "paper_overlap_word_count": pv["overlap"],
                              "paper_total_unique_words": pv["union"]})
        label = f"{a} vs {b}"
        print(f"{label:30s} {stats['overlap_rate_pct']:8.2f}  {stats['overlap_word_count']:8d} "
              f"{stats['total_unique_words']:8d}   vs  {pv['rate']:.2f} / {pv['overlap']} / {pv['union']}")

    with open(OUT / "overlap_reproduction.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(overlap_rows[0].keys()))
        w.writeheader()
        w.writerows(overlap_rows)

    print(f"\nWrote {OUT/'level1_coverage_reproduction.csv'} and {OUT/'overlap_reproduction.csv'}")


if __name__ == "__main__":
    main()
