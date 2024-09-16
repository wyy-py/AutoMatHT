#导入必要的库：
import os
import json
import numpy as np
import pandas as pd
from jarvis.core.atoms import Atoms
from jarvis.io.vasp.inputs import Poscar

# 加载json文件
f = open('jdft_3d-12-12-2022.json', 'r')  # figshare data: download from jarvis official website
data3d = json.load(f)
f.close()
df = pd.DataFrame(data3d)

# 创建一个目录来保存 POSCAR 文件
os.makedirs('C_entries', exist_ok=True)


def has_only_C(atoms_dict={}):
    atoms = Atoms.from_dict(atoms_dict)
    elements = atoms.elements
    return set(elements) == {'C'}


# 创建一个新列，用于标记仅包含Ci元素的条目：
df['only_C'] = df['atoms'].apply(lambda x: has_only_C(atoms_dict=x))

# 过滤出仅包含C元素的条目：
df_C = df[df['only_C']]
csv_filename = os.path.join('C_entries', f'carbon_jdft3d.csv')
df_C.to_csv(csv_filename, index=False)

# 保存仅包含C元素的条目为POSCAR文件：
for i, entry in df_C.iterrows():
    atoms = Atoms.from_dict(entry['atoms'])
    poscar = Poscar(atoms)
    jid = entry['jid']
    filename = os.path.join('C_entries', f'POSCAR-{jid}.vasp')
    poscar.write_file(filename)
