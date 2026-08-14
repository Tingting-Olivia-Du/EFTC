import os
import json
from collections import defaultdict

corpus_file = "F:/research_file/FAWL_Python/corpus/subject_corpus/subject_based_freq_output.json" 
output_file = "F:/research_file/FAWL_Python/results/subject_size.json"

def load_corpus(file_path):
    """Load the corpus JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)
    
def calculate_corpus_size(file):
    data = load_corpus(file)
    subject_size = defaultdict(int)
    for subject_index in data:
        subject_freq = sum(data[subject_index].values())
        subject_size[subject_index] = subject_freq
    with open(output_file, "w") as f:
        json.dump(subject_size, f, indent=4)

def whole_size(file):
    data = load_corpus(file)
    total = sum(data.values())  # Rename 'sum' to 'total'
    return total


total = whole_size(output_file)
print(total)
