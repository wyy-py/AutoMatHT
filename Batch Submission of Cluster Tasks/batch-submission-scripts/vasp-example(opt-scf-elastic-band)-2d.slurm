#!/bin/bash
#SBATCH --job-name=band            # 任务名称
#SBATCH --partition=tyhctest          # 分区名称
#SBATCH --nodes=1                     # 节点数量
#SBATCH --ntasks-per-node=12          # 每个节点的任务数（核数）
#SBATCH --error=%j.err                # 错误输出文件
#SBATCH --output=%j.out               # 标准输出文件
#SBATCH --time=72:00:00  # 设置为最大允许时间

# 用于结构优化-静态自洽-能带计算的slurm集群任务提交脚本示例
# 需要准备好对应输入文件，内容参考calc-standard-pbs文件夹，并将本文件复制到opt目录下方
# 获取当前工作目录
CURDIR=`pwd`
rm -r $CURDIR/nodelist.$SLURM_JOB_ID
NODES=`scontrol show hostnames $SLURM_JOB_NODELIST`
for i in $NODES
do
  echo "$i:$SLURM_NTASKS_PER_NODE" >> $CURDIR/nodelist.$SLURM_JOB_ID
done
echo "分配的总核数: $SLURM_NPROCS"

echo "任务开始时间: "
date
echo "++++++++++++++++++++++++++++++++++++++++"

# 设置环境变量
source /public/software/compiler/intel/oneapi/oneapi-2024.0.1/setvars.sh intel64  # intel oneapi Path
export PATH= vasp533_xy/bin:$PATH  # vasp.exe Path

# 启动第 1 阶段任务 (opt计算)
# 用vaspkit准备KPOINTS文件，如果没有手动编写的话，或者用opt_to_band-batch-calc.py
# vaspkit -task 102 -kpr 0.025
date "+01 Today's date is: %D. The time execution %T" >> time.info
mpirun -genv I_MPI_FABRICS shm:ofi -genv FI_PROVIDER mlx -machinefile $CURDIR/nodelist.$SLURM_JOB_ID -np $SLURM_NPROCS vasp_std > log.$SLURM_JOB_ID 2>&1
date "+02 Today's date is: %D. The time finish %T" >> time.info

# 准备机械性质计算输入文件
cp ./CONTCAR ./elastic/POSCAR
cp ./KPOINTS ./elastic/KPOINTS
cp ./POTCAR ./elastic/POTCAR
# INCAR文件需要手动设置好参数哦
cd ./elastic/
date "+01 Today's date is: %D. The time execution %T" >> time.info
mpirun -genv I_MPI_FABRICS shm:ofi -genv FI_PROVIDER mlx -machinefile $CURDIR/nodelist.$SLURM_JOB_ID -np $SLURM_NPROCS vasp_std > log.scf.$SLURM_JOB_ID 2>&1
date "+02 Today's date is: %D. The time finish %T" >> time.info

# 退出到opt目录下，准备自洽计算输入文件
cd ..
cp ./CONTCAR ./scf/POSCAR
cp ./KPOINTS ./scf/KPOINTS
cp ./POTCAR ./scf/POTCAR
# INCAR文件需要手动设置好参数哦
cd ./scf/
date "+01 Today's date is: %D. The time execution %T" >> time.info
mpirun -genv I_MPI_FABRICS shm:ofi -genv FI_PROVIDER mlx -machinefile $CURDIR/nodelist.$SLURM_JOB_ID -np $SLURM_NPROCS vasp_std > log.scf.$SLURM_JOB_ID 2>&1
date "+02 Today's date is: %D. The time finish %T" >> time.info

# 准备能带计算输入文件
cp ./CONTCAR ./band/POSCAR
cp ./POTCAR ./band/POTCAR
cp ./WAVECAR ./band/
# INCAR文件需要手动设置好参数哦
cd ./band/
# 生成高对称点路径并创建 KPOINTS 文件，在此之前请确保已经正确安装了vaspkit软件
vaspkit -task 302
mv KPATH.in KPOINTS
date "+01 Today's date is: %D. The time execution %T" >> time.info
mpirun -genv I_MPI_FABRICS shm:ofi -genv FI_PROVIDER mlx -machinefile $CURDIR/nodelist.$SLURM_JOB_ID -np $SLURM_NPROCS vasp_std > log.band.$SLURM_JOB_ID 2>&1
date "+02 Today's date is: %D. The time finish %T" >> time.info

# 清理和结束
echo "++++++++++++++++++++++++++++++++++++++++"
echo "任务完成时间: "
date
rm -r $CURDIR/nodelist.$SLURM_JOB_ID
