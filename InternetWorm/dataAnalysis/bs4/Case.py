#爬取三国演义所有的章节标题和章节内容

import requests
import os
from bs4 import BeautifulSoup

if __name__ == "__main__" :
    if not os.path.exists('Sanguoyanyi') :
        os.mkdir('Sanguoyanyi')
    #对首页的数据进行爬虫
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36'
    }
    url = 'https://www.shicimingju.com/book/sanguoyanyi.html'
    page_text = requests.get(url = url, headers = headers)
    #使用text时可能会乱码
    #原因：Requests推测的文本编码（ISO-8859-1）与源网页编码（utf-8)不一致
    # print(page_text.apparent_encoding)
    # print(page_text.encoding)
    #解决方法：
    page_text.encoding = 'utf-8'
    page_text = page_text.text
    #在首页中解析出章节的标题和章节内容
    # with open('sanguoyanyi.html', 'w', encoding = 'utf-8') as fp :
    #     fp.write(page_text)
    soup = BeautifulSoup(page_text, 'lxml')
    lst = soup.select(".book-mulu a")
    fp = open('sanguo.txt', 'w', encoding = 'utf-8')
    for i in range(1) :
        title = lst[i].text
        detail_url = 'https://www.shicimingju.com' + lst[i]['href']
        #对详情页发起请求
        detail_page_text = requests.get(detail_url, headers=headers)
        detail_page_text.encoding = 'utf-8'
        detail_page_text = detail_page_text.text
        print(detail_page_text)
        #解析出详情页的章节内容
        detail_soup = BeautifulSoup(detail_page_text, 'lxml')
        div_tag = detail_soup.find('div', class_ = 'chapter_content')
        content = div_tag.get_text()
        print(content)
        # content = detail_soup.select("#main > #main_left .chapter_content")[0].text
        # with open('Sanguoyanyi/' + title+'.txt', 'a+', encoding = 'utf-8') as fp :
        #     fp.write(content)
        # fp.write(title + ':' + content + '\n')
    fp.close()