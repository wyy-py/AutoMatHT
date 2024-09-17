import os
import shutil
import subprocess

import numpy as np
import pandas as pd

# 读取CSV文件
excel_file_path = "/public/home/weiyi22/C/data_order/SACADA_order.xlsx"

sacada_order = pd.read_excel(excel_file_path)
sacada_ids = sacada_order.id
sacada_path = "/public/home/weiyi22/C/SACADA-poscar-1"

calc_path_3d = "/public/home/weiyi22/C/calc-standard-pbs"
calc_path_2d = "/public/home/weiyi22/C/2d-calc-standard-pbs"

command_path_3d = "/public/home/weiyi22/C/SACADA-poscar-1/1/thermal-calc/phonopy/command"
command_path_2d = "/public/home/weiyi22/C/SACADA-poscar-1/2d_structure/2/thermal-calc-2d/phonopy/command"

sacada_opt_result_path = os.path.join(sacada_path, "error_file_opt.txt")


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
        elif 3.5 <= rounded_length < 6:
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
    poscar_file = "POSCAR"
    lattice_vectors = read_poscar(poscar_file)
    scaling_factors = get_supercell_factors(lattice_vectors)
    print(f"扩胞因子: {scaling_factors}")
    run_phonopy(scaling_factors)

    import os
    # 文件路径
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

    shell_script = "./Loop-phonopy.sh"  # Loop-phonopy.sh 文件路径
    pbs_file = os.path.join(os.getcwd(), "AutoSubmit.pbs")
    subprocess.run(['vaspkit', '-task', '102', '-kpr', '0.025'])
    grant_execute_permission(shell_script)
    run_command(shell_script, pbs_file)
    os.chdir('../../../../')


if __name__ == "__main__":
    main()
