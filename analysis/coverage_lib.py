"""
Core lexical-coverage metrics used throughout the EFTC (English Finance
Textbooks Corpus) lexical coverage study.

Re-implemented from scratch (clean-room) based on the metric definitions
given in the paper's Section 4.2.2 ("Coverage indicators and cumulative
coverage calculation"):

  1. Word list attestation rate = (# word-list entries found in the corpus)
                                   / (word-list size) * 100
  2. Type coverage              = (# word-list entries found in the corpus)
                                   / (# distinct types in the corpus) * 100
  3. Token coverage             = (summed corpus frequency of matched
                                   word-list entries)
                                   / (total corpus token frequency) * 100

The corpus is stored as a JSON dictionary: {word: {sub_id: count, ...}}.
A word's total frequency is the sum of its per-chapter/unit counts.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def load_json(path: str | Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_wordlist(path: str | Path) -> set[str]:
    """Word lists are stored as flat JSON arrays of lowercase strings."""
    data = load_json(path)
    if isinstance(data, dict):
        # Some word lists (e.g. BNC/COCA banded lists) are nested dicts of
        # band -> [words]; flatten them.
        words: set[str] = set()
        for v in data.values():
            if isinstance(v, list):
                words.update(v)
        return words
    return set(data)


class Corpus:
    """Wraps the EFTC frequency dictionary and precomputes per-word totals."""

    def __init__(self, path: str | Path):
        raw = load_json(path)
        self.freq: dict[str, int] = {
            word: sum(counts.values()) if isinstance(counts, dict) else counts
            for word, counts in raw.items()
        }
        self.total_types = len(self.freq)
        self.total_tokens = sum(self.freq.values())

    def __contains__(self, word: str) -> bool:
        return word in self.freq

    def __len__(self) -> int:
        return self.total_types


def coverage_stats(wordlist: Iterable[str], corpus: Corpus) -> dict:
    wl = set(wordlist)
    matched = [w for w in wl if w in corpus]
    matched_freq = sum(corpus.freq[w] for w in matched)

    wordlist_size = len(wl)
    attestation_rate = 100 * len(matched) / wordlist_size if wordlist_size else 0.0
    type_coverage = 100 * len(matched) / corpus.total_types if corpus.total_types else 0.0
    token_coverage = 100 * matched_freq / corpus.total_tokens if corpus.total_tokens else 0.0

    return {
        "wordlist_size": wordlist_size,
        "words_found_in_corpus": len(matched),
        "attestation_rate_pct": attestation_rate,
        "type_coverage_pct": type_coverage,
        "token_coverage_pct": token_coverage,
        "matched_token_frequency": matched_freq,
        "total_corpus_tokens": corpus.total_tokens,
    }


def overlap_stats(list_a: Iterable[str], list_b: Iterable[str]) -> dict:
    a, b = set(list_a), set(list_b)
    overlap = a & b
    union = a | b
    rate = 100 * len(overlap) / len(union) if union else 0.0
    return {
        "size_a": len(a),
        "size_b": len(b),
        "overlap_word_count": len(overlap),
        "total_unique_words": len(union),
        "overlap_rate_pct": rate,
    }
