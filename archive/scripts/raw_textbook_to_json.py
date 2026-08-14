import os
import json
from collections import defaultdict
import spacy

# Load spaCy's small English model
# spacy.require_gpu()
nlp = spacy.load('en_core_web_sm')
nlp.max_length = 2_500_00000  # Adjust to your needs

def process_files(directory):
    word_data = defaultdict(lambda: defaultdict(int))

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                text = file.read().lower()
                doc = nlp(text)  # Process text with spaCy
                for token in doc:
                    # Retain all words, including those with numbers or symbols
                    if not token.is_stop: #no need outside stop words
                        lemma = token.lemma_  # Use lemmatized form
                        word_data[lemma][filename] += 1

    return word_data

def save_to_json(word_data, output_path):
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(word_data, json_file, indent=4)

# Set your directory and output file
directory_path = "F:/research_file/FAWL_Python/Test"
output_file_path = "F:/research_file/FAWL_Python/corpus/textbooks_raw_json/textbook_1_clean.json"

word_data = process_files(directory_path)
save_to_json(word_data, output_file_path)

print(f"Word occurrences have been saved to {output_file_path}")
