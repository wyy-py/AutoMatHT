import glob
import os
import shutil
import subprocess

import numpy as np
import pandas as pd

# 读取CSV文件
excel_file_path = "materials information collection(carbon materials for example)/reference_query/ref_order_1.xlsx"

ref_order = pd.read_excel(excel_file_path)
ref_ids = ref_order.entry_name
ref_path = "/public/home/${User}/C/reference_new"
ref_path_incar = "Batch Submission of Cluster Tasks/calc-standard-pbs/phonopy/INCAR"
command_path_3d = "Batch Submission of Cluster Tasks/calc-standard-pbs/phonopy/command"
command_path_2d = "Batch Submission of Cluster Tasks/calc-standard-pbs/phonopy/command"

shell_script_path = "/public/home/weiyi22/C/SACADA-poscar-1/1/thermal-calc/phonopy/Loop-phonopy.sh"
submit_path = "Batch Submission of Cluster Tasks/calc-standard-pbs/phonopy/AutoSubmit.pbs"
ref_opt_result_path = os.path.join(ref_path, "error_file_opt.txt")


def read_poscar(filename="POSCAR"):
    """读取POSCAR文件，返回晶格矩阵和维度"""
    with open(filename, 'r') as f:
        lines = f.readlines()
        lattice_vectors = []
        for i in range(2, 5):  # 读取POSCAR中的3x3晶格矩阵
            lattice_vectors.append(list(map(float, lines[i].split())))
        return np.array(lattice_vectors)


def get_supercell_factors(lattice_vectors):
    """根据晶格常数，返回扩胞倍数"""
    scaling_factors = []
    for i in range(3):  # 遍历晶格的x、y、z方向
        length = np.linalg.norm(lattice_vectors[i])
        rounded_length = round(length)

        if rounded_length < 3.5:
            scaling_factors.append(3)
        elif 3.5 <= rounded_length < 7:
            scaling_factors.append(2)
        else:
            scaling_factors.append(1)

    return scaling_factors


def run_phonopy(scaling_factors):
    """根据扩胞倍数调用phonopy命令"""
    dim_string = f"{scaling_factors[0]} {scaling_factors[1]} {scaling_factors[2]}"
    command = f"phonopy -d --dim='{dim_string}'"
    os.system(command)


# 执行命令的函数
def run_command(shell_script, pbs_file):
    # 执行命令 './Loop-phonopy.sh $(pwd)/AutoSubmit.pbs'
    command = f"{shell_script} {pbs_file}"
    try:
        # 执行命令
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully executed: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute: {command}, error: {e}")


def grant_execute_permission(file_path):
    # 给文件赋予执行权限 (chmod +x)
    os.chmod(file_path, 0o755)


