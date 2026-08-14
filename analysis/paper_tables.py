"""
Every numeric table cell transcribed from paper/paper.md (Tables 2, 4, 5,
6, 7, 8, 9, 10), paired with the cached-pipeline output file name that the
original EFTC repository's `results/` folder claims to have produced it
from. Used by verify_cached_tables.py to check that paper.md is a faithful
transcription of the pipeline's own output files.

NOTE: this only proves paper.md == results/*.{csv,json}. It does NOT prove
results/*.{csv,json} were computed correctly from the raw textbooks --
that would require the Level 2-6 word-family-expanded word lists and the
BNC/COCA supplementary sub-lists, which are not present in the repository
(see report/verification_report.md, "Reproducibility gap").
"""

# (table, row_label, source_file, paper_size, paper_attestation_pct, paper_type_pct, paper_token_pct)
TABLE5_BNC_COCA_SUPPLEMENT = [
    ("Table 5", "Proper names",               "basewrd31_pn_low.json", 22409, 41.74, 7.74, 3.41),
    ("Table 5", "Marginal words",              "basewrd32_mw_low.json", 196,   34.18, 0.06, 0.06),
    ("Table 5", "Transparent compounds",       "basewrd33_tc_low.json", 6044,  25.53, 1.28, 0.66),
    ("Table 5", "Acronyms",                    "basewrd34_ab_low.json", 1149,  73.98, 0.70, 1.29),
    ("Table 5", "Combined supplementary list", "combined_additional.json", 29798, 39.65, 9.78, 5.42),
]

TABLE6_HSWL = [
    ("Table 6", "HSWL Level 1",  "HighSchool_1.json",     3448,  92.98, 2.65,  60.63),
    ("Table 6", "HSWL Level 1+", "add_HighSchool_1.json", 33138, 45.04, 12.35, 65.93),
    ("Table 6", "HSWL Level 2",  "HighSchool_2.json",     9854,  51.79, 4.22,  62.84),
    ("Table 6", "HSWL Level 2+", "add_HighSchool_2.json", 39413, 42.61, 13.90, 68.02),
    ("Table 6", "HSWL Level 3",  "HighSchool_3.json",     12792, 53.60, 5.67,  65.97),
    ("Table 6", "HSWL Level 3+", "add_HighSchool_3.json", 42351, 43.79, 15.35, 71.15),
    ("Table 6", "HSWL Level 4",  "HighSchool_4.json",     13750, 54.47, 6.20,  67.90),
    ("Table 6", "HSWL Level 4+", "add_HighSchool_4.json", 43309, 44.29, 15.87, 73.08),
    ("Table 6", "HSWL Level 5",  "HighSchool_5.json",     14951, 53.92, 6.67,  68.36),
    ("Table 6", "HSWL Level 5+", "add_HighSchool_5.json", 44510, 44.38, 16.35, 73.54),
    ("Table 6", "HSWL Level 6",  "HighSchool_6.json",     18023, 48.73, 7.27,  69.70),
    ("Table 6", "HSWL Level 6+", "add_HighSchool_6.json", 47582, 43.03, 16.94, 74.89),
]

TABLE7_CET4 = [
    ("Table 7", "CET-4 WL Level 1",  "cet4_1.json",     4543,  93.92, 3.53,  72.26),
    ("Table 7", "CET-4 WL Level 1+", "add_cet4_1.json", 34257, 46.71, 13.24, 77.44),
    ("Table 7", "CET-4 WL Level 2",  "cet4_2.json",     12885, 51.46, 5.49,  74.63),
    ("Table 7", "CET-4 WL Level 2+", "add_cet4_2.json", 42477, 43.14, 15.17, 79.69),
    ("Table 7", "CET-4 WL Level 3",  "cet4_3.json",     16359, 52.60, 7.12,  76.92),
    ("Table 7", "CET-4 WL Level 3+", "add_cet4_3.json", 45951, 44.18, 16.80, 81.99),
    ("Table 7", "CET-4 WL Level 4",  "cet4_4.json",     17595, 53.27, 7.76,  78.26),
    ("Table 7", "CET-4 WL Level 4+", "add_cet4_4.json", 47187, 44.65, 17.44, 83.32),
    ("Table 7", "CET-4 WL Level 5",  "cet4_5.json",     18991, 52.73, 8.29,  78.76),
    ("Table 7", "CET-4 WL Level 5+", "add_cet4_5.json", 48583, 44.68, 17.97, 83.83),
    ("Table 7", "CET-4 WL Level 6",  "cet4_66.json",    22664, 47.82, 8.97,  80.10),
    ("Table 7", "CET-4 WL Level 6+", "add_cet4_6.json", 52256, 43.12, 18.65, 85.17),
]

