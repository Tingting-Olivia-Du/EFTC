import json

# Load JSON data from files

input_1 = 'F:/research_file/FAWL_Python/wordlist/20241215_origin/compare_awl_cet/AWL.json'
input_2 = 'F:/research_file/FAWL_Python/wordlist/20241215_origin/compare_awl_cet/cet6_1.json'
output_path = 'F:/research_file/FAWL_Python/wordlist/20241215_origin/compare_awl_cet/cross_AWL_cet6.json'
with open(input_1, 'r') as file1:
    json1 = json.load(file1)

with open(input_2, 'r') as file2:
    json2 = json.load(file2)

# Find keys that are in json1 but not in json2
unique_to_json1 = list(set(json1) - set(json2))

# Find keys that are in json2 but not in json1
unique_to_json2 = list(set(json2) - set(json1))

# Prepare the output dictionary
output = {
    "unique_to_AWL": unique_to_json1,
    "unique_to_cet6": unique_to_json2
}

# Save the output to a new JSON file
with open(output_path, 'w') as output_file:
    json.dump(output, output_file, indent=4)

print("Output saved to output.json")
