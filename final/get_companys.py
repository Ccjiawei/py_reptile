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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
    }
headers_api = {
        'Host': 'api.investing.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183'
    }

# 变量
stock_company = 'cn_stock_company'
countryId = '37'
# 5-美国   35-日本   22-法国   46-台湾  11-韩国   4-英国   17-德国   14-印度  6-加拿大  25-澳大利亚
# 72-欧元区  32-巴西  9-瑞典  178-越南  42-马来西亚  41-泰国
# 56-俄罗斯 48-印度尼西亚 53-波兰 7-墨西哥 36-新加坡 63-土耳其 10-意大利 23-以色列  44-巴基斯坦  47-孟加拉国  54-奥地利
# 企业列表
companys = []
url_company = 'https://api.investing.com/api/financialdata/assets/equitiesByCountry/default'

page = 0

params={
    'fields-list':'id,name,symbol,high,low,last,lastPairDecimal,change,changePercent,volume,time,isOpen,url,flag,countryNameTranslated,exchangeId,performanceDay,performanceWeek,performanceMonth,performanceYtd,performanceYear,performance3Year,technicalHour,technicalDay,technicalWeek,technicalMonth,avgVolume,fundamentalMarketCap,fundamentalRevenue,fundamentalRatio,fundamentalBeta',
    'country-id': countryId,
    'page': page,
    'page-size':'50',
    'include-major-indices':'false',
    'include-additional-indices':'false',
    'include-primary-sectors':'false',
    'include-other-indices':'false',
    'limit':'0'
}

cookies_str='udid=87239b2fc7b5e7f470a85277942a08d4; _cc_id=e24f34d2a1e93a266807faa4f77b45cf; _hjSessionUser_174945=eyJpZCI6ImY3ZjUzY2Q5LWQwZmQtNWU2Ny04ZDU5LTY4NzMwOTMzMjBhNyIsImNyZWF0ZWQiOjE2ODU1MjExNzMyNzQsImV4aXN0aW5nIjp0cnVlfQ==; _fbp=fb.1.1685523614507.1922550153; finboxio-production:jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2aXNpdG9yX2lkIjoidi1Yb1FLNGVGNGZkSmotb2JEbmxZd08iLCJmaXJzdF9zZWVuIjoiMjAyMy0wNi0xNFQwMzoxMzo1NC4yNzNaIiwiY2FwdGNoYV92ZXJpZmllZCI6ZmFsc2UsIm11c3RfcmV2ZXJpZnkiOmZhbHNlLCJwcmV2aWV3X2FjY2VzcyI6eyJhc3NldHNfdmlld2VkIjpbIk5BU0RBUUdTOkFBUEwiLCJOWVNFOkJBIl0sImFzc2V0c19tYXgiOjUsInZhbGlkX3VudGlsIjoiMjAyMy0wNi0xNFQwMzoxODo1NC4wMDBaIn0sInJvbGVzIjpbImFub255bW91cyIsInZpc2l0b3IiLCJpbnZlc3RpbmciXSwiYm9vc3RzIjpbXSwiYXNzZXRzIjpbXSwicmVnaW9ucyI6W10sInNjb3BlcyI6WyJyb2xlOmFub255bW91cyIsInJvbGU6dmlzaXRvciIsInJvbGU6aW52ZXN0aW5nIl0sImZvciI6IjEwMy4xODYuMTEzLjIxNSIsImV4cCI6MTY4NjgxNTg0OCwiaWF0IjoxNjg2ODE1NTQ4fQ.d1FRXCn5LHpCMK3HYx52JsvI69FMN8Wj-WMB_h-qeaw; finboxio-production:jwt.sig=wRp7kA3fg5t57beJQdR-Iklp4uA; adBlockerNewUserDomains=1687657503; pm_score=clear; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jun+30+2023+16%3A41%3A43+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202303.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=48b83713-7d27-493b-9ae4-0cc9e7e298be&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=US%3BOR; OptanonAlertBoxClosed=2023-06-30T08:41:43.371Z; im_sharedid=9bc83317-baa8-4ea0-8d55-4eba793cc7aa; panoramaId=82ff57c3c7c651892bdfce0f4eb316d53938878fcc97b246f8d670ae0a0bc52f; panoramaIdType=panoIndiv; panoramaId_expiry=1690852672676; _gid=GA1.2.1800572276.1690424449; browser-session-counted=true; user-browser-sessions=16; smd=87239b2fc7b5e7f470a85277942a08d4-1690507880; __cflb=02DiuEaBtsFfH7bEbN4qQwLpwTUxNYEGzBRZqfTKDHFcY; gcc=TW; gsc=TNN; _hjSession_174945=eyJpZCI6ImNjMGIwMTk0LWZmYWUtNDIyNy1hZTEwLWYyZjkwNmZjMjgyMSIsImNyZWF0ZWQiOjE2OTA1MzI4OTg2MTYsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; __cf_bm=wQT.AlCxy1N0novKyT71kMfDoTDz3.bWl5qlcaymfas-1690533168-0-Achey6sQEny0FJgt/k01qusafhAs9pGayyQIeEQVaN1clAYgu0Wimlxbo56b02/Pmqt/njdU+hq6b5GjJMmzO0w=; __gads=ID=1062bebc74476d7f:T=1686809853:RT=1690533255:S=ALNI_MaaK1Gkiq9jT2NL3DWR4MYe0wNl6Q; __gpi=UID=00000c13a127fa05:T=1686809853:RT=1690533255:S=ALNI_MYOneuJQPPw88O-7aWsnES94iFwGA; invpc=11; _ga=GA1.1.1966509239.1686809841; page_view_count=11; lifetime_page_view_count=102; cto_bundle=ixd3A19JWUhkRFFyeG5GdktRUTNqRTJQVlp0ZjZHRnFsV3pteEhsU29SUVE0ZDh3aklvNFhtbkJoNSUyQmdoRUI3cmk4R0xNVSUyRlp6dUdjWGRqM2hlTnNLcGFrWGxTcTlFckJYeU8ySXB3M1prV2R0UTgyQk5oNCUyQkNhV1AzY2M0eFRIJTJGUjZDcDgxYjYlMkJhYXRrJTJGMVQlMkZVYlBtNlolMkZqWjUzR0ZVUVVNNUpzR29oWmd6MUxFRUZhVTFIQ2owRVBsdnlsUG1vamtk; _ga_C4NDLGKVMK=GS1.1.1690532897.53.1.1690533369.1.0.0'
cookies_dict = {cookie.split('=', 1)[0]: cookie.split('=', 1)[-1] for cookie in cookies_str.split('; ')}

