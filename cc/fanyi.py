import requests

# 准备翻译的数据
kw = input("请输入要翻译的词语：")
ps = {"kw": kw}
# 准备伪造请求
headers = {
    # User-Agent：首字母大写，表示请求的身份信息；一般直接使用浏览器的身份信息，伪造爬虫请求
    # 让浏览器认为这个请求是由浏览器发起的[隐藏爬虫的信息]
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome / 85.0.4183.83Safari / 537.36Edg / 85.0.564.41"
}
# 发送POST请求，附带要翻译的表单数据--以字典的方式进行传递
response = requests.post("https://fanyi.baidu.com/sug", data=ps)
# 打印返回的数据
# print(response.content)
print(response.content.decode("unicode_escape"))

#
