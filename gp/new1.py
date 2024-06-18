import tushare as ts

import pandas as pd

# 首先通过ts.get_stock_basics()命令获得股票代码的一些基本数据 ，然后通过to_excel()命令保存。

# 以下是本人保存的路径

source_date=r'C:\Users\Admin\Desktop\abc.xlsx'

# 我们需要提取股票代码，用于后面的for循环，首先读取之前下载好的文件，将第一列的股票代码进行字符串转化。

df=pd.read_excel(source_date,converters={'code':lambda x:str(x)})

# 将提取出来的股票代码列表化赋值与 stockcode 这个变量。

stockcode=list(map(str,df['code']))

# 开始进行循环下载。。

for i in stockcode:

    print('开始下载{}股票数据.....'.format(i))

#设定每个文件的文件名和存储地址。

file_address=r'C:\Users\Admin\Desktop\{}.xlsx'.format(i)

#提取单个股票的历史数据。

stock_data=ts.get_hist_data(i)

#导出到之前设定的好的文件地址。

stock_data.to_excel(file_address)

#由于导出的每个股票的历史数据中并没有包含股票代码，所以我把股票代码加入到Excel中，

#在日期的后一列加入股票代码，方便以后所有数据整合后可以进行股票筛选。

#如果不需要，可以删除下面三行代码。

dw_data=pd.read_excel(file_address)

dw_data.insert(loc=1,column='code',value=i)

dw_data.to_excel(file_address)

# 打印出下载进程，方便观察。。。

print('{}/{} has been downloaded,{}股票数据下载完毕'

.format(stockcode.index(i)+1,len(stockcode),i))

print('-----------------------------------------------------')