import os
import json
from collections import defaultdict

def load_wordlist(file_path):
    """Load the wordlist as a set for quick lookups."""
    with open(file_path, 'r') as f:
        return set(json.load(f))

def load_corpus(file_path):
    """Load the corpus JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def calculate_coverage(wordlist, corpus):
    """Calculate the word list's coverage on the corpus."""
    corpus_words = set(corpus.keys())
    words_in_corpus = wordlist.intersection(corpus_words)

    # Calculate simple coverage percentage
    wordlist_usage = (len(words_in_corpus) / len(wordlist)) * 100
    unique_words_covered_by_wl = (len(words_in_corpus) / len(corpus_words)) * 100

    # Calculate frequency-based coverage
    total_wordlist_frequency = sum(
        corpus[word] for word in words_in_corpus
    )
    total_corpus_frequency = sum(
        freqs for freqs in corpus.values()
    )
    frequency_coverage_percentage = (total_wordlist_frequency / total_corpus_frequency) * 100

    words_not_covered = corpus_words - wordlist

    # Return statistical values
    return {
        "wordlist_size": len(wordlist),
        "words_found_in_corpus": len(words_in_corpus),
        "wordlist_usage": wordlist_usage,
        "unique_words_covered_by_wl": unique_words_covered_by_wl,
        "total_wordlist_frequency_in_corpus": total_wordlist_frequency,
        "total_corpus_frequency": total_corpus_frequency,
        "frequency_coverage_percentage": frequency_coverage_percentage,
        "words_not_covered": list(words_not_covered)[:5]  # Sample of uncovered words
    }

def process_wordlists(wordlist_dir, corpus_file, output_file):
    """Process all wordlists in the given directory and store the coverage results."""
    corpus_all = load_corpus(corpus_file)
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
                results = json.load(f)
    else:
        results = defaultdict(lambda: defaultdict(float))
    for subject_corpus in corpus_all:
        # Load existing results if the output file already exists
        # Iterate over all wordlist files in the directory
        for filename in os.listdir(wordlist_dir):
            if filename.endswith(".json"):
                wordlist_file = os.path.join(wordlist_dir, filename)
                wordlist = load_wordlist(wordlist_file)

                # Only process the wordlist if it hasn't been processed yet
                if filename not in results:
                    coverage_stats = calculate_coverage(wordlist, corpus_all[subject_corpus])
                    
                    # Store the result in the dictionary
                    results[subject_corpus][filename] = coverage_stats

                    print(f"Processed coverage for wordlist: {filename}")
                else:
                    print(f"Skipped {filename} as it is already in the output file.")

    # Save the updated results back to the output JSON file
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)

    print(f"All results have been saved to {output_file}")

# Usage
wordlist_directory = "F:/research_file/FAWL_Python/wordlist/gen_addi_avl_eawl"  # Directory with all wordlist JSON files
corpus_file = "F:/research_file/FAWL_Python/corpus/subject_corpus/subject_based_freq_output.json"  # Path to the corpus file
output_file = "F:/research_file/FAWL_Python/results/subject_coverage_results.json"  # Output file for the results

# Run the processing function
process_wordlists(wordlist_directory, corpus_file, output_file)
