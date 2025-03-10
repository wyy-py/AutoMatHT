import pandas as pd
import os
import shutil
import subprocess
import csv

# 读取CSV文件
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
            if lines and "reached required accuracy - stopping structural energy minimisation" in lines[-1]:
                return True
    return False


for sacada_id in sacada_ids:
    sacada_3d_folder_path = os.path.join(sacada_path, str(sacada_id))
    sacada_2d_folder_path = os.path.join(sacada_path, "2d_structure", str(sacada_id))

    sacada_3d_cal_path = os.path.join(sacada_3d_folder_path, 'thermal-calc')
    sacada_2d_cal_path = os.path.join(sacada_2d_folder_path, 'thermal-calc-2d')

    # 构建 thermal/opt 文件夹路径
    sacada_3d_orig_folder_path = os.path.join(sacada_3d_cal_path, 'opt')
    sacada_2d_orig_folder_path = os.path.join(sacada_2d_cal_path, 'opt')

    sacada_3d_target_folder_path = os.path.join(sacada_3d_cal_path, 'scf')
    sacada_2d_target_folder_path = os.path.join(sacada_2d_cal_path, 'scf')

    try:
        if os.path.exists(sacada_3d_folder_path):
            sacada_3d_source_CONTCAR_path = os.path.join(sacada_3d_orig_folder_path, 'CONTCAR')
            sacada_3d_target_POSCAR_path = os.path.join(sacada_3d_target_folder_path, 'POSCAR')
            sacada_3d_log_path = os.path.join(sacada_3d_orig_folder_path, 'LOG.vasp')
            shutil.copy(pbs_path_3d, sacada_3d_target_folder_path)

            if os.path.exists(sacada_3d_log_path):
                if check_log_file(sacada_3d_log_path):
                    if os.path.exists(sacada_3d_source_CONTCAR_path):
                        shutil.copy(sacada_3d_source_CONTCAR_path, sacada_3d_target_POSCAR_path)
                    else:
                        with open(sacada_opt_result_path, 'a') as f:
                            f.write(f"not exist CONTCAR file: {sacada_id}\n")
                        continue  # Skip to the next sacada_id

                    os.chdir(sacada_3d_target_folder_path)

                    subprocess.run(['vaspkit', '-task', '102', '-kpr', '0.025'])
                    subprocess.run(['qsub', 'AutoSubmit.pbs'])
                    os.chdir('../../../../')
                else:
                    with open(sacada_opt_result_path, 'a') as f:
                        f.write(f"not reached required accuracy: {sacada_id}\n")
                        # subprocess.run(['mv', 'sacada_3d_target_folder_path', ''])
                    continue  # Skip to the next sacada_id
            else:
                with open(sacada_opt_result_path, 'a') as f:
                    f.write(f"log file not found: {sacada_id}\n")
                continue  # Skip to the next sacada_id

        elif os.path.exists(sacada_2d_folder_path):
            sacada_2d_source_CONTCAR_path = os.path.join(sacada_2d_orig_folder_path, 'CONTCAR')
            sacada_2d_target_POSCAR_path = os.path.join(sacada_2d_target_folder_path, 'POSCAR')
            sacada_2d_log_path = os.path.join(sacada_2d_orig_folder_path, 'LOG.vasp')
            shutil.copy(pbs_path_2d, sacada_2d_target_folder_path)

            if os.path.exists(sacada_2d_log_path):
                if check_log_file(sacada_2d_log_path):
                    if os.path.exists(sacada_2d_source_CONTCAR_path):
                        shutil.copy(sacada_2d_source_CONTCAR_path, sacada_2d_target_POSCAR_path)
                    else:
                        with open(sacada_opt_result_path, 'a') as f:
                            f.write(f"not exist CONTCAR file: {sacada_id}\n")
                        continue  # Skip to the next sacada_id

                    os.chdir(sacada_2d_target_folder_path)
                    subprocess.run(['vaspkit', '-task', '102', '-kpr', '0.025'])
                    subprocess.run(['qsub', 'AutoSubmit.pbs'])
                    os.chdir('../../../../../')
                else:
                    with open(sacada_opt_result_path, 'a') as f:
                        f.write(f"not reached required accuracy: {sacada_id}\n")
                        #
                    continue  # Skip to the next sacada_id
            else:
                with open(sacada_opt_result_path, 'a') as f:
                    f.write(f"log file not found: {sacada_id}\n")
                continue  # Skip to the next sacada_id

        else:
            with open(sacada_opt_result_path, 'a') as f:
                f.write(f"not exist folder: {sacada_id}\n")

    except Exception as e:
        with open(sacada_opt_result_path, 'a') as f:
            f.write(f"error processing {sacada_id}: {e}\n")

