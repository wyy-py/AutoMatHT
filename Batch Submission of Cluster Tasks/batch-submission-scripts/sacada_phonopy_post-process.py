import os
import numpy as np
import shutil
import subprocess
import pandas as pd


###########################
#  辅助函数定义部分
###########################

def read_poscar(filename="POSCAR"):
    """读取POSCAR文件，返回晶格矩阵（3×3 numpy数组）"""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lattice_vectors = []
    for i in range(2, 5):  # 读取第3~5行的晶格矩阵
        lattice_vectors.append(list(map(float, lines[i].split())))
    return np.array(lattice_vectors)


def get_supercell_factor(poscar="POSCAR", sposcar="SPOSCAR"):
    """
    通过比较POSCAR和SPOSCAR的晶格矩阵，
    自动计算扩胞因子列表 [f1, f2, f3]（四舍五入取整数）。
    """
    L = read_poscar(poscar)
    L_super = read_poscar(sposcar)
    factors = []
    for i in range(3):
        norm_orig = np.linalg.norm(L[i])
        norm_super = np.linalg.norm(L_super[i])
        if norm_orig < 1e-8:
            factor = None
        else:
            factor = int(round(norm_super / norm_orig))
        factors.append(factor)
    return factors


def read_num_atoms(poscar="POSCAR"):
    """
    读取POSCAR文件中原子总数。
    假设第6或第7行包含各元素原子数（以空格分隔）。
    """
    with open(poscar, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    try:
        counts = list(map(int, lines[5].split()))
    except Exception:
        counts = list(map(int, lines[6].split()))
    return sum(counts)


def update_band_conf(dim_factors, conf_file="band.conf", output_file=None):
    """
    读取band.conf文件，替换DIM后面的数值为dim_factors中给出的扩胞因子，
    并写回文件（如果output_file为None，则覆盖原文件）。
    """
    if output_file is None:
        output_file = conf_file
    # 读取原始文件内容
    with open(conf_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.strip().startswith("DIM="):
            # 重新构造 DIM 行，新行格式：DIM= f1 f2 f3\n
            new_line = "DIM= " + " ".join(str(f) for f in dim_factors) + "\n"
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    # 写回文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Updated {conf_file} with DIM= {' '.join(str(f) for f in dim_factors)}")


def update_mesh_conf(mesh_conf_path, dim_factors, mp_params):
    """
    读取mesh.conf文件，替换或插入 DIM= 和 MP= 行：
      - 替换DIM= 行为 "DIM= f1 f2 f3"
      - 替换或插入MP= 行为 "MP= p1 p2 p3"
    """
    with open(mesh_conf_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    mp_line_found = False
    for line in lines:
        if line.strip().startswith("DIM="):
            new_line = "DIM= " + " ".join(str(x) for x in dim_factors) + "\n"
            new_lines.append(new_line)
        elif line.strip().startswith("MP="):
            new_line = "MP= " + " ".join(str(x) for x in mp_params) + "\n"
            new_lines.append(new_line)
            mp_line_found = True
        else:
            new_lines.append(line)

    if not mp_line_found:
        for i, line in enumerate(new_lines):
            if line.strip().startswith("ATOM_NAME"):
                new_lines.insert(i + 1, "MP= " + " ".join(str(x) for x in mp_params) + "\n")
                break

    with open(mesh_conf_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(
        f"Updated {mesh_conf_path} with DIM= {' '.join(str(x) for x in dim_factors)} and MP= {' '.join(str(x) for x in mp_params)}")


def run_command(cmd, shell=True, env=None):
    """
    执行命令，捕获异常；若命令出错则打印错误信息，但继续执行后续命令。
    env: 可选的环境变量字典，将传递给 subprocess.run。
    """
    print("Running command:", cmd)
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Stderr:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Command failed:", e.cmd)
        print("Return code:", e.returncode)
        print("Output:", e.output)
        print("Error:", e.stderr)
        # 不抛出异常，继续执行后续命令


def run_phonopy_calculations():
    """
    按顺序执行 Phonopy 的命令：
      1. phonopy -f run-*/vasprun.xml
      2. phonopy --factor=521.471 --full-fc --writefc -p -s band.conf
      3. phonopy-bandplot --gnuplot >|band.dat
      4. phonopy -p -s mesh.conf   (计算声子态密度，不弹图)
      5. phonopy -t -p mesh.conf   (生成热学性质结果，不弹图，只保存文件)
    针对第5条命令，设置环境变量 MPLBACKEND=Agg 以避免图像弹出，并加上 --save 参数（如果 phonopy 支持）。
    """
    run_command("phonopy -f run-*/vasprun.xml")
    run_command("phonopy --factor=521.471 --full-fc --writefc -p -s band.conf")
    run_command("phonopy-bandplot --gnuplot >|band.dat")
    run_command("phonopy -p -s mesh.conf")

    # 设置环境变量，避免 matplotlib 弹出图像
    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"
    # 如果 phonopy 支持 --save 选项，则如下命令直接保存图像文件（否则可只设置 MPLBACKEND 变量）
    run_command("phonopy -t -p mesh.conf --save", env=env)
    print("Phonopy calculations finished.")

