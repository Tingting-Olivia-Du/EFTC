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

## 2026-08-21 (addendum): learning-burden claim quantified

The item flagged-but-not-changed in the previous entry has now been
resolved. The "over 60,000 lexical items" burden figure counted the
entire AVL\* combination (61,055 word forms), of which 29,798 come from
the BNC/COCA supplementary lists — 22,409 proper names, 6,044 transparent
compounds, 1,149 acronyms and 196 marginal words. These are items readers
decode from context or recognise without deliberate study, so counting
them as learning load overstated the burden by roughly half.

Both the Discussion and the pedagogical paragraph now cite the vocabulary
that actually requires study — the General Composite Word List plus the
AVL's net contribution, approximately **31,500 word forms** — with the
composition of the remainder stated explicitly. "Imposes an unbearable
learning load" was also tempered to "a load that is impractical for
standardised EMI curriculum teaching."

This strengthens rather than weakens the paper's argument: a defensible
31,500-word figure that still falls short of 95% supports the case for a
discipline-specific FAWL more credibly than an inflated 60,000 that a
reviewer could challenge.

## 2026-08-23: full data + content audit

Complete re-verification of every figure and claim in both documents.

**Corpus and Table 2 — verified exact.** Recomputed all three column
groups from the table itself: 49 + 26 + 19 = 94 books and 8,538,216 +
4,663,425 + 3,152,698 = 16,354,339 words, matching both the stated total
and the corpus file (16,354,339 tokens / 120,835 types).

**Case-sensitivity inconsistency found and fixed (the substantive item).**
The corpus is entirely lowercase after preprocessing, but Table 4 and the
standalone AVL row of Table 10 were computed from word lists with case
preserved. Two consequences:

1. *Tables 3 and 4 contradicted each other.* Table 3 reported CET-4
   Level 1 = 4,539 (lowercased), while Table 4's arithmetic required
   4,543 (4,543 + 3,448 − 2,862 = 5,129). A reviewer checking the union
   column would have found the discrepancy. After lowercasing, all three
   general-list rows reconcile exactly: 4,539 + 3,448 − 2,871 = 5,116 ✓,
   8,046 + 3,448 − 3,242 = 8,252 ✓, 4,539 + 8,046 − 4,307 = 8,278 ✓.
2. *The AVL list size was inflated.* 26 of its entries are capitalised
   (e.g. *American*) and can never match a lowercase corpus, yet were
   counted in the denominator of the attestation rate.

All word lists are now lowercased consistently. Changes: Table 4 — eight
of nine rows shift slightly (AWL vs NAWL unchanged); Table 10 — standalone
AVL 6,799/82.16/4.62/50.48 → 6,793/82.48/4.64/50.60, and AVL\* size/
attestation 61,055/47.37 → 61,030/44.57 (its token coverage stays 92.86%).
AWL\* and NAWL\* are unaffected, both lists being already lowercase.
Dependent prose figures updated accordingly, including the AVL composition
sentence (now 5,685 of 6,793 already covered, 1,108 net-new) and the
Discussion's overlap figure (19.65%) and 84% coverage claim.

**Verification performed after the fix.** Every percentage and count in
the prose was matched programmatically against the tables — all trace
correctly, and no superseded value (94.09%, 86.99%, 74.89%, 63,153,
18,558, etc.) survives anywhere in the body.

**Six drafting artifacts fixed.** These were identified in the original
verification report as findings T1/T2 but had only ever been corrected in
the Section 3 methods redline, never in the data document:
- a leftover `xxx` placeholder in §2.1;
- two unresolved either/or phrasings — "has been consistently/has long
  been" → "has long been"; "supplemented by/superimposed with" →
  "supplemented by";
- a stray `+` after "(Laufer & Sim, 1985)";
- "covers close 14%" → "covers close to 14%";
- "In a seminar work" → "In a seminal work".

**Two missing references supplied**, both for word lists central to the
study and previously un-citable: Browne, Culligan & Phillips (2013) for
the NAWL and Gardner & Davies (2014) for the AVL, inserted in alphabetical
position. **Please verify both against your own bibliographic source
before submission.**

**Four references still missing — author action required.** Cobb (2019),
Wang et al. (2020), Graves (2021) and Zhang & Liu (2022) are cited in the
Discussion but absent from the reference list. These were deliberately not
supplied, as guessing at their details would be worse than leaving the gap
visible.

## 2026-08-23 (addendum): references verified against sources

The two reference entries added earlier were checked against authoritative
sources rather than left on trust:

- **Gardner & Davies (2014)** — confirmed exactly as written via Oxford
  Academic: *Applied Linguistics*, 35(3), 305–327,
  https://doi.org/10.1093/applin/amt015.
