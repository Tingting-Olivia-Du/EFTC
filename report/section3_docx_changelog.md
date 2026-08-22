> **Note:** as of 2026-08-21 this changelog also covers
> `paper/Lexical coverage paper 202608015-Data_Revised.docx` (the actual
> data-tables document, not just the Section 3 methods redline) — see the
> entry at the bottom.

# Change Log: `paper/Section3_Methods_suggested_edits.docx`

Tracks what's been changed in the Section 3 ("The Study") redline document
and why, so the edits there stay traceable back to the analysis that
produced them. The docx itself is local-only (not in git, alongside the
rest of `paper/` — see repository README); this file is the record of its
history.

## 2026-08-21 update: Level-3 affix finding + Table 3 note refresh

Prompted by finishing the Java-source debugging exercise
(`report/level_reconstruction_attempt.md` §1, §7–9). Three changes:

1. **Legend expanded.** Added two more marker colors used by this update:
   **orange** for an open question that isn't a clean strikethrough→
   replacement (the fix direction depends on a call only the author can
   make), and **green** for "checked against the recovered Java source and
   confirmed accurate, no change needed" (documented here rather than
   marked inline in the docx, to avoid cluttering it with confirmations).

2. **New finding inserted after the `LevelListHandler` paragraph (§3.2.1):**
   an **orange, open-question note** flagging that the recovered
   `AffixLevelHandler.java` sets `level3prefixes = {}` (empty) and checks
   `non-`/`un-` as *suffixes*, not prefixes — contradicting both the
   sentence it's attached to ("items starting with Level-3 prefixes") and
   Table 1 in §2.3, which lists `non-`/`un-` as Level-3 prefixes. This is
   **not** marked as a clean fix because which side is "wrong" is a design
   question, not a bug with one obvious correct answer:
   - If Table 1 reflects the intended design, the *code* has a bug and
     should be fixed. (Re-running with this exact fix only marginally
     changed the numbers vs. the paper — see report §9 — so fixing it
     wouldn't meaningfully change any published figure.)
   - If the code's actual behavior is what produced the published Table
     3/6/7/8 numbers, then Table 1 and the "starting with Level-3
     prefixes" phrasing should be revised to describe Level 3 as
     suffix-only.
   Left this decision to the author rather than presuming an answer.

3. **Table 3 caveat note rewritten** (was: "the exact Level 2–6 source
   files are no longer in the repository, per Finding R1"; that was true
   when first written but is now stale). Updated to say the source files
   were subsequently recovered from the researcher's own working files,
   and that they reproduce Table 3's sizes within 0.1–0.5% and its
   downstream token-coverage figures within 0.1–0.5 percentage points —
   i.e. Table 3 is now effectively confirmed rather than merely
   "internally consistent with a cache we can't independently verify."

**Confirmed accurate, no change made** (green, per the new legend
category, noted here rather than inline): the `LevelList`/`TreeMap<String,
HashSet<String>>` description in §3.2.1's second paragraph, the
`Lemmatisation... Familizer/Lemmatizer tool (Cobb, 2007)` description
(confirmed: that tool's own documentation states it uses the AntBNC lemma
database for English — see report §8), and the `AffixLevelHandler... Java
referencing the affix hierarchy... Level 4 suffixes` description — all
of these read, before the Java source was recovered, as claims that might
not survive scrutiny; all of them did.

## 2026-08-14 (original draft)

First version. Marked two confirmed issues, found by close reading of
`paper.md` before the Java source was available:
- **T4**: garbled phrase in §3.1 ("...with limited insufficient on course
  textbooks" → "...due to insufficient course textbooks").
- **T3**: section-numbering collision in §3.2 (subsections mislabeled
  "4.2.1"/"4.2.2" instead of "3.2.1"/"3.2.2").

See `report/verification_report.md` Findings T3/T4 for the original
rationale (unchanged by this update).

---

# Change Log: `paper/Lexical coverage paper 202608015-Data_Revised.docx`

## 2026-08-21: Tables 3, 6, 7, 8, 9, and Table 10's AWL\*/NAWL\*/AVL\* rows
## recomputed with the bug-fixed pipeline

Resolves the open question raised in the Section 3 changelog above (and in
`Section3_Methods_suggested_edits.docx`) in favor of **fixing the code to
match Table 1's documented design**, rather than revising Table 1 to match
the code's actual (buggy) behavior. Concretely: `AffixLevelHandlerFixed`
(non-/un- as Level-3 prefixes) + the real AntBNC lemma database for
Level 2 (both already built and validated in
`analysis/java_port_pipeline.py`, see `report/level_reconstruction_attempt.md`
§7-9) were run end to end and every downstream table was regenerated:

- **Table 3** (word-list sizes): all 18 cells (HSWL/CET-4/CET-6 × Levels
  1-6) updated.
- **Tables 6, 7, 8** (HSWL/CET-4/CET-6 coverage by level): all 144 cells
  (12 rows × 4 metric columns × 3 tables) updated.
- **Table 9** (General Composite Word List, ± BNC/COCA supplement): both
  rows updated.
- **Table 10**: the `AWL*`, `NAWL*`, and `AVL*` rows updated (the
  standalone `AVL` row and `AVL*`'s previous ground-truth-based estimate,
  both from the 2026-08-20 AVL data-integrity correction, are superseded
  by this run's `AVL*` figure for internal consistency — all of Table 9/10
  is now computed by the same method). The standalone `AWL`/`NAWL`/`AVL`
  rows above them are untouched (unaffected by the Level construction fix).

Convention: same as elsewhere — strikethrough red = paper's originally
published value, underlined blue = recomputed value. One explanatory note
(orange) inserted immediately before Table 3 rather than annotating each
of the ~178 changed cells individually.

**Headline numbers, before vs. after (token coverage):** HSWL Level 6+
74.89% → 74.74%; CET-4 Level 6+ 85.17% → 85.05%; CET-6 Level 6+ 91.67% →
91.95%; General Composite+ 91.78% → 92.05%; AWL\* 91.93% → 92.11%; NAWL\*
92.50% → 92.73%; **AVL\* 94.09% → 92.86%** (vs. the 2026-08-20 ground-truth-based
estimate of 92.81% — the two independent methods agree to within 0.05pp).
None of these changes cross the 95%/98% comprehension thresholds the
paper's argument depends on, so the paper's qualitative conclusions are
unaffected; the quantitative table values throughout Tables 3/6/7/8/9/10
are.

Full old-vs-new data for every cell: `output/fixed_pipeline_table6_7_8.csv`
and `output/fixed_pipeline_table3_9_10.json`. Reproduce with
`python3 analysis/build_fixed_tables.py`.

## 2026-08-21 (later same day): full-document proofread, prose numbers
## brought in line with the corrected tables

The previous entry only updated the tables themselves; the surrounding
prose throughout the Abstract, Results, and Discussion still cited the
old numbers, and a full read-through of the whole document (not just the
tables) turned up a few more issues. All fixed in this pass:

**Section numbering (structural, not just the two spots found in the
original Section 3 review):** every top-level heading (1 Introduction, 2
Literature Review, 2.1, 2.2, 3 The Study, 3.1, 3.2, 4 Results, 4.1, 4.2, 5
Discussion and Conclusion) had lost its number entirely — Word's
paragraph text showed nothing where "1.", "2.1" etc. should be. The
Results subsections (4.1.1–4.1.4) and "3.2.2 Coverage indicators..."
were relying on Word's automatic multilevel numbering, which turned out
to be misconfigured to start counting from "4" at the top level even
inside Section 3 (the root cause of the original "4.2.1"/"4.2.2" bug —
it's baked into the numbering definition, not just stray literal text).
Rather than debug Word's list-numbering XML, every heading was converted
to a plain, literal, correctly-numbered prefix (the same approach already
used for "2.3" and "References"), which is unambiguous regardless of how
Word's internal counters are configured.

**Two corrupted sentences, evidently left over from an earlier manual
edit:** "...grouped into base lemma levels (Levels 1–2). . Initial word
lists..." (a stray lone period where a whole sentence about the
`LevelList`/`TreeMap<String, HashSet<String>>` class had been deleted —
restored, since the Java source recovered since then confirms that
sentence is accurate) and "...class was developed in referencing the
affix hierarchy..." (missing "Java" — restored).

**Every specific percentage/size figure in the Abstract, Results (Tables
4/6/7/8/9/10 discussion paragraphs), and Discussion** updated to match
the tables filled in the previous entry. This is the bulk of the change —
roughly 40 individual numbers across ~10 paragraphs.

**Claims whose truth value changed, not just their number**, rewritten
rather than patched:
- Table 4 discussion: AVL–AWL overlap (8.04%→17.94%) is no longer the
  *lowest* of the three academic-list pairs, it's now the *highest* —
  the sentence structure was reordered, not just the numbers swapped.
- Table 10 / Discussion: the claim that "the CET-6 WL (86.72%) and the
  AVL (86.99%) yield similar levels of token coverage" — the paper's
  second-most-quoted AVL claim after the headline 94.09% figure — is
  false once AVL is computed correctly (CET-6 87.02% vs. real AVL
  50.48%). Rewritten to state the two diverge sharply, and the sentence
  crediting this (false) comparability to Coxhead (2016) was rewritten
  to say the opposite: the AVL comparison does *not* support that
  observation in this corpus.
- "The addition of the AVL leads to a more substantial increase..." —
  no longer true (AVL* now beats NAWL* by 0.13pp, not decisively);
  rewritten to say so explicitly rather than leaving an overstated claim
  with just the percentage swapped in.
- "The AVL imposes a greater learning burden... given that it comprises
  considerably more word families than... CET-6 WL" — false with the
  corrected AVL size (6,799, smaller than CET-6's own Level-1 list);
  rewritten.
- "requires learners to master an additional **[number]** words" — this
  sentence had literally lost its number in an earlier edit ("an
  additional  words," with a stray double space); restored as "~1,133
  words" (the net-new vocabulary the corrected AVL adds on top of the
  General Composite + BNC/COCA baseline, per this run's own Table 9/10
  numbers — not the same as the ~7,352 figure in Finding D1 / the
  ground-truth-based run, since that used a different, more precise
  Level 6 source; both numbers and why they differ are in
  `report/level_reconstruction_attempt.md`).

**Two pre-existing typos, unrelated to any of the above, fixed while
proofreading:** "FETC" → "EFTC" (three occurrences: Table 7 discussion,
Table 8 discussion, Limitations paragraph) and "-al, -ation,- ous" → "-al,
-ation, -ous" (stray space).

Convention unchanged: strikethrough red = previous text, underlined blue
= corrected text. Verified after editing that no un-struck instance of
any of the old headline numbers (74.89%, 85.17%, 91.67%, 94.09%, 63,153,
etc.) remains anywhere in the document body.

## 2026-08-21 (same day): clean (non-redline) version generated

`paper/Lexical coverage paper 202608021-Clean.docx` (local-only) is a
derived copy of the redline `...202608015-Data_Revised.docx` with all
track-changes markup resolved: every strikethrough (old/deleted) run
removed, every underlined-blue (new) run accepted and de-formatted to
plain text, and the four bracketed meta-notes (`[Update 2: ...]`,
`[Update: ...]`, `[AVL data-integrity correction applied ...]`, `[Tables
3, 6, 7, 8, 9, ... recomputed end to end ...]`) deleted entirely, since
they're process notes for review, not paper content. Verified afterward
that no strikethrough or reviewer-color (red/blue/orange/green) run
remains anywhere in the body or tables. This is the version to use for
anything downstream of review (submission, sharing, further editing) —
the redline version stays the audit trail of what changed and why.

Note: the numbers baked into this clean copy are the ones described in
the entries above (the debugged-pipeline reconstruction for Tables
3/6/7/8/9/10, not the more precise ground-truth-based numbers from
`report/level_reconstruction_attempt.md` §2-3) — see that report and the
2026-08-21 entry above if you want to switch to the ground-truth figures
instead before finalizing.

## 2026-08-21 (final pass): removed an unsupported comparison and an
## analysis the study never performed

A close review of the Results and Discussion — prompted by the question
"did we actually run an *excluding* analysis?" — found that we had not,
and that the sentence built on it drew an invalid inference. Both
documents updated in sync.

**The phantom analysis.** §4.2 contained: *"Additionally, excluding the
General Composite Word List and the BNC/COCA supplementary lists, the
CET-6 WL (87.02%) and the AVL (50.48%) diverge sharply..."* No such
"excluding" analysis exists anywhere in the study. Those two figures are
simply the standalone values already reported in Tables 8 and 10; the
phrasing implies a separate subtraction experiment that was never run.

**The invalid inference.** The sentence concluded that "the standalone
AVL is considerably weaker than the CET-6 WL as an academic vocabulary
resource." That does not follow from the data, for two reasons:
- *Scale*: the figure quoted for CET-6 is its Level-6 word-family-expanded
  list (29,844 word forms) against the AVL's 6,799 — a 4.4× difference.
- *Composition* (the more serious problem): raw token coverage cannot
  fairly compare a general word list against an academic one. The CET-6
  WL contains 14 of the 15 most frequent function words in the corpus and
  covers 100% of its top-100 word types; the AVL contains 2 of those 15
  and covers 58.3%. Those top-100 types alone account for 25.9% of all
  running tokens. A general list therefore wins this comparison by
  construction, regardless of either list's quality.

Replaced with a statement of that methodological point: standalone
figures are not comparable across list types, the AVL's 50.48% reflects
its selective composition rather than a deficiency, and its contribution
is properly assessed by incremental gain over a general baseline.

**Same error, second location.** The Discussion used the identical
comparison to argue that Coxhead's (2016) overlap observation "is not
supported by the AVL comparison in this corpus." Coxhead's claim concerns
*overlap*, which is Table 4's data, not token coverage. On the correct
evidence the claim is in fact **supported**: AVL–CET-6 overlap is 19.57%,
the highest of any academic list against the CET-6 WL (AWL 10.29%, NAWL
7.78%), and 5,666 of the AVL's 6,799 word forms (83%) are already
contained in the general composite resource. Rewritten to cite the
overlap data and restore the corroboration, which the corrected data
supports.

**Internal contradiction in the learning-burden argument.** The
Discussion read "requires learners to master an additional ~1,133 words
... which constitutes a prohibitively heavy learning burden." ~1,133
additional word forms is not prohibitive, so the conclusion no longer
followed from its own premise (it did when the figure was the erroneous
18,558). Restructured to rest the argument on the aggregate instead: even
the most inclusive combination examined, at over 60,000 lexical items,
still fails to reach 95%. The 1,133 figure was moved to §4.2, where it
explains *why* the AVL's incremental gain is small — a use that supports
rather than undercuts the surrounding claim.

**Also fixed in this pass:** a sentence fragment ("...demonstrate that
when supplementing the AWL and the NAWL to the the BNC/COCA supplementary
lists only yields..."), which additionally mis-stated the baseline (the
academic lists are added to the General Composite Word List *and* the
BNC/COCA supplementary lists, not to the supplementary lists alone);
"overage" → "coverage"; and "General Compositve" → "General Composite".

**One item flagged but not changed** (author's call): the "over 60,000
lexical items" burden figure includes the 29,798-item BNC/COCA
supplementary lists, most of which are proper names and acronyms rather
than vocabulary a learner would deliberately study. The burden claim may
be overstated on that basis, but adjusting it would alter the paper's
pedagogical argument rather than correct an error, so it was left as
written.
