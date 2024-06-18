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

def get_json(cfbm, url, params=None, headers=None, proxies=None, timeout=None):

    c = 'adBlockerNewUserDomains=1684980225; udid=5964289634f7dbef26f12b5ff72c117f; _fbp=fb.1.1685328201542.1938040468; _gid=GA1.2.498094278.1685328203; _cc_id=e24f34d2a1e93a266807faa4f77b45cf; pm_score=fraud; reg_trk_ep=download%20data; _hjSessionUser_174945=eyJpZCI6IjEwNmI0NzYwLTY0NTAtNTdmNi04NjE5LTlhZTVlMTJhZGFjZCIsImNyZWF0ZWQiOjE2ODUzMjg2NzIxOTksImV4aXN0aW5nIjp0cnVlfQ==; OptanonAlertBoxClosed=2023-05-30T09:25:26.421Z; OptanonConsent=isGpcEnabled=0&datestamp=Tue+May+30+2023+17%3A25%3A38+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202303.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=dfc775ef-a97d-4699-b325-f97a7e7e9de0&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=US%3BOR; browser-session-counted=true; user-browser-sessions=4; bfp_sn_rf_8b2087b102c9e3e5ffed1c1478ed8b78=Direct; bfp_sn_rt_8b2087b102c9e3e5ffed1c1478ed8b78=1685498161430; panoramaId_expiry=1685591445918; __cflb=02DiuEaBtsFfH7bEbN4qQwLpwTUxNYEGyTxiDrpCBUUUc; invpc=15; page_view_count=15; smd=5964289634f7dbef26f12b5ff72c117f-1685514033; gcc=HK; gsc=HCW; _hjIncludedInSessionSample_174945=0; _hjSession_174945=eyJpZCI6IjdiNzA4MmI4LTg3MDctNDI4MC05YjhlLTVmMmVlMWE2NWY2YiIsImNyZWF0ZWQiOjE2ODU1MTQwNjk0MzksImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; cto_bundle=9GlRw19hbmVUSkxIeDhHVklWcUFrTkFpb2t2d1I3VkxjV2lTUTBlaExqVUtSQkZzWjZadHRUUjBYMzI3NWhLdzNla0pRc2pBOXRvQkcxckNUN08xdUFqd2VtamVNeWElMkZMdjdsVklqcTZwcEJNYXZpYjZIYzVFb1RYMjhETlM4czEya0Q1WTJETkFGcTdLY3A0dDZHNnNmJTJGN2V3JTNEJTNE; _ga_C4NDLGKVMK=GS1.1.1685514033.18.1.1685515744.54.0.0; __gads=ID=976bfab3dbf59a44:T=1684980229:RT=1685515745:S=ALNI_MbxuJheMS5tT0rSsHbIJptP64NHQw; __gpi=UID=00000c0a52d945d6:T=1684980229:RT=1685515745:S=ALNI_MaTd-8k2C5lSyKxbNjhoNR1fiiu2g; _ga=GA1.2.1717928824.1684980228; __cf_bm='+cfbm
    cookie = {'cookie': c}
    response = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=timeout,cookies=cookie)
    return response

headers = {
        'Host': 'cn.investing.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
    }
headers_api = {
        'Host': 'api.investing.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
    }
#企业列表
companys = []
url_company = 'https://api.investing.com/api/financialdata/assets/equitiesByCountry/default' \
              '?fields-list=id%2Cname%2Csymbol%2Chigh%2Clow%2Clast%2ClastPairDecimal%2Cchange%2CchangePercent%2Cvolume%2Ctime%2CisOpen%2Curl%2Cflag%2CcountryNameTranslated%2CexchangeId%2CperformanceDay%2CperformanceWeek%2CperformanceMonth%2CperformanceYtd%2CperformanceYear%2Cperformance3Year%2CtechnicalHour%2CtechnicalDay%2CtechnicalWeek%2CtechnicalMonth%2CavgVolume%2CfundamentalMarketCap%2CfundamentalRevenue%2CfundamentalRatio%2CfundamentalBeta' \
              '&country-id=5&page=0&page-size=500&include-major-indices=false' \
              '&include-additional-indices=false&include-primary-sectors=false&include-other-indices=false&limit=0'

cfbm = 'a24hgb_uR2LRvUWdouDXdX.IiJngqta2EnEAnCx8crg-1686100236-0-AR9ItkDIXrdPhxDyYD/ClaQhC3EKA+Idq96z8i6bMebA5iD+3wcqG6qW0k5tmOSW0FgChFigURp04oOmfLJb9W0='

response = get_json(cfbm,url_company, headers=headers_api)

res = json.loads(response.text)  # 转为字典
total = res['total']
pageSize = res['pageSize']
allpages = math.ceil(total / pageSize)

page = 0
while(page < allpages):
    url_company = 'https://api.investing.com/api/financialdata/assets/equitiesByCountry/default'\
                  '?fields-list=id%2Cname%2Csymbol%2Chigh%2Clow%2Clast%2ClastPairDecimal%2Cchange%2CchangePercent%2Cvolume%2Ctime%2CisOpen%2Curl%2Cflag%2CcountryNameTranslated%2CexchangeId%2CperformanceDay%2CperformanceWeek%2CperformanceMonth%2CperformanceYtd%2CperformanceYear%2Cperformance3Year%2CtechnicalHour%2CtechnicalDay%2CtechnicalWeek%2CtechnicalMonth%2CavgVolume%2CfundamentalMarketCap%2CfundamentalRevenue%2CfundamentalRatio%2CfundamentalBeta'\
                  '&country-id=5&page='+str(page)+'&page-size=500&include-major-indices=false'\
                  '&include-additional-indices=false&include-primary-sectors=false&include-other-indices=false&limit=0'
    params = None
    response = get_json(cfbm, url_company, headers=headers_api, params=params)
    cookies = response.cookies
    if '__cf_bm' in cookies:
        cfbm = cookies['__cf_bm']

    res = json.loads(response.text)
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

    inc_list = page_inc.find_all('table', 'genTbl reportTbl')
    bal_list = page_bal.find_all('table', 'genTbl reportTbl')
    cas_list = page_cas.find_all('table', 'genTbl reportTbl')

    if len(inc_list) > 0:
        inc_list = page_inc.find_all('table', 'genTbl reportTbl')[0]
    if len(bal_list) > 0:
        bal_list = page_bal.find_all('table', 'genTbl reportTbl')[0]
    if len(cas_list) > 0:
        cas_list = page_cas.find_all('table', 'genTbl reportTbl')[0]

    # 比率数据抽取 收益、负债、现金流
    n = 0
    while(n < len(summary_list)):
        info_list = summary_list[n].find_all('div', 'info float_lang_base_2')
        block_item_name = summary_list[n].find_all('h3')[0].a.text if len(summary_list[n].find_all('h3')) > 0 else ''
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

