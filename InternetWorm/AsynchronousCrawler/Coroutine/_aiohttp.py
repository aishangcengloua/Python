import requests
import asyncio
import aiohttp#使用该模块ClientSession对象进行网络请求
import time

start = time.time()
urls = [
    'http://127.0.0.1:5000/heige',
    'http://127.0.0.1:5000/james',
    'http://127.0.0.1:5000/tom'
]

async def get_page(url) :
    print('正在下载', url)
    #requests.get是基于同步的
    #aiohttp基于异步网络请求的模块
    # response = requests.get(url = url)
    async with aiohttp.ClientSession() as session :
        #get(), post()
        #headers, params/data, proxy = 'http://ip:port'
        async with await session.get(url) as response :
            #text()返回字符串形式的响应数据
            #read()返回二进制形式的响应数据
            #json()返回json数据对象
            #获取响应数据之前要使用await进行手动挂起
            page_text = await response.text()
            print(page_text)

tasks = []
for url in urls :
    tasks.append(asyncio.ensure_future(get_page(url)))

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()
print('total_time : ', end - start)