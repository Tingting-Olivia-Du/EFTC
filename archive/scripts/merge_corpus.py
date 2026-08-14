import json
import glob
from collections import defaultdict

def merge_word_frequencies(folder_path):
    # Use defaultdict to store word frequencies
    merged_frequencies = defaultdict(lambda: defaultdict(int))
    
    # Loop through all JSON files in the folder
    for file in glob.glob(f"{folder_path}/word_freq_text_*.json"):
        with open(file, 'r') as f:
            data = json.load(f)
        
        # Merge frequencies for each word
        for word, details in data.items():
            for idx, freq in details['frequency'].items():
                merged_frequencies[word][idx] += freq
    
    # Convert defaultdict back to normal dictionary for final result
    merged_frequencies = {word: dict(freq) for word, freq in merged_frequencies.items()}
    
    return merged_frequencies

def save_merged_frequencies(output_path, merged_frequencies):
    with open(output_path, 'w') as f:
        json.dump(merged_frequencies, f, indent=4)

# Usage
folder_path = "F:/research_file/FAWL_Python/output"  # Path to your folder containing the files
output_path = "F:/research_file/FAWL_Python/corpus/merged_corpus_all.json"

merged_frequencies = merge_word_frequencies(folder_path)
save_merged_frequencies(output_path, merged_frequencies)

print(f"Merged frequencies saved to: {output_path}")
