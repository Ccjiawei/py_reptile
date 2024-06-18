# coding:utf-8
# 股市企业-获取不同股市企业量

import datetime
import sys
import time
import requests
from bs4 import BeautifulSoup
import pymysql
import json
import math

def get_page(url, params=None, headers=None, proxies=None, timeout=None):
    response = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=timeout, stream=True)
    #print("解析网址：", response.url)
    page = BeautifulSoup(response.text, 'lxml')
    #print("响应状态码：", response.status_code)
    return page

def get_json(cookie, url, params=None, headers=None, proxies=None, timeout=None):
    response = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=timeout,cookies=cookie, stream=True)
    return response

headers = {
        'Host': 'cn.investing.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
headers_api = {
        'Host': 'api.investing.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58'
    }

# 变量
stock_company = 'uk_stock_company'
countryId = '4'  # 5-美国   35-日本   22-法国   46-台湾  11-韩国   4-英国

#企业列表
companys = []
url_company = 'https://cn.investing.com/stock-screener/Service/SearchStocks'   # 筛股器

page = 1

params={
    "country[]": 4,
    "sector": "32,30,25,36,26,33,35,34,27,28,31,24,29",
    "industry": "186,198,201,189,194,227,192,206,230,175,211,216,177,210,209,213,225,197,185,223,173,196,231,188,193,181,184,179,226,208,205,229,228,183,224,190,174,203,172,212,221,222,215,180,191,232,182,217,187,219,214,195,178,220,176,204,207,218,200,202,199",
    "equityType": "ORD,DRC,Preferred,Unit,ClosedEnd,REIT,ELKS,OpenEnd,Right,ParticipationShare,CapitalSecurity,PerpetualCapitalSecurity,GuaranteeCertificate,IGC,Warrant,SeniorNote,Debenture,ETF,ADR,ETC",
    "pn": page,
    "order[col]": "eq_market_cap",
    "order[dir]": "d"
}

cookies_str='udid=5f7581f789d7859bc26bbff1e401ff40; _fbp=fb.1.1687922469810.470467589; _cc_id=bb03faa92e57e69904041443e3c3e74d; protectedMedia=100; pms={"f":100,"s":2}; _pbjs_userid_consent_data=3524755945110770; _imhb_exp_udid=a; pm_score=fraud; _hjSessionUser_174945=eyJpZCI6IjAzY2UyZWRmLTY3MDUtNTMxMS05ZDM3LTdiZDE4OTFhMzIzYyIsImNyZWF0ZWQiOjE2ODc5MjI3MDQ1NzcsImV4aXN0aW5nIjp0cnVlfQ==; adBlockerNewUserDomains=1687931966; trc_cookie_storage=taboola%2520global%253Auser-id%3D26014977-40e7-4041-868a-55d08ae8edd7-tuct6cb258e; user-browser-sessions=2; browser-session-counted=true; sunset_announcement_shown=1; _hjHasCachedUserAttributes=true; _gid=GA1.2.1095806926.1688114636; panoramaId_expiry=1688201044942; cto_bundle=Fo3US19pamsyUHhvcmNDZ3BMRGdRdk01aGpJdmtDQ0RGc2xUSHdPZE9hamI4JTJGbkNVcVQ3bWg1a1I2b3dGJTJCb0NUcjZncllXdWplVzlmSlolMkZEUGFHSVFvQm1QQ0Q5RGtwckFtWG5hZW5yTlg5eHdSJTJCNGlJSmlQYjB3R2lsZm41JTJCTE9sMVIlMkJuWXVreUZaemV6c3B3RGFMTTBiQ3clM0QlM0Q; PHPSESSID=b9pjkjb4c2osvpt59615n2vsj7; geoC=US; Hm_lvt_a1e3d50107c2a0e021d734fe76f85914=1687922518,1688114805; adsFreeSalePopUp=3; SideBlockUser=a%3A2%3A%7Bs%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A8%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A287%3Bs%3A10%3A%22pair_title%22%3Bs%3A6%3A%22Lloyds%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A28%3A%22%2Fequities%2Flloyds-banking-grp%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A280%3Bs%3A10%3A%22pair_title%22%3Bs%3A4%3A%22HSBC%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A23%3A%22%2Fequities%2Fhsbc-holdings%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A43351%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A26%3A%22%2Fequities%2Fhanall-biopharma%22%3B%7Di%3A3%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A103016%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A24%3A%22%2Fequities%2Fgrand-petroche%22%3B%7Di%3A4%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A102997%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A24%3A%22%2Fequities%2Ftai-roun-produ%22%3B%7Di%3A5%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A102981%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A20%3A%22%2Fequities%2Ftwn-cement%22%3B%7Di%3A6%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A404%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fequities%2Fcarrefour%22%3B%7Di%3A7%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A385%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A26%3A%22%2Fequities%2Fair-france---klm%22%3B%7D%7D%7Ds%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7D%7D; OptanonAlertBoxClosed=2023-06-30T08:53:38.825Z; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jun+30+2023+16%3A53%3A39+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202303.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=9ddb3731-19e2-44f2-9e7e-d6d1cb24f928&interactionCount=0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=US%3B; _data_browser=chrome; _im_last_pv=1688115312.1881920119; _im_session_id=1688115312.9213460043; session_id=1688115312.9213460043; user_id=1688115312.9213460043; _im_session_data=; _im_sampling=eyJhdWN0aW9uIjpmYWxzZX0=; _data_pm=e30=; _hjSessionUser_1863091=eyJpZCI6ImUzYWRhMDUxLTM3NDMtNTFkYi1iNTViLTZjNDIyOGI0MWY1ZiIsImNyZWF0ZWQiOjE2ODgxMTUzMTM2NTIsImV4aXN0aW5nIjpmYWxzZX0=; _im_fb=eyJmYmMiOiIiLCJmYnAiOiJmYi4xLjE2ODc5MjI0Njk4MTAuNDcwNDY3NTg5In0=; nyxDorf=OT4%2BbTRnN3VmMWxpYDszL2U1ZD03MjQoNDQ0NjQx; invpc=9; Hm_lpvt_a1e3d50107c2a0e021d734fe76f85914=1688115438; _ga=GA1.1.785084322.1687922470; page_view_count=8; lifetime_page_view_count=11; smd=5f7581f789d7859bc26bbff1e401ff40-1688117113; __cf_bm=fiz8LVhErYkHevWVL31FE5BNGZuPQVa5Rkg36Ge_5Ec-1688117278-0-AaNeyjpEXofkyMVKfivvzZjy+ik2QzEEjJricD3hbwBQm7KGpYDH2ksdtg6t0EqJfRDs16wLCwokP2e7L1c+u3E=; _gat_allSitesTracker=1; __gads=ID=d87e0c9c216eb94d:T=1687922469:RT=1688117514:S=ALNI_MZNM0pZEUpTc9XR99yvXfTwUH262Q; __gpi=UID=00000c1aafb30415:T=1687922469:RT=1688117514:S=ALNI_MbnTZeYk_tIS0DW7viyqMmLiBS3Bg; _ga_C4NDLGKVMK=GS1.1.1688114635.5.1.1688117516.60.0.0'
cookies_dict = {cookie.split('=', 1)[0]: cookie.split('=', 1)[-1] for cookie in cookies_str.split('; ')}

response = get_json(cookie=cookies_dict, url=url_company, params=params, headers=headers_api)

if response.status_code != 200:
    print("获取数据总量--请求访问拒绝...url===>"+str(url_company))
    sys.exit()

res = json.loads(response.text)  # 转为字典
total = res['totalCount']  # 11502-us    3925-japan    803-franch   1846-tw    2711-kr    2761-uk
pageSize = res['pageSize']
allpages = math.ceil(total / pageSize)

print('总数量'+str(total))
print('每页大小'+str(pageSize))
print('总页数'+str(allpages))
print('============开始============')

while(page < allpages):

    print("第" + str(page) + "页企业数据解析开始...")

    params["page"] = page

    # 发送请求
    response = get_json(cookie=cookies_dict, url=url_company, headers=headers_api, params=params)

    if response.status_code != 200:
        print("数据跑批--请求访问拒绝...url===>"+str(url_company))
        sys.exit()

    # 重置cookie有效期
    if '__cf_bm' in response.cookies:
        cfbm = requests.utils.dict_from_cookiejar(response.cookies)
        cookies_dict["__cf_bm"] = cfbm["__cf_bm"]

    # 数据处理
    res = json.loads(response.text)
    company_list = res['data']
    if len(company_list) <= 0:
        sys.exit()

    for com in company_list:
        exchange_name = ''
        if com['Url'] != '':
            url_exchange = 'https://cn.investing.com' + com['Url']

            try:
                page_exchange = get_page(url_exchange, headers=headers, params=None)
            except Exception as e:
                print(f"出现了异常{e}")
                sys.exit()

            exchange_name_list = page_exchange.find_all('span', 'text-xs ml-1') or page_exchange.find_all('span', 'text-xs leading-4 font-normal overflow-hidden text-ellipsis flex-shrink')
            exchange_name = exchange_name_list[0].text if len(exchange_name_list) > 0 else ''
            currency_list = page_exchange.find_all('span', 'instrument-metadata_text__Rq22W font-bold')
            currency = currency_list[0].text if len(currency_list) > 0 else ''
        cc = [com['Id'], com['Symbol'], exchange_name, currency, com['Url'], com['Name']]
        companys.append(cc)
        #time.sleep(0.5)#防封

    print("第"+str(page)+"页企业数据解析完成...")
    print("companys 收集完毕---------------------【共"+str(len(companys))+"家企业】")

    data_list = []
    i = 0
    counts = math.ceil(len(companys) / 500)

    while(i < counts):
        listc = companys[i*500: i*500+500 if i*500+500 < len(companys) else len(companys)]
        nm = 0
        while nm < len(listc):
            value = (listc[nm][0], listc[nm][1], listc[nm][2], listc[nm][3], listc[nm][4], listc[nm][5])
            data_list.append(value)
            nm += 1
        i += 1

    conn = pymysql.connect(host='81.68.197.104', database='python_test', password='Baiwa@0601', port=3307, user='root',
                           charset='utf8')
    while True:
        try:
            cs = conn.cursor()  # 获取游标
            cs.executemany("insert into " + stock_company + " (comid,symbol,exchange_name,currency,url,name) values(%s,%s,%s,%s,%s,%s)", data_list)
            conn.commit()
            cs.close()
            conn.close()
            print('入库OK')
            print('')
            break
        except Exception as error:
            conn.ping(True)

    page += 1
    companys = []