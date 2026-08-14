import json
import re

# Define a set of stop words
STOP_WORDS = {
    "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", 
    "while", "of", "at", "by", "for", "with", "about", "against", "between", 
    "into", "through", "during", "before", "after", "above", "below", "to", 
    "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", 
    "further", "then", "once", "here", "there", "when", "where", "why", "how", 
    "all", "any", "both", "each", "few", "more", "most", "other", "some", 
    "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", 
    "very", "s", "t", "can", "will", "just", "don", "should", "now", "he", 
    "she", "it", "they", "we", "you", "me", "him", "her", "us", "them", 
    "my", "your", "his", "its", "our", "their", "i", "who", "whom", "this", 
    "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", 
    "being", "have", "has", "had", "do", "does", "did", "doing"
}

# Function to check if a word is valid (non-stop word, non-repeated characters)
def is_valid_word(word):
    if word in STOP_WORDS:
        return False
    if not re.match(r'^[a-zA-Z]{2,}$', word):  # Exclude non-alphabetic words or very short words
        return False
    if len(set(word)) == 1:  # Exclude repeated characters like 'aaa'
        return False
    return True

# Process the text file and convert to JSON format
def process_file_to_json(file_path, output_path):
    word_data = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            words = line.lower().split()  # Convert to lowercase and split into words
            for word in words:
                if is_valid_word(word):
                    word_data[word] = 1  # Set value to 1 for each valid word

    # Save the result to a JSON file
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(word_data, json_file, indent=4)

    print(f"Data has been saved to {output_path}")

# Usage example
input_file = "F:/study_file/cs61b/fa23-s962/proj-research/data/countUnitMap/cet6_6.txt"  # Replace with your file path
output_file = "F:/research_file/FAWL_Python/wordlist/cet6_6.json"
process_file_to_json(input_file, output_file)
