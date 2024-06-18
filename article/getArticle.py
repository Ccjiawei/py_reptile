import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import io

def get_substring_after_char(text, char):
    parts = text.split(char, 1)  # 分割一次，返回列表最多包含两个元素
    if len(parts) > 1:
        return parts[1]  # 如果找到了分隔符，返回分隔符后的字符串
    else:
        return text  # 如果没有找到分隔符，返回原字符串

path = "C:/Users/Admin/Desktop/DOI/"
os.chdir("C:/Users/Admin/Desktop")
os.getcwd()

if os.path.exists(path) == False:
    os.mkdir(path)  # 20210607更新，创建保存下载文章的文件夹
f = open(path + "DOI.txt", "r", encoding="utf-8")  # 存放DOI码的.txt文件中，每行存放一个文献的DOI码，完毕须换行（最后一个也须换行！）
head = { \
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36' \
    }

for line in f.readlines():
    # line = line[:-1]  # 去换行符
    url = "https://www.nature.com/articles/" + line  # 20210515更新：现在换成这个sci hub检索地址
    # url = "https://doi.org/" + line   # 20210515更新：现在换成这个sci hub检索地址
    try:
        # download_url = ""
        # r = requests.get(url, headers = head)
        # r.raise_for_status()
        # r.encoding = r.apparent_encoding
        # soup = BeautifulSoup(r.text, "html.parser")

        #doi_suff = get_substring_after_char(line, "/")
        url_pdf = "https://www.nature.com/articles/"+ line +".pdf"

        download_r = requests.get(url_pdf, headers = head)
        download_r.raise_for_status()

        # ab:以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
        with open(path + line.replace("/", "_") + ".pdf", "wb+") as temp:
            temp.write(download_r.content)
    finally:
        f.close()




f.close()