- **Browne, Culligan & Phillips (2013)** — corrected to the project's own
  recommended form, "New academic word list 1.0.
  http://www.newgeneralservicelist.org/".

Cobb (2019), Wang et al. (2020), Graves (2021) and Zhang & Liu (2022)
remain outstanding and are for the author to supply.

## 2026-08-23 (advisor query): academic word lists — sourcing, sizes and
## counting unit

Two points raised in supervision, both substantiated.

**1. Table 10 sizes did not match the published figures.** Checked against
the original distributions. The word-family counts match exactly (AWL 570,
NAWL 963, AVL 1,991); the discrepancies are entirely a matter of how
"word forms" are counted:

| List | Families | Published forms | Distinct forms used here |
|---|---|---|---|
| AWL | 570 ✓ | 3,112 | 3,107 |
| NAWL | 963 ✓ | 2,604 | 2,598 |
| AVL | 1,991 ✓ | 7,728 | 6,793 |

The AVL gap of ~930 is fully accounted for: its distribution lists
family-by-part-of-speech entries, and 824 forms carry more than one tag
(*level* as noun, adjective and verb; *model* as noun, verb and
adjective), giving 6,799 + 928 = 7,727 rows. Since the EFTC is an untagged
type-frequency list, a form can match only once regardless of its tags, so
coverage must be computed over distinct orthographic forms. The residual
AWL and NAWL differences (3–6 forms) reflect minor version differences
between the machine-readable distribution used and the published counts.
Table 10 now states families in the row labels, labels the size column
"Size (word forms)", and carries a note explaining the collapse.

**2. The methods section never described the academic word lists at all** —
neither their provenance and size nor how they were operationalised. Two
paragraphs added: §3.1 now gives source and size for each list and states
that coverage is computed over distinct orthographic forms; §3.2.1 now
states that the academic lists were *not* put through the six-level affix
expansion, and why.

**A comparability problem surfaced while answering this.** The three lists
are not distributed at the same counting unit, which the paper had not
registered:

| List | Derivational members | Counting unit |
|---|---|---|
| AWL | 59% | full word family (≈ Level 6) |
| NAWL | **21%** | **lemma — inflections and spelling variants only (≈ Level 2)** |
| AVL | 54% | full word family (≈ Level 6) |

The diagnostic is decisive: the NAWL lists *absorb* and *absorption* as
**separate headwords**, which a family-based list would not. Its lower
standalone coverage (5.15%) is therefore partly an artefact of counting
unit rather than of lexical selection — the same class of error as the
AVL-versus-CET-6 comparison corrected on 2026-08-21. The asymmetry is now
stated in §3.2.1, in the Table 10 note, and as a caveat in §4.2 where the
standalone figures are discussed.

## 2026-08-23 (advisor follow-up): academic word lists rebuilt through all
## six affix levels

The academic word lists are no longer analysed in their published form.
`analysis/build_academic_leveled.py` rebuilds all three from their
headwords through the identical pipeline used for the general lists —
AntBNC lemma database for Level 2, BNC/COCA family database for Level 6,
Bauer & Nation affix rules (corrected Level-3 handling) for Levels 3–5.

**Level 1 by table mapping.** Each list's own nested structure supplies its
headwords: the sublist keys of the AWL distribution, the top-level keys of
the NAWL distribution, and the `family` column of the AVL spreadsheet.
These recover the published counts exactly — 570, 963 and 1,991 — which
validates the extraction. Between 97.6% and 99.5% of those headwords are
locatable in the BNC/COCA family database, so the expansion has near-full
coverage of each list.

**This resolves the counting-unit confound.** Rebuilding at a common unit
raises the NAWL's token coverage from 5.15% in its published lemma form to
**14.92%** at Level 6 — close to a threefold increase — while the AWL
(20.19% → 19.64%) and the AVL (50.60% → 51.07%) barely move. The NAWL's
apparent weakness in the published comparison was therefore largely an
artefact of it being distributed as lemmas rather than families, exactly as
the asymmetry noted in the previous entry predicted.

**Table 10 restructured** from six rows to twenty-one: three lists × six
levels of standalone coverage, followed by the three starred combinations.
The starred values vary by at most 0.21 percentage points across the six
levels — the general baseline already contains nearly every form that
expanding an academic list would add — so they are reported at Level 6
only, with a note recording the invariance.

**Revised figures.** AWL\* 92.05%, NAWL\* 92.74%, AVL\* 92.87%; the AVL
still leads but by 0.13 points over the NAWL. Of the 11,906 word forms in
the Level-6 AVL, 9,818 (82%) are already in the general composite, leaving
2,088 net-new. The vocabulary requiring deliberate study rises to
approximately 32,500 word forms. Sections 3.1, 3.2.1, 4.2, the Discussion,
the pedagogical paragraph, the Abstract and the Table 10 note were all
updated to match.

