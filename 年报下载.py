import requests
import pathlib
import pandas as pd
import numpy as np
import concurrent.futures



base_url = 'http://www.cninfo.com.cn/new/announcement/download'
root_dir = pathlib.Path.cwd()
pdf_dir = root_dir.joinpath('pdf')
pdf_dir.mkdir(exist_ok=True)

def download_pdf(base_url, params, headers, pdf_dir, pdf_name):
    response = requests.get(url=base_url, params=params, headers=headers)
    pdf_path = pdf_dir.joinpath(pdf_name + '.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(response.content)



df = pd.read_csv('./pdf_to_download.csv', dtype={'secCode': object})
df['announcementTime'] = pd.to_datetime(df['announcementTime'], unit='ms').dt.date


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}

# 创建线程池，指定最大线程数
max_workers = 4  # 例如，使用4个线程并行下载
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = []

    for i in range(len(df)):
        params = {
            'bulletinId': df['announcementId'][i],
            'announceTime': df['announcementTime'][i]
        }

        code_name = df['secCode'][i]
        firm_name = df['secName'][i]


        code_dir = pdf_dir.joinpath(code_name)
        code_dir.mkdir(exist_ok=True)
        pdf_name = firm_name + '：' + df['announcementTitle'][i]
        

        print(f'正在下载 -- {pdf_name}')

        # 使用submit方法将下载任务提交给线程池
        future = executor.submit(download_pdf, base_url, params, headers, pdf_dir, pdf_name)
        futures.append(future)
    
    # 等待所有任务完成
    concurrent.futures.wait(futures)

    
    #response = requests.get(url=base_url, params=params, headers=headers)
    #pdf_path = code_dir.joinpath(pdf_name + '.pdf')
    #with open(pdf_path, 'wb') as f:
        #f.write(response.content)

print('\n全部文件下载完毕！')
    