# EFTC Lexical Coverage Paper — Data & Content Verification Report

**Paper checked:** `paper/paper.md` ("Are Chinese finance undergraduates ready for
English-medium instruction? Evidence from lexical coverage analysis of English
finance textbooks"), from the [tdu/EFTC](https://github.com) repository, as of 2026-08-14.
**Updated 2026-08-19** with a critical data-integrity finding (V1) identified
after advisor review, and again the same day with a full audit of every other
data source used in the study — see
[`data_source_audit.md`](data_source_audit.md) for that companion document
(AWL and NAWL independently confirmed correct; HSWL/CET-4/CET-6/corpus show
no red flags but aren't as rigorously checkable; the BNC/COCA supplementary
lists and Level 2–6 expansion remain unverifiable, per Finding R1).
**Updated 2026-08-20**: the official BNC/COCA word-family data and
supplementary lists behind most of Finding R1's "reproducibility gap" have
been recovered and used to rebuild Level 2–6, and — after the original
Java source code and working data files were subsequently located and
reviewed too — a high-confidence corrected estimate for `AVL*`
(**~92.81%**, down from the paper's reported 94.09%; a sanity check using
this same ground-truth data reproduces the paper's own 94.09% exactly) —
see [`level_reconstruction_attempt.md`](level_reconstruction_attempt.md).

**What this report covers:** (1) a full re-run of every number in the paper that
can be independently recomputed from the raw files present in the repository,
using brand-new code (`analysis/`), (2) a consistency check of the remaining numbers
against the pipeline's own cached output files, and (3) a close read of the
manuscript text for content, citation, and internal-consistency issues.

---

## 0. Critical update (2026-08-19): the "AVL" word list is not the AVL

**The word list used throughout the pipeline as "AVL" is not the Academic
Vocabulary List (Gardner & Davies, 2014).** `archive/scripts/flatten_avl.py`
built `AVL.json` (18,558 words — the file behind every AVL number in Table 4
and Table 10) by flattening `archive/wordlist/AVL_nested.json`, which is
actually a 42-band **general-frequency word list** (band_1: "the, of, be,
and, a, in, to, that, for, have" — ordinary function words, not academic
vocabulary), not AVL data.

The real AVL (from the official Gardner & Davies 2014 family/word-form data,
`data/wordlists/families-AVL.xlsx`) has 1,991 word families / 6,799 word
forms — roughly a third the size of the 18,558-word file the paper actually
used. Recomputed with the correct list:

| Metric | Paper (wrong file) | Corrected |
|---|---|---|
| AVL size | 18,558 | 6,799 |
| AVL attestation rate | 81.50% | 82.16% |
| AVL type coverage | 12.52% | 4.62% |
| **AVL token coverage** | **86.99%** | **50.48%** |
| AVL vs. CET-6 overlap | 39.46% | 19.57% |
| AVL vs. AWL overlap | 8.04% | 17.94% |
| AVL vs. NAWL overlap | 5.31% | 6.55% |

This invalidates the paper's central claim that "the CET-6 WL (86.72%) and
the AVL (86.99%) yield similar levels of token coverage" and the framing of
AVL as the strongest-performing academic word list — the real AVL covers
about half the corpus's tokens on its own, far below CET-6. **Update
2026-08-20:** the starred "AVL\*" combined row (94.09%, the paper's headline
best result) has now been re-derived twice — see
[`level_reconstruction_attempt.md`](level_reconstruction_attempt.md) —
first using recovered official BNC/COCA data to rebuild Level 2–6 from
scratch, then using the actual near-final word lists recovered from the
original researcher's Java project working files, which reproduce the
paper's own (wrong-AVL) 94.09% figure *exactly*. High-confidence estimate:
**AVL\* drops to ~92.81%**, only narrowly ahead of NAWL\* (92.50%, exact
match to the paper) and AWL\* (91.93%, exact match) — a far cry from the
clear win the paper reports, though the overall "nothing reaches 95%"
conclusion still holds. The relative ranking of AVL vs. AWL vs. NAWL survives
directionally but the margin needs a full re-run of the original pipeline
with the corrected AVL source
file. See Finding V1 for full detail and `analysis/avl_data_integrity_check.py`
to reproduce.

**This supersedes Finding D1 in severity and should be fixed before anything
else in this report.**

---

## 1. Headline result

**No numeric transcription errors were found against the pipeline's own cached
output** — but the pipeline's own AVL input data was wrong (see §0/Finding V1
above), so "matches the paper" and "is correct" turned out to be two different
things. Every one of the 64 checked table cells across Tables 2, 4, 5, 6, 7, 8,
9, and 10 matches what the data files say, to the 2-decimal precision the
paper reports. Where independent recomputation from raw inputs was possible
(Level-1 word lists, standalone AWL/NAWL/AVL, all pairwise overlaps, corpus
totals — 15 rows), fresh code reproduced the paper's numbers **exactly**, with
zero difference from the pipeline's own files — the AVL-related rows among
these are simply reproducibly wrong, not transcribed incorrectly.

The investigation also surfaced:
- **A critical data-integrity bug**: the "AVL" word list used throughout is
  actually a general-frequency word list, not the Academic Vocabulary List
  (Finding V1, §0 above).
- **One real numerical/interpretive error** in the Discussion section (Finding D1).
- **A reproducibility gap**: the word-family-expanded (Level 2–6) word lists and
  the BNC/COCA supplementary lists that ~60% of the paper's tables depend on no
  longer exist in the repository in their final form — only the pipeline's
  cached *output* files do (Finding R1).
- **Six in-text citations with no matching reference-list entry** (Finding C1).
- **Several leftover drafting artifacts** (stray text, unresolved phrasing
  alternatives, a section-numbering collision) that should be cleaned up before
  submission (Findings T1–T4).

Finding V1 **does** change a substantive conclusion of the paper (AVL is not,
in fact, comparable to CET-6). The rest do not change the paper's other
substantive conclusions (HSWL/CET-4/
CET-6/AWL/NAWL/AVL all fall short of the 95% comprehension threshold), but D1
and R1 are worth fixing/addressing before the manuscript goes out.

---

## 2. Independent numeric reproduction

### 2.1 What could be recomputed from scratch

The repository still contains the *raw* (Level-1, unexpanded) word lists —
`AWL.json`, `NAWL.json`, `AVL.json`, and the Level-1 HSWL/CET-4/CET-6 lists —
and the full corpus frequency file (`corpus/cleaned_merged_corpus_all.json`,
120,835 types / 16,354,339 tokens). `analysis/coverage_lib.py` re-implements the
paper's three metrics (attestation rate, type coverage, token coverage) and
its overlap formula from the method description in Section 4.2.2, without
looking at any of the old scripts' output. Running it
(`analysis/run_level1_reproduction.py`) against these raw files reproduces:

| Check | Result |
|---|---|
| Corpus totals (120,835 types / 16,354,339 tokens) | **exact match** to Table 2's grand total |
| AWL, NAWL, AVL standalone coverage (Table 10, 3 rows × 3 metrics) | **exact match** |
| HSWL / CET-4 / CET-6 Level-1 coverage (Tables 6/7/8, 3 rows × 3 metrics) | **exact match** |
| All 9 pairwise word-list overlaps (Table 4, in full) | **exact match** |

Every value differs from the paper by 0.00 percentage points. Full output in
`output/level1_coverage_reproduction.csv` and `output/overlap_reproduction.csv`.

*(Minor note: the raw HSWL Level-1 and CET-6 Level-1 and AWL JSON files each
contain a handful of literal duplicate string entries — e.g. HSWL Level-1 has
3,451 array entries but only 3,448 distinct words. This has no effect on the
results since coverage must be computed over a de-duplicated set either way,
which is what both the old pipeline and the new code do — but it is a minor
data-hygiene issue in the raw list files worth cleaning up.)*

### 2.2 What could only be checked against cached output

Tables 3, 5 (partly), 6–9 (Level 2–6 rows), and the starred rows of Table 10
depend on:
- word-family-expanded word lists (Level 2–6, built via the affix rules in
  Table 1 plus a BNC/COCA word-family database), and
- the BNC/COCA supplementary lists (proper names, marginal words, transparent
  compounds, acronyms).

Neither the expanded word-list files nor the supplementary-list source files
exist anywhere in the current repository (see Finding R1). What **does**
exist is `results/statistics.csv` and `results/aca_statistics.csv` — the
pipeline's own cached output. `analysis/verify_cached_tables.py` checks all 49
remaining table rows (Tables 5, 6, 7, 8, 9, and starred Table 10) against
these cache files.

**Result: 49/49 rows match exactly** (`output/cached_table_verification.csv`).
So the paper is a faithful, error-free transcription of what the pipeline last
produced — the open question is whether that pipeline run is still
reproducible from what's in the repo today (it is not — see R1).

---

## 3. Findings

### V1 — The "AVL" word list is not the Academic Vocabulary List (Critical priority)

**Root cause.** `archive/scripts/flatten_avl.py` generates `AVL.json` (used
for every AVL number in Table 4 and Table 10) by flattening the keys of
`archive/wordlist/AVL_nested.json`:

```python
input_path = './wordlist/AVL_nested.json'
...
for band in nested_data.values():
    word_list.extend(band.keys())
```

`AVL_nested.json` is structured as 42 numbered "bands" (`band_1` ...
`band_42`), each containing words with a `frequency` rank and `PoS` tag.
Inspecting it directly:

```
band_1 (first 10 words): the, of, be, and, a, in, to, that, for, have
```

These are the most common function words in English — exactly what a
*general* frequency word list looks like, and exactly what an *academic*
vocabulary list should **not** contain (AWL/NAWL/AVL are explicitly built to
exclude words this basic). `AVL_nested.json` is a general-frequency word
list that was mislabeled or substituted for the real AVL data at some point
in the pipeline's history; nothing in the repository indicates where it
actually came from.

**Scale of the error.** The authoritative AVL (Gardner & Davies, 2014) has
1,991 word families / 6,799 word forms — this is available in
`data/wordlists/families-AVL.xlsx` (the official family/word-form spreadsheet,
column `word` = word form, column `family` = family headword). The `AVL.json`
actually used has 18,558 entries: **2.7× too large**, and a spot check shows
it also contains 351 proper nouns/demonyms (*American, Arabic, Australian,
Afrikaner...*) and ordinary non-academic vocabulary (*bean, wool, grin, canal,
antelope, poet...*) that have no business in an academic word list at all.
Only 4,955 of the 18,558 entries (27%) are actually part of the real AVL;
1,844 real AVL word forms are missing from the file entirely.

**Effect on the paper's numbers**, recomputed with the corrected list
(`analysis/avl_data_integrity_check.py`, which also regenerates
`data/wordlists/AVL_correct.json` from the spreadsheet):

| | Paper (`AVL.json`, wrong) | Corrected (`AVL_correct.json`) |
|---|---|---|
| Size | 18,558 | 6,799 |
| Attestation rate | 81.50% | 82.16% |
| Type coverage | 12.52% | 4.62% |
| **Token coverage** | **86.99%** | **50.48%** |
| Overlap vs. CET-6 WL | 39.46% (7,536 words) | 19.57% (2,434 words) |
| Overlap vs. AWL | 8.04% (1,613 words) | 17.94% (1,507 words) |
| Overlap vs. NAWL | 5.31% (1,067 words) | 6.55% (578 words) |

**Why this matters for the paper's argument.** Section 4.2 states: "the CET-6
WL (86.72%) and the AVL (86.99%) yield similar levels of token coverage,
which further validates the potential of the CET-6 WL as a practical academic
vocabulary resource" — and the abstract frames AVL as the strongest-performing
academic word list. With the corrected data, standalone AVL token coverage is
50.48%, not comparable to CET-6 at all. **Update 2026-08-20:** the starred
"AVL\*" combination (94.09%, the paper's headline best result) has now been
re-derived using the actual near-final word lists recovered from the
original researcher's Java project files (a sanity check with this data
reproduces the paper's own wrong-AVL 94.09% exactly) — see
`level_reconstruction_attempt.md`. High-confidence estimate: AVL\* drops to
~92.81%, only narrowly ahead of NAWL\* (92.50%, exact match to the paper)
and AWL\* (91.93%, exact match) — the paper's ranking of AVL as clearly the
best academic word list does not survive the correction (the real lead is
0.31–0.88pp, not 1.6–2.2pp), though a full re-run of the original pipeline
with the corrected AVL source remains the authoritative way to get a final
publication-ready number.

**Recommended fix:** re-run the original pipeline's AVL-dependent steps
(Table 4's three AVL rows, Table 10's AVL and AVL\* rows, and the
discussion/abstract claims built on them) using `data/wordlists/AVL_correct.json`
(or a fresh export from `families-AVL.xlsx`) in place of the current
`AVL.json`. It would also be worth checking AWL.json (3,109 words vs. the
canonical 3,112) and NAWL.json (2,598 vs. canonical 2,604) for similar,
smaller-scale drift against their authoritative sources, since those came
from the same general pipeline — the gaps there are small enough to plausibly
be normal list-version differences, but haven't been traced to an
authoritative source the way AVL now has been.

### R1 — Reproducibility gap: source files for the word-family expansion are missing (High priority)

The paper's method section (§4.2.1) describes a Java pipeline (`LevelList`,
`AffixLevelHandler`, `LevelListHandler` classes) that expands each Level-1
word list into Levels 2–6 using the Bauer & Nation (1993) affix rules and "the
BNC/COCA word family dataset (Nation, 2017)". None of the following exist in
the repository:
- Any `.java` source file.
- The Level 2–6 expanded word-list files that were actually used to produce
  `results/statistics.csv` (Dec 2024). The only leveled lists present
  (`wordlist_2/wordlist_json_whole/cet4_2.json` etc., dated Oct 2024) are an
  **earlier draft** — e.g. its `cet4_2.json` has 12,998 words vs. the 12,885
  used in the published Table 7, a ~1% difference driven by a later cleanup
  pass that isn't reflected in any file still in the repo.
- The BNC/COCA level-6 word-family dataset itself (Nation, 2017) — this is a
  licensed/external resource, understandably not committed.
- The raw "BNC/COCA supplementary lists" (proper names / marginal words /
  transparent compounds / acronyms — `basewrd31_pn_low.json` etc. referenced
  in `statistics.csv`) — not found anywhere in the repo.

**Practical implication:** if the word-list-generation step ever needs to be
re-run (e.g., adding a textbook, fixing a bug, responding to a reviewer), it
cannot be done from what's currently in version control — only the finished
numbers can be re-displayed. Recommend committing the final Level 1–6 word
list JSON files and the BNC/COCA supplementary sub-lists (they're small, no
copyright issue — derived word lists, not text) to the repository, or at
minimum documenting where they live outside of git.

### D1 — Discussion overstates the AVL's incremental vocabulary burden (Medium priority)

Paper.md, line 188 (Discussion):

> "...integrating these academic word lists still fails to meet the 95%
> threshold for adequate reading comprehension **but requires learners to
> master an additional 18,558 words**, amounting to over 60,000 lexical items
> in total..."

18,558 is the **standalone size of the AVL** (Table 10, "AVL" row). It is not
the number of *additional* words a learner who already knows the General
Composite Word List + BNC/COCA supplementary lists (55,801 words, Table 9)
would need to learn. Because the AVL overlaps substantially with the general
lists (Table 4 shows AVL vs. CET-6 alone overlap at 39.46%), the actual
combined list (AVL*, Table 10) is only 63,153 words — i.e. the true
incremental burden is:

```
63,153 (AVL*, General Composite + BNC/COCA + AVL)
− 55,801 (General Composite + BNC/COCA alone, Table 9)
= 7,352 net-new words
```

not 18,558. The claim overstates the added learning burden by roughly **2.5×**.
The "over 60,000 lexical items in total" figure immediately after is correct
(63,153); only the "additional 18,558 words" framing needs to be fixed —
suggest replacing it with "an additional ~7,350 words beyond the general
composite baseline."

### C1 — Six in-text citations have no matching reference-list entry (Medium priority)

`analysis/check_citations.py` flags candidate mismatches; manually confirmed against
the reference list, these six in-text citations are genuinely absent:

| In-text citation | Location (paper.md) | Notes |
|---|---|---|
| Browne et al. (2013) | line 15, line 174 | Source of the **NAWL** — one of the paper's three core word lists |
| Gardner and Davies (2014) | line 15, line 174 | Source of the **AVL** — one of the paper's three core word lists |
| Cobb (2019) | line 188 | Cited for critique of untargeted vocabulary memorization |
| Wang et al. (2020) | line 189 | Cited re: EMI research scope |
| Graves (2021) | line 190 | Cited re: EMI lexical optimization |
| Zhang & Liu (2022) | line 191 | Cited re: static coverage vs. practical comprehension |

Browne et al. (2013) and Gardner & Davies (2014) are particularly notable
since they're the origin papers for two of the study's six word lists and are
currently un-citable by a reader.

*(Note: `check_citations.py` also flags several second-author names — e.g.
"Nation (1993)", "Yu (2007)", "Gablasova (2015)" — as false positives; those
references do exist, just under their first author's surname. The six above
were manually confirmed as genuinely missing.)*

### T1 — Leftover placeholder text (Low priority, easy fix)

Line 12 ends with a stray `xxx`:
> "...a notable gap between general English competence and discipline-specific
> academic English literacy. xxx"

### T2 — Unresolved drafting alternatives / stray character (Low priority, easy fix)

- Line 18: "lexical coverage has been **consistently/has long been** identified
  as the strongest predictor..." — two alternate phrasings left un-merged,
  plus a stray `+` immediately after the citation: "(Laufer & Sim, 1985)+."
- Line 21: "...general word lists **with and without being supplemented
  by/superimposed with** mainstream academic word lists..." — same pattern.

### T3 — Section-numbering collision (Low priority, easy fix)

Section 3.2 "Data processing" contains subsections numbered **4.2.1** and
**4.2.2** (lines 67, 82: "4.2.1 Construction of leveled word lists" / "4.2.2
Coverage indicators and cumulative coverage calculation"). These should be
3.2.1 / 3.2.2 — as numbered, they collide with the real Section 4.2 ("Coverage
of the academic word lists") that appears later in the Results section.

### T4 — Garbled phrase (Low priority, easy fix)

Line 50: "...is seldom taught at universities with **limited insufficient on**
course textbooks." Reads as a merge of two edits ("limited... textbooks" /
"insufficient... textbooks"); likely should read "...is seldom taught at
universities due to insufficient course textbooks" or similar.

T3 and T4, plus a newer open question about Table 1's Level-3 affix rule
found after the Java source was recovered, are tracked with a redline
Word document at `paper/Section3_Methods_suggested_edits.docx` (local-only)
— see `report/section3_docx_changelog.md` for what's been marked there and
why.

---

## 4. Table-by-table verification detail

See `output/cached_table_verification.csv` for the full row-by-row diff
(49 rows, all "OK") and `output/level1_coverage_reproduction.csv` /
`output/overlap_reproduction.csv` for the from-scratch reproduction (15 rows,
all exact). "Exact"/"matches cache" below means the paper faithfully
transcribes the pipeline's own output — see the ⚠️ rows and Finding V1 for
where that output itself was computed from bad input data.

| Paper table | How verified | Result |
|---|---|---|
| Table 2 (corpus composition) | Arithmetic check (subtotals + grand total) + corpus token count reproduced from raw corpus file | ✅ exact |
| Table 4 (pairwise overlap) | Reproduced from scratch from raw word lists | ✅ exact (9/9) — but the 3 AVL rows use the wrong AVL file, see Finding V1 ⚠️ |
| Table 5 (BNC/COCA supplement) | Checked against cached `statistics.csv` (raw supplement files missing from repo, see R1) | ✅ matches cache (5/5) |
| Table 6 (HSWL) | Level 1 reproduced from scratch; Levels 2–6 checked against cache | ✅ exact / ✅ matches cache (12/12) |
| Table 7 (CET-4 WL) | Level 1 reproduced from scratch; Levels 2–6 checked against cache | ✅ exact / ✅ matches cache (12/12) |
| Table 8 (CET-6 WL) | Level 1 reproduced from scratch; Levels 2–6 checked against cache | ✅ exact / ✅ matches cache (12/12) |
| Table 9 (General Composite) | Checked against cache (depends on Level-6 lists, see R1) | ✅ matches cache (2/2) |
| Table 10 (academic word lists) | Standalone rows reproduced from scratch; starred rows checked against cache | ✅ exact (3/3) / ✅ matches cache (3/3) — but the AVL and AVL* rows use the wrong AVL file, see Finding V1 ⚠️ |

---

## 5. How to reproduce this check

```bash
python3 analysis/run_level1_reproduction.py    # from-scratch reproduction (Tables 2, 4, 6-8 L1, 10 unstarred)
python3 analysis/verify_cached_tables.py       # cache-consistency check (Tables 5, 6-9, 10 starred)
python3 analysis/avl_data_integrity_check.py   # Finding V1: correct-AVL-vs-wrong-AVL comparison
python3 analysis/check_citations.py paper/paper.md   # citation/reference cross-check (needs paper/paper.md locally)
```
Run these from the repository root.

`avl_data_integrity_check.py` requires `openpyxl` (`pip install openpyxl`) to
read `data/wordlists/families-AVL.xlsx`; everything else is standard-library
only.
