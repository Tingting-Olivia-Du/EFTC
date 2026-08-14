"""
Cross-checks paper.md Tables 5, 6, 7, 8, 9 and the starred rows of Table 10
against the original pipeline's cached output files
(data/cached_results/statistics.csv and aca_statistics.csv).

These tables depend on Level 2-6 word-family-expanded word lists and the
BNC/COCA supplementary lists, whose raw source files are not present in
the EFTC repository (see report). This script therefore checks
"does paper.md match what the pipeline last produced?" rather than
"is the pipeline's own computation correct?" -- that distinction is the
core finding of report/verification_report.md.

Run: python3 src/verify_cached_tables.py
"""
import csv
from pathlib import Path

from paper_tables import ALL_STATISTICS_CSV_ROWS, TABLE10_ACADEMIC_STANDALONE

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cached_results"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

TOL = 0.011  # paper rounds to 2 decimals; allow 0.01 rounding slack


def load_statistics_csv(path):
    rows = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            attest = r["coverage_percentage"] or r["wordlist_usage"]
            rows[r["file_name"]] = {
                "size": int(r["wordlist_size"]),
                "attestation_pct": float(attest) if attest else None,
                "type_pct": float(r["unique_words_covered_by_wl"]),
                "token_pct": float(r["frequency_coverage_percentage"]),
            }
    return rows


def load_aca_statistics_csv(path):
    rows = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows[r["file_name"]] = {
                "size": int(r["wordlist_size"]),
                "attestation_pct": float(r["wordlist_usage"]),
                "type_pct": float(r["unique_words_covered_by_wl"]),
                "token_pct": float(r["frequency_coverage_percentage"]),
            }
    return rows


def check(table, label, source_file, paper_vals, cached_row, results, mismatches):
    if cached_row is None:
        results.append([table, label, source_file, "MISSING FROM CACHE", "", "", "", "", "", "", ""])
        mismatches.append(f"{table} / {label}: source file '{source_file}' not found in cache")
        return

    paper_size, paper_attest, paper_type, paper_token = paper_vals
    size_ok = cached_row["size"] == paper_size
    attest_ok = cached_row["attestation_pct"] is None or abs(cached_row["attestation_pct"] - paper_attest) <= TOL
    type_ok = abs(cached_row["type_pct"] - paper_type) <= TOL
    token_ok = abs(cached_row["token_pct"] - paper_token) <= TOL
    ok = size_ok and attest_ok and type_ok and token_ok

    results.append([
        table, label, source_file,
        paper_size, cached_row["size"], "OK" if size_ok else "MISMATCH",
        f"{paper_attest:.2f}", f"{cached_row['attestation_pct']:.2f}" if cached_row["attestation_pct"] is not None else "n/a",
        f"{paper_type:.2f}", f"{cached_row['type_pct']:.2f}",
        f"{paper_token:.2f}", f"{cached_row['token_pct']:.2f}",
        "OK" if ok else "MISMATCH",
    ])
    if not ok:
        mismatches.append(f"{table} / {label} ({source_file}): paper={paper_vals} cached={cached_row}")


def main():
    stats = load_statistics_csv(CACHE / "statistics.csv")
    aca_stats = load_aca_statistics_csv(CACHE / "aca_statistics.csv")

    results = [["table", "row", "source_file", "paper_size", "cached_size", "size_check",
                "paper_attest%", "cached_attest%", "paper_type%", "cached_type%",
                "paper_token%", "cached_token%", "overall"]]
    mismatches = []

    for table, label, source_file, size, attest, typ, token in ALL_STATISTICS_CSV_ROWS:
        check(table, label, source_file, (size, attest, typ, token), stats.get(source_file), results, mismatches)

    for table, label, source_file, size, attest, typ, token in TABLE10_ACADEMIC_STANDALONE:
        check(table, label, source_file, (size, attest, typ, token), aca_stats.get(source_file), results, mismatches)

    with open(OUT / "cached_table_verification.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(results)

    n_checked = len(results) - 1
    n_bad = len(mismatches)
    print(f"Checked {n_checked} paper table rows against cached pipeline output files.")
    print(f"  Matches: {n_checked - n_bad}")
    print(f"  Mismatches: {n_bad}")
    if mismatches:
        print("\nMismatch details:")
        for m in mismatches:
            print(" -", m)
    print(f"\nFull row-by-row comparison written to {OUT/'cached_table_verification.csv'}")


if __name__ == "__main__":
    main()
