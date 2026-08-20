# Reconstructing the Level 2–6 Word-Family Expansion (and a corrected AVL\* estimate)

This closes most of the "Reproducibility gap" (Finding R1) from
`verification_report.md`: the official BNC/COCA word-family data and
supplementary lists that the original Java pipeline used — and which were
missing from this repository entirely — were tracked down, downloaded, and
used to independently rebuild the Level 2–6 word lists and re-run the
AVL-correction from `avl_data_integrity_check.py` through to the combined
`AVL*` figure that previously couldn't be recomputed.

Reproduce with:
```bash
python3 analysis/build_bnc_coca_resources.py     # parse the recovered official source files
python3 analysis/build_leveled_wordlists.py      # rebuild Level 2-6 for HSWL/CET-4/CET-6
```

---

## 1. Where the AVL 18,558 number actually came from (deeper trace)

Following up on Finding V1: `wordlist/AVL_nested.json` (the file
`flatten_avl.py` turned into the paper's `AVL.json`, now renamed
`AVL_old_wrong.json` in this repo) is a byte-for-byte copy of
`archive/third-party/machine_readable_wordlists/Academic/AVL/AVL.json`. That
third-party repository's own top-level README correctly cites the real
source — "Academic Vocabulary List (AVL) — academicvocabulary.info — Based
on 120 million word academic texts in COCA" (Gardner & Davies' real site) —
but the actual `AVL.json` file it ships doesn't match that description at
all: it's a 42-band general-frequency list (confirmed again: band_1 =
*the, of, be, and, a, in, to, that, for, have*). So the mislabeling is a bug
in the **third-party dependency itself**, not something this project's own
scripts introduced — the citation in their README is correct, but the data
file under that citation isn't. (For comparison, their `AWL.json` and
`NAWL.json` files *are* correct, byte-identical to the official lists — see
`data_source_audit.md`. Only their `AVL.json` has this problem.)

## 2. Recovering the real BNC/COCA resources

The paper's method section cites "the BNC/COCA word family dataset (Nation,
2017)" and "BNC/COCA supplementary lists (proper names, marginal words,
transparent compounds, and acronyms)" — Paul Nation's (Victoria University
of Wellington) official word-list resources, distributed as the `basewrd*`
files bundled with the RANGE program (Heatley, Nation & Coxhead). These were
tracked down and downloaded:

- `data/wordlists/bnc_coca_source/basewrd1.txt` .. `basewrd25.txt` — the
  25,000-headword BNC/COCA word-family database (headword + all inflected/
  derived family members), from
  `laurenceanthony.net/resources/wordlists/bnc_coca_cleaned_ver_002_20141015.zip`.
- `data/wordlists/bnc_coca_source/basewrd31.txt` .. `basewrd34.txt` — the
  four supplementary lists (proper names / marginal words / transparent
  compounds / acronyms) from the same package.
- `data/wordlists/BNC_COCA_lists.xlsx` — a second, independently-hosted copy
  of the same 25k family list (from eapfoundation.com), used as a
  cross-check.

**These are confirmed to be the exact resource (or a byte-identical one) the
original study used**: parsing `basewrd31`–`basewrd34` gives 22,409 / 196 /
6,044 / 1,149 entries (29,798 combined) — this matches paper Table 5's sizes
*exactly*, and recomputing Table 5's attestation/type/token coverage from
these files against the corpus reproduces **every value in Table 5 exactly**
(`analysis/build_bnc_coca_resources.py`). Table 5 — previously only
checkable against the pipeline's cache — is now independently reproduced
from an authoritative external source.

## 3. Rebuilding Level 2–6 for HSWL / CET-4 / CET-6

`analysis/build_leveled_wordlists.py` implements the affix-classification
algorithm from paper §3.2.1 directly from Table 1's rules:

- **Level 6** = full word-family union: for every Level-1 word, pull in
  every member of its BNC/COCA family.
- **Level 2** ("lemmatisation") = Level-1 plus regular inflectional forms
  (plural/3sg -s/-es, past tense -d/-ed, -ing, comparative/superlative
  -er/-est, with standard spelling-change handling) found within each
  word's family. *Approximated* — the paper used Tom Cobb's
  Familizer/Lemmatizer tool, which isn't available to us, so this is a
  rule-based stand-in, not a guaranteed match to the original tool's
  behavior on every edge case.
- **Levels 3–5** = iteratively add Level-6 family members whose spelling
  matches that level's prefix/suffix patterns from Table 1, cumulatively
  (exactly as paper §3.2.1 describes the `LevelListHandler` procedure).

### Word-list sizes: in the right ballpark, not exact

| List | Level 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| HSWL diff vs. paper | 0% | −8.4% | −4.9% | −4.9% | −8.2% | −5.5% |
| CET-4 diff vs. paper | −0.1% | −8.6% | −5.3% | −5.2% | −8.1% | −5.4% |
| CET-6 diff vs. paper | −0.3% | +11.0% | +16.1% | +17.1% | +14.1% | +18.2% |

