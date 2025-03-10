import pandas as pd
import os
import shutil
import subprocess
# 自动识别错误并重新提交
# Identifying two different types of errors generated in the folders of individual materials 
# during batch structural optimization calculations
# I. forrtl: severe (168): Program Exception - illegal instruction
# II. ZBRENT: fatal error in bracketing
# 读取Excel文件
excel_file_path = "/public/home/$username/C/data_order/SACADA_order.xlsx"
sacada_order = pd.read_excel(excel_file_path)
sacada_ids = sacada_order.id
sacada_path = "/public/home/$username/C/SACADA-poscar-1"

calc_path_3d = "/public/home/$username/C/calc-standard-pbs"
calc_path_2d = "/public/home/$username/C/2d-calc-standard-pbs"

pbs_path_3d = "/public/home/$username/C/calc-standard-pbs/AutoSubmit.pbs"
pbs_path_2d = "/public/home/$username/C/2d-calc-standard-pbs/AutoSubmit.pbs"

sacada_opt_result_path = os.path.join(sacada_path, "error_file.txt")


def check_log_file(log_file_path):
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if "forrtl: severe (168): Program Exception - illegal instruction" in line:
                    return "illegal instruction"
                elif "ZBRENT: fatal error in bracketing" in line:
                    return "bracketing error"
                else:
                     pass
    return None


for sacada_id in sacada_ids:
    sacada_3d_folder_path = os.path.join(sacada_path, str(sacada_id))
    sacada_2d_folder_path = os.path.join(sacada_path, "2d_structure", str(sacada_id))

    sacada_3d_cal_path = os.path.join(sacada_3d_folder_path, 'thermal-calc')
    sacada_2d_cal_path = os.path.join(sacada_2d_folder_path, 'thermal-calc-2d')

    sacada_3d_target_folder_path = os.path.join(sacada_3d_folder_path, 'thermal-calc', 'opt')
    sacada_2d_target_folder_path = os.path.join(sacada_2d_folder_path, 'thermal-calc-2d', 'opt')

    sacada_3d_log_path = os.path.join(sacada_3d_target_folder_path, 'LOG.vasp')
    sacada_2d_log_path = os.path.join(sacada_2d_target_folder_path, 'LOG.vasp')

    if os.path.exists(sacada_3d_folder_path):
        sacada_source_poscar_path = os.path.join(sacada_3d_folder_path, 'POSCAR')
        sacada_source_contcar_path = os.path.join(sacada_3d_folder_path, 'CONTCAR')
        sacada_target_poscar_path = os.path.join(sacada_3d_target_folder_path, 'POSCAR')
        error_type = check_log_file(sacada_3d_log_path)
        if error_type == "illegal instruction":
            shutil.copy(sacada_source_poscar_path, sacada_target_poscar_path)
            os.chdir(sacada_3d_target_folder_path)
            subprocess.run(['qsub', 'AutoSubmit.pbs'])
            os.chdir('../../../../')
        elif error_type == "bracketing error":
            with open(sacada_opt_result_path, 'a') as f:
                shutil.copy(sacada_source_poscar_path, sacada_target_poscar_path)
                os.chdir(sacada_3d_target_folder_path)
                subprocess.run(['qsub', 'AutoSubmit.pbs'])
                os.chdir('../../../../')
                f.write(f"bracketing error: {sacada_id}\n")
    elif os.path.exists(sacada_2d_folder_path):
        sacada_source_poscar_path = os.path.join(sacada_2d_folder_path, 'POSCAR')
        sacada_target_poscar_path = os.path.join(sacada_2d_target_folder_path, 'POSCAR')
        sacada_source_contcar_path = os.path.join(sacada_2d_folder_path, 'CONTCAR')
        error_type = check_log_file(sacada_2d_log_path)
        if error_type == "illegal instruction":
            shutil.copy(sacada_source_poscar_path, sacada_target_poscar_path)
            os.chdir(sacada_2d_target_folder_path)
            subprocess.run(['qsub', 'AutoSubmit.pbs'])
            os.chdir('../../../../../')
        elif error_type == "bracketing error":
            with open(sacada_opt_result_path, 'a') as f:
                shutil.copy(sacada_source_poscar_path, sacada_target_poscar_path)
                os.chdir(sacada_2d_target_folder_path)
                subprocess.run(['qsub', 'AutoSubmit.pbs'])
                os.chdir('../../../../../')
                f.write(f"bracketing error: {sacada_id}\n")
    else:
        print(f"successful run folder_path:{sacada_id}")
        pass

