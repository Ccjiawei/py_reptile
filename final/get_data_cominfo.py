# coding:utf-8
# 股市企业-企业行业、板块、股票类型、简介 数据爬取

import datetime
import sys
import time
import requests
from bs4 import BeautifulSoup
import pymysql
import json
import math
import re

def get_page(url, params=None, headers=None, proxies=None, timeout=None):
    response = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=timeout)
    page = BeautifulSoup(response.text, 'lxml')
    if str(response.status_code) == '403':
        print("【触发网站反爬机制,请稍后再试】")
        sys.exit()
    return page

headers = {
        'Host': 'cn.investing.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43'
    }
headers_www = {
        'Host': 'www.investing.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43'
    }
# 变量
stock_company = 'cn_stock_company'
stock_company_info = 'cn_stock_company_info'
#currency = 'AUD'  # USD  JPY  EUR  TWD  KRW  GBP INR CAD AUD   已废弃 改为从抓取页面获取货币 20230714

conn = pymysql.connect(host='81.68.197.104', database='python_test', password='Baiwa@0601', port=3307, user='root',
                       charset='utf8')
cur = conn.cursor()
cur.execute('select count(1) as count from ' + stock_company)
counts = cur.fetchall()
pagesize = 50
allpages = math.ceil(counts[0][0] / pagesize)
pagenum = 0

conn.commit()
cur.close()
conn.close()

print('总数量'+str(counts[0][0]))
print('每页大小'+str(pagesize))
print('总页数'+str(allpages))
print('============开始============')

while pagenum < allpages:
    print("当前页数："+str(pagenum))
    companys = []

    limit1 = pagesize * pagenum

    conn = pymysql.connect(host='81.68.197.104',database = 'python_test',password='Baiwa@0601',port=3307,user='root',charset='utf8')
    cur = conn.cursor()
    cur.execute('select comid,symbol,exchange_name,currency,url from ' + stock_company + ' limit ' + str(limit1) + ', ' + str(pagesize) + '')
    rest = cur.fetchall()

    for i in rest:
        companys.append(i)

    all_data = {}

    # 1-企业数据处理
    for company in companys:
        # url
        url_info = ''
        if company[4].find('?') >= 0:
            uri = company[4].split('?')
            if len(uri) != 2:
                print("企业【"+str(company[0])+"=="+str(company[1])+"】url中含有不止一个？,跳过....")
                continue
            url_info = 'https://cn.investing.com' + uri[0] + '-company-profile' + '?' +uri[1]
        else:
            url_info = 'https://cn.investing.com'+ company[4] + '-company-profile'


        if url_info == '':
            print("企业【"+str(company[0])+"=="+str(company[1])+ "】url为空,跳过....")
            continue

        #time.sleep(1)
        params = None

        try:
            page_info = get_page(url_info, headers=headers, params=params)
        except Exception as e:
            print(f"出现了异常{e}")
            sys.exit()

        # 1-企业名称 无名称跳过
        company_name = page_info.find_all('h2', 'float_lang_base_1 inlineblock')
        if len(company_name) <= 0:
            print("企业【"+str(company[0])+"=="+str(company[1])+"】无档案信息,跳过...")
            continue
        cname_info = company_name[0].text
        company_name = cname_info[0:-4]

        # 2-行业 板块 股票类型
        companyProfileHeader = page_info.find_all('div', 'companyProfileHeader')
        if len(companyProfileHeader) <= 0:
            textcompanyProfileHeader = ''
        else:
            textcompanyProfileHeader = companyProfileHeader[0].text
        texthead = re.split(r"\n+", textcompanyProfileHeader)

        # 3-简介
        companyProfileBody = page_info.find_all('div', 'companyProfileBody')
        if len(companyProfileBody) <= 0:
            textcompanyProfileBody = ''
        else:
            textcompanyProfileBody = companyProfileBody[0].text
        textbody = re.split(r"\n+", textcompanyProfileBody)

        # 英文简介
        if textbody == ['']:
            url_info = url_info.replace('https://cn.', 'https://www.')
            try:
                page_info_intro = get_page(url_info, headers=headers_www, params=params)
            except Exception as e:
                print(f"出现了异常{e}")
                sys.exit()
            cpb = page_info_intro.find_all('div', 'companyProfileBody')
            if len(cpb) <= 0:
                textcompanyProfileBody = ''
            else:
                textcompanyProfileBody = cpb[0].text
            textbody = re.split(r"\n+", textcompanyProfileBody)

        # 货币
        currency_div = page_info.find_all('div', 'bottom lighterGrayFont arial_11')
        if len(currency_div) <= 0:
            print("企业【" + str(company[0]) + "==" + str(company[1]) + "】抓取货币信息失败...")
        currency_spans = currency_div[0]
        currency = currency_spans.contents[6].text


        all_data[company_name] = [
                                  company[2], company[1],
                                  texthead[1][2:] if len(texthead) > 0 and texthead != [''] else '',
                                  texthead[2][2:] if len(texthead) > 0 and texthead != [''] else '',
                                  texthead[4][4:] if len(texthead) > 0 and texthead != [''] else '',
                                  textbody[1] if len(textbody) > 0 and textbody != [''] else '',
                                  currency
                                  ]

    print("数据收集完毕...")

    # 2-入库
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = 'insert into ' + stock_company_info + '(exchange_name,symbol,company_name,currency,industry,plate,stock_type,introduction,create_time) values'
    for key, value in all_data.items():

        exchange_name = value[0] if value[0] != '' else ''
        symbol = value[1] if value[1] != '' else ''
        industry = value[2] if value[2] != '' else ''
        plate = value[3] if value[3] != '' else ''
        stock_type = value[4] if value[4] != '' else ''
        introduction = value[5] if value[5] != '' else ''
        currency = value[6] if value[6] != '' else ''

        introduction = introduction.replace("'", "\\\'") # 将单引号转成\单引号
        introduction = introduction.replace('"', '\\\"') # 将双引号转成\双引号

        key = key.replace("'", "\\\'")  # 将单引号转成\单引号
        key = key.replace('"', '\\\"')  # 将双引号转成\双引号

        #sq = '(\'' + exchange_name +'\',\''+ symbol +'\',\''+ key +'\',"JPY",\''+ industry +'\',\''+ plate +'\',\''+ stock_type +'\',\"'+ introduction  + '\",\''+ date + '\')' + ','
        sq = '(\'' + exchange_name + '\',\'' + symbol + '\',\'' + key + '\',\'' + currency + '\',\'' + industry + '\',\'' + plate + '\',\'' + stock_type + '\',\"' + introduction + '\",\'' + date + '\')' + ','

        sql += sq

    cur.execute(sql[0:len(sql)-1])


    print("数据入库完毕...")
    print("")
    print("")



    conn.commit()
    cur.close()
    conn.close()
    pagenum += 1
