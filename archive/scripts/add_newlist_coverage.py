import json

def load_wordlist(file_path):
    """Load the wordlist as a set for quick lookups."""
    with open(file_path, 'r') as f:
        return set(json.load(f))

def load_corpus(file_path):
    """Load the corpus JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def calculate_coverage(wordlist, corpus):
    """Calculate the word list's coverage on the corpus."""
    corpus_words = set(corpus.keys())
    words_in_corpus = wordlist.intersection(corpus_words)

    # Calculate simple coverage percentage
    coverage_percentage = (len(words_in_corpus) / len(wordlist)) * 100
    unique_words_covered_by_wl = (len(words_in_corpus) / len(corpus_words)) * 100
    # Calculate frequency-based coverage
    total_wordlist_frequency = sum(
        sum(corpus[word].values()) for word in words_in_corpus
    )
    total_corpus_frequency = sum(
        sum(freqs.values()) for freqs in corpus.values()
    )
    frequency_coverage_percentage = (total_wordlist_frequency / total_corpus_frequency) * 100

    words_not_covered = corpus_words - wordlist

    # Prepare results
    return {
        "wordlist_size": len(wordlist),
        "words_found_in_corpus": len(words_in_corpus),
        "wordlist_usage": coverage_percentage,
        "unique_words_covered_by_wl": unique_words_covered_by_wl,
        "total_wordlist_frequency_in_corpus": total_wordlist_frequency,
        "total_corpus_frequency": total_corpus_frequency,
        "frequency_coverage_percentage": frequency_coverage_percentage,
        "words_not_covered": list(words_not_covered)[:10]  # Sample of uncovered words
    }

def update_results_file(result_file, wordlist_name, coverage_results):
    """Update the results JSON file with the new coverage data."""
    try:
        with open(result_file, 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        results = {}

    # Add the new results
    results[wordlist_name] = coverage_results

    # Save back to file
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=4)

# Usage
wordlist_file = "F:/research_file/FAWL_Python/wordlist/combine_gen_aca/combined/high_cet4_6_awl.json"
corpus_file = "F:/research_file/FAWL_Python/corpus/cleaned_merged_corpus_all.json"
result_file = "F:/research_file/FAWL_Python/results/wordlist_coverage_results.json"

wordlist = load_wordlist(wordlist_file)
corpus = load_corpus(corpus_file)

# Calculate coverage and update the result file
coverage_results = calculate_coverage(wordlist, corpus)
update_results_file(result_file, "high_cet4_cet6_awl", coverage_results)
