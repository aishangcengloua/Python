# -实现方法：
#         -greenlet，早期模块
#         -yield关键字
#         -asyncio装饰器
#         -async、await关键字(最主流)
#greenlet模块实现
# from greenlet import greenlet
#
# def func1() :
#     print(1)           #第1步
#     gr2.switch()       #第3步：切换到func2函数
#     print(2)           #第6步
#     gr2.switch()       #第7步：切换到func2函数，从上次执行的位置继续向后执行
#
# def func2() :
#     print(3)           #第4步
#     gr1.switch()       #第5步：切换到func1函数
#     print(4)           #第8步
#
# gr1 = greenlet(func1)
# gr2 = greenlet(func2)
# gr1.switch() #第1步：执行func1函数

# yield关键字实现
# def func1() :
#     yield 1
#     yield from func2()
#     yield 2
# def func2() :
#     yield 3
#     yield 4
#
# f1 = func1()
# for item in f1 :
#     print(item) # output: 1 3 4 2

#asyncio实现
# import asyncio
#
# @asyncio.coroutine #表示变成协程函数
# def func1() :
#     print(1)
#     yield from asyncio.sleep(2) #遇到 IO 耗时操作，在等待过程中自动化切换到tasks中的其他任务中
#     print(2)
#
# @asyncio.coroutine
# def func2() :
#     print(3)
#     yield from asyncio.sleep(2) #遇到 IO 耗时操作，在等待过程中自动化切换到tasks中的其他任务中
#     print(4)
#
# #将协程函数放到一个任务中
# tasks = [
#     asyncio.ensure_future(func1()),
#     asyncio.ensure_future(func2())
# ]
#
# #执行协程函数
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))

#async 和 await关键字，本质上跟asyncio是一样的，只是代码更加简洁
import asyncio

#表示变成协程函数
async def func1() :
    print(1)
    await asyncio.sleep(2) #遇到 IO 耗时操作，在等待过程中自动化切换到tasks中的其他任务中
    print(2)

async def func2() :
    print(3)
    await asyncio.sleep(2) #遇到 IO 耗时操作，在等待过程中自动化切换到tasks中的其他任务中
    print(4)

#将协程函数放到一个任务中
tasks = [
    asyncio.ensure_future(func1()),
    asyncio.ensure_future(func2())
]

#执行协程函数
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))