import json

def load_corpus(file_path):
    """Load the corpus JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def remove_long_words(corpus, max_length=17):
    """Remove words longer than the specified max length from the corpus."""
    cleaned_corpus = {}
    filtered_words = {}

    # Separate long words from the normal corpus
    for word, freqs in corpus.items():
        if len(word) <= max_length:
            cleaned_corpus[word] = freqs
        else:
            filtered_words[word] = freqs

    return cleaned_corpus, filtered_words

def save_json(data, output_file):
    """Save the given data to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

# Usage
input_file = "F:/research_file/FAWL_Python/corpus/merged_corpus_all.json"
cleaned_output_file = "F:/research_file/FAWL_Python/corpus/cleaned_merged_corpus_all.json"
filtered_words_file = "F:/research_file/FAWL_Python/corpus/filtered_words_in_corpus_all.json"

# Load the original corpus
corpus = load_corpus(input_file)

# Remove long words from the corpus and get the filtered words
cleaned_corpus, filtered_words = remove_long_words(corpus)

# Save the cleaned corpus and filtered words to separate files
save_json(cleaned_corpus, cleaned_output_file)
save_json(filtered_words, filtered_words_file)

print(f"Cleaned corpus saved to: {cleaned_output_file}")
print(f"Filtered words saved to: {filtered_words_file}")

# Optional: Print a sample of the filtered words
print(f"Sample filtered words: {list(filtered_words.keys())[:10]}")
