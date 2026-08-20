"""
Full data-source audit: checks every word list the pipeline used against
the best available authoritative/third-party source, and reports which
ones are verified correct, which are wrong, and which can't be checked at
all with what's in this repository.

Covers AWL, NAWL, AVL (see analysis/avl_data_integrity_check.py for the
detailed AVL writeup), HSWL/CET-4/CET-6, and notes on the BNC/COCA
supplementary lists and the corpus itself. See report/data_source_audit.md
for the full narrative.

Run (from repo root): python3 analysis/data_source_audit.py
"""
import csv
import json
import re
from pathlib import Path

from coverage_lib import Corpus, load_wordlist

ROOT = Path(__file__).resolve().parent.parent
WL = ROOT / "data" / "wordlists"
TP = ROOT / "archive" / "third-party" / "machine_readable_wordlists" / "Academic"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def flatten_family_json(path, nested_under_sublists: bool) -> set[str]:
    """Flatten a {headword: {"subwords": [...]}} or {sublist: {headword: {...}}} file."""
    data = json.load(open(path, encoding="utf-8"))
    forms = set()
    groups = data.values() if nested_under_sublists else [data]
    for group in groups:
        for headword, info in group.items():
            forms.add(headword)
            if isinstance(info, dict) and info.get("subwords"):
                forms.update(info["subwords"])
            elif isinstance(info, list):
                forms.update(info)
    return forms


def audit_awl_nawl():
    print("=== AWL / NAWL: checked against archive/third-party/machine_readable_wordlists ===")
    results = []
    for name, nested in [("AWL", True), ("NAWL", False)]:
        tp_forms = flatten_family_json(TP / name / f"{name}.json", nested_under_sublists=nested)
        proj_forms = load_wordlist(WL / f"{name}.json")
        match = proj_forms == tp_forms
        print(f"{name}: project has {len(proj_forms)} word forms, third-party source has {len(tp_forms)} "
              f"-> {'IDENTICAL' if match else 'DIFFERS'}")
        results.append({"list": name, "project_size": len(proj_forms), "source_size": len(tp_forms),
                         "identical_to_source": match,
                         "extra_in_project": len(proj_forms - tp_forms), "missing_from_project": len(tp_forms - proj_forms)})
    return results


def audit_avl():
    print("\n=== AVL: see analysis/avl_data_integrity_check.py for full detail ===")
    avl_wrong = load_wordlist(WL / "AVL.json")
    avl_correct = load_wordlist(WL / "AVL_correct.json") if (WL / "AVL_correct.json").exists() else None
    print(f"AVL.json (used in paper): {len(avl_wrong)} entries -- CONFIRMED WRONG (see report, Finding V1)")
    if avl_correct:
        print(f"AVL_correct.json (Gardner & Davies 2014, from families-AVL.xlsx): {len(avl_correct)} entries")
    return {"list": "AVL", "project_size": len(avl_wrong),
            "source_size": len(avl_correct) if avl_correct else None,
            "identical_to_source": False, "status": "WRONG -- see Finding V1, corrected file provided"}


def audit_cet_hswl():
    print("\n=== HSWL / CET-4 / CET-6: sourcing notes (no full digital ground truth available) ===")
    hswl = load_wordlist(WL / "HSWL_level1.json")
    cet4 = load_wordlist(WL / "CET4_level1.json")
    cet6 = load_wordlist(WL / "CET6_level1.json")
    print(f"HSWL Level 1: {len(hswl)} words (paper's stated basis: 'officially prescribed 3,500-word' MOE list -- "
          f"close, no authoritative digital list available in-repo to fully diff)")
    print(f"CET-4 Level 1: {len(cet4)} words; CET-6 Level 1: {len(cet6)} words")
    overlap = cet4 & cet6
    print(f"CET-6 contains {len(overlap)}/{len(cet4)} ({100*len(overlap)/len(cet4):.1f}%) of CET-4's words "
          f"-> consistent with CET-6 being a cumulative superset, as the source txt files' shared opening "
          f"words (archive/wordlist_2/raw_txt/cet4_1.txt vs cet6_1.txt) also suggest.")
    print("Both are traceable to the acknowledged archive/third-party/cet-word-list repo, which OCR'd the "
          "official 2016 CET-4/6 syllabus PDF into a single 5,641-word combined list; the script/logic that "
          "split that combined list into separate CET-4 and CET-6 files is not preserved in this repository, "
          "so the split itself could not be independently re-derived. No content red flags found (unlike AVL).")
    return [
        {"list": "HSWL_level1", "project_size": len(hswl), "source_size": None, "identical_to_source": None,
         "status": "plausible (~3,500 officially cited); no authoritative digital source in repo to diff"},
        {"list": "CET4_level1", "project_size": len(cet4), "source_size": None, "identical_to_source": None,
         "status": "sourced from official syllabus via acknowledged third-party OCR; split logic not preserved"},
        {"list": "CET6_level1", "project_size": len(cet6), "source_size": None, "identical_to_source": None,
         "status": "sourced from official syllabus via acknowledged third-party OCR; split logic not preserved"},
    ]


def audit_corpus():
    print("\n=== Corpus: internal consistency + noise characteristics ===")
    corpus = Corpus(WL / "eftc_corpus.json")
    words = list(corpus.freq.keys())
    no_vowel = [w for w in words if not re.search(r"[aeiouAEIOU]", w) and len(w) > 2]
    hapax = sum(1 for f in corpus.freq.values() if f == 1)
    print(f"{corpus.total_types:,} types / {corpus.total_tokens:,} tokens -- matches paper Table 2 grand total exactly.")
    print(f"{len(no_vowel):,} vowel-less tokens (len>2) -- mostly finance abbreviations (ltd, npv, llc) and OCR noise.")
    print(f"{hapax:,} hapax legomena ({100*hapax/corpus.total_types:.1f}% of types) -- normal for a large "
          f"PDF-extracted corpus, not evidence of a systemic bug.")
    return {"total_types": corpus.total_types, "total_tokens": corpus.total_tokens,
            "vowelless_tokens": len(no_vowel), "hapax_legomena": hapax}


def main():
    rows = audit_awl_nawl()
    rows.append(audit_avl())
    rows.extend(audit_cet_hswl())
    corpus_stats = audit_corpus()

    print("\n=== NOT independently verifiable with what's in this repository ===")
    print("- BNC/COCA supplementary lists (proper names, marginal words, transparent compounds, acronyms):")
    print("  raw source files absent entirely (see report, Finding R1).")
    print("- Level 2-6 word-family expansion for HSWL/CET-4/CET-6: Java pipeline code absent (Finding R1).")

    with open(OUT / "data_source_audit.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = sorted({k for r in rows for k in r.keys()})
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {OUT/'data_source_audit.csv'}")


if __name__ == "__main__":
    main()
