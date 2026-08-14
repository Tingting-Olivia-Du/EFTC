import json

# Load the corpus from a file
corpus_file = "F:/research_file/FAWL_Python/corpus/cleaned_merged_corpus_all.json"  # Update with your actual file path

def load_corpus(file_path):
    """Load the corpus JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def extract_keys_as_list(corpus):
    """Extract keys from the JSON corpus and return them as a list."""
    words_list = list(corpus.keys())  # Extract keys
    return words_list

def save_json(data, output_file):
    """Save the given data to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

# Load the corpus
corpus = load_corpus(corpus_file)

# Extract words (keys) from the corpus
words_list = extract_keys_as_list(corpus)

# Save the words as a JSON list to a file
output_file = "F:/research_file/FAWL_Python/corpus/corpus_list_all.json"  # Specify the output file path
save_json(words_list, output_file)

print(f"Words list saved to: {output_file}")
