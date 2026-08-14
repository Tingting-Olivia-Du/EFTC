import spacy
import json

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Define a function to process text in chunks and extract proper nouns

def extract_entities_in_chunks(text, chunk_size=1000000, entity_labels=None):
    entities = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        doc = nlp(chunk)
        chunk_entities = [ent.text for ent in doc.ents if ent.label_ in entity_labels]
        entities.extend(chunk_entities)
    return entities

entity_labels = {"ORG"}  # Add or remove labels as needed

# Read the file with specified encoding
file_path = "F:/previous-FAWL/FAC_Project/texts/textbooks_pdf/01_corporate_finance/pdf/1_1.txt"
with open(file_path, "r", encoding="ISO-8859-1") as file:
    text = file.read()

# Extract proper nouns in chunks

filtered_entities = extract_entities_in_chunks(text, entity_labels=entity_labels)

# Save the proper nouns to a JSON file
output_path = "F:/research_file/FAWL_Python/corpus/1_1_pn_org.json"
with open(output_path, "w", encoding="utf-8") as json_file:
    json.dump(filtered_entities, json_file, ensure_ascii=False, indent=4)

print(f"Proper nouns have been saved to {output_path}")
