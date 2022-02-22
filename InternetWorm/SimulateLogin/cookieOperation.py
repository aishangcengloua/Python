#模拟登录后爬取当前用户的相关的用户信息(个人主页信息)
#模拟登录古诗文网
#1.获取验证码图片的文字数， 2.对post请求发送(处理请求参数)， 3.对响应数据进行持久化处理
#使用打码平台识别验证码的流程：
    # -将验证码图片进行本地下载
    # -调用平台提供的示例代码进行图片识别

import requests
import chaojiying
import cv2 as cv
from lxml import etree

if __name__ == "__main__" :
    #验证码图片的捕获和识别
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36'
    }
    url = "https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx"
    session = requests.Session()
    page_text = session.get(url = url, headers = headers).text
    parse = etree.HTMLParser(encoding = "utf-8")
    tree = etree.HTML(page_text, parser = parse)

    img_src = "https://so.gushiwen.cn/" + tree.xpath('///*[@id="imgCode"]/@src')[0]
    img_data = session.get(url = img_src, headers = headers).content

    with open('imgCode.jpg', 'wb') as fp :
        fp.write(img_data)

    #验证码识别
    chaojiying = chaojiying.Chaojiying_Client('1845386579czh', '140409chen', '929228')
    with open('imgCode.jpg', 'rb') as fp :
        img = fp.read()
    result = chaojiying.PostPic(img, 1902)["pic_str"]

    #post请求的发送
    login_url = 'https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx'
    __VIEWSTATE = tree.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
    __VIEWSTATEGENERATOR = tree.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
    data = {
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
        'from': 'http://so.gushiwen.cn/user/collect.aspx',
        'email': 'zhihonghaha@outlook.com',
        'pwd': '140409chen',
        'code': result,
        'denglu': '登录'
    }
    # print(result)
    # 使用Session对象提交请求，相当于在浏览器中连续操作网页，而如果直接使用```request.post()```,
    # 则相当没提交一次请求，则打开一个浏览器，我们在实际使用浏览器的经验告诉我们，这样是不行的
    # session = requests.Session()
    response = session.post(url = login_url, headers = headers, data = data)
    # 验证模拟登录是否成功，如果是200就是成功了
    print(response.status_code)
    login_page_text = response.text
    with open('gushiwen.html', 'w', encoding = 'utf-8') as fp :
        fp.write(login_page_text)

    # 爬取当前用户的个人主页对应的页面数据
    detail_url = "https://so.gushiwen.cn/mingjus/"
    #手动cookie处理
    # heades = {
    #     'Cookie' : 'ASP.NET_SessionId=so1zgavln0nzb0obdis31ucj; wsEmail=zhihonghaha%40outlook.com; Hm_lvt_9007fab6814e892d3020a64454da5a55=1645504554,1645513419,1645513466; codeyzgswso=1093ebd36c926430; gsw2017user=2500596%7c00CBF504D99837105F3B1ED9EE1BAD2C; login=flase; wxopenid=defoaltid; gswZhanghao=zhihonghaha%40outlook.com; gswEmail=zhihonghaha%40outlook.com; Hm_lpvt_9007fab6814e892d3020a64454da5a55=1645514243'
    # }
    detail_page_text = session.get(url=detail_url, headers=headers).text
    with open('czh.html', 'w', encoding='utf-8') as fp:
        fp.write(detail_page_text)
