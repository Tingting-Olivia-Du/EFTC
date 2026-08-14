import json
import pandas as pd

# Input and output file paths
input_file = "F:/research_file/FAWL_Python/results/subject_coverage_eawl.json"  # Replace with your JSON file path
output_file = "F:/research_file/FAWL_Python/results/output_table.xlsx"  # Desired output Excel file name

# Metrics to extract
metrics_to_extract = [
    "wordlist_size",
    "wordlist_usage",
    "unique_words_covered_by_wl",
    "frequency_coverage_percentage"
]

# Mapping dictionary to replace keys
textbook_dict = {
    "1": "Corporate Finance",
    "2": "International Finance",
    "3": "Risk Management and Financial Institutions",
    "4": "Investment",
    "5": "Bank Management and Financial Services",
    "6": "Macro-economics",
    "7": "Economics",
    "8": "Microeconomics",
    "9": "Econometrics",
    "10": "Statistics",
    "11": "Financial Accounting",
    "12": "Public Finance",
    "13": "Finance",
    "14": "Math Analytics",
    "15": "Advanced Mathematics",
    "16": "Financial Derivatives",
    "17": "Organizational Behavior",
    "18": "Financial Statement Analysis",
    "19": "Management"
}

# Load the JSON data
with open(input_file, 'r') as f:
    data = json.load(f)

# Initialize a list to hold the table rows
rows = []

# Ensure all textbook names are included, even if not in data
for key, textbook_name in textbook_dict.items():
    # Create a row starting with the textbook name
    row = [textbook_name]
    
    # Get the data for the key from the JSON (if it exists)
    values = data.get(key, {})
    
    # Append each metric value (or None if not present)
    for metric in metrics_to_extract:
        row.append(values.get(metric, None))
    
    # Add the row to the table
    rows.append(row)

# Create a DataFrame
columns = ["Textbook"] + metrics_to_extract  # Define the column headers
df = pd.DataFrame(rows, columns=columns)

# Save the DataFrame to an Excel file
df.to_excel(output_file, index=False)

print(f"Data has been successfully written to {output_file}")
