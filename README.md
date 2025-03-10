# Materials-Information-Collection
This guide provides a step-by-step guideline on building a material database for training models. The repository includes a collection of practical scripts designed to retrieve material structures from the latest online databases and perform thorough material data cleaning.
# 材料数据库结构爬取
详细代码参考：Materials-Information-Collection/materials information collection(carbon materials for example)
OQMD_query：批量获取OQMD数据库的材料结构
aflow query： 批量获取AFLOW数据库的材料结构
jarvis_query：批量获取JARVIS数据库的材料结构
mp_query： 批量获取Materials Project数据库的材料结构
sacada_query：批量获取SACADA数据库的材料结构
data clean scripts：结构清洗、去重、结构转换、2D和3D材料分类
# 批量提交计算任务
详细代码参考：Materials-Information-Collection/Batch Submission of Cluster Tasks
calc-standard-pbs：3D材料计算示例文件夹，材料结构文件需要自行准备，部分参数需要调整
2d-calc-standard-pbs：2D材料计算示例文件夹，材料结构文件需要自行准备，部分参数需要调整
批量提交任务脚本：
sacada_calculation
