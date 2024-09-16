import os
import json
import pandas as pd
import numpy as np
import ase.io
from pymatgen.core.structure import Structure
from pymatgen.io.ase import AseAtomsAdaptor


# 加载json文件
with open('crystals-1261160-supplementary.json', 'r') as f:
    data = json.load(f)

# 转换为DataFrame
df = pd.DataFrame.from_dict(data, orient='index')
ref_id_df = pd.DataFrame(df.index)
# # 重命名索引列为'id'
# df.index.name = 'id'

# 显示DataFrame
print(df)
print(df.columns)
print("structure==", df.structure)
# df.to_csv("F:/learning materials/data_all/reference/crystals_1.csv", index=False)
# ref_id_df.to_csv("F:/learning materials/data_all/data_order/ref_id_df.csv", index=False)


for structure in df.structure:
    print(str(structure))
    # print(structure)


def parse_structure_data(structure_str):
    # 将字符串解析为包含结构信息的字典
    lines = structure_str.strip().split('\n')
    full_formula = lines[0].replace("Full Formula (", "").replace(")", "")
    print(full_formula)
    reduced_formula = lines[1].split(":")[1].strip()
    print(reduced_formula)
    abc_values = list(map(float, lines[2].split(":")[1].split()))
    angles_values = list(map(float, lines[3].split(":")[1].split()))

    # 解析 Sites 数据
    atom_data = []
    for line in lines[5:]:
        if line.startswith("#"):
            continue
        values = line.split()
        atom_data.append({
            'SP': values[1],
            'a': float(values[2]),
            'b': float(values[3]),
            'c': float(values[4])
        })

    structure_data = {
        "Full Formula": full_formula,
        "Reduced Formula": reduced_formula,
        "abc": abc_values,
        "angles": angles_values,
        "Sites": atom_data
    }

    return structure_data

structures = df.structure
structure_0 = structures[0]
ids = df.index
id_0 = ids[0]
print("id_0=:", id_0)
print("structure_0=:", structure_0)
structure_parse0 = parse_structure_data(structure_0)
print("structure_parse0=", structure_parse0)
