# Level 2–6 Reconstruction and a High-Confidence Corrected AVL\* Estimate

**Updated 2026-08-20 (part 2):** the user located and provided the original
Java source code and the researcher's working data files
(`java_source/`, kept local-only — see "What's not in git" below). This
upgrades everything in this document from "best-effort approximation" to
"near-exact ground truth" and **resolves the CET-6 anomaly this document
originally reported as a possible pipeline inconsistency — it wasn't one;
it was an artifact of the from-scratch reconstruction's own limitations.**
That section is kept below, marked as superseded, for the record.

Reproduce the ground-truth verification with:
```bash
python3 analysis/verify_ground_truth_levels.py
```

---

## 1. What the Java source revealed

`archive/java_source/hyponym/` (14 files, copied from the user-provided
project — the full original project, including the researcher's local copy
of the raw textbook corpus, stays out of git; see below) contains the
`LevelList`, `LevelListHandler`, `AffixLevel`, `AffixLevelHandler`,
`Coverage`, and `Lemmatize` classes the paper's methods section describes.

Three concrete findings from reading the actual code:

1. **Level 3 has an affix-rule quirk relative to Table 1.**
   `AffixLevelHandler.java` sets `level3prefixes = {}` (empty!) and
   `level3suffixes = {"able", "er", "ish", "less", "ly", "ness", "th", "y",
   "non", "un"}`. Table 1 in the paper lists `non-`/`un-` as Level-3
   *prefixes*; the actual code checks them as *suffixes*
   (`word.endsWith("un")`, not `word.startsWith("un")`) — a real
   implementation quirk that a word-for-word reading of the paper's
   methods section would not predict. Levels 4 and 5 match Table 1 exactly.
   Level 6 is *not* affix-filtered at all — `buildLevel()` is only used for
   Levels 3–5; Level 6 is read directly from a pre-built
   `*_family_horizontal.txt` file (the full BNC/COCA family, unfiltered).
2. **Level 2 depends on an external file this project doesn't have.**
   `LevelListHandler` builds Level 2 by reading `*_lemmas_horizontal.txt` —
   a pre-computed headword→inflection mapping file. `Lemmatize.java` (Stanford
   CoreNLP) turns out to lemmatize the *corpus text*, not the word lists, so
   it isn't the source of that file either. The actual lemma-mapping file
   the paper attributes to "the Familizer/Lemmatizer tool (Cobb, 2007)" is
   not present anywhere in what was provided — Level 2 remains
   unreproducible from first principles, same conclusion as before.
3. **AVL never appears anywhere in the Java source** (`grep -ri avl` across
   every `.java` file: zero matches). This confirms, from the actual
   codebase this time rather than by inference, that AVL was handled
   entirely by the Python scripts already examined in Finding V1 — the
   Java pipeline is not implicated in that bug at all.

The constructor that's actually active in the provided snapshot only builds
`HighSchool_levelList1..6` — the `cet4_levelList*` / `cet6_levelList*` code
paths are present but commented out. This is not evidence of a bug; it's
evidence that this is a working research repo where the developer
repeatedly commented/uncommented blocks to run one list at a time, and the
snapshot provided happens to have HighSchool live. It does confirm, more
concretely than before, why the exact final run that produced every number
in the paper can't be replayed from what exists: there is no single
"run everything" entry point in the saved state.

## 2. The real Level 1–6 word lists were sitting in the working files

`java_source/research_file/FAWL_Python/wordlist/gen_leveled/` contains
`HighSchool_{1-6}.txt`, `cet4_{1-6}.txt`, `cet6_{1-6}.txt` — 18 files, one
per list per level. These are **not tracked in git** (see below) but were
used to regenerate `data/wordlists/leveled_ground_truth/{HSWL,CET4,CET6}/level{1-6}.json`,
which *is* tracked.

These are a very slightly earlier snapshot than whatever produced the final
published Table 3 — sizes are consistently ~0.1–0.5% larger (missing one
last, small cleanup pass we don't have a script for) — but coverage numbers
computed from them are essentially exact:

| Metric | n | mean diff | max \|diff\| | stdev |
|---|---|---|---|---|
| Token coverage, Tables 6/7/8, all 6 levels × 3 lists | 18 | +0.13pp | 0.52pp | 0.11pp |

This is roughly 3x tighter than the from-scratch reconstruction in §5 below
(which had stdev 0.38pp), and — critically — **shows no CET-6-specific
anomaly**. Level-by-level sizes for CET-6 (8046 / 16346 / 19528 / 20434 /
21718 / 25199) track the paper's (8074 / 16390 / 19572 / 20478 / 21762 /
25243) just as tightly as HSWL and CET-4 do. The 11–18% CET-6-specific
overshoot reported in §5's original analysis was real, but it was a
property of *this document's own from-scratch reconstruction* (most likely
the "first family wins" tie-breaking rule used when a word could plausibly
belong to more than one BNC/COCA family, which the actual Java `TreeMap`
logic evidently resolves differently) — not a finding about the paper or
the original pipeline. Withdrawn as a finding; kept in §5 below for the
record, clearly marked.