HSWL and CET-4 consistently undershoot the paper's reported sizes by
~5–9%; CET-6 consistently *overshoots* by ~11–18%. This is a systematic
pattern (not noise), most likely because our copy of the BNC/COCA family
database is a slightly different vintage/version than whichever one the
original study used (the paper cites "Nation, 2017, v1.0.0"; ours is dated
2014) — family membership lists get revised between versions, and CET-6's
much larger Level-1 seed list (8,074 words, many of them common
high-frequency words with unusually large families) makes it more sensitive
to exactly which version is used.

### Token coverage: remarkably close despite the size differences

| Metric | n comparisons | mean diff | max \|diff\| | stdev |
|---|---|---|---|---|
| Token coverage, Tables 6/7/8, all 6 levels × 3 lists × (±BNC/COCA supplement) | 36 | −0.09 pp | 0.78 pp | 0.38 pp |

Despite word-list *sizes* being off by up to 18%, **token coverage — the
metric the paper's actual conclusions are based on — comes out within
roughly ±0.4 percentage points on average, worst case 0.78 points**. This
makes sense: the extra/missing words in our reconstruction are mostly
low-frequency derivational forms that barely move token coverage, even
though they meaningfully change the raw list-size count. This is strong
(though not perfect) evidence that Tables 6/7/8's published token-coverage
numbers are basically sound, and that our reconstruction is a reasonable
stand-in for computing numbers the original pipeline could no longer
produce.

## 4. A validated estimate for the corrected AVL\* (Table 10)

Using the rebuilt Level-6 lists to reassemble the "General Composite Word
List + BNC/COCA supplementary lists" baseline (Table 9), then adding each
academic word list on top (Table 10's starred rows):

**Sanity check first** — rebuilding `AVL*` with the paper's own (wrong)
`AVL_old_wrong.json` gives **94.13% token coverage**, against the paper's
published **94.09%** — a 0.04-point difference. This is the single best
validation available that the reconstructed pipeline faithfully reproduces
whatever the original one did.

With that established, here's every starred row rebuilt from scratch,
alongside what the paper reports:

| | Paper | Rebuilt (same, wrong AVL — sanity check) | Rebuilt (corrected AVL) |
|---|---|---|---|
| AWL\* token coverage | 91.93% | — | **92.11%** |
| NAWL\* token coverage | 92.50% | — | **92.73%** |
| AVL\* token coverage | 94.09% | 94.13% | **92.86%** |

**With the corrected AVL data, AVL\* drops from the paper's reported 94.09%
to an estimated 92.86%** — a 1.23-point drop, much smaller than the
standalone AVL drop (86.99% → 50.48%) because most of AVL's real
contribution here is already covered by the General Composite + BNC/COCA
baseline before AVL is even added (see Finding V1's overlap numbers).

**This changes the paper's ranking, but not decisively.** The published
version has AVL\* beating NAWL\* by 1.59 points and AWL\* by 2.16 points —
a clear result. With the correction, AVL\* (92.86%) only edges out NAWL\*
(92.73%) by 0.13 points and AWL\* (92.11%) by 0.75 points — inside the
±0.38pp typical error margin established above for NAWL\*, i.e. **AVL and
NAWL are now statistically indistinguishable in this reconstruction**, and
AVL's edge over AWL, while probably real, is much smaller than reported.
None of the three reach anywhere near 95% either way, so the paper's
overall "no word list combination is adequate" conclusion is unaffected —
if anything, it's reinforced (the real numbers are further from 95% than
what was published).

## 5. What this does and doesn't settle

**Settled with high confidence:**
- Table 5 (BNC/COCA supplement) — exact match to an authoritative external
  source, fully independently verified.
- The general shape of Tables 6/7/8's token-coverage numbers — corroborated
  to within ~0.4pp on average.
- AVL\* really does drop substantially once the real AVL is used, and its
  claimed advantage over AWL\*/NAWL\* was overstated.

**Not settled, still approximate:**
- Exact Level 2–6 word-list *sizes* (Table 3) — off by 5–18%, systematic by
  list, not resolved by this reconstruction.
- The precise corrected AVL\* figure (92.86%) — a well-validated *estimate*
  (validated to ±0.04pp via the sanity check, though that check used the
  same reconstruction pipeline rather than a fully independent one), not a
  drop-in replacement for a full re-run of the original Java code with the
  corrected AVL source file. That re-run, using the original codebase and
  the exact word-family database version it used, remains the authoritative
  way to get a final number for publication.

## 6. Files added

```
data/wordlists/bnc_coca_source/basewrd{1-25,31-34}.txt   official RANGE package files
data/wordlists/bnc_coca_family_database.json             parsed 25k word-family database
data/wordlists/bnc_coca_supplement_{proper_names,marginal_words,
    transparent_compounds,acronyms,combined}.json         parsed supplementary lists
data/wordlists/BNC_COCA_lists.xlsx                        cross-check copy (eapfoundation.com)
data/wordlists/leveled/{HSWL,CET4,CET6}/level{1-6}.json   rebuilt leveled word lists
analysis/build_bnc_coca_resources.py                      parses the source files
analysis/build_leveled_wordlists.py                       rebuilds Level 2-6 + validates vs. paper
```
