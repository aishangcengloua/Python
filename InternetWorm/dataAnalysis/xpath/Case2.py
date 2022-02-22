#解析下载图片数据
import requests
import os
from lxml import etree

if __name__ == "__main__" :
    parse = etree.HTMLParser(encoding = "utf-8")
    headers = {
        'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36"
    }
    url = "https://pic.netbian.com/4kmeinv/"
    page_text = requests.get(url = url, headers = headers)
    # page_text.encoding = page_text.apparent_encoding
    page_text = page_text.text
    tree = etree.HTML(page_text, parser = parse)
    li_list = tree.xpath('//ul[@ class = "clearfix"]/li')

    if not os.path.exists('picLibs') :
        os.mkdir('picLibs')

    for li in li_list :
        img_name = li.xpath('./a/img/@alt')[0] + '.jpg'
        #通用处理中文乱码的解决方案
        img_name = img_name.encode('iso-8859-1').decode('gbk')
        img_src = "https://pic.netbian.com/" + li.xpath('./a/img/@src')[0]
        img_data = requests.get(url = img_src, headers = headers).content

        with open('picLibs/' + img_name, 'wb') as fp :
            fp.write(img_data)