import json
from collections import defaultdict

def accumulate_frequencies(json_file):
    # Open the JSON file and load its data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Dictionary to accumulate frequencies by subject
    subject_freqs = defaultdict(lambda: defaultdict(int))
    for word in data:
    # Iterate through the data and accumulate frequencies by subject
        for key, freq in data[word].items(): # each word is a dictionary as well
            # Split key into subject and book number (e.g., '6_2' -> subject 6, book 2)
            subject, _ = key.split('_')
            # print(subject)
            
            # Add the frequency of the word to the subject's total count
            subject_freqs[word][subject] += freq
        
    return subject_freqs

# Example usage
if __name__ == "__main__":
    json_file = 'F:/research_file/FAWL_Python/corpus/cleaned_merged_corpus_all.json'  # replace with the actual file path
    subject_freqs = accumulate_frequencies(json_file)
    
    # Print the accumulated frequencies by subject
    output_file = 'F:/research_file/FAWL_Python/corpus/subject_corpus/subject_freq_output.json'  # replace with the desired output file path
    
    # Write the accumulated frequencies to the output file in a readable JSON format
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(subject_freqs, f, indent=4, ensure_ascii=False)

    print(f"Output saved to {output_file}")


