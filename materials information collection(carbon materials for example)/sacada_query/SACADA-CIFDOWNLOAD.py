import os
import requests

# 设置下载链接的起始和结束编号
start_index = 1
end_index = 1192

# 设置下载链接的基础部分
base_url = 'https://www.sacada.info/download/'

# 设置保存文件的目录
output_directory = 'SACADA-structure/'

# 创建保存文件的目录
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 批量下载文件
for i in range(start_index, end_index + 1):
    url = f'{base_url}{i}.zip'
    output_path = os.path.join(output_directory, f'{i}.zip')

    # 发送 HTTP 请求
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 保存文件
        with open(output_path, 'wb') as output_file:
            output_file.write(response.content)

        print(f'Downloaded {i}.zip successfully.')
    else:
        print(f'Failed to download {i}.zip. Status code: {response.status_code}')
