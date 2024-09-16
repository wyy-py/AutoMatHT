import json
import os

import pandas as pd
import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# copy from the website: http://aflowlib.duke.edu/search/ui/API/aflux/?species(C),$catalog(ICSD),$paging(1,1000)
with open('aflow_C.json') as f:
  data_aflow = json.load(f)

print(type(data_aflow))
print(data_aflow[0]['compound'])
# {'compound': 'C4',
# 'auid': 'aflow:00ecd25494ac4070',
# 'aurl': 'aflowlib.duke.edu:AFLOWDATA/ICSD_WEB/HEX/C1_ICSD_290661',
# 'spacegroup_relax': 194,
# 'Pearson_symbol_relax': 'hP4',
# 'species': ['C']}

# json数据转换
aflow_data_list = []
for i in range(len(data_aflow)):
  aflow_compound = data_aflow[i]['compound']
  aflow_auid = data_aflow[i]['auid']
  aflow_aurl = data_aflow[i]['aurl']
  aflow_spacegroup_relax = data_aflow[i]['spacegroup_relax']
  aflow_Pearson_symbol_relax = data_aflow[i]['Pearson_symbol_relax']
  aflow_species = data_aflow[i]['species']

  # auid_prefix = aflow_aurl.split(':')[0]
  # print(auid_prefix)

  aurl_syn = aflow_aurl.split(':')[-1]
  print(aurl_syn)
  # AFLOWDATA/ICSD_WEB/HEX/C1_ICSD_290661

  auid_dir = aflow_aurl.split('/')[-1]
  # print(auid_dir)

  aflow_dict = {'compound': aflow_compound,
                'auid': aflow_auid,
                'aurl': "https://aflowlib.duke.edu/" + aurl_syn + '/' + auid_dir + '.cif',
                # https://aflowlib.duke.edu/AFLOWDATA/ICSD_WEB/HEX/C1_ICSD_290661/C1_ICSD_290661.cif
                'aurl_http': "https://aflowlib.duke.edu/" + aurl_syn,  # 所有信息的url
                # https://aflowlib.duke.edu/AFLOWDATA/ICSD_WEB/HEX/C1_ICSD_290661/
                'spacegroup_relax': aflow_spacegroup_relax,
                'Pearson_symbol_relax': aflow_Pearson_symbol_relax,
                'species': aflow_species}
  aflow_data_list.append(aflow_dict)

pd.DataFrame(aflow_data_list).to_csv("aflow_json.csv", index=False)


def download_cif_from_url(url, output_dir, id_name):
    try:
        # 检查输出目录是否存在，如果不存在则创建
        # 创建以auid命名的子文件夹
        auid_dir = os.path.join(output_dir, id_name.split(':')[-1])
        if not os.path.exists(auid_dir):
            os.makedirs(auid_dir)
        # 拼接输出文件的路径，只使用auid作为文件名
        filename = os.path.join(auid_dir, url.split('/')[-1])
        urllib.request.urlretrieve(url, filename)
        urllib.request.urlretrieve(url, filename)
        print("File downloaded as:", filename)
    except urllib.error.HTTPError as e:
        print(f"CIF file cannot download from {url}: {e}")


csv_file = 'aflow_json.csv'
df_csv = pd.read_csv(csv_file)
auid_list = df_csv['auid']
url_list = df_csv['aurl']

# 批量下载.cif文件
output_directory = 'cif_files'
for aflow_url, auid in zip(url_list, auid_list):
    download_cif_from_url(aflow_url, output_directory, auid)