## 2026-08-23 (full review): methods clarity and remaining gaps

A complete read-through following the six-level rebuild of the academic
word lists. Three items were requested; seven further gaps were found and
closed.

**Requested — how the academic lists were used.** §3.2.1 already stated
that the six-level expansion was applied to them, but not how their
Level-1 baseline was obtained. It now specifies that the headwords were
recovered from each list's own published structure (AWL sublist entries,
NAWL lemma entries, AVL family column), that this reproduces the published
570 / 963 / 1,991 exactly, and that Levels 2–6 used the same AntBNC lemma
database and BNC/COCA family database as the general lists. A pointer was
added noting that Table 3 gives the general-list sizes and Table 10 the
academic-list sizes.

**Requested — the starred invariance.** Already present in §4.2 and the
Table 10 note; now also stated in the Discussion, where it carries the
interpretation that the general baseline already contains nearly every
form that expanding an academic list would contribute.

**Further gaps closed:**

1. §3.2.1's second paragraph described the affix levels as classifying
   *corpus* words ("all words were categorised into Levels 3–6 … items
   failing to match any affix pattern were grouped into base lemma
   levels"), which is not what the procedure does — the levels classify
   *word-list members*. Rewritten to describe the actual mechanism.
2. §3.2.2 did not say which level the General Composite Word List was
   built at, nor which form of the academic lists was merged into it. Both
   now specified as Level 6.
3. The BNC/COCA supplementary lists were defined but never motivated. A
   rationale now explains why they are reported separately: these
   categories are largely recognised or decoded in context rather than
   learned, so reporting coverage with and without them brackets lexis
   that imposes little learning burden.
4. RQ2 did not mention affix levels although the analysis answering it is
   level-based; it now does.
5. "Boosts token coverage by roughly 5% and type coverage by around 10%"
   and "performs about 10% better" misuse percentages for what are
   differences in percentage points. Corrected in both places.
6. §4.2 gave the AWL's and NAWL's gains across levels in points but not
   the AVL's, despite calling it the largest; 11.60 points now stated.
7. **A new limitation added.** The six-level expansion of the academic
   lists uses the BNC/COCA family database rather than each list's own
   family definition, so the rebuilt lists exceed their published sizes
   (Level-6 AWL 3,898 against Coxhead's 3,107; Level-6 AVL 11,906 against
   6,793). The limitations section now records this and states that
   coverage figures for the expanded academic lists are estimates of what
   a learner with the corresponding morphological knowledge would
   recognise, not properties of the published lists.

**A Data Availability Statement was added** before the References,
pointing to the public repository.

## 2026-08-23 (structure): Limitations promoted to its own section, and a
## document-structure bug repaired

**Limitations is now Section 6.** The four limitations had been packed
into a single 2,400-character paragraph at the end of Section 5. They are
now a numbered top-level section with one paragraph each, which also let
the fourth — the methodological limitation on the academic-list expansion
— be developed properly rather than appended.

While splitting them, an error introduced by the previous edit came to
light: the sentence "Future studies can integrate longitudinal learner
tracking…" had originally closed the *third* limitation (about not
measuring learner knowledge), but inserting the fourth limitation ahead of
it left it trailing the counting-unit discussion, where it read as though
longitudinal tracking would address a counting-unit problem. It has been
returned to the third limitation, and the fourth now closes with its own
forward-looking sentence: that a finer-grained alternative would be to
expand each list using its own compiler's family criteria and report both
expansions side by side.

The fourth limitation also now tells readers where to look for
comparability: the Level-1 rows of Table 10 correspond to the headwords as
published, so those are the figures to set against previously published
coverage rates for the AWL, NAWL and AVL.

**Document-structure bug found and repaired.** Sixteen headings had
silently lost their Heading styles and were rendering as body text — the
document outline showed only three of nineteen headings. The cause was in
the earlier heading-numbering pass: `p._p.insert(0, run)` placed the new
number run *before* the paragraph's `<w:pPr>` element. OOXML requires
`w:pPr` to be the first child of `w:p`, so the paragraph properties were
invalidated and the style dropped. Only the two headings edited by a
different method survived. All heading levels have been restored (Heading 1
for sections 1–6, Abstract, Data Availability and References; Heading 2 for
2.1–2.3, 3.1, 3.2, 4.1, 4.2; Heading 3 for 3.2.1, 3.2.2 and 4.1.1–4.1.4)
and the outline now renders correctly, which also restores navigation, the
table of contents and any style-driven journal template.
