import os
import pandas as pd

oqmd_poscar_path = "poscars/"

# oqmd_order =
for filename in os.listdir(oqmd_poscar_path):
    # 检查文件名是否以"POSCAR_"开头
    if filename.startswith("POSCAR_"):
        # 获取oqmd_id，即文件名中"POSCAR_"之后的部分
        oqmd_id = filename[len("POSCAR_"):]
        print(len(oqmd_id))

        # 创建以oqmd_id命名的文件夹
        new_folder = os.path.join(oqmd_poscar_path, oqmd_id)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)

        # 构建新的文件路径
        new_filename = os.path.join(new_folder, "POSCAR")

        # 重命名并移动文件
        os.rename(os.path.join(oqmd_poscar_path, filename), new_filename)
        print(f"Moved {filename} to {new_filename}")


