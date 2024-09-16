import pandas as pd
import os
import shutil

# 读取CSV文件
# prepare a csv. file that containing all the folders with large atoms that you want to delete. 
# e.g. sacada_large_atoms.csv
csv_file_path = "sacada_large_atoms.csv"

sacada_order = pd.read_csv(csv_file_path)  # sacada_ids
sacada_ids = sacada_order.folder_name
sacada_path = "SACADA-poscar-1"

for sacada_id in sacada_ids:
    sacada_3d_folder_path = os.path.join(sacada_path, str(sacada_id))
    sacada_2d_folder_path = os.path.join(sacada_path, "2d_structure", str(sacada_id))

    # 检查源文件夹和目标文件夹是否存在
    # 检查源文件夹和目标文件夹是否存在
    if os.path.exists(sacada_3d_folder_path):
        shutil.rmtree(sacada_3d_folder_path)
        os.chdir('../')

    elif os.path.exists(sacada_2d_folder_path):
        shutil.rmtree(sacada_2d_folder_path)
        os.chdir('../../')

    else:
        continue  # 对于不存在的文件夹，继续下一个sacada_id


