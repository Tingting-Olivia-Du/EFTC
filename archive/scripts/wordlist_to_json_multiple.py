import os
import json

# Define the directory containing the .txt files
txt_directory = "./wordlist/cet"
json_directory = "./wordlist/cet"  # Define a separate folder for json files

# Create json directory if it doesn't exist
os.makedirs(json_directory, exist_ok=True)

# Iterate over all files in the directory
for filename in os.listdir(txt_directory):
    if filename.endswith(".txt"):  # Process only .txt files
        txt_file = os.path.join(txt_directory, filename)
        json_file = os.path.join(json_directory, filename.replace(".txt", ".json"))

        # Read the text file and store the words in a list
        with open(txt_file, "r") as f:
            words = [line.strip() for line in f if line.strip()]  # Remove empty lines and strip whitespace

        # Save the list as JSON
        with open(json_file, "w") as f:
            json.dump(words, f, indent=4)

        print(f"Wordlist {filename} has been successfully converted to {json_file}")

print("All .txt files have been successfully converted to .json")
