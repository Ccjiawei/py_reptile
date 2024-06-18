#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
import time
import requests
import openpyxl
from bs4 import BeautifulSoup
import pymysql

def get_page(url, params=None, headers=None, proxies=None, timeout=None):
    response = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=timeout)
    print("解析网址：", response.url)
    page = BeautifulSoup(response.text, 'lxml')
    print("响应状态码：", response.status_code)
    return page

companys = [
    't-d-holdings,-inc.'
]

tabs = [
    '-income-statement', #利润表
    '-balance-sheet', #资产负债表
    '-cash-flow' #现金流量表
]
"""

利润表：（GET）
年度：https://cn.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=44148&report_type=INC&period_type=Annual
季度：https://cn.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=44148&report_type=INC&period_type=Interim

资产负债：
年度：https://cn.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=44148&report_type=BAL&period_type=Annual
季度：https://cn.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=44148&report_type=BAL&period_type=Interim

现金流量：
年度：https://cn.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=44148&report_type=CAS&period_type=Annual
季度：https://cn.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=44148&report_type=CAS&period_type=Interim
"""

writer = pd.ExcelWriter(r'C:\Users\Admin\Desktop\yyy.xlsx')
for company in companys:

    for tab in tabs:
        url = 'https://cn.investing.com/equities/' + company + tab

        headers = {
            'Host': 'cn.investing.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
        }

        params = None

        page = get_page(url, headers=headers, params=params)

        stocks = []
        stocks_list = page.find_all('table', 'genTbl reportTbl')[0]


        for stock in stocks_list:
            if stock == '\n':
                continue
            # th
            th_list = stock.find_all('th')

            for th in th_list:
                if th.div:
                    stocks.append(th.span.text + '/' + th.div.text)
                else:
                    stocks.append(th.span.text)
            # tr
            tr_list = stock.find_all('tr')

            for tr in tr_list:

                if 'class' in tr.attrs and tr.attrs['class'] == ['noHover']:
                    continue
                td_list = tr.find_all('td')

                # td
                for td in td_list:
                    if td.span:
                        stocks.append(td.span.text)
                    else:
                        stocks.append(td.text)
        #分割
        result = []
        i = 0
        while(i < len(stocks)):
           result.append(stocks[i:i+5:1])
           i = i + 5

        # realResult = []
        # j = 0
        # while(j < len(result)):
        #     m = 0
        #     temp = []
        #     while(m < len(result[j])):
        #         temp.append(result[j][m:m+1:1])
        #         m = m + 1
        #     realResult.append(temp)
        #     j = j + 1


        dataframe = pd.DataFrame({'财务状况': result})

        print(dataframe)
        dataframe = pd.DataFrame(dataframe['财务状况'].values.tolist())
        print(dataframe)

        dataframe.to_excel(writer, sheet_name=tab, header=None, index=False)

        #result 入库
        conn=pymysql.connect(host='81.68.197.104',password='Baiwa@0601',port=3307,user='root',charset='utf8')
        cur = conn.cursor()

        cur.execute('show databases')
        cur.fetchone()  # 返回前一条记录
        cur.fetchmany(2)  # 返回前两条记录
        cur.fetchall()  # 返回所有记录

        cur.close()
        conn.close()

        time.sleep(1)


writer.close()
