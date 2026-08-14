# Archive

The original, exploratory research pipeline that produced the English
Finance Textbooks Corpus (EFTC) and the word-list coverage results used in
the paper. Kept for provenance and traceability, but superseded as the
"official" entry point by the top-level `analysis/`, `data/`, and `report/`
folders (see the repository root [README](../README.md)).

## Layout

| Folder | Contents |
|---|---|
| `Textbooks_all/`, `Test/`, `Test_2/` | Textbook-extraction test fixtures. **Raw prose text is git-ignored** (see root `.gitignore`) — only files already committed before the copyright cleanup remain untracked locally; nothing here is pushed. |
| `Test_result/` | Sample word-frequency output from the extraction test fixtures. |
| `corpus/` | The full EFTC corpus build artifacts (merged word-frequency JSON, corpus file list). |
| `output/` | Per-textbook word-frequency JSON (19 files), one per source book/chapter grouping. |
| `results/` | Every intermediate coverage/overlap CSV and JSON the pipeline produced across its many iterations (Oct 2024 – Jan 2025). `statistics.csv` and `aca_statistics.csv` are the ones the paper's numbers were sourced from — a copy of just those lives in `../data/cached_results/` for the verification scripts. |
| `scripts/` | ~50 standalone Python scripts (PDF→text extraction, word-list cleaning, affix-level classification, coverage/overlap calculation, format conversion). Many have hardcoded local paths (`F:/research_file/FAWL_Python/...`) from the original Windows dev machine and are not run-as-is; see `../report/verification_report.md` (Finding R1) for what this means for reproducibility. |
| `wordlist/`, `wordlist_2/` | Word-list source files and their affix-level-expanded variants, in various stages of the pipeline's evolution. |
| `test_merge/` | Scratch output from a merge script test run. |
| `third-party/` | Vendored copies of two external open word-list repositories (see Acknowledgements below). |
| `textbook_collection/`, `textbooks_cleaned_slice/`, `textbooks_pdf/`, `textbooks_raw/` | Empty in this snapshot (intermediate PDF/TXT staging directories from the extraction pipeline). |
| `LEGACY_README.md` | The original repository README. |

## Acknowledgements

- https://github.com/lpmi-13/machine_readable_wordlists
- https://github.com/JavaProgrammerLB/cet-word-list
