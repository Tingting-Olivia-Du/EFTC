import json

# Load the wordlist (stored as a list) and corpus
with open("F:/research_file/FAWL_Python/wordlist/HighSchool_6.json", "r") as f:
    wordlist = set(json.load(f))  # Convert list to a set for fast lookup

with open("F:/research_file/FAWL_Python/corpus/merged_corpus_test.json", "r") as f:
    corpus = json.load(f)

# Extract the set of words from the corpus
corpus_words = set(corpus.keys())

# Calculate coverage
words_in_corpus = wordlist.intersection(corpus_words)
coverage_percentage = (len(words_in_corpus) / len(wordlist)) * 100

# Accumulate frequency-based coverage
total_wordlist_frequency = sum(
    sum(corpus[word].values()) for word in words_in_corpus
)
total_corpus_frequency = sum(
    sum(data.values()) for data in corpus.values()
)
frequency_coverage_percentage = (total_wordlist_frequency / total_corpus_frequency) * 100

# Find words in the corpus that are not covered by the wordlist
words_not_covered_by_wordlist = corpus_words - wordlist

# Display results
print(f"Total words in wordlist: {len(wordlist)}")
print(f"Words found in corpus: {len(words_in_corpus)}")
print(f"Coverage by word count: {coverage_percentage:.2f}%")
print(f"Total wordlist frequency in corpus: {total_wordlist_frequency}")
print(f"Total corpus frequency: {total_corpus_frequency}")
print(f"Coverage by frequency: {frequency_coverage_percentage:.2f}%")

# List words not covered by the wordlist
print(f"Words in corpus not covered by wordlist: {len(words_not_covered_by_wordlist)}")
print(f"Sample of words not covered: {list(words_not_covered_by_wordlist)[:10]}")  # Display a few examples
