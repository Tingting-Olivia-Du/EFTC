import json
import os

# Directory containing the input JSON files
input_dir = 'F:/research_file/FAWL_Python/wordlist/additional lists/json_additional_lists_new/'
output_dir = 'F:/research_file/FAWL_Python/wordlist/additional lists/json_additional_lists_lowercase/'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process each JSON file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        input_path = os.path.join(input_dir, filename)

        # Load JSON data from file
        with open(input_path, 'r') as file:
            data = json.load(file)

        # Convert each item to lowercase
        data_lowercase_items = [item.lower() if isinstance(item, str) else item for item in data]

        # Create the output path by appending "_low" to the original filename
        output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_low.json")

        # Save the modified JSON data to a new file
        with open(output_path, 'w') as file:
            json.dump(data_lowercase_items, file, indent=4)

        print(f"All items in {filename} have been converted to lowercase and saved to {output_path}")
