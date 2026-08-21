"""
Parses Laurence Anthony's AntBNC Lemma List into JSON -- a real lemma
database (headword -> inflectional forms only, same part of speech; e.g.
"organize -> organize, organized, organizes, organizing", correctly
excluding derivational forms like "organization") to replace the
regex-based inflection heuristic in java_port_pipeline.py's Level 2
construction.

Source: https://www.laurenceanthony.net/resources/wordlists/antbnc_lemmas_ver_004.zip
(linked from the AntConc homepage's "Lemma Lists" section). This is the
same "AntBNC" lemma resource that Tom Cobb's Familizer/Lemmatizer tool
(cited in the paper for Level 2 construction) uses under the hood for
English -- see https://www.lextutor.ca/familizer/, which documents
"different lemma databases depending on language (AntBNC for English)".
Not necessarily byte-identical to whatever exact version the original
study used, but the same underlying resource, not a heuristic substitute.

Run (from repo root): python3 analysis/build_antbnc_lemma_db.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "wordlists" / "antbnc_source" / "antbnc_lemmas_ver_004.txt"
OUT = ROOT / "data" / "wordlists" / "antbnc_lemma_database.json"


def main():
    lemma_db = {}
    with open(SRC, encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            headword = parts[0].strip().lower()
            forms = [p.strip().lower() for p in parts[2:] if p.strip()]
            if headword and forms:
                lemma_db[headword] = forms

    print(f"Parsed {len(lemma_db)} lemma entries from {SRC.name}")
    json.dump(lemma_db, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Wrote {OUT}")

    for name in ["HSWL_level1", "CET4_level1", "CET6_level1"]:
        words = {w.lower() for w in json.load(open(ROOT / "data" / "wordlists" / f"{name}.json"))}
        found = sum(1 for w in words if w in lemma_db)
        print(f"{name}: {found}/{len(words)} ({100*found/len(words):.1f}%) found as lemma headwords")


if __name__ == "__main__":
    main()
