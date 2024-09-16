import json
import os
import re
import shutil
import pandas as pd

# F:\learning materials\data_all\reference\crystals-1261160-supplementary.json
# with open('F:/learning materials/data_all/reference/crystals-1261160-supplementary.json', 'r') as f:
#     data = json.load(f)
#     # print(data)
#
# df = pd.DataFrame.from_dict(data, orient='index')
# # print(df)
# # print(df.index)
#
# ref_list = df.index.values
# print(ref_list.dtype)  # 206-1-16-C-r0-np-id355667 顺序不对

ref_poscar_path = "reference"
ref_poscar_path_new = "reference_new"


def natural_sort_key(s):
    """
    自定义排序函数，将字符串中的数字部分转换为整数，用于自然排序。
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


def sort_folders_by_number(folder_path):
    """
    按照文件夹名称中的数字进行排序。
    """
    folders = os.listdir(folder_path)
    sorted_folders = sorted(folders, key=natural_sort_key)

    return sorted_folders


# for ref_id in ref_list:
#     id_folder = os.path.join(ref_poscar_path_new, ref_id)
#     new_filename = os.path.join(id_folder, "POSCAR")
#
#     if not os.path.exists(id_folder):
#         os.makedirs(id_folder)
#
#     for refname in ref_old_name:
#         shutil.copy(os.path.join(ref_poscar_path, refname), new_filename)
#         # os.rename(os.path.join(ref_poscar_path, refname), new_filename)
#         print(f"Moved {refname} to {new_filename}")

ref_old_list = sort_folders_by_number(ref_poscar_path)
print(ref_old_list)

ref_list_sort = [filename.split('_POSCAR')[0] for filename in ref_old_list]
print(ref_list_sort)

for i in range(904):
    ref_id = ref_list_sort[i]  # ['3-10-36-C-r58x-p-id545421', '20-3-20-C-r7x-p-id545421', ……]
    id_folder = os.path.join(ref_poscar_path_new, ref_id)
    new_filename = os.path.join(id_folder, "POSCAR")

    if not os.path.exists(id_folder):
        os.makedirs(id_folder)

    refname = ref_old_list[i]  # 206-1-16-C-r0-np-id355667-POSCAR
    shutil.copy(os.path.join(ref_poscar_path, refname), new_filename)
    # 206-1-16-C-r0-np-id355667-POSCAR
    print(f"Moved {refname} to {new_filename}")
