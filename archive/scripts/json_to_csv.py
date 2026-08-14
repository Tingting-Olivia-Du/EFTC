import json
import pandas as pd

def json_to_table(input_path, output_path):
    # Load the JSON file
    with open(input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Prepare a list to hold rows for the DataFrame
    rows = []

    # Iterate through the outermost keys in the JSON
    for key, metrics in data.items():
        row = {"file_name": key}  # Start with the file name
        
        # Flatten the metrics into columns
        for metric_key, metric_value in metrics.items():
            if isinstance(metric_value, list):
                # Convert lists (e.g., words_not_covered) to a comma-separated string
                row[metric_key] = ", ".join(metric_value)
            else:
                row[metric_key] = metric_value
        
        rows.append(row)

    # Create a DataFrame
    df = pd.DataFrame(rows)

    # Save the DataFrame to a CSV file
    df.to_csv(output_path, index=False, encoding='utf-8')

# Specify the input and output file paths
input_path = "F:/research_file/FAWL_Python/results/aca_results.json"  # Replace with your input JSON file path
output_path = "F:/research_file/FAWL_Python/results/aca_statistics.csv"  # Replace with your desired output CSV file path

# Run the function
json_to_table(input_path, output_path)

print(f"Table saved to {output_path}")
