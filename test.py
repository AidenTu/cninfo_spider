import requests
from bs4 import BeautifulSoup

# 发送HTTP GET请求获取网页内容
url = "https://xueqiu.com/snowman/S/SZ000002/detail#/GSLRB"
response = requests.get(url)

# 使用Beautiful Soup解析网页内容
soup = BeautifulSoup(response.content, "html.parser")

# 找到包含表格的HTML元素，通常是<table>
table = soup.find("table")

# 初始化一个空的二维列表来存储表格数据
table_data = []

# 遍历表格的每一行
for row in table.find_all("tr"):
    # 初始化一个空的列表来存储行数据
    row_data = []
    
    # 遍历每一行的单元格
    for cell in row.find_all("td"):
        # 获取单元格文本，并添加到行数据列表中
        cell_text = cell.get_text(strip=True)
        row_data.append(cell_text)
    
    # 将行数据添加到表格数据列表中
    table_data.append(row_data)

# 打印提取的表格数据
for row in table_data:
    print("\t".join(row))