## 3. Table 9 and Table 10, rebuilt from ground truth

| | Ground truth build | Paper |
|---|---|---|
| Table 9, General Composite (size / token%) | 26,344 / 87.00% | 26,411 / 86.88% |
| Table 9, General Composite+ (size / token%) | 55,718 / **91.78%** | 55,801 / **91.78%** |
| Table 10, AWL\* (size / token%) | 56,171 / **91.93%** | 56,254 / **91.93%** |
| Table 10, NAWL\* (size / token%) | 56,692 / **92.50%** | 56,775 / **92.50%** |
| Table 10, AVL\* sanity check, paper's own (wrong) AVL data | 63,105 / **94.09%** | 63,153 / **94.09%** |

Every token-coverage figure above matches the paper **to two decimal
places** except the still-slightly-smaller General Composite baseline
(87.00 vs. 86.88, a 0.12pp gap consistent with the ~0.1–0.5% missing final
cleanup pass). The **AVL\* sanity check now reproduces the paper's reported
94.09% exactly** (63,105 vs. 63,153 in size, a 0.08% difference that
rounds away entirely in the coverage percentage). This is about as strong a
validation as this kind of independent reconstruction can produce without
the original code actually running.

### The corrected AVL\* estimate

| | Size | Attestation | Type% | **Token%** |
|---|---|---|---|---|
| AVL\* (corrected AVL, ground-truth composite) | 57,453 | 46.01% | 21.88% | **92.81%** |
| AVL\* (paper, published) | 63,153 | 47.37% | 24.76% | 94.09% |

**Updated, higher-confidence estimate: AVL\* drops from the published
94.09% to ~92.81%** (previously estimated ~92.86% from the from-scratch
reconstruction — the two independent methods agree to within 0.05pp,
which is itself a good consistency check). Final ranking of the three
starred rows:

| | Token coverage |
|---|---|
| NAWL\* | 92.50% |
| AVL\* (corrected) | **92.81%** |
| AWL\* | 91.93% |

AVL\* still edges out NAWL\* (by 0.31pp) and AWL\* (by 0.88pp) — so the
paper's directional claim ("AVL is the best of the three academic word
lists") survives, but the *margin* the paper reports (94.09% vs. 92.50%/
91.93%, a 1.6–2.2 point lead) does not — the real lead is small enough that
it would not obviously read as decisive in a paper, and the paper's framing
of AVL as clearly superior needs to be revised down substantially.

## 4. What's not in git, and why

`java_source/` (2.6GB) is git-ignored. It contains, alongside the valuable
`.java` files and `gen_leveled/` word lists used above: the researcher's
personal IntelliJ workspace config, a full second copy of the raw
copyright-sensitive textbook corpus (`FAWL_Python/Textbooks_all/`, etc. —
same material already excluded elsewhere in this repo for the same reason),
and several entirely unrelated reference projects (a Berkeley CS61B
assignment, unrelated NLP repos) that happened to be in the same working
directory. Only the specific files with independent value and no
copyright/privacy concern were extracted into the tracked repo:

```
archive/java_source/                                    the .java source (14 files)
data/wordlists/leveled_ground_truth/{HSWL,CET4,CET6}/level{1-6}.json   parsed gen_leveled/ word lists
```

## 5. [Superseded] Original from-scratch reconstruction and the CET-6 finding

*Kept for the record. The CET-6-specific claim below is withdrawn — see §2.*

Before the Java source was available, this document built Level 2–6 from
scratch using a downloaded BNC/COCA family database and a
reimplementation of the Table 1 affix rules
(`analysis/build_leveled_wordlists.py`). That reconstruction is still
useful as an independent cross-check (it doesn't depend on the recovered
`gen_leveled` files at all) and its results are summarized here unchanged:

- Word-list sizes were off by 5–18% depending on list.
- Token coverage matched within ~0.4pp on average (max 0.78pp) — worse than
  the ground-truth files above, but still directionally useful.