response = get_json(cookie=cookies_dict, url=url_company, params=params, headers=headers_api)

if response.status_code != 200:
    print("获取数据总量--请求访问拒绝...url===>"+str(url_company))
    sys.exit()

res = json.loads(response.text)  # 转为字典
total = res['total']  # 11502-us    3925-japan    803-franch   1846-tw    2711-kr    2761-uk   4579-de  6466-ind  4853-ca  2123-au  1394-no   1416-br   10001-my
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
        # exchange_name = ''
        # if com['Url'] != '':
        #     url_exchange = 'https://cn.investing.com' + com['Url']
        #
        #     try:
        #         page_exchange = get_page(url_exchange, headers=headers, params=None)
        #     except Exception as e:
        #         print(f"出现了异常{e}")
        #         sys.exit()
        #
        #     exchange_name_list = page_exchange.find_all('span', 'text-xs ml-1') or page_exchange.find_all('span', 'text-xs leading-4 font-normal overflow-hidden text-ellipsis flex-shrink')
        #     exchange_name = exchange_name_list[0].text if len(exchange_name_list) > 0 else ''
        #     currency_list = page_exchange.find_all('span', 'instrument-metadata_text__Rq22W font-bold')
        #     currency = currency_list[0].text if len(currency_list) > 0 else ''
        # cc = [com['Id'], com['Symbol'], exchange_name, currency, com['Url'], com['Name']]

        # 交易所
        exchange_name = ''
        exchangeId = com['ExchangeId']
        # if(exchangeId == '3'):
        #     exchange_name = '伦敦'
        # if(exchangeId == '153'):
        #     exchange_name = 'Aquis Exchange'

        # if (exchangeId == '105'):
        #     exchange_name = 'TradeGate'
        # if (exchangeId == '104'):
        #     exchange_name = '德国法兰克福'
        # if (exchangeId == '106'):
        #     exchange_name = '慕尼黑'
        # if (exchangeId == '107'):
        #     exchange_name = '斯图加特'
        # if (exchangeId == '123'):
        #     exchange_name = '杜塞尔多夫证券交易所'
        # if (exchangeId == '112'):
        #     exchange_name = '柏林'
        # if (exchangeId == '125'):
        #     exchange_name = '汉堡证券交易所'
        # if (exchangeId == '4'):
        #     exchange_name = '法兰克福'

        # if (exchangeId == '46'):
        #     exchange_name = '印度NSE'
        # if (exchangeId == '74'):
        #     exchange_name = '孟买BSE'

        # if (exchangeId == '127'):
        #     exchange_name = 'CBOE加拿大'
        # if (exchangeId == '109'):
        #     exchange_name = '加拿大CSE'
        # if (exchangeId == '51'):
        #     exchange_name = '加拿大多伦多'
        # if (exchangeId == '108'):
        #     exchange_name = '多伦多创业板'

        # if (exchangeId == '18'):
        #     exchange_name = '澳大利亚悉尼'
        # if (exchangeId == '121'):
        #     exchange_name = 'BATS Europe'
        # if (exchangeId == '47'):
        #     exchange_name = '巴西圣保罗'
        # if (exchangeId == '113'):
        #     exchange_name = '美联储系统公开市场账户'

        # if (exchangeId == '114'):
        #     exchange_name = '瑞典创业板NGM'
        # if (exchangeId == '12'):
        #     exchange_name = '瑞典斯德哥尔摩'
        # if (exchangeId == '141'):
        #     exchange_name = '瑞典聚焦股票市场'


        # if (exchangeId == '122'):
        #     exchange_name = '胡志明市证券交易所'
        # if (exchangeId == '72'):
        #     exchange_name = '越南河内'

        # if (exchangeId == '62'):
        #     exchange_name = '马来西亚吉隆坡'

        # if (exchangeId == '69'):
        #     exchange_name = '泰国'
        # if (exchangeId == '40'):
        #     exchange_name = '莫斯科'
        # if (exchangeId == '57'):
        #     exchange_name = '印尼雅加达'
        # if (exchangeId == '25'):
        #     exchange_name = '波兰华沙'
        # if (exchangeId == '144'):
        #     exchange_name = 'BIVA'
        # if (exchangeId == '53'):
        #     exchange_name = '墨西哥'

        # if (exchangeId == '19'):
        #     exchange_name = '新加坡'
        # if (exchangeId == '49'):
        #     exchange_name = '土耳其伊斯坦布尔'
        # if (exchangeId == '6'):
        #     exchange_name = '米兰'
        # if (exchangeId == '26'):
        #     exchange_name = '以色列特拉维夫'
        # if (exchangeId == '63'):
        #     exchange_name = '巴基斯坦卡拉奇'
        # if (exchangeId == '115'):
        #     exchange_name = '孟加拉达卡'
        # if (exchangeId == '17'):
        #     exchange_name = '奥地利维也纳'
        # if (exchangeId == '8'):
        #     exchange_name = '挪威奥斯陆'
        # if (exchangeId == '22'):
        #     exchange_name = '南非约翰内斯堡'
        # if (exchangeId == '65'):
        #     exchange_name = '菲律宾'
        # if (exchangeId == '37'):
        #     exchange_name = '阿根廷'
        # if (exchangeId == '5'):
        #     exchange_name = '瑞士'
        # if (exchangeId == '67'):
        #     exchange_name = '斯里兰卡'
        # if (exchangeId == '28'):
        #     exchange_name = '沙特阿拉伯'
        # if (exchangeId == '33'):
        #     exchange_name = '埃及'
        # if (exchangeId == '146'):
        #     exchange_name = 'LATIBEX'
        # if (exchangeId == '11'):
        #     exchange_name = '西班牙马德里'
        # if (exchangeId == '43'):
        #     exchange_name = '罗马尼亚'
        # if (exchangeId == '16'):
        #     exchange_name = '芬兰赫尔辛基'
        # if (exchangeId == '42'):
        #     exchange_name = '智利圣地亚哥'
        # if (exchangeId == '64'):
        #     exchange_name = '秘鲁利马'
        # if (exchangeId == '15'):
        #     exchange_name = '丹麦哥本哈根'
        # if (exchangeId == '14'):
        #     exchange_name = '比利时布鲁塞尔'
        # if (exchangeId == '29'):
        #     exchange_name = '约旦安曼'
        # if (exchangeId == '41'):
        #     exchange_name = '希腊雅典'
        # if (exchangeId == '27'):
        #     exchange_name = '科威特'
        # if (exchangeId == '30'):
        #     exchange_name = '迪拜'
        # if (exchangeId == '100'):
        #     exchange_name = '阿布扎比'
        # if (exchangeId == '83'):
        #     exchange_name = '新西兰'
        # if (exchangeId == '96'):
        #     exchange_name = '拉各斯'
        # if (exchangeId == '7'):
        #     exchange_name = '阿姆斯特丹'
        # if (exchangeId == '124'):
        #     exchange_name = '牙买加'
        # if (exchangeId == '116'):
        #     exchange_name = '伊拉克'
        # if (exchangeId == '23'):
        #     exchange_name = '匈牙利布达佩斯'
        # if (exchangeId == '44'):
        #     exchange_name = '保加利亚'
        # if (exchangeId == '117'):
        #     exchange_name = '哈萨克斯坦'
        # if (exchangeId == '86'):
        #     exchange_name = '毛里求斯'
        # if (exchangeId == '48'):
        #     exchange_name = '突尼斯'
        # if (exchangeId == '36'):
        #     exchange_name = '摩洛哥卡萨布兰卡'
        # if (exchangeId == '129'):
        #     exchange_name = '蒙古证券交易所'
        # if (exchangeId == '78'):
        #     exchange_name = '塞浦路斯'
        # if (exchangeId == '55'):
        #     exchange_name = '哥伦比亚'
        # if (exchangeId == '101'):
        #     exchange_name = '波斯尼亚'
        # if (exchangeId == '10'):
        #     exchange_name = '葡萄牙里斯本'
        # if (exchangeId == '128'):
        #     exchange_name = '黑山证券交易所'
        # if (exchangeId == '35'):
        #     exchange_name = '卡塔尔多哈'

        # if (exchangeId == '32'):
        #     exchange_name = '巴勒斯坦拉姆安拉'
        # if (exchangeId == '56'):
        #     exchange_name = '布拉格'
        # if (exchangeId == '102'):
        #     exchange_name = '贝尔格莱德'
        # if (exchangeId == '111'):
        #     exchange_name = '西非区域'
        # if (exchangeId == '58'):
        #     exchange_name = '爱尔兰'
        # if (exchangeId == '70'):
        #     exchange_name = '乌克兰'
        # if (exchangeId == '39'):
        #     exchange_name = '巴林'
        # if (exchangeId == '45'):
        #     exchange_name = '克罗地亚'
        # if (exchangeId == '52'):
        #     exchange_name = '冰岛'
        # if (exchangeId == '82'):
        #     exchange_name = '马尔他'
        # if (exchangeId == '81'):
        #     exchange_name = '立陶宛'
        # if (exchangeId == '34'):
        #     exchange_name = '黎巴嫩贝鲁特'
        # if (exchangeId == '99'):
        #     exchange_name = '赞比亚'
        # if (exchangeId == '61'):
        #     exchange_name = '卢森堡'
        # if (exchangeId == '77'):
        #     exchange_name = '博茨瓦纳'
        # if (exchangeId == '71'):
        #     exchange_name = '委内瑞拉'
        # if (exchangeId == '79'):
        #     exchange_name = '爱沙尼亚塔林'
        # if (exchangeId == '88'):
        #     exchange_name = '坦桑尼亚'
        # if (exchangeId == '76'):
        #     exchange_name = '乌干达'
        # if (exchangeId == '84'):
        #     exchange_name = '斯洛伐克'
        # if (exchangeId == '91'):
        #     exchange_name = '哥斯达黎加'
        # if (exchangeId == '90'):
        #     exchange_name = '卢旺达'
        # if (exchangeId == '59'):
        #     exchange_name = '肯尼亚'

        if (exchangeId == '54'):
            exchange_name = '上海'
        if (exchangeId == '103'):
            exchange_name = '深圳'
        cc = [com['Id'], com['Symbol'], exchange_name, '', com['Url'], com['Name']]


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