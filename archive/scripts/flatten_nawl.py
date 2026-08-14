import json

# 输入与输出路径
input_path = './wordlist/NAWL_nested.json'  # 修改为你的 NAWL 文件路径
output_path = './wordlist/NAWL/NAWL.json'

# 读取 NAWL 嵌套 JSON
with open(input_path, 'r', encoding='utf-8') as f:
    nested_data = json.load(f)

# 扁平化：收集所有 key 和其派生词
word_list = []
for base_word, derived_list in nested_data.items():
    word_list.append(base_word)
    word_list.extend(derived_list)

# 去重 & 排序（可选）
word_list = sorted(set(word_list))

# 保存为扁平 list 格式
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(word_list, f, indent=2, ensure_ascii=False)

print(f"✅ Flattened NAWL list has been saved as {output_path}")
