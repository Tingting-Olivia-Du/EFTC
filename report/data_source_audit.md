# Data Source Audit

Full audit of every word list and data source behind the paper's coverage
analysis: what it's supposed to be, what it actually is, and how each was
checked. Prompted by the advisor catching that the AVL word-list size didn't
match the published figures (see `verification_report.md`, Finding V1, for
the full writeup of that one). This document extends the same scrutiny to
every other data source used in the study.

Reproduce with: `python3 analysis/data_source_audit.py` (and
`python3 analysis/avl_data_integrity_check.py` for the AVL detail).

---

## Summary

| Data source | Status | Basis |
|---|---|---|
| **AWL** (Coxhead, 2000) | ✅ Verified correct | Byte-for-byte identical word-form set to the acknowledged third-party source; matches the official 570-family count exactly |
| **NAWL** (Browne et al., 2013) | ✅ Verified correct | Byte-for-byte identical word-form set to the acknowledged third-party source; matches the official 963-family count exactly |
| **AVL** (Gardner & Davies, 2014) | ❌ **Confirmed wrong — now fixed** | Was actually a general-frequency word list mislabeled as "AVL" in an upstream third-party dependency, not the real Academic Vocabulary List. See Finding V1. |
| **HSWL** (MOE high school list) | ⚠️ Plausible, not independently verifiable | Size (3,448) is close to the commonly-cited "3,500-word" figure; no authoritative digital source in the repo to fully diff its contents against |
| **CET-4 / CET-6** | ⚠️ Plausible, not independently verifiable | Traceable to the official 2016 CET syllabus via an acknowledged third-party OCR'd list; the CET-4/CET-6 split logic itself isn't preserved in the repo |
| **BNC/COCA supplementary lists** (proper names, marginal words, transparent compounds, acronyms) | ❌ Cannot verify | Raw source files are entirely absent from the repository (Finding R1) |
| **Level 2–6 word-family expansion** (all six word lists) | ❌ Cannot verify | The Java pipeline that built these is entirely absent from the repository (Finding R1) |
| **EFTC corpus** (`eftc_corpus.json`) | ✅ Internally consistent | 120,835 types / 16,354,339 tokens matches paper Table 2 exactly; noise levels typical of a large PDF-extracted corpus |

Only **AVL** turned out to be wrong. AWL and NAWL are independently
confirmed correct against a real external source (not just self-consistent
with the paper, which is a weaker check — see `verification_report.md`
§1 for that distinction). HSWL/CET-4/CET-6 and the corpus show no red flags
but also could not be as rigorously checked, for lack of an authoritative
digital source to diff against. The BNC/COCA supplementary lists and the
Level 2–6 expansion remain entirely unverifiable with what's in this
repository — that gap (Finding R1) is unchanged by this audit.

---

## 1. AWL and NAWL — verified correct

`archive/third-party/machine_readable_wordlists/Academic/{AWL,NAWL}/*.json`
is a vendored copy of the repository this project explicitly acknowledges
(github.com/lpmi-13/machine_readable_wordlists). Flattening its
family→word-form structure and comparing directly to `data/wordlists/AWL.json`
and `NAWL.json`:

- **AWL**: 570 word families → 3,107 word forms in both the third-party
  source and the project's file. Identical sets, zero differences.
- **NAWL**: 963 word families → 2,598 word forms in both. Identical sets,
  zero differences.

Both family counts (570, 963) match the well-known published figures for
Coxhead (2000) and Browne et al. (2013) respectively. The word-form counts
the advisor initially compared against (3,112 and 2,604, from
eapfoundation.com) differ by a handful of words from what's used here — that
reflects normal variation between two independent, legitimate secondary
compilations of the same official word-family lists into individual word
forms, not a data error. **No action needed for AWL or NAWL.**

## 2. AVL — confirmed wrong (see Finding V1 for full detail)

The word list used throughout the pipeline as "AVL" (`data/wordlists/AVL.json`,
18,558 entries) is not the Academic Vocabulary List. Tracing it back:

1. `archive/scripts/flatten_avl.py` built it by flattening
   `archive/wordlist/AVL_nested.json`.
2. `AVL_nested.json` is, byte-for-byte, the same file as
   `archive/third-party/machine_readable_wordlists/Academic/AVL/AVL.json` —
   i.e. it's a straight copy of the acknowledged third-party dependency, not
   something corrupted by this project's own processing.
3. That third-party file is *itself* mislabeled: its own README describes it
   as "organized by frequency band (1-42) of 500 words (lemmas) each," and
   band 1 is `the, of, be, and, a, in, to, that, for, have` — ordinary
   high-frequency function words. This is not academic vocabulary by any
   definition, and it is not what Gardner & Davies (2014) published.

