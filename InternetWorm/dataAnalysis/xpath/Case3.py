#爬取所有城市的名称

import requests
from lxml import etree

if __name__ == "__main__" :
    # headers = headers = {
    #     'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36"
    # }
    # url = "https://www.aqistudy.cn./historydata/"
    # parse = etree.HTMLParser(encoding="utf-8")
    # page_text = requests.get(url = url, headers = headers, verify=False).text
    #
    # tree = etree.HTML(page_text, parser = parse)
    # hot_li_list = tree.xpath('//div[@ class = "hot"]//ul[@ class = "unstyled"]/li')
    # print(len(hot_li_list))
    # hot_city_names = []
    # for li in hot_li_list :
    #     hot_city_names.append(li.xpath('./a/text()')[0])
    #
    # all_city_names = []
    # all_li_list = tree.xpath('//div[@ class = "all"]//div[@ class = "bottom"]/ul/div[2]/li')
    # for li in all_li_list :
    #     all_city_names.append(li.xpath('./a/text()')[0])
    #
    # print(hot_city_names)
    # print(all_city_names)
    headers = headers = {
        'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36"
    }
    url = "https://www.aqistudy.cn./historydata/"
    parse = etree.HTMLParser(encoding="utf-8")
    page_text = requests.get(url = url, headers = headers, verify=False).text

    tree = etree.HTML(page_text, parser = parse)
    #热门城市和全部城市的标签不同：
    #热门城市：div/ul/li/a
    #全部城市：div/ul/div[2]/li/a
    all_city_names = []
    a_list = tree.xpath('//div[@ class = "bottom"]/ul/li/a | //div[@ class = "bottom"]/ul/div[2]/li/a')
    for a in a_list :
        all_city_names.append(a.xpath('./text()')[0])
    print(all_city_names, len(all_city_names))