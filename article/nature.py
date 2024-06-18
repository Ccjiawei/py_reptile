#加载所需库
import requests
from bs4 import BeautifulSoup

#Nature
# 发起HTTP请求获取网页内容
url = 'https://www.nature.com/nature/volumes/619/issues/7971'
response = requests.get(url)
html_content = response.text

# 使用BeautifulSoup解析网页内容，指定解析器为html.parser
soup = BeautifulSoup(html_content, 'html.parser')

# 假设我们想提取网页中所有的标题文本
titles = soup.find_all('h3')

# 创建一个文件并将标题写入文件，去除空行
with open('nature_titles.txt', 'w', encoding='utf-8') as file:
    for title in titles:
        title_text = title.text.strip()  # 去除标题两端的空白字符
        if title_text:  # 检查标题是否为空
            file.write(title_text + '\n')

print("标题已保存到文件 nature_titles.txt")