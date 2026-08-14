import re
import json
import os
from collections import defaultdict

# Specify the input directory and output JSON file
input_directory = "F:/research_file/FAWL_Python/textbook_collection"
output_file_path = "F:/research_file/FAWL_Python/corpus/proper_noun/combined_initials.json"

# Regular expression to find phrases followed by abbreviations
pattern = r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*\(([A-Z]+)\)"

# Dictionary to store valid full terms and abbreviation frequencies
abbreviation_data = defaultdict(lambda: {"full_term": None, "frequency": defaultdict(int)})

# Function to verify if a full term matches its abbreviation
def is_correct_full_term(full_term, abbreviation):
    initials = ''.join(word[0] for word in full_term.split())
    return abbreviation in initials.upper()

# Iterate through all .txt files in the input directory and subdirectories
for root, dirs, files in os.walk(input_directory):
    for file_name in files:
        if file_name.endswith(".txt"):
            file_path = os.path.join(root, file_name)
            file_id = os.path.splitext(file_name)[0]  # Extract the file identifier (e.g., '1_1')

            # Read text from the file with UTF-8 encoding
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            # Find all matches for full terms and abbreviations
            matches = re.findall(pattern, text)

            # Process each match
            for full_term, abbreviation in matches:
                if is_correct_full_term(full_term, abbreviation):
                    if abbreviation in abbreviation_data:
                        if abbreviation_data[abbreviation]["full_term"] == full_term:
                            abbreviation_data[abbreviation]["frequency"][file_id] += 1
                        # else:
                        #     # Log a warning for mismatched full terms
                        #     print(f"Warning: Mismatch for '{abbreviation}': '{full_term}' "
                        #           f"vs '{abbreviation_data[abbreviation]['full_term']}'")
                    else:
                        abbreviation_data[abbreviation]["full_term"] = full_term
                        abbreviation_data[abbreviation]["frequency"][file_id] += 1

            # Count standalone occurrences of abbreviations without full terms
            for abbreviation in abbreviation_data:
                abbreviation_data[abbreviation]["frequency"][file_id] += len(re.findall(rf"\b{abbreviation}\b", text))

# Save the combined data to the output JSON file
with open(output_file_path, "w") as json_file:
    json.dump(abbreviation_data, json_file, indent=4)

print(f"Processed data saved to '{output_file_path}'.")
