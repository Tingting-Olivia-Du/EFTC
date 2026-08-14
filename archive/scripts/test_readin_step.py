import os
import re

# Set your directory path where the text files are located
directory_path = "F:/research_file/FAWL_Python/Test"  # Replace with your directory path

# Function to clean the filename and extract the numeric index
def extract_index(filename):
    clean_name = filename.split('.')[0]
    match = re.match(r'([0-9]+[-_]?[0-9]*)', clean_name)
    if match:
        index = match.group(1).replace('-', '_')
        return index
    return None

# Function to check if a token is valid (non-word filtering)
def is_valid_word(word):
    if not re.match(r'^[a-zA-Z]{2,}$', word):
        return False  # Exclude non-alphabetic sequences or very short words
    if len(set(word)) == 1:  # Exclude repeated characters (e.g., "ii", "aaa")
        return False
    return True

# Function to read and tokenize the text files
def tokenize_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_index = extract_index(filename)  # Extract the file index
            file_path = os.path.join(directory, filename)
            print(f"\nReading file: {filename} (Index: {file_index})")
            # Read and tokenize the text content
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().lower()  # Read and convert to lowercase
                tokens = re.findall(r'\b\w+\b', content)  # Tokenize using regex
                valid_tokens = [token for token in tokens if is_valid_word(token)]  # Filter valid words
                
                print(f"Tokens: {tokens[-50:]}...")  # Print first 50 tokens for verification
                print(f"Valid Tokens: {valid_tokens[-50:]}...")  # Print first 50 valid tokens

# Define stop words and non-words detection (if not defined already)


STOP_WORDS = {
    "a", "an", "the", "he", "she", "it", "we", "you", "they", "this", "that", 
    "is", "am", "are", "was", "were", "in", "on", "at", "by", "for", "with", 
    "and", "but", "or", "of", "to", "as", "from", "then", "there", "here", 
    "so", "such", "not", "be", "have", "has", "had", "do", "does", "did"
}

def is_non_word(token):
    """Check if a token is a non-word (e.g., random characters)."""
    return bool(re.match(r'^[^a-zA-Z]+$', token))

def filter_tokens(tokens):
    """Filter tokens and capture filtered-out words."""
    valid_tokens = []
    filtered_out = []

    for token in tokens:
        token_lower = token.lower()  # Make token lowercase for comparison
        if token_lower in STOP_WORDS or is_non_word(token_lower):
            filtered_out.append(token)  # Store the filtered word
        else:
            valid_tokens.append(token)

    return valid_tokens, filtered_out

# Example read and tokenize function
def read_and_tokenize(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        tokens = re.findall(r'\b\w+\b', content)  # Simple tokenization
        valid_tokens, filtered_out = filter_tokens(tokens)

        print(f"Tokens: {tokens[-50:]}")  # Print last 50 tokens
        print(f"Valid Tokens: {valid_tokens[-50:]}")  # Print last 50 valid tokens
        print(f"Filtered-out Words: {filtered_out[-50:]}")  # Print last 50 filtered-out words

    return valid_tokens

# Test the function with a file
read_and_tokenize('F:/research_file/FAWL_Python/Test/2_9.txt')
