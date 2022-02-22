# requests模块模拟浏览器对数据进行抓取
# 流程：
# 1.指定url
# 2.发起请求
# 3.获取响应数据
# 4.持久化存储
# -*- coding:utf-8 -*-
import requests

if __name__ == "__main__":
    url = 'https://www.sogou.com/'
    # get方法返回一个响应对象
    response = requests.get(url = url)
    # text返回字符串形式的响应数据
    page_text = response.text
    print(page_text)
    with open('sogou.html', 'w', encoding = 'utf-8') as fp:
        fp.write(page_text)
    print('end!')
