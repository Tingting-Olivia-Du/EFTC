import os
import json
import csv

# 配置输入文件夹路径和输出CSV路径
input_folder = r"F:/research_file/FAWL_Python/wordlist/20241215_origin/level_map/level_map_stats"  # 根据实际情况修改
output_csv_path = r"F:/research_file/FAWL_Python/results/level_stats.csv"

# 准备CSV表头
header = ["wordlist_name", "level-1", "level-2", "level-3", "level-4", "level-5", "level-6"]

# 打开CSV文件进行写入
with open(output_csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    
    # 遍历输入文件夹中的JSON文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            # 构造文件完整路径
            filepath = os.path.join(input_folder, filename)
            
            # 打开并加载JSON数据
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 提取各级别percentage数据
            # 假设JSON中level的Key是字符串"level-1","level-2", ... "level-6"
            # 如果实际JSON中有不同的level顺序，需要自行调整
            levels = ["level-1", "level-2", "level-3", "level-4", "level-5", "level-6"]
            percentages = []
            for lvl in levels:
                # 考虑到有的文件可能缺某level项, 可以加个get避免报错
                lvl_data = data.get(lvl, {})
                percentage = lvl_data.get("percentage", "")
                percentages.append(percentage)
            
            # 去除文件名中的扩展名作为词表名字
            wordlist_name = os.path.splitext(filename)[0]
            
            # 写入一行CSV
            row = [wordlist_name] + percentages
            writer.writerow(row)

print("CSV文件生成完毕！")
