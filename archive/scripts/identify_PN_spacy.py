import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Increase the maximum length limit
nlp.max_length = 3000000000  # Increase as needed, e.g., to 3,000,000
# Read your finance text file
file_path = "F:/previous-FAWL/FAC_Project/texts/textbooks_pdf/01_corporate_finance/pdf/1_1.txt"
with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
    text = file.read()

# Process the text with spaCy
doc = nlp(text)

# Extract proper nouns
proper_nouns = [token.text for token in doc if token.pos_ == "PROPN"]

# Display or save the results
print("Proper Nouns Found:", set(proper_nouns))  # Use `set` to remove duplicates