- It originally reported: *"HSWL and CET-4 consistently undershoot the
  paper's reported sizes by ~5–9%; CET-6 consistently overshoots by
  ~11–18%... most likely because [CET-6's word list is denser in
  family-internal duplication, and] our family-boundary tie-breaking
  differs from the original Java `TreeMap`'s."* That diagnosis of *why*
  was correct (confirmed by the 29.6%-vs-16-19% "members of another
  family" statistic in the original analysis); the conclusion that this
  reflected something about the *paper's own* CET-6 processing was not —
  §2 shows the paper's real CET-6 numbers scale perfectly consistently
  with HSWL/CET-4, with no anomaly. The gap was entirely in this
  document's own reconstruction method.
- Its independently-produced AVL\* estimate (~92.86%) is superseded by the
  ground-truth-based ~92.81% in §3, but the close agreement between the two
  independent methods (0.05pp apart) is itself reassuring.

Full original methodology detail (affix rules, inflectional-form heuristic
for Level 2, iterative Level 3-5 merge procedure) is unchanged in
`analysis/build_leveled_wordlists.py`'s docstring and code.

## 6. What this does and doesn't settle, updated

**Settled with high confidence:**
- Table 5 (BNC/COCA supplement) — exact match to an authoritative source.
- Tables 6/7/8's token-coverage numbers — corroborated to within ~0.13pp
  average, 0.52pp max, using near-original data.
- Table 9 and the AWL\*/NAWL\* rows of Table 10 — corroborated to within
  0.12pp, in most cases matching to 2 decimal places.
- **AVL\* really does drop substantially** (94.09% → ~92.81%), and the
  paper's framing of AVL as clearly, decisively the best academic word list
  is not supported — validated via a sanity check that reproduces the
  paper's own published AVL\* figure exactly.
- The CET-6 word-family expansion behaves normally; there is no evidence of
  a pipeline-specific issue for CET-6 (this reverses what part of this
  document originally suggested).

**Still not settled:**
- Exact Table 3 sizes (off by 0.1-0.5%, one small cleanup step short).
- The exact corrected `AVL*` figure to two decimal places — 92.81% is a
  high-confidence estimate, not a re-run of the original code with the
  corrected AVL source file substituted in. That remains the authoritative
  way to get a final publication-ready number, though at this point the
  gap between "estimate" and "final number" is small.

## 7. Debugging exercise: a faithful Python port of the Java pipeline

`analysis/java_port_pipeline.py` is a line-for-line Python port of
`LevelList`, `AffixLevel`/`AffixLevelHandler`, and `LevelListHandler`,
generalized to run for all three lists (the Java source only has HighSchool
live) and wired to the data this repo actually has in place of the two
external files the Java code depended on but that were never provided
(`*_family_horizontal.txt` → rebuilt from the real BNC/COCA family
database; `*_lemmas_horizontal.txt` → approximated with the same regular-
inflection heuristic `build_leveled_wordlists.py` used, since Tom Cobb's
Familizer/Lemmatizer tool isn't available). Two bugs found while porting,
both handled explicitly rather than silently:

- **The Level-3 affix quirk is real and was replicated faithfully**:
  `level3prefixes = {}`, and `non`/`un` sit in `level3suffixes`, checked
  via `endsWith` — i.e. Level 3 does *not* do a `non-`/`un-` prefix check
  at all, contrary to Table 1's description.
- **`buildLevel()`'s hardcoded `HighSchool_levelList6` reference is a
  copy-paste bug that was fixed, not replicated** — generalizing the method
  to scan each list's own Level 6 (which is clearly the intended behavior,
  and required for CET-4/CET-6 to work at all).

**Debugging result: the faithful port does not reproduce the paper any
better than an approximate one.** Token coverage vs. the paper across all
18 Table 6/7/8 rows: mean −0.10pp, stdev 0.42pp — actually slightly *worse*
than the earlier, deliberately-approximate `build_leveled_wordlists.py`
(stdev 0.38pp), and both are much worse than simply using the recovered
real `gen_leveled` files (stdev 0.11pp, §2). A second variant was tested
with `non-`/`un-` moved to Level-3 *prefixes* (matching Table 1's
description instead of the literal code) — that lands at stdev 0.39pp,
statistically indistinguishable from the faithful-quirk version. **The
Level-3 prefix/suffix bug turns out not to be the dominant source of
error either way** — it matters at the margin (mainly for Level 3
specifically) but the bigger, harder-to-close gap is the missing Level-2
lemma file: without Tom Cobb's actual tool output, no regular-inflection
heuristic gets particularly close, and that error propagates into every
level above it via the cumulative merge.

**Practical conclusion**: this port is a useful, fully transparent,
reproducible artifact (and would immediately become much more accurate if
the real `*_lemmas_horizontal.txt` files ever turn up), but for actually
citable numbers, the recovered `gen_leveled/` ground-truth files (§2-3)
remain strictly better than anything this repo can compute from first
principles, precisely because they don't depend on reconstructing the
missing Level-2 lemmatizer step at all.

## 8. Files added

```
archive/java_source/hyponym/*.java, main/Main.java, Utils/FileUtils.java   recovered Java source (14 files)
data/wordlists/leveled_ground_truth/{HSWL,CET4,CET6}/level{1-6}.json       parsed real gen_leveled/ word lists
analysis/verify_ground_truth_levels.py                                     ground-truth verification + Table 9/10 rebuild
analysis/java_port_pipeline.py                                             faithful Python port of the Java classes + debugging notes
data/wordlists/leveled_java_port/{HSWL,CET4,CET6}/level{1-6}.json          output of the Python port (for comparison; gen_leveled is authoritative)
```

(§5's from-scratch files -- `data/wordlists/bnc_coca_source/`,
`bnc_coca_family_database.json`, `leveled/`, `build_bnc_coca_resources.py`,
`build_leveled_wordlists.py` -- remain in the repo as an independent
cross-check method.)
