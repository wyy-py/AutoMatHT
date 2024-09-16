import os
import zipfile
import shutil
import pandas as pd

# 设置文件夹路径和csv表格路径
zip_folder = 'SACADA-structure/'
unzip_folder = 'SACADA-structure-unzip/'
# csv_path = 'SACADA-structure/SACADA.csv'

# 读取csv表格，获取Topology列的值,除去了24个
exclude_sacada_topologies = [
    4, 6, 7, 9, 14, 21, 64, 110, 137,
    149, 150, 166, 178, 253, 306, 313,
    314, 880, 881, 882, 894, 912, 914, 1071]
# df = pd.read_csv(csv_path)
# valid_topologies = set(df['Topology']) - set(exclude_topologies)

# 解压缩指定的.zip文件，创建子文件夹并进行相应操作
for i in range(1, 1193):
    if i in exclude_sacada_topologies:
        continue

    zip_file_path = os.path.join(zip_folder, f'{i}.zip')
    extraction_folder = os.path.join(unzip_folder, f'{i}')

    # 解压缩.zip文件
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_folder)

print("Done.")

