#爬取梨视频的视频数据
#原则：线程池处理的是阻塞较为耗时的数据
import requests
import random
import re
import os
from multiprocessing.dummy import Pool
from lxml import etree

def get_vedio_info(headers) :
    url = 'https://www.pearvideo.com/category_5'
    session = requests.Session()
    page_text = session.get(url = url, headers = headers).text
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//*[@id="listvideoListUl"]/li')

    urls = [] #存储视频的网址
    for li in li_list :
        detail_url = 'https://www.pearvideo.com/' + li.xpath('.//a/@href')[0]
        name = li.xpath('.//a/div[2]/text()')[0] + '.mp4'
        #对详情页发起请求
        detail_page_text = session.get(url = detail_url, headers = headers).text
        #注意这里，url要使用动态url
        ajax_url = "https://www.pearvideo.com/videoStatus.jsp?"
        params = {
            'contId': detail_url.split('_')[-1],
            'mrd': random.random()
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'Referer' : detail_url #表示一个来源
        }
        json_data = session.get(url = ajax_url, headers = headers, params = params).json()
        #寻找规则，将伪装网址替换成真视频网址
        # src = 'https://video.pearvideo.com/mp4/third/20220223/cont-1752582-13293812-085442-hd.mp4'
        # src = 'https://video.pearvideo.com/mp4/third/20220223/1645596094850-13293812-085442-hd.mp4'
        rel = 'cont-' + params['contId']
        lst = json_data['videoInfo']['videos']['srcUrl'].split("/")
        false_src_part = lst[-1].split("-")[0]
        real_vedio_src = re.sub(false_src_part, rel, json_data['videoInfo']['videos']['srcUrl'])

        vedio_info = {'Name' : name, 'Url' : real_vedio_src}
        urls.append(vedio_info)
    return urls

#对视频链接发起请求获取视频的二进制数据，然后将数据进行返回
def get_vedio_data(vedio_info) :
    url = vedio_info['Url']
    data = requests.get(url = url, headers = headers).content
    #持久化存储
    with open('Vedio/' + vedio_info['Name'], 'wb') as fp :
        fp.write(data)
        print(vedio_info['Name'],'下载成功!')

if __name__ == "__main__" :
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }
    if not os.path.exists('Vedio') :
        os.mkdir('Vedio')
    urls = get_vedio_info(headers)
    #使用线程池对视频数据进行请求(较为耗时的阻塞数据)
    pool = Pool(4)
    pool.map(get_vedio_data, urls)

    pool.close()
    pool.join()