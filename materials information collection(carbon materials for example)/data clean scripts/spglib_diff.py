import os

import pandas as pd
import spglib
import numpy as np

# utilize spglib package to get the symmetry information.


def read_poscar(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # 读取晶胞参数
    cell = np.zeros((3, 3))
    for i in range(3):
        cell[i] = [float(x) for x in lines[2 + i].split()]

    # 读取原子类型和数量
    species = lines[5].split()
    # print(species) C
    num_atoms = [int(x) for x in lines[6].split()]
    positions = []
    start_line = 8  # 假设原子位置从第 9 行开始（索引为 8）
    for i, num in enumerate(num_atoms):
        for j in range(num):
            pos = [float(x) for x in lines[start_line + sum(num_atoms[:i]) + j].split()]
            positions.append(pos)

    return cell, species, positions, num_atoms


def get_symmetry(filename, tolerance=1e-5):
    cell, species, positions, num_atoms = read_poscar(filename)
    lattice = cell
    positions = np.array(positions)
    numbers = []
    for i, num in enumerate(num_atoms):
        numbers += [i + 1] * num

    # 使用 spglib 获取对称性信息
    #dataset = spglib.get_symmetry_dataset((lattice, positions, numbers))
    dataset = spglib.get_symmetry_dataset((lattice, positions, numbers), symprec=tolerance)

    # 提取额外的对称性信息
    symmetry_info = {
        'space_group_international': dataset['international'],
        'space_group_number': dataset['number'],
        'point_group_type': dataset['pointgroup']
    }
    return symmetry_info


# 使用 POSCAR 文件
poscar_file = 'POSCAR'  # 替换为你的 POSCAR 文件路径 your_path_to/POSCAR_
tolerance = 1e-7  # 设置容差值，可以根据需要调整
symmetry_info = get_symmetry(poscar_file, tolerance)

# 打印对称性信息
print(f"Space Group Symbols (International): {symmetry_info['space_group_international']}")
print(f"Space Group Number: {symmetry_info['space_group_number']}")
print(f"Point Group Type: {symmetry_info['point_group_type']}")

df_unremoved = pd.read_csv("structure_remove_largestructures.csv")
unremoved_id = df_unremoved.name
ids = unremoved_id
folder_path = "clean_data_1"
space_group_international_list = []
space_group_number_list = []
point_group_type_list = []

df_unremoved_1 = pd.DataFrame(df_unremoved)

for i in range(1388):  # 表格有1389列，除标题共1388列
    print("i==", i)
    id_i = ids[i]
    print("id==", id_i)
    poscar_file_path = os.path.join(folder_path, str(id_i), "POSCAR")
    tolerance = 1e-6
    symmetry_info = get_symmetry(poscar_file_path, tolerance)
    print("symmetry_info==", symmetry_info)
    space_group_international = symmetry_info['space_group_international']
    space_group_number = symmetry_info['space_group_number']
    point_group_type = symmetry_info['point_group_type']
    space_group_international_list.append(space_group_international)
    space_group_number_list.append(space_group_number)
    point_group_type_list.append(point_group_type)

spg_data = {"space_group_international": space_group_international_list, "space_group_number": space_group_number_list,
            "point_group_type": point_group_type_list}
df_spg = pd.DataFrame(data=spg_data)
df_new = pd.concat([df_unremoved_1, df_spg], axis=1)
print(df_new)
df_new.to_csv("structure_remove_largestructures_1.csv")