def main():
    # 示例运行代码
    # poscar_file = "POSCAR"
    # lattice_vectors = read_poscar(poscar_file)
    # scaling_factors = get_supercell_factors(lattice_vectors)
    # print(f"扩胞因子: {scaling_factors}")
    # run_phonopy(scaling_factors)

    for ref_id in ref_ids:  # ref_ids
        ref_3d_folder_path = os.path.join(ref_path, str(ref_id))
        ref_2d_folder_path = os.path.join(ref_path, "2d_structure", str(ref_id))

        ref_3d_cal_path = os.path.join(ref_3d_folder_path, 'thermal-calc')
        ref_2d_cal_path = os.path.join(ref_2d_folder_path, 'thermal-calc-2d')

        # 构建 thermal/opt 文件夹路径
        ref_3d_orig_folder_path = os.path.join(ref_3d_cal_path, 'opt')
        ref_2d_orig_folder_path = os.path.join(ref_2d_cal_path, 'opt')

        ref_3d_target_folder_path = os.path.join(ref_3d_cal_path, 'phonopy')
        ref_2d_target_folder_path = os.path.join(ref_2d_cal_path, 'phonopy')

        try:
            if os.path.exists(ref_3d_folder_path):
                ref_3d_source_CONTCAR_path = os.path.join(ref_3d_orig_folder_path, 'CONTCAR')
                ref_3d_target_POSCAR_path = os.path.join(ref_3d_target_folder_path, 'POSCAR')

                if os.path.exists(ref_3d_source_CONTCAR_path):
                    # shutil.rmtree(ref_3d_target_folder_path)
                    # 删除run-*文件夹
                    run_folders = glob.glob(os.path.join(ref_3d_target_folder_path, 'run-*'))
                    for folder in run_folders:
                        shutil.rmtree(folder)
                        print(f"Deleted folder: {folder}")
                    os.chdir(ref_3d_target_folder_path)
                    shutil.copy(command_path_3d, ref_3d_target_folder_path)
                    # shutil.copy(pbs_path_3d, ref_3d_target_folder_path)
                    shutil.copy(ref_3d_source_CONTCAR_path, ref_3d_target_POSCAR_path)
                    file_path = "KPOINTS"
                    file_path_1 = "POTCAR"

                    # 检查文件是否存在并删除
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"{file_path} has been deleted.")
                    else:
                        print(f"{file_path} does not exist.")

                    if os.path.exists(file_path_1):
                        os.remove(file_path_1)
                        print(f"{file_path_1} has been deleted.")
                    else:
                        print(f"{file_path_1} does not exist.")

                    poscar_file_3d = "POSCAR"
                    lattice_vectors_3d = read_poscar(poscar_file_3d)
                    scaling_factors_3d = get_supercell_factors(lattice_vectors_3d)
                    print(f"扩胞因子: {scaling_factors_3d}")
                    run_phonopy(scaling_factors_3d)

                    # 修改command参数，使得大概为10
                    shell_script_origin_target = "Loop-phonopy.sh"
                    shutil.copy(shell_script_path, shell_script_origin_target)

                    shell_script = "./Loop-phonopy.sh"  # Loop-phonopy.sh 文件路径
                    pbs_file = os.path.join(os.getcwd(), "AutoSubmit.pbs")
                    shutil.copy(submit_path, pbs_file)
                    print(f"Copied submit.pbs to {pbs_file}")
                    incar_target_path = "INCAR"
                    shutil.copy(ref_path_incar, incar_target_path)
                    print(f"Copied incar to {incar_target_path}")

                    subprocess.run(['vaspkit', '-task', '102', '-kpr', '0.1'])
                    grant_execute_permission(shell_script)
                    run_command(shell_script, pbs_file)
                    os.chdir('../../../')
                else:
                    with open(ref_opt_result_path, 'a') as f:
                        f.write(f"not reached required accuracy: {ref_id}\n")
                        # subprocess.run(['mv', 'ref_3d_target_folder_path', ''])
                        continue  # Skip to the next ref_id

            elif os.path.exists(ref_2d_folder_path):

                ref_2d_source_CONTCAR_path = os.path.join(ref_2d_orig_folder_path, 'CONTCAR')
                ref_2d_target_POSCAR_path = os.path.join(ref_2d_target_folder_path, 'POSCAR')

                if os.path.exists(ref_2d_source_CONTCAR_path):
                    # shutil.rmtree(ref_3d_target_folder_path)
                    # 删除run-*文件夹
                    run_folders = glob.glob(os.path.join(ref_2d_target_folder_path, 'run-*'))
                    for folder in run_folders:
                        shutil.rmtree(folder)
                        print(f"Deleted folder: {folder}")
                    os.chdir(ref_2d_target_folder_path)
                    shutil.copy(command_path_2d, ref_2d_target_folder_path)
                    # shutil.copy(pbs_path_2d, ref_2d_target_folder_path)
                    shutil.copy(ref_2d_source_CONTCAR_path, ref_2d_target_POSCAR_path)

                    os.chdir(ref_2d_target_folder_path)
                    file_path = "KPOINTS"
                    file_path_1 = "POTCAR"

                    # 检查文件是否存在并删除
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"{file_path} has been deleted.")
                    else:
                        print(f"{file_path} does not exist.")
                    if os.path.exists(file_path_1):
                        os.remove(file_path_1)
                        print(f"{file_path_1} has been deleted.")
                    else:
                        print(f"{file_path_1} does not exist.")

                    poscar_file_2d = "POSCAR"
                    lattice_vectors_2d = read_poscar(poscar_file_2d)
                    scaling_factors_2d = get_supercell_factors(lattice_vectors_2d)
                    print(f"扩胞因子: {scaling_factors_2d}")
                    run_phonopy(scaling_factors_2d)

                    # 修改command参数，使得大概为10
                    shell_script_origin_target = "Loop-phonopy.sh"
                    shutil.copy(shell_script_path, shell_script_origin_target)

                    shell_script = "./Loop-phonopy.sh"  # Loop-phonopy.sh 文件路径
                    pbs_file = os.path.join(os.getcwd(), "AutoSubmit.pbs")
                    shutil.copy(submit_path, pbs_file)
                    print(f"Copied submit.pbs to {pbs_file}")
                    incar_target_path = "INCAR"
                    shutil.copy(ref_path_incar, incar_target_path)
                    print(f"Copied incar to {incar_target_path}")
                    subprocess.run(['vaspkit', '-task', '102', '-kpr', '0.1'])
                    grant_execute_permission(shell_script)
                    run_command(shell_script, pbs_file)
                    os.chdir('../../../../../')
                else:
                    with open(ref_opt_result_path, 'a') as f:
                        f.write(f"not reached required accuracy: {ref_id}\n")
                        #
                    continue  # Skip to the next ref_id

            else:
                with open(ref_opt_result_path, 'a') as f:
                    f.write(f"not exist folder: {ref_id}\n")

        except Exception as e:
            with open(ref_opt_result_path, 'a') as f:
                f.write(f"error processing {ref_id}: {e}\n")


if __name__ == "__main__":
    main()
