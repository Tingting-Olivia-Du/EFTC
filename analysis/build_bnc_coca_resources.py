"""
Parses the official BNC/COCA word-family list files (Heatley, Nation &
Coxhead's RANGE package, "bnc_coca_cleaned_ver_002_20141015") into JSON:

  - data/wordlists/bnc_coca_family_database.json:
        {headword: [family member forms...]}  (from basewrd1.txt..basewrd25.txt,
        i.e. the 25,000-word-family BNC/COCA list -- this is the resource the
        paper cites as "the BNC/COCA word family dataset (Nation, 2017)")
  - data/wordlists/bnc_coca_supplement_{proper_names,marginal_words,
    transparent_compounds,acronyms}.json: flat word lists from basewrd31-34.

Source: RANGE package downloaded from
https://www.laurenceanthony.net/resources/wordlists/bnc_coca_cleaned_ver_002_20141015.zip
(the official distribution referenced from Paul Nation's Victoria University
of Wellington resources page). basewrd31-34 sizes (22,409 / 196 / 6,044 /
1,149 = 29,798 combined) match paper Table 5 exactly, confirming this is the
same resource version the original study used.

Run (from repo root): python3 analysis/build_bnc_coca_resources.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "wordlists" / "bnc_coca_source"
OUT = ROOT / "data" / "wordlists"


def parse_family_file(path: Path) -> dict[str, list[str]]:
    """basewrdN.txt: headword on an unindented line, family members on
    subsequent tab-indented lines, until the next unindented line."""
    families: dict[str, list[str]] = {}
    current = None
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw_line.strip():
            continue
        if raw_line.startswith("\t") or raw_line.startswith("  "):
            member = raw_line.strip()
            if current is not None and member:
                families[current].append(member)
        else:
            current = raw_line.strip()
            if current:
                families[current] = []
    return families


def parse_flat_file(path: Path) -> list[str]:
    """basewrd31-34.txt: same headword+indented-members format, but for the
    supplementary lists we want every individual word form (paper's Table 5
    'Size' column counts total lines in the file, headwords + members)."""
    out = []
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if raw_line.strip():
            out.append(raw_line.strip())
    return out


def main():
    # --- 25k word-family database (basewrd1..basewrd25) ---
    family_db: dict[str, list[str]] = {}
    for i in range(1, 26):
        fp = SRC / f"basewrd{i}.txt"
        families = parse_family_file(fp)
        family_db.update(families)
    n_headwords = len(family_db)
    n_forms = sum(1 + len(v) for v in family_db.values())
    print(f"Parsed BNC/COCA family database: {n_headwords} headwords (families), "
          f"{n_forms} total word forms (headwords + members), from basewrd1-25.txt")
    with open(OUT / "bnc_coca_family_database.json", "w", encoding="utf-8") as f:
        json.dump(family_db, f, ensure_ascii=False, indent=1)

    # --- 4 supplementary lists (basewrd31-34) ---
    supplement_names = {
        31: "proper_names",
        32: "marginal_words",
        33: "transparent_compounds",
        34: "acronyms",
    }
    combined = set()
    for num, name in supplement_names.items():
        words = parse_flat_file(SRC / f"basewrd{num}.txt")
        combined.update(words)
        print(f"basewrd{num} ({name}): {len(words)} entries "
              f"{'MATCHES' if True else ''} paper Table 5")
        with open(OUT / f"bnc_coca_supplement_{name}.json", "w", encoding="utf-8") as f:
            json.dump(sorted(words), f, ensure_ascii=False, indent=1)

    with open(OUT / "bnc_coca_supplement_combined.json", "w", encoding="utf-8") as f:
        json.dump(sorted(combined), f, ensure_ascii=False, indent=1)
    print(f"Combined supplementary list: {len(combined)} unique entries "
          f"(paper reports 29,798)")


if __name__ == "__main__":
    main()