So the bug's origin is one level upstream of this project: an external,
acknowledged open-source dependency has bad data in its `Academic/AVL/`
folder, and nothing in the pipeline caught it before it propagated into
every AVL-related number in the paper. (A basic sanity check — "does the
list I'm using for 'academic vocabulary' contain the word 'the'?" — would
have caught this immediately, for what it's worth going forward.)

The fix: `data/wordlists/families-AVL.xlsx` (the real Gardner & Davies 2014
family/word-form spreadsheet) and `data/wordlists/AVL_correct.json` (6,799
word forms extracted from it) are now in the repository. Recomputed
coverage numbers are in `verification_report.md`, Finding V1 — headline
change: AVL's standalone token coverage drops from the paper's reported
86.99% to 50.48%.

## 3. HSWL, CET-4, CET-6 — plausible, not independently verifiable

**HSWL.** The paper states its basis as "the officially prescribed
3,500-word high school vocabulary list (Ministry of Education of the
People's Republic of China, 2019)." The project's HSWL Level-1 list has
3,448 words — 1.5% under the commonly-cited 3,500 figure, which is a
plausible amount of normal list-compilation variation (e.g., a handful of
proper nouns or duplicate cross-listed items excluded). There is no
authoritative *digital, diffable* version of the official MOE list in this
repository or its acknowledged dependencies, so — unlike AWL/NAWL/AVL —
this could not be checked word-for-word against an external ground truth.

**CET-4 / CET-6.** Both are traceable to a legitimate source: the
acknowledged `archive/third-party/cet-word-list` repository, whose README
states its word list was OCR'd directly from the official *National College
English Test (CET-4 and CET-6) Syllabus (2016 revised edition)* PDF — the
same source the paper cites in its references. That repository provides one
**combined** list of 5,641 words (CET-4 and CET-6 together, undifferentiated).
The project's separate `cet4_1.txt` (4,543 words) and `cet6_1.txt` (8,078
words, 8,074 after de-duplication) must therefore have been split out from
that combined list (or an equivalent source) by some process not preserved
in this repository — no script or intermediate file documenting the split
logic was found.

What can be confirmed: CET-6 contains 4,311 of CET-4's 4,543 words (94.9%),
and both files' source `.txt` versions open with the identical run of words
(`B.C., Bible, Britain, British, Canada...`). This is consistent with CET-6
being compiled as a **cumulative** list (all of CET-4's vocabulary plus
CET-6-specific additions) rather than an independent CET-6-only list — a
reasonable and common design choice, and consistent with how the paper uses
these lists (see Table 4's 51.90% CET-4/CET-6 overlap). It does *not*, on
its own, explain why CET-6 totals 8,074 words against the "~6,400 words"
figure the paper's introduction cites (National College English Test
Committee, 2016) — that gap may simply reflect the difference between
"cumulative total vocabulary" and "CET-6-specific target vocabulary," two
different things that get conflated across different published descriptions
of CET-6, but this repository doesn't contain enough to settle it either way.

**No red flags were found for HSWL, CET-4, or CET-6** — nothing resembling
the AVL situation (an obviously wrong, mislabeled file) turned up. But
"no red flags in a size-and-provenance check" is a weaker guarantee than
the byte-for-byte match achieved for AWL/NAWL, so these three should be
considered plausible rather than independently confirmed.

## 4. BNC/COCA supplementary lists — cannot verify (unchanged from Finding R1)

Table 5's four components (proper names, marginal words, transparent
compounds, acronyms) and their combined list are computed from source files
(`basewrd31_pn_low.json`, `basewrd32_mw_low.json`, `basewrd33_tc_low.json`,
`basewrd34_ab_low.json`) that do not exist anywhere in this repository. This
audit did not turn up any new leads on their whereabouts or an external
authoritative source to substitute. This remains an open gap — see
`verification_report.md`, Finding R1.

## 5. Level 2–6 word-family expansion — cannot verify (unchanged from Finding R1)

Same situation as the BNC/COCA lists: the Java code (`LevelList`,
`AffixLevelHandler`, `LevelListHandler`) and the resulting expanded word-list
files for Levels 2–6 of HSWL/CET-4/CET-6 are not in this repository. No new
information surfaced in this audit beyond what Finding R1 already documents.

## 6. The corpus itself — internally consistent, normal noise levels

`data/wordlists/eftc_corpus.json` has 120,835 distinct types and 16,354,339
total tokens, matching the paper's Table 2 grand total exactly. Basic noise
checks:

- 5,324 tokens (of 120,835) contain no vowel and are longer than 2
  characters — spot-checking these shows a mix of legitimate finance
  abbreviations (`ltd`, `npv`, `llc`) and OCR/extraction artifacts. Not
  unusual for a corpus built by stripping non-alphabetic characters from
  94 PDF-derived textbooks.
- 41.6% of types occur exactly once (hapax legomena) — expected for a
  large, topically diverse corpus with many proper nouns and technical
  terms; not evidence of a systemic extraction problem.

No corpus-level issues were found beyond what the paper's own limitations
section already acknowledges (structural imbalance from repeated textbook
adoption, uneven course representation).

---

## What "rerunning all the data" actually means here

Given the above, "re-running everything" breaks into three buckets:

1. **AWL, NAWL, HSWL, CET-4, CET-6, corpus totals** — already re-run from
   raw data as part of this audit and the earlier verification pass
   (`analysis/run_level1_reproduction.py`, `analysis/data_source_audit.py`).
   All confirmed either correct (AWL/NAWL) or unchanged/plausible
   (HSWL/CET-4/CET-6/corpus). Nothing to fix.
2. **AVL** — re-run with corrected data
   (`analysis/avl_data_integrity_check.py`). Standalone AVL numbers are
   now known; the combined AVL\* figure and Table 4's AVL rows need the
   original Java pipeline re-run with the corrected AVL source file to get
   final, paper-ready numbers (bucket 3 below explains why this repo can't
   do that step itself).
3. **Level 2–6 expansion, BNC/COCA supplementary lists, and everything
   downstream of them (Tables 3, 5, 6–9's higher levels, Table 10's starred
   rows)** — cannot be re-run at all from this repository; the source
   files and code that would do it don't exist here (Finding R1). This is
   the one piece of "rerun everything" that remains genuinely blocked, not
   for lack of trying.
