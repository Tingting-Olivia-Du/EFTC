import json
import os

# ✅ 设置两个词表的名字（只需要修改这两个变量即可）
name1 = "cet6_1"
name2 = "AVL"

# ✅ 自动生成路径
# input_1 = f'./wordlist/{name1}/{name1}.json'
input_1 = f'./wordlist_2/{name1}.json'
input_2 = f'./wordlist/{name2}/{name2}.json'
output_path = f'./wordlist/overlap/{name2}_{name1}.json'

# ✅ 读取 JSON 文件
with open(input_1, 'r', encoding='utf-8') as file1:
    wordlist1 = set(json.load(file1))

with open(input_2, 'r', encoding='utf-8') as file2:
    wordlist2 = set(json.load(file2))

# ✅ 差集与交集
unique_to_1 = list(wordlist1 - wordlist2)
unique_to_2 = list(wordlist2 - wordlist1)
overlap_words = list(wordlist1 & wordlist2)

# ✅ 计算重合率
num_overlap = len(overlap_words)
total_words = len(wordlist1 | wordlist2)
overlap_rate = num_overlap / total_words if total_words > 0 else 0.0

# ✅ 构建输出
output = {
    f"unique_to_{name1}": unique_to_1,
    f"unique_to_{name2}": unique_to_2,
    "overlap_words": overlap_words,
    "overlap_rate": round(overlap_rate, 4),
    "stats": {
        f"{name1}_word_count": len(wordlist1),
        f"{name2}_word_count": len(wordlist2),
        "overlap_word_count": num_overlap,
        "total_unique_words": total_words
    }
}

# ✅ 保存 JSON 输出
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as output_file:
    json.dump(output, output_file, indent=4, ensure_ascii=False)

# ✅ 打印信息
print(f"✅ Output saved to: {output_path}")
print(f"✅ Overlap Rate: {overlap_rate:.2%}")
print(f"{name1} Word Count: {len(wordlist1)}")
print(f"{name2} Word Count: {len(wordlist2)}")
print(f"Overlap Word Count: {num_overlap}")
