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
