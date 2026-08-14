import os
import json
import re
from collections import defaultdict
import spacy

# Load spaCy's small English model
# spacy.require_gpu()
nlp = spacy.load('en_core_web_sm')
nlp.max_length = 2_500_00000  # Adjust to your needs


def extract_index(filename):
    clean_name = filename.split('.')[0]
    match = re.match(r'([0-9]+[-_]?[0-9]*)', clean_name)
    if match:
        index = match.group(1).replace('-', '_')
        return index
    return None

def is_valid_word(word):
    if not re.match(r'^[a-zA-Z]{2,}$', word):
        return False
    if len(set(word)) == 1:
        return False
    return True

def process_files(directory):
    word_data = defaultdict(lambda: {"index": set(), "frequency": defaultdict(int)})

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            file_index = extract_index(filename)
            if file_index:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                    text = file.read().lower()
                    doc = nlp(text)  # Process text with spaCy
                    for token in doc:
                        if not token.is_stop and token.is_alpha:  # Filter stop words and non-alphabetic tokens
                            lemma = token.lemma_  # Use lemmatized form
                            if is_valid_word(lemma):
                                word_data[lemma]["index"].add(file_index)
                                word_data[lemma]["frequency"][file_index] += 1

    for word in word_data:
        word_data[word]["index"] = list(word_data[word]["index"])

    return word_data

def save_to_json(word_data, output_path):
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(word_data, json_file, indent=4)



# Set your directory and output file
directory_path = "F:/research_file/FAWL_Python/textbooks_19"
output_file_path = "F:/research_file/FAWL_Python/output/word_freq_text_19.json"

word_data = process_files(directory_path)
save_to_json(word_data, output_file_path)

print(f"Word occurrences have been saved to {output_file_path}")
