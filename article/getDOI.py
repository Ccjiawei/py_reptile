import requests
from bs4 import BeautifulSoup


def get_doi_from_nature_research(article_url):
    response = requests.get(article_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        doi_element = soup.find('meta', {'name': 'DOI'})
        if doi_element:
            return doi_element['content']
    return None

def get_pageNums(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ul = soup.find('ul', {'class': 'c-pagination'})
        li_items = ul.find_all('li')
        # 获取倒数第二个li标签
        if li_items:
            second_last_li = li_items[-2]
            print(second_last_li.text)
            page_last = second_last_li.attrs['data-page']
            #print(page_last)
            return int(page_last)
        else:
            print('ul标签中没有li标签')
    return None

def get_articlesListByPage(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        a_items = soup.find_all('a', 'c-card__link u-link-inherit')
        # 获取倒数第二个li标签
        articles_url_list = []
        for a in a_items:
            href = a.attrs['href']
            print(href)
            articles_url_list.append(href)
        return articles_url_list
    return None

#research_articles_url = "https://www.nature.com/nature/research-articles?type=article&year=2024";

path = "C:/Users/Admin/Desktop/DOI/"
# 总页数
half_url = "https://www.nature.com/nature/research-articles?searchType=journalSearch&sort=PubDate&type=article&year=2024&page=";
pagenums = get_pageNums(half_url + '1')

#循环
page = 1
while page < pagenums:
    research_articles_url = half_url + str(page)
    articles_url_list = get_articlesListByPage(research_articles_url)

    # 保存doi
    # ab:以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
    with open(path + "DOI.txt", "a+") as temp:
        for doi in articles_url_list:
            parts = doi.split('/', 2)  # 分割2次，返回列表最多包含3个元素
            if len(parts) > 1:
                temp.write(parts[2] + '\n')  # 换行
            else:
                continue

    page += 1

# 示例文章URL
#article_url = 'https://www.nature.com/articles/s41586-024-07471-4'
#doi = get_doi_from_nature_research(article_url)
#print(doi)


