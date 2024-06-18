# 英为财情美股企业财务状态数据收集
# coding: utf-8
import datetime
import sys
import time
import requests
from bs4 import BeautifulSoup
import pymysql
import json
import math

def get_page(url, params=None, headers=None, proxies=None, timeout=None):
    response = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=timeout)
    #print("解析网址：", response.url)
    page = BeautifulSoup(response.text, 'lxml')
    #print("响应状态码：", response.status_code)
    return page

def get_json(url, headers=None):
    payload = {
        'country[]': '5'
        # 'sector':'32,30,25,36,26,33,35,34,27,28,31,24,29',
        # 'industry':'186,198,201,189,194,227,192,206,230,175,211,216,177,210,209,213,225,197,185,223,173,196,231,188,193,181,184,179,226,208,205,229,228,183,224,190,174,203,172,212,221,222,215,180,191,232,182,217,187,219,214,195,178,220,176,204,207,218,200,202,199',
        # 'equityType':'ORD,DRC,Preferred,Unit,ClosedEnd,REIT,ELKS,OpenEnd,Right,ParticipationShare,CapitalSecurity,PerpetualCapitalSecurity,GuaranteeCertificate,IGC,Warrant,SeniorNote,Debenture,ETF,ADR,ETC',
        # 'pn':'1',
        # 'order[col]':'eq_market_cap',
        # 'order[dir]':'d'
    }
    response = requests.post(url, headers=headers, data=payload)
    res = json.loads(response.text)
    print(res)
    return res

headers = {
        'Host': 'cn.investing.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
        # 'Accept': "application/json"
}

#企业列表
companys = []
url_company = 'https://cn.investing.com/stock-screener/Service/SearchStocks'
#url_company = 'https://cn.investing.com/stock-screener/?sp=country::5|sector::a|industry::a|equityType::a%3Ceq_market_cap;1'


res = get_json(url_company, headers=headers)
totalCount = res['totalCount']
pageNumber = res['pageNumber']
# allpages = math.ceil(totalCount / pageSize)

page = 0

company_list = res['data']
if len(company_list) <= 0:
    sys.exit()
for com in company_list:
    exchange_name = ''
    if com['Url'] != '':
        url_exchange = 'https://cn.investing.com' + com['Url']
        params = None
        page_exchange = get_page(url_exchange, headers=headers, params=params)
        exchange_name_list = page_exchange.find_all('span', 'text-xs ml-1') or page_exchange.find_all('span', 'text-xs leading-4 font-normal overflow-hidden text-ellipsis flex-shrink')
        exchange_name = exchange_name_list[0].text if len(exchange_name_list) > 0 else ''
        currency_list = page_exchange.find_all('span', 'instrument-metadata_text__Rq22W font-bold')
        currency = currency_list[0].text if len(currency_list) > 0 else ''
    cc = [com['Id'], com['Symbol'], exchange_name, currency]
    companys.append(cc)
page += 1

# companys = [
#     ['239','GM','纽约'],
#     ['44148','8795','纽约']
# ]

#年度数据 Interim-季度  Annual-年度
period_type = 'Annual'
report_type = ['INC','BAL','CAS']

conn=pymysql.connect(host='81.68.197.104',database = 'python_test',password='Baiwa@0601',port=3307,user='root',charset='utf8')
cur = conn.cursor()

