# EFTC Lexical Coverage Paper — Data & Content Verification Report

**Paper checked:** `paper/paper.md` ("Are Chinese finance undergraduates ready for
English-medium instruction? Evidence from lexical coverage analysis of English
finance textbooks"), from the [tdu/EFTC](https://github.com) repository, as of 2026-08-14.

**What this report covers:** (1) a full re-run of every number in the paper that
can be independently recomputed from the raw files present in the repository,
using brand-new code (`analysis/`), (2) a consistency check of the remaining numbers
against the pipeline's own cached output files, and (3) a close read of the
manuscript text for content, citation, and internal-consistency issues.

---

## 1. Headline result

**No numeric transcription errors were found.** Every one of the 64 checked
table cells across Tables 2, 4, 5, 6, 7, 8, 9, and 10 matches what the data
files say, to the 2-decimal precision the paper reports. Where independent
recomputation from raw inputs was possible (Level-1 word lists, standalone
AWL/NAWL/AVL, all pairwise overlaps, corpus totals — 15 rows), fresh code
reproduced the paper's numbers **exactly**, with zero difference.

However, the investigation surfaced:
- **One real numerical/interpretive error** in the Discussion section (Finding D1).
- **A reproducibility gap**: the word-family-expanded (Level 2–6) word lists and
  the BNC/COCA supplementary lists that ~60% of the paper's tables depend on no
  longer exist in the repository in their final form — only the pipeline's
  cached *output* files do (Finding R1).
- **Six in-text citations with no matching reference-list entry** (Finding C1).
- **Several leftover drafting artifacts** (stray text, unresolved phrasing
  alternatives, a section-numbering collision) that should be cleaned up before
  submission (Findings T1–T4).

None of these findings change the paper's substantive conclusions (HSWL/CET-4/
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

---

## 4. Table-by-table verification detail

See `output/cached_table_verification.csv` for the full row-by-row diff
(49 rows, all "OK") and `output/level1_coverage_reproduction.csv` /
`output/overlap_reproduction.csv` for the from-scratch reproduction (15 rows,
all exact). Summary:

| Paper table | How verified | Result |
|---|---|---|
| Table 2 (corpus composition) | Arithmetic check (subtotals + grand total) + corpus token count reproduced from raw corpus file | ✅ exact |
| Table 4 (pairwise overlap) | Reproduced from scratch from raw word lists | ✅ exact (9/9) |
| Table 5 (BNC/COCA supplement) | Checked against cached `statistics.csv` (raw supplement files missing from repo, see R1) | ✅ matches cache (5/5) |
| Table 6 (HSWL) | Level 1 reproduced from scratch; Levels 2–6 checked against cache | ✅ exact / ✅ matches cache (12/12) |
| Table 7 (CET-4 WL) | Level 1 reproduced from scratch; Levels 2–6 checked against cache | ✅ exact / ✅ matches cache (12/12) |
| Table 8 (CET-6 WL) | Level 1 reproduced from scratch; Levels 2–6 checked against cache | ✅ exact / ✅ matches cache (12/12) |
| Table 9 (General Composite) | Checked against cache (depends on Level-6 lists, see R1) | ✅ matches cache (2/2) |
| Table 10 (academic word lists) | Standalone rows reproduced from scratch; starred rows checked against cache | ✅ exact (3/3) / ✅ matches cache (3/3) |

---

## 5. How to reproduce this check

```bash
python3 analysis/run_level1_reproduction.py   # from-scratch reproduction (Tables 2, 4, 6-8 L1, 10 unstarred)
python3 analysis/verify_cached_tables.py      # cache-consistency check (Tables 5, 6-9, 10 starred)
python3 analysis/check_citations.py paper/paper.md   # citation/reference cross-check
```
Run these from the repository root.

No third-party dependencies are required (standard library only).
