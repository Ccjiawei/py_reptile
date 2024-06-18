import openpyxl
import requests
import pandas
from bs4 import BeautifulSoup
from lxml import etree
from urllib.request import urlopen


if __name__ == '__main__':
    #url = 'http://stockdata.stock.hexun.com/2009_cwbl_600859.shtml'
    url = 'https://cn.investing.com/equities/t-d-holdings,-inc.-income-statement'
#某些网页的表格数据可以直接使用 pandas的 read_html()方法获取，但是这个网页不行
# tables = pandas.read_html(url)
# print(len(tables))
# print(tables[0])


#使用方法二 ：request请求获取网页的HTML ，在通过beautifulsoup 的方法 遍历解析获取对应的td 标签的数据
# 模仿浏览器的headers
headers = {
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}

html1 = urlopen(url)

bsObj = BeautifulSoup(html1, "html.parser")
trs = bsObj.find_all('tr')

print(len(trs))


#定义存放所有数据的列表
all_data = []

for tdall in trs:
    # 解析网页可以获取到 当 len(tdall)是 4 时每一行我们需要的数据，其他数据我们并不需要，是脏数据，可以通过这个进行过滤
    if len(tdall) == 4:
    # 获取每一个tr中所有的td数据
        tds = tdall.find_all('td')
        # 遍历tds 获取每一个td中的值
        row_data = []
        for td in tds:
        # 定义存放每一行数据的列表
            value = td.find(name='div', attrs={"class": "tishi"}).text
            # 有的数据为空，对为空的数据进行替换
            if value == '':
                value = '0'
            #<>.text获取标签中的值
            row_data.append(value)
            # 也可以尝试使用正则匹配字符串中的值，后来发现beautifulsoup有直接获取值的方法
            # reg = r'<div class="tishi">([\s\S]+?)</div>'
            # pattern = re.compile(reg)
            # tags = re.findall(pattern, vlaue.text)
            # print(tags)
            #将每一行数据放入所有数据的列表中
        print(row_data)
        all_data.append(row_data)



#使用pandas中将列表转为dataframe
df = pandas.DataFrame(all_data,columns=all_data[0])

print(df)

df.to_excel(r'C:\Users\Admin\Desktop\abc.xlsx', index = False);

#开始使用requests中方法请求，获取不到数据，尝试了其他方式，原因暂时还没有找到，感兴趣的小伙伴可以自己探索一下，后期有结果也会去跟进发布的
# resp = requests.get(url, headers)
# resp.encoding = 'utf-8'
# html = resp.text

