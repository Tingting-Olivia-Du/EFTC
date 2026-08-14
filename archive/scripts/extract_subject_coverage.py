import json
from collections import defaultdict

inuput_path = "F:/research_file/FAWL_Python/results/subject_coverage_results.json"
output_path = "F:/research_file/FAWL_Python/results/subject_coverage_eawl.json"
def load_json(file_path):
    """Load the corpus JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def getSubjectCoverage(inuput_path, output_path):
    results = {}
    data = load_json(inuput_path)
    for i in range(1, 20):
        key = str(i)
        results[key] = data[key]["gen_addi_avl_EAWL.json"]
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)

getSubjectCoverage(inuput_path, output_path)