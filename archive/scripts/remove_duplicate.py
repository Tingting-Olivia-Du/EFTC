import os
import json

# Define the input and output directories
input_directory = 'F:/research_file/FAWL_Python/wordlist/business_v2/origin'
output_directory = 'F:/research_file/FAWL_Python/wordlist/business_v2/clean'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Loop through each JSON file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(".json"):
        input_file_path = os.path.join(input_directory, filename)
        
        # Load the data from the JSON file
        with open(input_file_path, 'r') as file:
            words_list = json.load(file)
        
        # Remove duplicates by converting to a set, then back to a list
        unique_words = list(set(words_list))
        
        # Define the output file path
        output_file_path = os.path.join(output_directory, filename)
        
        # Write the unique words to the output file
        with open(output_file_path, 'w') as output_file:
            json.dump(unique_words, output_file, indent=4)
        
        print(f"Cleaned file saved to {output_file_path}")

print("All JSON files have been cleaned and saved to the output directory.")
