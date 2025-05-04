# AutoMatHT: Materials-Information-Collection & high computational workflow
This guide provides a step-by-step guideline on building a material database for training models. 
The repository includes a collection of practical scripts designed to retrieve material structures from the latest online databases and perform thorough material data cleaning.
![image](https://github.com/user-attachments/assets/bba9337d-b5f2-4916-9873-0915c6c8f642)

# 材料数据库结构爬取

详细代码参考：Materials-Information-Collection/materials information collection(carbon materials for example)

OQMD_query.py：批量获取OQMD数据库的材料结构

aflow query.py： 批量获取AFLOW数据库的材料结构

jarvis_query.py：批量获取JARVIS数据库的材料结构

mp_query.py： 批量获取Materials Project数据库的材料结构

sacada_query.py：批量获取SACADA数据库的材料结构

data clean scripts：结构清洗、去重、结构转换、2D和3D材料分类
# 批量提交计算任务
详细代码参考：Materials-Information-Collection/Batch Submission of Cluster Tasks

calc-standard-pbs：3D块体材料计算示例文件夹，材料结构文件需要自行准备，部分参数需要调整

2d-calc-standard-pbs：2D材料计算示例文件夹，材料结构文件需要自行准备，部分参数需要调整

批量提交任务脚本：

calc-standard-pbs包含了所需准备的任务模版文件夹，其中INCAR部分参数需要进一步修改，POSCAR需要替换，文件结构为：
```
calc-standard-pbs/
└──  AutoSubmit.pbs
└──  opt
│   ├── elastic
│   │   └── INCAR
│   ├── INCAR
│   ├── pbs-example(opt-scf-elastic-band).pbs
│   ├── POSCAR
│   └── scf
│       ├── band
│       │   └── INCAR
│       └── INCAR
└── phonopy
    ├── AutoSubmit.pbs   
    ├── band.conf    
    ├── command    
    ├── INCAR    
    ├── KPOINTS    
    ├── Loop-phonopy.sh    
    └── mesh.conf
```  
batch-submission-scripts是批量提交任务的代码，文件结构为：
```
batch-submission-scripts
└──  opt_scf_elastic_to_band-batch-calc.py  一次性提交从结构优化-自洽/机械性质-能带计算的所有任务
└──  pbs-example(opt-scf-elastic-band)-2d.pbs 二维材料任务提交脚本（pbs集群）
└──  pbs-example(opt-scf-elastic-band).pbs  块体材料任务提交脚本（pbs集群）
└──  phonopy-batch-submit.py  声子谱任务提交
└──  sacada_phonopy_post-process.py 声子谱计算结果后处理，得到热容、自由能、热膨胀系数等
└──  sacada_qsub_opt_identify-error.py 查看结构优化过程中可能存在的问题
└──  vasp-example(opt-scf-elastic-band)-2d.slurm  二维材料任务提交脚本（slurm集群）
└── vasp-example(opt-scf-elastic-band).slurm  块体材料任务提交脚本（slurm集群）
```
