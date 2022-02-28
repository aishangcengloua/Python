import time
import aiohttp
import asyncio
import requests
import os
from lxml import etree

async def get_img_data(img_src, img_name, headers) :
    async with aiohttp.ClientSession() as session :
        print('开始下载 : ', img_name)
        async with await session.get(url = img_src, headers = headers) as response :
            img_data = await response.read()
            with open('imgData/' + img_name, 'wb') as fp :
                fp.write(img_data)
            print('下载结束 : ', img_name)

if __name__ == '__main__':
    start = time.time()
    if not os.path.exists('imgData') :
        os.mkdir('imgData')
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }
    url = 'https://pic.netbian.com/4kmeinv/'
    response = requests.get(url = url, headers = headers)
    response.encoding = response.apparent_encoding
    page_text = response.text
    parse = etree.HTMLParser(encoding = 'utf-8')
    tree = etree.HTML(page_text, parser = parse)
    li_list = tree.xpath('//*[@id="main"]/div[3]/ul/li')
    img_src_tasks = []
    for li in li_list :
        img_src = 'https://pic.netbian.com/' + li.xpath('./a/img/@src')[0]
        img_name = li.xpath('./a/img/@alt')[0] + '.jpg'
        task = asyncio.ensure_future(get_img_data(img_src, img_name, headers))
        img_src_tasks.append(task)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(img_src_tasks))
    print('total time : ', time.time() - start)