from bs4 import BeautifulSoup as bs
from time import sleep
import re
import pandas as pd
from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc

browser = uc.Chrome()
browser.get('https://cn.investing.com/equities/t-d-holdings,-inc.-financial-summary')

sleep(6)

# browser.maximize_window()
sleep(5)
browser.find_element(by=By.XPATH, value='//*[@id="widget"]').click()

sleep(5)
browser.find_element(by=By.XPATH, value='//*[@id="startDate"]').clear()
browser.find_element(by=By.XPATH, value='//*[@id="startDate"]').send_keys('2019/01/01')

sleep(2)
browser.find_element(by=By.XPATH, value='//*[@id="endDate"]').clear()
browser.find_element(by=By.XPATH, value='//*[@id="endDate"]').send_keys('2020/10/29')

sleep(2)
browser.find_element(by=By.XPATH, value='//*[@id="applyBtn"]').click()
sleep(8)

print(browser.current_url)
print(browser.page_source)
a = browser.page_source
soup = bs(a, "lxml")
content = soup.find('div', id="results_box").find_all('tbody')[0].find_all('tr')

resultdf = pd.DataFrame({'date': [],
                         'close': [],
                         'open': [],
                         'high': [],
                         'low': []})
for tr in content:
    td = tr.find_all('td')
    date = re.findall(r'<td[^>]*>(.*?)</td>', str(td[0]), re.I | re.M)[0]
    resultdf = resultdf.append(pd.DataFrame({'date': [date],
                                             'close': [float(td[1].get("data-real-value"))],
                                             'open': [float(td[2].get("data-real-value"))],
                                             'high': [float(td[3].get("data-real-value"))],
                                             'low': [float(td[4].get("data-real-value"))]}), ignore_index=True)
