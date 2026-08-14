import json

# Define the file path for input and output
input_file_path = 'F:/research_file/FAWL_Python/wordlist/additional lists/original_additional_lists/basewrd31_on.txt'
flattened_output_path = 'F:/research_file/FAWL_Python/wordlist/additional lists/json_additional_lists/pn_flattened_list.json'

# Initialize the flattened list structure
flattened_list = []

# Read the file and add each word directly to the flattened list
with open(input_file_path, 'r') as file:
    for line in file:
        # Remove extra whitespace
        word = line.strip()
        
        if word:  # If the line is not empty
            flattened_list.append(word)

# Save the flattened list to the specified JSON file
with open(flattened_output_path, 'w', encoding='utf-8') as f:
    json.dump(flattened_list, f, ensure_ascii=False, indent=2)
