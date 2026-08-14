import os
import json

# Define the directory containing the JSON files
directory = 'F:/research_file/FAWL_Python/wordlist/Aca_lists'

# Initialize an empty set to store unique words
unique_words = set()

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        file_path = os.path.join(directory, filename)
        
        # Open and load the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
            
            # Add words from the current file to the set (automatically removes duplicates)
            unique_words.update(data)

# Convert the set back to a list
combined_data = list(unique_words)

# Specify the output file path
output_file = 'F:/research_file/FAWL_Python/wordlist/Aca_lists/gen_BEAWL_add.json'

# Write the combined data to the output file
with open(output_file, 'w') as outfile:
    json.dump(combined_data, outfile, indent=4)

print(f"Combined JSON file saved to {output_file}")