TABLE8_CET6 = [
    ("Table 8", "CET-6 WL Level 1",  "cet6_1.json",     8074,  93.88, 6.27,  82.32),
    ("Table 8", "CET-6 WL Level 1+", "add_cet6_1.json", 37719, 51.04, 15.93, 87.48),
    ("Table 8", "CET-6 WL Level 2",  "cet6_2.json",     16390, 60.52, 8.21,  84.00),
    ("Table 8", "CET-6 WL Level 2+", "add_cet6_2.json", 45895, 46.92, 17.82, 88.96),
    ("Table 8", "CET-6 WL Level 3",  "cet6_3.json",     19572, 59.39, 9.62,  85.49),
    ("Table 8", "CET-6 WL Level 3+", "add_cet6_3.json", 49077, 47.35, 19.23, 90.45),
    ("Table 8", "CET-6 WL Level 4",  "cet6_4.json",     20478, 58.99, 9.99,  85.72),
    ("Table 8", "CET-6 WL Level 4+", "add_cet6_4.json", 49983, 47.40, 19.61, 90.68),
    ("Table 8", "CET-6 WL Level 5",  "cet6_5.json",     21762, 57.97, 10.44, 86.03),
    ("Table 8", "CET-6 WL Level 5+", "add_cet6_5.json", 51267, 47.26, 20.05, 90.99),
    ("Table 8", "CET-6 WL Level 6",  "cet6_6.json",     25243, 52.58, 10.98, 86.72),
    ("Table 8", "CET-6 WL Level 6+", "add_cet6_6.json", 54748, 45.45, 20.59, 91.67),
]

TABLE9_GENERAL_COMPOSITE = [
    ("Table 9", "General Composite Word List",  "high_cet4_cet6_level6.json",      26411, 51.49, 11.25, 86.88),
    ("Table 9", "General Composite Word List+", "addi_high_cet4_cet6_level6.json", 55801, 45.09, 20.82, 91.78),
]

# Table 10 starred rows live in statistics.csv (combined_5 / gen_addi_nawl / gen_AVL_add);
# unstarred (standalone) rows live in aca_statistics.csv (different column layout).
TABLE10_ACADEMIC_STARRED = [
    ("Table 10", "AWL*",  "combined_5.json",     56254, 45.07, 20.98, 91.93),
    ("Table 10", "NAWL*", "gen_addi_nawl.json",  56775, 44.75, 21.03, 92.50),
    ("Table 10", "AVL*",  "gen_AVL_add.json",    63153, 47.37, 24.76, 94.09),
]

TABLE10_ACADEMIC_STANDALONE = [
    ("Table 10", "AWL",  "AWL.json",  3107,  62.63, 1.61,  20.19),
    ("Table 10", "NAWL", "NAWL.json", 2598,  48.08, 1.03,  5.15),
    ("Table 10", "AVL",  "AVL.json",  18558, 81.50, 12.52, 86.99),
]

ALL_STATISTICS_CSV_ROWS = (
    TABLE6_HSWL + TABLE7_CET4 + TABLE8_CET6 + TABLE9_GENERAL_COMPOSITE
    + TABLE10_ACADEMIC_STARRED + TABLE5_BNC_COCA_SUPPLEMENT
)
