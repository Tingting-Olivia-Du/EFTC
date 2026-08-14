"""
Scans paper.md for in-text (Author, Year) citations and checks each one
has a matching entry in the References list. Prints any in-text citation
that has no corresponding reference entry.

LIMITATION: matching is done against the reference list's FIRST author
surname only, so a citation naming a second author (e.g. "Bauer & Nation,
1993" -> reference list under "Bauer, L., & Nation..." ) will show up as a
false-positive "missing" match if only "Nation" was extracted from the
in-text citation. Treat the output as a shortlist to manually confirm, not
a final verdict -- see report/verification_report.md for the manually
confirmed list of genuinely missing references.

Run (from repo root): python3 analysis/check_citations.py paper/paper.md
"""
import re
import sys
from pathlib import Path


def main(paper_path: str):
    text = Path(paper_path).read_text(encoding="utf-8")
    idx = text.index("\nReferences")
    body, refs_text = text[:idx], text[idx:]

    ref_entries = []
    for line in refs_text.splitlines():
        line = line.strip()
        m = re.search(r"\((\d{4}[a-z]?)\)", line)
        if m:
            ref_entries.append((line.split(",")[0].strip(), m.group(1)))

    citations = set()
    # Pattern 1: "(Author, Year)" or "(Author1, Year; Author2, Year)"
    for m in re.finditer(r"\(([^()]*\d{4}[a-z]?[^()]*)\)", body):
        for part in m.group(1).split(";"):
            mm = re.search(r"([A-Z][A-Za-zÀ-ÿ\-']+)[^,]*,?\s*(\d{4}[a-z]?)", part.strip())
            if mm:
                citations.add((mm.group(1), mm.group(2)))
    # Pattern 2: "Author (Year)" / "Author et al. (Year)" narrative citations
    for m in re.finditer(r"([A-Z][A-Za-zÀ-ÿ\-']+)(?:\s+et al\.)?\s*\((\d{4}[a-z]?)\)", body):
        citations.add((m.group(1), m.group(2)))

    missing = []
    for author, year in sorted(citations):
        year4 = year[:4]
        if not any(author.lower() in s.lower() or s.lower() in author.lower()
                   for s, y in ref_entries if y[:4] == year4):
            missing.append((author, year))

    print(f"In-text citations found: {len(citations)}")
    print(f"Reference-list entries found: {len(ref_entries)}")
    print(f"\nIn-text citations with NO matching reference-list entry ({len(missing)}):")
    for a, y in missing:
        print(f"  - {a} ({y})")


if __name__ == "__main__":
    default_path = Path(__file__).resolve().parent.parent / "paper" / "paper.md"
    main(sys.argv[1] if len(sys.argv) > 1 else str(default_path))
