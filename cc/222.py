import requests as rqt
# from pyquery import PyQuery as pq
# from bs4 import BeautifulSoup as bs
import pandas as pd
#url = "https://cn.investing.com/equities/t-d-holdings,-inc.-income-statement"
url = "https://cn.investing.com/equities/t-d-holdings,-inc."
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"}
req2 = rqt.get(url, headers=headers)
htm = req2.text.encode("utf-8")

# de = chardet.detect(htm)
# soup = bs(htm,"lxml")
# content = soup.select('#myTable04')[0]
tb = pd.read_html(htm)
for df in tb:
    # print(df.columns)
    print("----------------------------------------\n")
    print(df)

