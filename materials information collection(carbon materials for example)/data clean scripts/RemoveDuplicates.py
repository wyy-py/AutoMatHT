#!/usr/bin/env python
# coding: utf-8
# 利用pymatgen的matches功能比较两个列表中的结构是否相似

from pymatgen.core import Structure
from pymatgen.symmetry import analyzer
import os 


def GetFileFromThisRootDir(dir,ext = None):
    allfiles = []
    needExtFilter = (ext != None)
    for root,dirs,files in os.walk(dir):
        for filespath in files:
            #filepath = os.path.join(root, filespath)
            filepath = os.path.join( filespath)
            extension = os.path.splitext(filepath)[1][1:]
            if needExtFilter and extension in ext:
                allfiles.append(filepath)
            elif not needExtFilter:
                allfiles.append(filepath)
    return allfiles
def del_file(filepath):
    """
    删除某一目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
# 转换文件格式和编码方式
def to_lf(path, isLF, encoding = 'utf-8'):
    """
    :param path: 文件路径
    :param isLF: True 转为Unix(LF)  False 转为Windows(CRLF)
    :param encoding: 编码方式，默认utf-8
    :return:
    """
    newline = '\n' if isLF else '\r\n'
    tp = 'Unix(LF)' if isLF else 'Windows(CRLF)'
    with open(path, newline=None, encoding=encoding) as infile:
        str = infile.readlines()
        with open(path, 'w', newline=newline, encoding=encoding) as outfile:
            outfile.writelines(str)
            #print("文件转换成功，格式：{0} ;编码：{1} ;路径：{2}".format(tp, encoding, path))

#结构匹配查询
structure_name_list1 = GetFileFromThisRootDir( "./input/",ext = 'cif')
structure_name_list1 += GetFileFromThisRootDir( "./input/",ext = 'vasp')

structure_name_list2 = []

if (len(structure_name_list1)):
    structure_name_list2 =[structure_name_list1[0]]

k = 0
for i in range(1,len(structure_name_list1)):
    structure1 = Structure.from_file("./input/"+structure_name_list1[i])
    notfund = True
    for j in range(len(structure_name_list2)):
        structure2 = Structure.from_file("./input/"+structure_name_list2[j])
        #调节参数可控制去重力度！
        
        result = structure1.matches(structure2,ltol=0.2, stol=0.25, angle_tol=6, primitive_cell=True, scale=False, 
                           attempt_supercell=False, allow_subset=False)       
        if result:      
            if (k <= 0):
                print("找到重复结构！")
            k = k + 1
            notfund = False   #说明找到重复结构
            print(structure_name_list1[i],structure_name_list2[j])
            break
    if notfund:
        structure_name_list2 +=[structure_name_list1[i]]         



make_super = [3,3,3]

if os.path.exists('output_structure')==False:
    os.mkdir('output_structure')
else:
    del_file('output_structure')    
    
if os.path.exists('output_supercell_structure')==False:
    os.mkdir('output_supercell_structure')
else:
    del_file('output_supercell_structure')


for structure_name in structure_name_list2:
    structure = Structure.from_file("./input/"+structure_name)

    POSCAR = structure.to(fmt = 'poscar')  #不输出原胞，输出原始结构 
        
    with open("./output_structure/" + structure_name,"w",encoding='UTF8') as file_save:
        file_save.write(POSCAR)
    file_save.close()

    structure.make_supercell(make_super)
    Super_cell = structure.to(fmt = 'poscar')
    with open("./output_supercell_structure/" + structure_name,"w") as file_save:
        file_save.write(Super_cell)
    file_save.close()  
    with open("./output_supercell_structure/Super_cell.vasp","a") as file_save:
        file_save.write(Super_cell)
    file_save.close()
    
isLF = True  # True 转为Unix(LF)  False 转为Windows(CRLF)
#输出原始结构
path_list = os.listdir('./output_structure')
path_list.sort(key=lambda x:int(x[:-4])) #对读取的路径进行排序
for filename in path_list:
    path = os.path.join('./output_structure',filename)
    to_lf(path, isLF) 
        
path_list = os.listdir('./output_supercell_structure')
path_list.sort(key=lambda x:int(x[:-4])) #对读取的路径进行排序
for filename in path_list:
    path = os.path.join('./output_supercell_structure',filename)
    to_lf(path, isLF)
print("结构去重完成！")

