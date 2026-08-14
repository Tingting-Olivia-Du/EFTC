import json
from collections import defaultdict

subject_based_dict = defaultdict(lambda: defaultdict(int))
def convert_to_subject_base(file):
    with open(file, 'r') as f:
        data = json.load(f)
    for word in data:
        for book, freq in data[word].items():
            subject_based_dict[book][word] = freq
    return subject_based_dict

if __name__ == "__main__":
    word_based_file = 'F:/research_file/FAWL_Python/corpus/subject_corpus/subject_freq_output.json'
    subject_freqs = convert_to_subject_base(word_based_file)
    
    # Print the accumulated frequencies by subject
    output_file = 'F:/research_file/FAWL_Python/corpus/subject_corpus/subject_based_freq_output.json'  # replace with the desired output file path
    
    # Write the accumulated frequencies to the output file in a readable JSON format
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(subject_freqs, f, indent=4, ensure_ascii=False)

    print(f"Output saved to {output_file}")