import json

# 指定输入输出路径
input_path = 'F:/research_file/FAWL_Python/wordlist/AWL_nested.json'
output_txt_path = 'F:/research_file/FAWL_Python/wordlist/AWL/level/headwords.txt'
output_json_path = 'F:/research_file/FAWL_Python/wordlist/AWL/level/headwords.json'

# 从JSON文件读取数据
with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

headwords = []

# 提取所有 headword
for sublist_name, words_dict in data.items():
    for headword in words_dict.keys():
        headwords.append(headword)

# 将 headwords 写入 txt 文件
with open(output_txt_path, 'w', encoding='utf-8') as f_txt:
    for hw in headwords:
        f_txt.write(hw + '\n')

# 将 headwords 写入 json 文件（以列表形式）
with open(output_json_path, 'w', encoding='utf-8') as f_json:
    json.dump(headwords, f_json, ensure_ascii=False, indent=4)

# 打印统计结果
print("Total number of headwords:", len(headwords))
print("Headwords have been written to:")
print("TXT file:", output_txt_path)
print("JSON file:", output_json_path)
