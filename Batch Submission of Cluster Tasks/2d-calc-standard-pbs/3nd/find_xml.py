import os

def check_vasprun(folder_path):
    vasprun_path = os.path.join(folder_path, 'vasprun.xml')
    print(vasprun_path)
    return os.path.isfile(vasprun_path)

def main():
    base_folder = '/home/whd/ettest/C/mp-66/third'  # 替换为你实际的基础文件夹路径

    for i in range(1, 72):  # 需要改数量
        folder_name = f'run-{i:02d}'
        folder_path = os.path.join(base_folder, folder_name)

        if check_vasprun(folder_path):
            print(f"find sucessfully")
        else:
            print(f"vasprun.xml not found in {folder_name}")

if __name__ == "__main__":
    main()
