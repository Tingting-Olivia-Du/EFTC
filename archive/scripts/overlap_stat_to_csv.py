import os
import json
import csv

# Define the folder containing JSON files
input_folder = "F:/research_file/FAWL_Python/wordlist/20241215_origin/overlap/overlap_stat"
output_csv = "F:/research_file/FAWL_Python/results/combined_overlap_statistics.csv"

# List of files to process
json_files = [file for file in os.listdir(input_folder) if file.endswith(".json")]

# Open a CSV file for writing
with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    
    # Write the header row
    writer.writerow(["Comparison Name", "Overlap Rate", "Overlap Word Count", "Total Unique Words"])
    
    # Process each JSON file
    for json_file in json_files:
        file_path = os.path.join(input_folder, json_file)
        
        # Load JSON content
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # Extract key-value pairs
            for comparison, metrics in data.items():
                overlap_rate = metrics.get("overlap_rate", "N/A")
                overlap_word_count = metrics.get("overlap_word_count", "N/A")
                total_unique_words = metrics.get("total_unique_words", "N/A")
                
                # Write a row for each comparison
                writer.writerow([comparison, overlap_rate, overlap_word_count, total_unique_words])

print(f"Data successfully written to {output_csv}")