for company in companys:
    """
    概况：https://cn.investing.com/instruments/Financials/changesummaryreporttypeajax?action=change_report_type&pid=239&financial_id=239&ratios_id=239&period_type=Annual

    详情：https://cn.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=239&report_type=INC&period_type=Annual
    """

    url_summary = 'https://cn.investing.com/instruments/Financials/changesummaryreporttypeajax?action=change_report_type&pid='\
          +company[0]+'&financial_id='+company[0]+'&ratios_id='+company[0]+'&period_type='+period_type+''
    url_inc = 'https://cn.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID='\
          +company[0]+'&report_type=INC&period_type='+period_type+''
    url_bal = 'https://cn.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=' \
              + company[0] + '&report_type=BAL&period_type=' + period_type + ''
    url_cas = 'https://cn.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=' \
              + company[0] + '&report_type=CAS&period_type=' + period_type + ''

    params = None
    page_summary = get_page(url_summary, headers=headers, params=params)
    page_inc = get_page(url_inc, headers=headers, params=params)
    page_bal = get_page(url_bal, headers=headers, params=params)
    page_cas = get_page(url_cas, headers=headers, params=params)

    all_data = {}
    summary_list = page_summary.find_all('div', 'companySummaryIncomeStatement')

    inc_list = page_inc.find_all('table', 'genTbl reportTbl')[0]
    bal_list = page_bal.find_all('table', 'genTbl reportTbl')[0]
    cas_list = page_cas.find_all('table', 'genTbl reportTbl')[0]

    # 比率数据抽取 收益、负债、现金流
    n = 0
    while(n < len(summary_list)):
        info_list = summary_list[n].find_all('div', 'info float_lang_base_2')
        block_item_name = summary_list[n].find_all('h3')[0].a.text
        kvs = []
        for info in info_list:
            info_in_list = info.find_all('div', 'infoLine')
            for info_in in info_in_list:
                span_key = info_in.find_all('span','float_lang_base_1')[0]
                span_value = info_in.find_all('span','float_lang_base_2 text_align_lang_base_2 dirLtr bold')[0]
                kv = [span_key.text, span_value.text, '']
                kvs.append(kv)

        if ('收益表' in block_item_name):
            operate_list = inc_list
        if ('资产负债表' in block_item_name):
            operate_list = bal_list
        if ('现金流量表' in block_item_name):
            operate_list = cas_list

        # 表格详情数据抽取 收益、负债、现金流tab页面
        th_list = []
        for operate in operate_list:
            if operate == '\n':
                continue
            th_list = operate.find_all('th')
            if len(th_list) > 0:
                break # 防止th_list被覆盖 只取第一次的年度头

        if len(th_list) <= 0:
            continue # 年度数据表头为空 没有对应的详情数据

        for operate in operate_list:
            if operate == '\n':
                continue
            tr_list = operate.find_all('tr')
            for tr in tr_list:
                if 'class' in tr.attrs and tr.attrs['class'] == ['noHover']:
                    continue
                td_list = tr.find_all('td')
                if len(td_list) <= 0:
                    continue
                block_name = td_list[0].span.text
                tdnum = 0
                while(tdnum < len(td_list)):
                    if tdnum == 0:
                        tdnum += 1
                        continue
                    item_value = td_list[tdnum].text
                    item_year = th_list[tdnum].span.text + '/' + th_list[tdnum].div.text
                    kv_t = [block_name, item_value, item_year]
                    kvs.append(kv_t)
                    tdnum += 1
        n += 1
        all_data[block_item_name] = kvs

    # 表格数据抽取 概况页
    # table = page_summary.find_all('table', 'genTbl openTbl companyFinancialSummaryTbl')[n]
    # th_list = table.find_all('thead')[0].find_all('tr')[0].find_all('th')
    # tr_list = table.find_all('tbody')[0].find_all('tr')
    # num = 0
    # while(num < len(th_list)):
    #     if 'class' in th_list[num].attrs and 'arial_11' in th_list[num].attrs['class']:
    #         num = num + 1
    #         continue
    #     for tr in tr_list:
    #         block_name = tr.find_all('td', 'bold left')[0].text
    #         item_value = tr.find_all('td')[num].text
    #         kv_t = [block_name, item_value ,th_list[num].text]
    #         kvs.append(kv_t)
    #     num = num + 1
    # n = n + 1
    # all_data[block_item_name] = kvs

    # 入库
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    for key,value in all_data.items():
        print(key, ":", value)
        block_item_name = ''
        if('收益表' in key):
            block_item_name = '利润表'
        if ('资产负债表' in key):
            block_item_name = '资产负债表'
        if ('现金流量表' in key):
            block_item_name = '现金流量表'
        sql = 'insert into stock_info_us(stock_code,currency,exchange_name,block_item_name,item_name,item_value,item_date,item_year) values'
        for vul in value:
            item_name = vul[0] if vul[0] != '' else ''
            item_value = vul[1] if vul[1] != '' else ''
            item_year = vul[2] if vul[2] != '' else ''
            sq = '(\'' + company[1] +'\',\''+company[3]+'\',\''+company[2]+'\',\'' +block_item_name+'\',\''+item_name+'\',\''+item_value+'\',\''+date+'\',\''+item_year + '\')' + ','
            sql += sq
        cur.execute(sql[0:len(sql)-1])

    time.sleep(1)
conn.commit()
cur.close()
conn.close()

