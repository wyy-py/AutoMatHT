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
source /public/software/compiler/intel/oneapi/oneapi-2024.0.1/setvars.sh intel64
export PATH=/work/home/acqfz4noj8/software/vasp.6.3.0/bin:$PATH

# 启动第 1 阶段任务 (SCF计算)
date "+01 Today's date is: %D. The time execution %T" >> time.info
mpirun -genv I_MPI_FABRICS shm:ofi -genv FI_PROVIDER mlx -machinefile $CURDIR/nodelist.$SLURM_JOB_ID -np $SLURM_NPROCS vasp_std > log.$SLURM_JOB_ID 2>&1
date "+02 Today's date is: %D. The time finish %T" >> time.info

# 准备第 2 阶段输入文件
cp ./CONTCAR ./scf/POSCAR
cd ./scf/
date "+01 Today's date is: %D. The time execution %T" >> time.info
mpirun -genv I_MPI_FABRICS shm:ofi -genv FI_PROVIDER mlx -machinefile $CURDIR/nodelist.$SLURM_JOB_ID -np $SLURM_NPROCS vasp_std > log.scf.$SLURM_JOB_ID 2>&1
date "+02 Today's date is: %D. The time finish %T" >> time.info

# 准备第 3 阶段输入文件
cp ./CONTCAR ./band/POSCAR
cp ./WAVECAR ./band/
cd ./band/
date "+01 Today's date is: %D. The time execution %T" >> time.info
mpirun -genv I_MPI_FABRICS shm:ofi -genv FI_PROVIDER mlx -machinefile $CURDIR/nodelist.$SLURM_JOB_ID -np $SLURM_NPROCS vasp_std > log.band.$SLURM_JOB_ID 2>&1
date "+02 Today's date is: %D. The time finish %T" >> time.info

# 清理和结束
echo "++++++++++++++++++++++++++++++++++++++++"
echo "任务完成时间: "
date
rm -r $CURDIR/nodelist.$SLURM_JOB_ID
