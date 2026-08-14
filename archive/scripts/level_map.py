import os
import json

# Define the affixes for each level
LEVEL_AFFIXES = {
    "level-2": {"prefixes": [], "suffixes": []},  # Inflectional suffixes handled dynamically
    "level-3": {"prefixes": [], "suffixes": ["able", "er", "ish", "less", "ly", "ness", "th", "y", "non", "un"]},
    "level-4": {"prefixes": ["in"], "suffixes": ["al", "ation", "ess", "ful", "ism", "ist", "ity", "ize", "ment", "ous"]},
    "level-5": {
        "prefixes": [
            "anti", "ante", "arch", "bi", "circum", "counter", "en", "ex", "fore", "hyper", "inter", "mid",
            "mis", "neo", "post", "pro", "semi", "sub", "un"
        ],
        "suffixes": [
            "age", "al", "ally", "an", "ance", "ant", "ary", "atory", "dom", "eer", "en", "ence", "ent", "ery", "ese",
            "esque", "ette", "hood", "ian", "ite", "let", "ling", "ly", "most", "ory", "ship", "ward", "ways", "wise"
        ]
    },
    "level-6": {
        "prefixes": ["pre", "re"],
        "suffixes": ["able", "ee", "ic", "ify", "ion", "ist", "ition", "ive", "th", "y"]
    }
}


def is_head(word, head_path):
    # Load the heads from the JSON file
    with open(head_path, 'r', encoding='utf-8') as file:
        heads = json.load(file)
    
    # Check if the word is in the list of heads or contains a hyphen
    if word in heads or '-' in word:
        return True
    return False

def map_word_to_level(word, head_path):
    # Level 2: Check for inflectional suffixes
    if is_head(word, head_path):
        return "level-1", "head"

    # Other levels
    for level, affixes in LEVEL_AFFIXES.items():
        # Check prefixes
        for prefix in affixes["prefixes"]:
            if word.startswith(prefix):
                return level, prefix
        # Check suffixes
        for suffix in affixes["suffixes"]:
            if word.endswith(suffix):
                return level, suffix
    return "level-2", 'inflectional'  # Default to level-1 if no match

def process_folder(input_folder, output_folder):
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            level_word_map = {level: {} for level in LEVEL_AFFIXES.keys()}
            level_word_map["level-1"] = {}

            level_stats = {level: 0 for level in LEVEL_AFFIXES.keys()}
            level_stats["level-1"] = 0

            total_words = 0

            with open(os.path.join(input_folder, file_name), "r", encoding="utf-8") as f:
                words = json.load(f)

            for word in words:
                total_words += 1
                level, affix = map_word_to_level(word)
                level_stats[level] += 1

                if affix not in level_word_map[level]:
                    level_word_map[level][affix] = []
                level_word_map[level][affix].append(word)

            # Calculate percentages for the second JSON output
            level_percentages = {
                level: {"count": count, "percentage": round((count / total_words) * 100, 2)}
                for level, count in level_stats.items()
            }

            # Save the first JSON output
            output_file_base = os.path.splitext(file_name)[0]
            with open(os.path.join(output_folder, f"{output_file_base}_level_word_map.json"), "w", encoding="utf-8") as f:
                json.dump(level_word_map, f, indent=4, ensure_ascii=False)

            # Save the second JSON output
            with open(os.path.join(output_folder, f"{output_file_base}_stats.json"), "w", encoding="utf-8") as f:
                json.dump(level_percentages, f, indent=4, ensure_ascii=False)

# Example usage
input_folder = "F:/research_file/FAWL_Python/wordlist/AWL/level/AWL_family"
output_folder = "F:/research_file/FAWL_Python/wordlist/AWL/level/AWL_family/level_map"
# head_path =

os.makedirs(output_folder, exist_ok=True)
process_folder(input_folder, output_folder)
