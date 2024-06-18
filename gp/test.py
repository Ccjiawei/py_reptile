#
import chardet as chardet
import openpyxl
import requests
import pandas
from bs4 import BeautifulSoup
from lxml import etree
from urllib.request import urlopen
import requests

if __name__ == '__main__':
    #url = 'http://stockdata.stock.hexun.com/2009_cwbl_600859.shtml'
    url = 'https://cn.investing.com/equities/t-d-holdings,-inc.-income-statement'
#某些网页的表格数据可以直接使用 pandas的 read_html()方法获取，但是这个网页不行
# tables = pandas.read_html(url)
# print(len(tables))
# print(tables[0])

# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"}
#
# html1 = urlopen(url)
#
# bsObj = BeautifulSoup(html1, "html.parser")
# trs = bsObj.find_all('tr')
#
# print(len(trs))


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"}
req2 = requests.get(url, headers=headers)
htm = req2.text.encode("utf-8")

# de = chardet.detect(htm)
# soup = bs(htm,"lxml")
# content = soup.select('#myTable04')[0]
tb = pandas.read_html(htm)
for df in tb:
    print(df.columns)
    print("----------------------------------------\n")
    print(df)