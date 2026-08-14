import json

def extract_unique_words(input_path, output_path):
    # 初始化一个集合来存储唯一单词
    unique_words = set()
    
    # 读取文件并提取单词
    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            words = line.split()  # 按空格拆分单词
            unique_words.update(words)  # 添加到集合中（去重）
    
    # 将单词排序并转换为列表
    sorted_words_list = sorted(unique_words)
    
    # 转换为 JSON 格式
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(sorted_words_list, json_file, indent=4, ensure_ascii=False)
    
    print(f"Unique words have been extracted and saved to {output_path}")

# 输入和输出文件路径
input_file_path = 'F:/research_file/FAWL_Python/wordlist/AWL/level/AWL_family.txt'  # 替换为你的输入文件路径
output_file_path = 'F:/research_file/FAWL_Python/wordlist/AWL/level/AWL_family.json'  # 替换为你的输出文件路径

# 调用函数
extract_unique_words(input_file_path, output_file_path)
