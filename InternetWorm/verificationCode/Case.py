#使用打码平台识别验证码的流程：
    # -将验证码图片进行本地下载
    # -调用平台提供的示例代码进行图片识别

import requests
import chaojiying
import cv2 as cv
from lxml import etree

if __name__ == "__main__" :
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36'
    }
    url = "https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx"
    page_text = requests.get(url = url, headers = headers).text
    parse = etree.HTMLParser(encoding = "utf-8")
    tree = etree.HTML(page_text, parser = parse)

    img_src = "https://so.gushiwen.cn/" + tree.xpath('///*[@id="imgCode"]/@src')[0]
    img_data = requests.get(url = img_src, headers = headers).content

    with open('imgCode.jpg', 'wb') as fp :
        fp.write(img_data)

    chaojiying = chaojiying.Chaojiying_Client('1845386579czh', '140409chen', '929228')
    with open('imgCode.jpg', 'rb') as fp :
        img = fp.read()
    print(chaojiying.PostPic(img, 1902))
