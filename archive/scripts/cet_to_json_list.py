import json

# Define file paths
txt_file = "F:/research_file/FAWL_Python/wordlist/raw_txt/cet6_1.txt"
json_file = "F:/research_file/FAWL_Python/wordlist/cet6_1.json"

# Read the text file and store the words in a list
with open(txt_file, "r") as f:
    words = [line.strip() for line in f if line.strip()]  # Remove empty lines and strip whitespace

# Save the list as JSON
with open(json_file, "w") as f:
    json.dump(words, f, indent=4)

print(f"Wordlist has been successfully converted to {json_file}")
