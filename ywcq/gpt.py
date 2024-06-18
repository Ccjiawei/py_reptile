import requests
from bs4 import BeautifulSoup

url = 'https://www.investing.com/equities/StocksFilter?index_id=17'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', {'id': 'cross_rate_markets_stocks_1'})
rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    if cols:
        name = cols[1].text.strip()
        symbol = cols[2].text.strip()
        print(symbol, name)