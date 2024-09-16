import os

import pandas as pd
from pymatgen.io.vasp import Poscar
from pymatgen.core.structure import Structure

ref_path = "reference_new"
ref_order = pd.read_csv('ref_id_df.csv')
# entry_poscar_name
# F:\learning materials\data_all\reference\reference_new
# with open(POSCAR_file_path, 'r') as f:
#     poscar_content = f.read()
ref_list = ref_order['entries']
ref_conv_list = []
ref_pri_list = []

for i in ref_list:
    print("entries=:", i)
    ref_folder_path = os.path.join(ref_path, str(i))
    ref_poscar_path = os.path.join(ref_folder_path, "POSCAR")
    ref_poscar = Poscar.from_file(ref_poscar_path)
    ref_s_conv = ref_poscar.structure
    print("ref_s_conv=:", ref_s_conv)

    ref_conv_list.append(ref_s_conv)
    ref_s_pri = ref_s_conv.get_primitive_structure()
    print("ref_s_pri=:", ref_s_pri)

    ref_pri_list.append(ref_s_pri)

ref_stru_df = {"ref_conv_list": ref_conv_list, "ref_pri_list": ref_pri_list}
ref_stru_pd = pd.DataFrame(ref_stru_df)
ref_stru_pd.to_csv("structure.csv", index=False)

