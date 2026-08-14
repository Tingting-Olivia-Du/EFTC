import json
import os
from itertools import combinations

# Input folder containing word list JSON files
input_folder = './wordlist/20241215_origin/overlap/awl_cet6'
output_path = './wordlist/20241215_origin/overlap/awl_cet6/awl_cet6_overlap_statistics.json'


# Load all JSON files from the folder with error handling
wordlists = {}
for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        filepath = os.path.join(input_folder, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                wordlists[filename] = set(json.load(file))
        except json.JSONDecodeError as e:
            print(f"Error in file {filename}: {e}")
            continue  # Skip this file and proceed

# Compare all pairs of word lists
results = {}
for (file1, words1), (file2, words2) in combinations(wordlists.items(), 2):
    overlap_words = words1 & words2
    num_overlap = len(overlap_words)
    total_words = len(words1 | words2)
    overlap_rate = round(num_overlap / total_words, 4) if total_words > 0 else 0.0

    # Save comparison stats
    pair_name = f"{file1} vs {file2}"
    results[pair_name] = {
        "overlap_rate": overlap_rate,
        "overlap_word_count": num_overlap,
        "total_unique_words": total_words,
        "overlap_words": list(overlap_words)
    }

# Save the results to a JSON file
with open(output_path, 'w', encoding='utf-8') as output_file:
    json.dump(results, output_file, indent=4, ensure_ascii=False)

# Print results summary
print(f"Overlap statistics saved to: {output_path}")
