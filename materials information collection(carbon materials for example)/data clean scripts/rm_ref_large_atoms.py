import pandas as pd
import os
import shutil

# 读取CSV文件
csv_file_path = "/public/home/weiyi22/C/atoms/ref_large_atoms.csv"

ref_order = pd.read_csv(csv_file_path)  # ref_ids
ref_ids = ref_order.folder_name
ref_path = "/public/home/weiyi22/C/reference_new"

for ref_id in ref_ids:
    ref_3d_folder_path = os.path.join(ref_path, str(ref_id))
    ref_2d_folder_path = os.path.join(ref_path, "2d_structure", str(ref_id))

    # 检查源文件夹和目标文件夹是否存在
    # 检查源文件夹和目标文件夹是否存在
    if os.path.exists(ref_3d_folder_path):
        shutil.rmtree(ref_3d_folder_path)
        os.chdir('../')

    elif os.path.exists(ref_2d_folder_path):
        shutil.rmtree(ref_2d_folder_path)
        os.chdir('../../')

    else:
        continue  # 对于不存在的文件夹，继续下一个ref_id


