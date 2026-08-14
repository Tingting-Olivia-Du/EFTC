import json

# Load the complex JSON file
with open('./wordlist/AWL_nested.json', 'r') as f:
    data = json.load(f)

# Function to flatten the nested dictionary into a list
def flatten_json(data):
    flat_list = []
    
    # Iterate through the sublists
    for sublist in data:
        # For each word, add the word and its subwords to the list
        for word, word_data in data[sublist].items():
            flat_list.append(word)
            # Check if 'subwords' exists and is a list
            if word_data and isinstance(word_data.get("subwords"), list):
                flat_list.extend(word_data["subwords"])

    return flat_list

# Flatten the JSON
flattened_list = flatten_json(data)

# Save the flattened structure as a new JSON list
with open('./wordlist/AWL/AWL.json', 'w') as f:
    json.dump(flattened_list, f, indent=4)

print("Flattened JSON list has been saved as 'AWL.json'")
