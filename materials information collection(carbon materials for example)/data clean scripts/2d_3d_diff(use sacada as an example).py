import os
import shutil
import subprocess

import numpy as np
import pandas as pd
from pymatgen.core import Structure
from pymatgen.io.vasp import Poscar


def get_max3_from_POSCAR(poscar_file):
    '''
    :param poscar_file: for example--
    2.5653212943138017    0.0000000000000000    0.0000000000000000
    -1.2826606471569009    2.2216331056125935    0.0000000000000000
     0.0000000000000000    0.0000000000000000   20.0000000000000000
    :return: 20.0000000000000000
    '''
    with open(poscar_file, 'r') as f:
        poscar_content = f.read()
        # 提取目标行
        lines = poscar_content.split('\n')
        line1 = lines[2]
        line2 = lines[3]
        line3 = lines[4]  # 一直到第8行开始是direct后面的坐标了

        # 将提取的信息分配给变量
        var1 = [float(coord) for coord in line1.split()]
        var2 = [float(coord) for coord in line2.split()]
        var3 = [float(coord) for coord in line3.split()]

        # 输出变量的值
        print("Variable 1:", var1)
        print("Variable 2:", var2)
        print("Variable 3:", var3)

        # max([abs(num) for num in numbers])

        print(max(var3))

        max_c = max([abs(num) for num in var3])

        # 计算每一行中0.0000000000000000的出现次数
        # count_zero_line3 = var1.count(0.0)
        # count_zero_line4 = var2.count(0.0)
        # count_zero_line5 = var3.count(0.0)

        # 计算第三行最大值
        return max_c

        #if count_zero_line3 == 2 or count_zero_line4 == 2 or count_zero_line5 == 2:
        # if (count_zero_line5 == 2 and max(var3) > 10) or (count_zero_line4 == 2 and max(var2) > 10) \
        #         or (count_zero_line3 == 2 and max(var1) > 10):
        #     return "二维材料"
        # else:
        #     return "三维材料"

# order file construction : ids + folder name
sacada_order = pd.read_excel('data_all/data_order/SACADA_order.xlsx')  # oqmd_name

sacada_path = "data_all/SACADA-poscar"  # F:\learning materials\data_all\SACADA-poscar

sacada_frac_coords = []

sacada_Vacuum_list = []

sacada_list = sacada_order.id


for i in sacada_list:
    sacada_folder_path = os.path.join(sacada_path, str(i))
    sacada_poscar_path = os.path.join(sacada_folder_path, "CONVCELL.vasp")  # POSCAR对应了原胞;CONVCELL.vasp对应惯胞
    sacada_poscar = Poscar.from_file(sacada_poscar_path)
    sacada_s = sacada_poscar.structure
    sacada_frac_coordinates = sacada_s.frac_coords
    sacada_Vacuum = get_max3_from_POSCAR(sacada_poscar_path)
    sacada_frac_coords.append(sacada_frac_coordinates)
    sacada_Vacuum_list.append(sacada_Vacuum)


sacada_max_coords = []
sacada_min_coords = []
sacada_eff_thickness = []
sacada_maxmin_coords = []


for sacada_frac_coord in sacada_frac_coords:
    # print("frac_coord=", sacada_frac_coord)
    sacada_max_coord = np.max(sacada_frac_coord, axis=0)
    # print("max_coord=:", sacada_max_coord)
    sacada_min_coord = np.min(sacada_frac_coord, axis=0)
    # print("min_coord=:", sacada_min_coord)
    sacada_maxmin_coord = sacada_max_coord[2] - sacada_min_coord[2]  # 对应着z的最大值减去最小值
    sacada_max_coords.append(sacada_max_coord[2])
    sacada_min_coords.append(sacada_min_coord[2])
    sacada_maxmin_coords.append(sacada_maxmin_coord)

print(sacada_max_coords[1100:1105])
print(len(sacada_max_coords))
print(sacada_min_coords[1100:1105])
print(len(sacada_min_coords))
print(sacada_maxmin_coords[1100:1105])
print(len(sacada_maxmin_coords))


sacada_eff_thickness = []

for i in range(1168):
    sacada_folder_name_i = sacada_list[i]
    sacada_maxmin_coord_i = sacada_maxmin_coords[i]
    sacada_Vacuum_i = sacada_Vacuum_list[i]
    sacada_eff_thick = sacada_maxmin_coord_i * sacada_Vacuum_i
    sacada_eff_thickness.append(sacada_eff_thick)

print(len(sacada_list))
print(len(sacada_maxmin_coords))
print(len(sacada_Vacuum_list))
print(len(sacada_eff_thickness))

data_eff = {"folder_name": sacada_list, "maxmin_coords": sacada_maxmin_coords,
            "Vacuum_layer": sacada_Vacuum_list, "eff_thickness": sacada_eff_thickness}
eff_df = pd.DataFrame(data_eff)
eff_df.to_csv("data_effective_thickness/sacada_eff_thickness_conv.csv", index=False)


