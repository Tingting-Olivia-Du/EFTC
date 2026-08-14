import os
import json

# Define the directory containing the JSON files (Input1)
input_directory = 'F:/research_file/FAWL_Python/wordlist/version_2/bnc_aca_addi'
# Define the path to the target addition JSON file (Input2)
target_addition_path = 'F:/research_file/FAWL_Python/wordlist/business_v2/clean/BWL2.json'
# Define the output directory for combined JSON files
output_directory = 'F:/research_file/FAWL_Python/wordlist/business_v2/bnc_aca_EAWL'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Load the data from the target addition JSON file
with open(target_addition_path, 'r') as target_file:
    target_data = json.load(target_file)

# Loop through each JSON file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(input_directory, filename)
        
        # Load the current JSON file data
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Combine the current file data with the target addition data, removing duplicates
        combined_data = list(set(data + target_data))  # Assuming both are lists
        
        # Define the output file path in the specified output directory
        output_file = os.path.join(output_directory, f'/BWL2_addi_{filename}')
        
        # Write the combined data to the output file
        with open(output_file, 'w') as outfile:
            json.dump(combined_data, outfile, indent=4)
        
        print(f"Combined JSON file saved to {output_file}")
