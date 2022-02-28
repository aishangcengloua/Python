import asyncio
# async def func(url) :
#     print('正在请求的url : ', url)
#     print('Successul')
#     return url
#
# c = func('www.baidu.com')

#Task的使用
# loop = asyncio.get_event_loop()
# task = loop.create_task(c)
# print(task)
# loop.run_until_complete(task)
# print(task)

#future的使用
# loop = asyncio.get_event_loop()
# fut = asyncio.ensure_future(c)
# print(fut)
# loop.run_until_complete(fut)
# print(fut)

# def callback_func(task) :
#     print(task.result())

#绑定回调
# loop = asyncio.get_event_loop()
# task = asyncio.ensure_future(c)
#将回调函数绑定到任务对象中
# task.add_done_callback(callback_func)
# loop.run_until_complete(task)

#多任务协程
import time
async def request(url) :
    print('正在下载', url)
    await asyncio.sleep(2)
    print('下载完毕！')
start = time.time()
urls = [
    'www.baidu.com',
    'www.sogou.com',
    'www.goubanjia.com'
]
#任务列表
stacks = []
for url in urls :
    c = request(url)
    task = asyncio.ensure_future(c)
    stacks.append(task)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(stacks))
print(time.time() - start)