import os
import pandas as pd
from pymatgen.io.cif import CifParser


aflow_folder_path = 'cif_files/aflow_cif_files'
aflow_folder_path_new = 'aflow-poscar'

df_order = pd.read_csv("aflow_json.csv")
print(df_order)
# id  subdir    cif_name
auid = df_order.auid
aflow_ids = auid.split(':')[-1]
print(len(aflow_ids))
# aflow_subdirs = df_order.subdir
# aflow_cif_names = df_order.cif_name

for i in range(0, 819):  # 563报错，但转换到586重启，可能586对应id为563.563文件夹对应i=546
    aflow_cif_path = os.path.join(aflow_folder_path, str(aflow_ids[i]))

    if os.path.exists(aflow_cif_path) and os.path.isdir(aflow_cif_path):
        for file_name in os.listdir(aflow_cif_path):
            if file_name.endswith(".cif"):
                print(aflow_cif_path)
                cif_file_path = os.path.join(aflow_cif_path, file_name)
                parser = CifParser(cif_file_path)
                structure_cif = parser.get_structures()[0]  # default: primitive = True
                structure_conv = parser.get_structures(primitive=False)[0]

                aflow_poscar_path = os.path.join(aflow_folder_path_new, str(aflow_ids[i]))
                if not os.path.exists(aflow_poscar_path):
                    os.makedirs(aflow_poscar_path)
                try:
                    structure_cif.to(fmt='POSCAR', filename=os.path.join(aflow_poscar_path, 'POSCAR'))  # PRIMITIVE_CELL
                    structure_conv.to(fmt='POSCAR', filename=os.path.join(aflow_poscar_path, 'CONVCELL.vasp'))  # CONVCELL_CELL
                    print("Successfully converted to POSCAR:", aflow_cif_path)
                except ValueError as e:
                    print(f"Error converting {aflow_cif_path} to POSCAR: {e}")
