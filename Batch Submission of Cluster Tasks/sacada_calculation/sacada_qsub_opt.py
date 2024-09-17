import pandas as pd
import os
import shutil
import subprocess
import csv

# 读取CSV文件
excel_file_path = "/public/home/$username/C/data_order/SACADA_order.xlsx"

sacada_order = pd.read_excel(excel_file_path)  # sacada_ids
sacada_ids = sacada_order.id
sacada_path = "/public/home/$username/C/SACADA-poscar-1"

calc_path_3d = "/public/home/$username/C/calc-standard-pbs"
calc_path_2d = "/public/home/$username/C/2d-calc-standard-pbs"

pbs_path_3d = "/public/home/$username/C/calc-standard-pbs/AutoSubmit.pbs"
pbs_path_2d = "/public/home/$username/C/2d-calc-standard-pbs/AutoSubmit.pbs"

for sacada_id in sacada_ids:
    sacada_3d_folder_path = os.path.join(sacada_path, str(sacada_id))
    sacada_2d_folder_path = os.path.join(sacada_path, "2d_structure", str(sacada_id))

    sacada_3d_cal_path = os.path.join(sacada_3d_folder_path, 'thermal-calc')
    sacada_2d_cal_path = os.path.join(sacada_2d_folder_path, 'thermal-calc-2d')

    # 构建 thermal/opt 文件夹路径
    sacada_3d_target_folder_path = os.path.join(sacada_3d_folder_path, 'thermal-calc', 'opt')
    sacada_2d_target_folder_path = os.path.join(sacada_2d_folder_path, 'thermal-calc-2d', 'opt')

    # 检查源文件夹和目标文件夹是否存在
    if os.path.exists(sacada_3d_folder_path):
        if os.path.exists(sacada_3d_cal_path):
            shutil.rmtree(sacada_3d_cal_path)
        shutil.copytree(calc_path_3d, sacada_3d_cal_path)  # 复制计算示例文件夹

        sacada_source_poscar_path = os.path.join(sacada_3d_folder_path, 'CONVCELL.vasp')
        sacada_target_poscar_path = os.path.join(sacada_3d_target_folder_path, 'POSCAR')
        shutil.copy(sacada_source_poscar_path, sacada_target_poscar_path)
        shutil.copy(pbs_path_3d, sacada_3d_target_folder_path)

        os.chdir(sacada_3d_target_folder_path)
        # subprocess.run(['bash', 'GeneratePBS.sh'])
        subprocess.run(['vaspkit', '-task', '102', '-kpr', '0.025'])
        subprocess.run(['qsub', 'AutoSubmit.pbs'])
        os.chdir('../../../../')

    elif os.path.exists(sacada_2d_cal_path):
        shutil.rmtree(sacada_2d_cal_path)
        shutil.copytree(calc_path_2d, sacada_2d_cal_path)  # 复制计算示例文件夹
        sacada_source_poscar_path = os.path.join(sacada_2d_folder_path, 'CONVCELL.vasp')
        sacada_target_poscar_path = os.path.join(sacada_2d_target_folder_path, 'POSCAR')
        shutil.copy(sacada_source_poscar_path, sacada_target_poscar_path)
        shutil.copy(pbs_path_2d, sacada_2d_target_folder_path)

        os.chdir(sacada_2d_target_folder_path)
        # subprocess.run(['bash', 'GeneratePBS.sh'])
        subprocess.run(['vaspkit', '-task', '102', '-kpr', '0.025'])
        subprocess.run(['qsub', 'AutoSubmit.pbs'])
        os.chdir('../../../../../')
    else:
        print(f"can not find folder_path:{sacada_id}")
        pass
