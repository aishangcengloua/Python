import requests

headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36'
    }
url = "http://www.whatismyip.com.tw/"

response = requests.get(url = url, headers = headers, proxies = {'http' : '115.152.233.62'})
response.encoding = response.apparent_encoding
page_text = response.text
with open('ip.html', 'w', encoding = 'utf-8') as fp :
    fp.write(page_text)