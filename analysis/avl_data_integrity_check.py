"""
CRITICAL FINDING: the AVL.json used throughout the pipeline (and therefore
throughout paper.md's Table 4 and Table 10) is NOT the Academic Vocabulary
List (Gardner & Davies, 2014). It was built by archive/scripts/flatten_avl.py
flattening archive/wordlist/AVL_nested.json -- which is actually a 42-band
general-frequency word list (band_1 starts with "the, of, be, and, a, in,
to, that, for, have"), not academic vocabulary.

This script builds the CORRECT AVL word-form list from the authoritative
source (data/wordlists/families-AVL.xlsx, the official Gardner & Davies
2014 family/word-form spreadsheet) and recomputes every AVL-dependent
number that raw data supports, comparing it against what the paper
currently reports.

Requires: pip install openpyxl

Run (from repo root): python3 analysis/avl_data_integrity_check.py
"""
import json
from pathlib import Path

import openpyxl

from coverage_lib import Corpus, load_wordlist, coverage_stats, overlap_stats

ROOT = Path(__file__).resolve().parent.parent
WL = ROOT / "data" / "wordlists"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

PAPER_AVL_STANDALONE = {"size": 18558, "attestation_pct": 81.50, "type_pct": 12.52, "token_pct": 86.99}
PAPER_AVL_OVERLAP = {
    "CET6_level1": {"rate": 39.46, "overlap": 7536, "union": 19096},
    "AWL": {"rate": 8.04, "overlap": 1613, "union": 20052},
    "NAWL": {"rate": 5.31, "overlap": 1067, "union": 20089},
}


def build_correct_avl_wordlist() -> list[str]:
    """Extract the official AVL word-form list from families-AVL.xlsx.

    Sheet 'data' has one row per (family, word-form, PoS) combination, with
    columns famRank, family, famFreq, word, PoS, freq, ratio, categ, domain.
    We take the distinct 'word' column values -- this is the same
    granularity ("word forms", not "word families") that the paper uses to
    size AWL (3,107 forms from 570 families) and NAWL (2,598 forms from 963
    families), so it is the correct apples-to-apples basis for AVL too.
    """
    wb = openpyxl.load_workbook(WL / "families-AVL.xlsx", read_only=True)
    ws = wb["data"]
    rows = list(ws.iter_rows(values_only=True))[1:]
    families = {r[1] for r in rows}
    word_forms = sorted({str(r[3]) for r in rows})  # str() guards 2 cells Excel parsed as bool (true/false)
    print(f"Official AVL (Gardner & Davies, 2014): {len(families)} word families, "
          f"{len(word_forms)} unique word forms ({len(rows)} family/PoS rows).")
    out_path = WL / "AVL_correct.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(word_forms, f, ensure_ascii=False, indent=2)
    print(f"Wrote {out_path}")
    return word_forms


def diagnose_wrong_file():
    nested_path = ROOT / "archive" / "wordlist" / "AVL_nested.json"
    if not nested_path.exists():
        print("(archive/wordlist/AVL_nested.json not found -- skipping diagnostic dump)")
        return
    nested = json.load(open(nested_path, encoding="utf-8"))
    band1 = list(nested.get("band_1", {}).keys())[:10]
    total = len({w for band in nested.values() for w in band})
    print(f"\nWhat AVL.json was actually built from (archive/wordlist/AVL_nested.json):")
    print(f"  {len(nested)} frequency bands, {total} unique words total")
    print(f"  band_1 (should be the MOST 'academic' words if this were really AVL): {band1}")
    print("  -> these are ordinary high-frequency function words, not academic vocabulary.")
    print("  -> archive/scripts/flatten_avl.py flattened this into the 18,558-word AVL.json used everywhere.")


def main():
    diagnose_wrong_file()
    avl_correct = build_correct_avl_wordlist()

    corpus = Corpus(WL / "eftc_corpus.json")
    avl_wrong = load_wordlist(WL / "AVL.json")
    awl = load_wordlist(WL / "AWL.json")
    nawl = load_wordlist(WL / "NAWL.json")
    cet6 = load_wordlist(WL / "CET6_level1.json")

    print("\n=== Standalone AVL coverage: paper (wrong file) vs. corrected ===")
    rows = []
    for label, wl in [("AVL_wrong (used in paper)", avl_wrong), ("AVL_correct (Gardner & Davies 2014)", avl_correct)]:
        s = coverage_stats(wl, corpus)
        rows.append({"list": label, **s})
        print(f"{label:38s} size={s['wordlist_size']:6d}  attest={s['attestation_rate_pct']:6.2f}%  "
              f"type={s['type_coverage_pct']:6.2f}%  token={s['token_coverage_pct']:6.2f}%")
    print(f"{'paper-reported AVL row (for reference)':38s} size={PAPER_AVL_STANDALONE['size']:6d}  "
          f"attest={PAPER_AVL_STANDALONE['attestation_pct']:6.2f}%  type={PAPER_AVL_STANDALONE['type_pct']:6.2f}%  "
          f"token={PAPER_AVL_STANDALONE['token_pct']:6.2f}%")

    print("\n=== Table 4 AVL overlap rows: paper (wrong file) vs. corrected ===")
    overlap_rows = []
    for name, other in [("CET6_level1", cet6), ("AWL", awl), ("NAWL", nawl)]:
        s_wrong = overlap_stats(avl_wrong, other)
        s_correct = overlap_stats(avl_correct, other)
        pv = PAPER_AVL_OVERLAP[name]
        overlap_rows.append({"pair": f"AVL vs {name}", **{f"wrong_{k}": v for k, v in s_wrong.items()},
                              **{f"correct_{k}": v for k, v in s_correct.items()},
                              "paper_rate_pct": pv["rate"], "paper_overlap": pv["overlap"], "paper_union": pv["union"]})
        print(f"AVL vs {name:12s} paper/wrong: rate={s_wrong['overlap_rate_pct']:6.2f}%  "
              f"overlap={s_wrong['overlap_word_count']:6d}  union={s_wrong['total_unique_words']:6d}   |   "
              f"corrected: rate={s_correct['overlap_rate_pct']:6.2f}%  overlap={s_correct['overlap_word_count']:6d}  "
              f"union={s_correct['total_unique_words']:6d}")

    import csv
    with open(OUT / "avl_correction.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(OUT / "avl_overlap_correction.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(overlap_rows[0].keys()))
        w.writeheader()
        w.writerows(overlap_rows)
    print(f"\nWrote {OUT/'avl_correction.csv'} and {OUT/'avl_overlap_correction.csv'}")

    print("\nNOTE: Table 10's starred 'AVL*' row (94.09% -- AVL combined with the General")
    print("Composite Word List + BNC/COCA supplementary lists) cannot be recomputed with")
    print("the corrected AVL list: it needs the Level 2-6 word-family-expanded general")
    print("lists and BNC/COCA supplementary lists, which are not in this repository (see")
    print("report, Finding R1). Given the standalone AVL token coverage drops from 86.99%")
    print("to 50.48%, AVL* should be expected to drop substantially below 94.09% as well,")
    print("and the paper's ranking of AVL as the best-performing academic word list should")
    print("be re-examined once the pipeline is re-run with the corrected AVL source file.")


if __name__ == "__main__":
    main()
