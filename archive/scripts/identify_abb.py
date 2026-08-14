import re
import json
from collections import defaultdict

# Specify input and output file paths
input_file_path = "F:/previous-FAWL/FAC_Project/texts/textbooks_pdf/01_corporate_finance/pdf/1_1.txt"
output_file_path = "F:/research_file/FAWL_Python/corpus/proper_noun/abbreviation_1_1_adjusted.json"

# Read text from the input file
with open(input_file_path, "r") as file:
    text = file.read()

# Regular expression to find phrases followed by abbreviations
pattern = r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*\(([A-Z]+)\)"

# Dictionary to store valid full terms and abbreviation frequencies
abbreviation_data = defaultdict(lambda: {"full_term": None, "frequency": 0})

# Function to verify if a full term matches its abbreviation (using last two words)
def is_correct_full_term(full_term, abbreviation):
    # Split the full term and get the last two words
    words = full_term.split()
    if len(words) >= 2:
        last_two_words = words[-2:]
    else:
        last_two_words = words  # Use all words if less than two

    # Extract initials of the last two words
    initials = ''.join(word[0] for word in last_two_words)
    return initials.upper() == abbreviation

# Find all matches for full terms and abbreviations
matches = re.findall(pattern, text)

# Process each match
for full_term, abbreviation in matches:
    if is_correct_full_term(full_term, abbreviation):  # Only process if full term matches abbreviation
        if abbreviation in abbreviation_data:
            # Check if the stored full term matches the current one
            if abbreviation_data[abbreviation]["full_term"] == full_term:
                abbreviation_data[abbreviation]["frequency"] += 1
            else:
                # Warn if there is a mismatch with the stored full term
                print(f"Mismatch found for '{abbreviation}': '{full_term}' does not match stored full term '{abbreviation_data[abbreviation]['full_term']}'")
        else:
            # Store the full term and initialize frequency if abbreviation is new
            abbreviation_data[abbreviation]["full_term"] = full_term
            abbreviation_data[abbreviation]["frequency"] += 1

# Count standalone occurrences of abbreviations without full terms
for abbreviation in abbreviation_data:
    abbreviation_data[abbreviation]["frequency"] += len(re.findall(rf"\b{abbreviation}\b", text))

# Save the result to the specified output JSON file
with open(output_file_path, "w") as json_file:
    json.dump(abbreviation_data, json_file, indent=4)

print(f"Processed data saved to '{output_file_path}'.")
