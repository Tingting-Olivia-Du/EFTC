import json

# 设置路径
cet4_path = './wordlist/cet/cet4_1.json'
cet6_path = './wordlist/cet/cet6_1.json'

# 加载词表
with open(cet4_path, 'r', encoding='utf-8') as f:
    cet4_words = json.load(f)

with open(cet6_path, 'r', encoding='utf-8') as f:
    cet6_words = json.load(f)

# 统计词数
print(f'CET-4 Word Count: {len(cet4_words)}')
print(f'CET-6 Word Count: {len(cet6_words)}')
