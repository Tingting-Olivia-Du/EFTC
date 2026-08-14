import json
import nltk
from nltk.corpus import words

# Download the NLTK words corpus if it's not already available
nltk.download('words')

def load_corpus(file_path):
    """Load the corpus JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def is_nonsense_word(word):
    """Heuristic check for nonsense words."""

    if sum(1 for char in word if char in 'aeiou') < 1:  # Too few vowels
        return True
    return False

def filter_nonsense_words(corpus):
    """Filter out words not in the English dictionary or flagged as nonsense."""
    cleaned_corpus = {}
    filtered_words = {}

    for word, freqs in corpus.items():
        if is_nonsense_word(word):
            filtered_words[word] = freqs
        else:
            cleaned_corpus[word] = freqs

    return cleaned_corpus, filtered_words

def save_json(data, output_file):
    """Save the given data to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

# File paths
input_file = "F:/research_file/FAWL_Python/corpus/test_corpus/merged_corpus_test.json"  # Input corpus file
cleaned_output_file = "F:/research_file/FAWL_Python/corpus/test_corpus/cleaned_corpus_no_nonsense_1.json"  # Cleaned corpus output
filtered_words_file = "F:/research_file/FAWL_Python/corpus/test_corpus/filtered_words_no_nonsense_1.json"  # Filtered nonsense words output

# Load the corpus
corpus = load_corpus(input_file)

# Filter out nonsense words
cleaned_corpus, filtered_words = filter_nonsense_words(corpus)

# Save the cleaned corpus and filtered nonsense words
save_json(cleaned_corpus, cleaned_output_file)
save_json(filtered_words, filtered_words_file)

print(f"Cleaned corpus saved to: {cleaned_output_file}")
print(f"Filtered words saved to: {filtered_words_file}")

# Print a sample of the filtered words for quick verification
print(f"Sample filtered words: {list(filtered_words.keys())[:10]}")
