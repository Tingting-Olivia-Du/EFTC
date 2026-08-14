import json

# 输入输出路径
input_path = './wordlist/AVL_nested.json'  # 修改为你的实际路径
output_path = './wordlist/AVl/AVL.json'

# 加载嵌套词表
with open(input_path, 'r') as f:
    nested_data = json.load(f)

# 扁平化所有词项为一个 list
word_list = []
for band in nested_data.values():
    word_list.extend(band.keys())

# 去重 & 排序（可选）
word_list = sorted(set(word_list))

# 保存为扁平 list 格式
with open(output_path, 'w') as f:
    json.dump(word_list, f, indent=2, ensure_ascii=False)

print(f"✅ Flattened AWL list has been saved as {output_path}")
