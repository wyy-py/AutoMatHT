import os
import json
import pandas as pd
import numpy as np
import ase.io
from pymatgen.core.structure import Structure
from pymatgen.io.ase import AseAtomsAdaptor

# 如果把不同数据库中的结构信息通过pymatgen存储到同一个表格中，读取结构中信息的方法。

df = pd.read_csv("crystals.csv")
print(df.structure)
df_id = pd.read_csv("entries.csv")


def parse_structure_data(structure_str):
    # 将字符串解析为包含结构信息的字典
    lines = structure_str.strip().split('\n')
    # print("lines0==", lines[0])
    full_formula = lines[0].replace("Full Formula (", "").replace(")", "")
    # print(full_formula)
    reduced_formula = lines[1].split(":")[1].strip()
    # print(reduced_formula)
    # print(lines[2])
    # a_values = float(lines[2].split(" ")[6])
    # print(a_values)
    abc_values = lines[2].split(":")[1]
    # print(abc_values)
    angles_values = lines[3].split(":")[1]
    # print(angles_values)
    # abc_values = list(map(float, lines[2].split(":")[1].split()))
    # angles_values = list(map(float, lines[3].split(":")[1].split()))
    site_values = lines[4]
    # print(site_values)
    atom_data_0 = lines[7:]
    # print(atom_data_0)

    # 解析 Sites 数据
    atom_data = []
    # for line in lines[5:]:
    #     if line.startswith("#"):
    #         continue
    #     values = line.split()
    #     atom_data.append({
    #         'SP': values[1],
    #         'a': float(values[2]),
    #         'b': float(values[3]),
    #         'c': float(values[4])
    #     })

    structure_data = {
        "Full Formula": full_formula,
        "Reduced Formula": reduced_formula,
        "abc": abc_values,
        "angles": angles_values,
        "sites": site_values,
        "atom_sites": atom_data_0
    }

    return structure_data


structures = df.structure
structure_0 = structures[0]
ids = df_id.entries
id_0 = ids[0]
print(id_0)
print(structure_0)
structure_parse0 = parse_structure_data(structure_0)
print(structure_parse0)


import os

import numpy as np
from pymatgen.core.structure import Lattice


def split_formula(full_formula):
    # 提取字母部分和数字部分
    element = ''.join(filter(str.isalpha, full_formula))
    count = ''.join(filter(str.isdigit, full_formula))

    # 将数字部分转换为整数，如果为空，则默认为1
    count = int(count) if count else 1

    return element, count


def write_poscar(structure_data, output_folder, entry):
    # 提取结构信息
    full_formula = structure_data["Full Formula"]
    element, count = split_formula(full_formula)
    abc_values = [float(value) for value in structure_data["abc"].split()]
    angles_values = [float(value) for value in structure_data["angles"].split()]
    lattice = Lattice.from_parameters(a=abc_values[0], b=abc_values[1], c=abc_values[2],
                                      alpha=angles_values[0], beta=angles_values[1], gamma=angles_values[2])

    # # 计算晶格参数
    # a_vector, b_vector, c_vector = calculate_lattice_vectors(*abc_values, *angles_values)

    # 写入 POSCAR 文件
    poscar_content = f"""{full_formula}
1.0
{lattice:.16f}
{element}
{count}
direct
"""

    # 提取原子坐标信息
    site_lines = structure_data["atom_sites"]
    for line in site_lines:
        elements = line.split()
        print(elements)
        element, x, y, z = elements[1:6]  # 提取正确的索引
        print(x)
        poscar_content += f"   {float(x):.16f}    {float(y):.16f}    {float(z):.16f} {element}\n"

    # 将内容写入文件
    poscar_file_path = os.path.join(output_folder, f"{entry}_POSCAR")
    with open(poscar_file_path, "w") as poscar_file:
        poscar_file.write(poscar_content)


output_folder_path = "exa_1"
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

write_poscar(structure_parse0, output_folder_path, id_0)

for i in range(904):
    print("i==", i)
    id_i = ids[i]
    print("id==", id_i)
    structure_i = structures[i]
    # print("structure_i==", structure_i)
    structure_parsei = parse_structure_data(structure_i)
    # print("structure_parsei==", structure_parsei)
    write_poscar(structure_parsei, output_folder_path, id_i)

# for i in ids:
#     print(i)
# with open('crystals-11-00783-s001/crystals-1261160-supplementary.json', 'r') as f:
#     data = json.load(f)
#
#
# structure_strs = []
# entries = []
# for entry_id, entry_data in data.items():
#     # 获取结构信息
#     structure_str = entry_data["structure"]
#     write_poscar(structure_str, output_folder_path, entry_id)


# for structure in structures:
#     structure_parse = parse_structure_data(structure)
#     write_poscar(structure_parse, output_folder_path)
