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

    # Display results
    print(f"Total words in wordlist: {len(wordlist)}")
    print(f"Words found in corpus: {len(words_in_corpus)}")
    print(f"wordlist usage: {coverage_percentage:.2f}%")
    print(f"unique corpus words covered by wordlist: {unique_words_covered_by_wl:.2f}%")
    print(f"Total wordlist frequency in corpus: {total_wordlist_frequency}")
    print(f"Total corpus frequency: {total_corpus_frequency}")
    print(f"Coverage by frequency: {frequency_coverage_percentage:.2f}%")
    print(f"Words in corpus not covered by wordlist: {len(words_not_covered)}")
    # print(f"Sample of words not covered: {list(words_not_covered)[:10]}")  # Show a few examples


# Usage
wordlist_file = "F:/research_file/FAWL_Python/wordlist/additional lists/json_additional_lists_lowercase/basewrd34_ab_low.json"
corpus_file = "F:/research_file/FAWL_Python/corpus/cleaned_merged_corpus_all.json"  # Use your uploaded corpus

wordlist = load_wordlist(wordlist_file)
corpus = load_corpus(corpus_file)

calculate_coverage(wordlist, corpus)
