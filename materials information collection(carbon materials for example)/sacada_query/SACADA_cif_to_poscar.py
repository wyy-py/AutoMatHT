import os
import pandas as pd
from pymatgen.io.cif import CifParser


def cif_to_structure(cif_file):
    # 使用CifParser读取cif文件
    parser = CifParser(cif_file)
    structure = parser.get_structures()[0]
    return structure


SACADA_folder_path = 'SACADA-structure-unzip'
SACADA_folder_path_new = 'SACADA-poscar'

df_order = pd.read_excel("SACADA_order.xlsx")  # recollected the information, delete all the unstable structures in SACADA
print(df_order)
# id  subdir    cif_name
sacada_ids = df_order.id
print(len(sacada_ids))
sacada_subdirs = df_order.subdir
sacada_cif_names = df_order.cif_name

for i in range(len(sacada_ids)):  
    sacada_cif_path = os.path.join(SACADA_folder_path, str(sacada_ids[i]),
                                   str(sacada_subdirs[i]))

    if os.path.exists(sacada_cif_path) and os.path.isdir(sacada_cif_path):
        for file_name in os.listdir(sacada_cif_path):
            if file_name.endswith(".cif") and not file_name.endswith("_IN.cif"):
                # cif_file_path = os.path.join(sacada_cif_path, file_name)
                # poscar_file_path = os.path.join(sacada_cif_path, "POSCAR")
                print(sacada_cif_path)
                cif_file_path = os.path.join(sacada_cif_path, file_name)
                parser = CifParser(cif_file_path)
                structure_cif = parser.get_structures()[0]  # default: primitive = True
                structure_conv = parser.get_structures(primitive=False)[0]

                sacada_poscar_path = os.path.join(SACADA_folder_path_new, str(sacada_ids[i]))
                if not os.path.exists(sacada_poscar_path):
                    os.makedirs(sacada_poscar_path)
                try:
                    structure_cif.to(fmt='POSCAR', filename=os.path.join(sacada_poscar_path, 'POSCAR'))  # PRIMITIVE_CELL
                    structure_conv.to(fmt='POSCAR', filename=os.path.join(sacada_poscar_path, 'CONVCELL.vasp'))  # CONVCELL_CELL
                    print("Successfully converted to POSCAR:", sacada_cif_path)
                except ValueError as e:
                    print(f"Error converting {sacada_cif_path} to POSCAR: {e}")
    # print(sacada_cif_path)
    # parser = CifParser(sacada_cif_path)
    # structure_cif = parser.get_structures()[0]  # default: primitive = True
    # structure_conv = parser.get_structures(primitive=False)[0]
    # sacada_poscar_path = os.path.join(SACADA_folder_path_new, str(sacada_ids[i]),
    #                                   str(sacada_subdirs[i]))
    # if not os.path.exists(sacada_poscar_path):
    #     os.makedirs(sacada_poscar_path)
    # try:
    #     structure_cif.to(fmt='POSCAR', filename=os.path.join(sacada_poscar_path, 'POSCAR'))
    #     structure_conv.to(fmt='POSCAR', filename=os.path.join(sacada_poscar_path, 'CONVCELL.vasp'))
    #     print("Successfully converted to POSCAR:", sacada_cif_path)
    # except ValueError as e:
    #     print(f"Error converting {sacada_cif_path} to POSCAR: {e}")
    # 'pymatgen_structure_mp24.vasp'
