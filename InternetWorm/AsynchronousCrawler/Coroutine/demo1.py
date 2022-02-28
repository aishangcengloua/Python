# import asyncio
# async def func():
#     print('cao')
#
# result = func()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(result)
# asyncio.run(result)
# 等价上面的写法

# import asyncio
# async def func():
#     print('come on')
#     response = await asyncio.sleep(2)
#     print('结束', response)
#
# asyncio.run(func())

# 示例2：
# import asyncio
# async def others() :
#     print("start")
#     await asyncio.sleep(2)
#     print('end')
#     return '返回值'
#
# async def func() :
#     print('执行协程函数内部代码')
#     #当遇到操作挂起当前任务，等IO操作完成之后再继续往下执行，当前协程挂起时，事件循环可以去执行其他协程
#     response = await others()
#     print('IO请求结束，结果为 : ', response)
#
# asyncio.run(func())

# import asyncio
# async def others():
#     print("start")
#     await asyncio.sleep(2)
#     print('end')
#     return '返回值'
#
#
# async def func():
#     print('执行协程函数内部代码')
#     # 当遇到操作挂起当前任务，等IO操作完成之后再继续往下执行，当前协程挂起时，事件循环可以去执行其他协程
#     response = await others()
#     print('IO请求结束，结果为 : ', response)
#
#     response = await others()
#     print('IO请求结束，结果为 : ', response)
#
# asyncio.run(func())

# import asyncio
# async def func() :
#     print(1)
#     await asyncio.sleep(2)
#     print(2)
#     return '返回值'
#
# async def main() :
#     print('main start')
#
#     #创建Task对象，将当前执行func函数任务添加至事件循环
#     task1 = asyncio.create_task(func())
#     #创建Task对象，将当前执行func函数任务添加至事件循环
#     task2 = asyncio.create_task(func())
#     #此时事件列表中有[main(), func(), func()]
#     print('main end')
#
#     ret1 = await task1
#     ret2 = await task2
#
#     print(ret1, ret2)
#
# asyncio.run(main()) #结果：1 1 2 2

# import asyncio
#
# async def func():
#     print(1)
#     await asyncio.sleep(2)
#     print(2)
#     return '返回值'
#
#
# async def main():
#     print('main start')
#
#     # 创建Task对象，将当前执行func函数任务添加至事件循环
#     # task1 = asyncio.create_task(func())
#     # 创建Task对象，将当前执行func函数任务添加至事件循环
#     # task2 = asyncio.create_task(func())
#     # 此时事件列表中有[main(), func(), func()]
#
#     task_list = [
#         asyncio.create_task(func(), name = 'n1'),
#         asyncio.create_task(func(), name = 'n2')
#     ]
#     print('main end')
#
#     done, pending = await asyncio.wait(task_list, timeout = None)
#     #pending没有意义，done是个集合是任务的返回值
#     print(done)
#
# asyncio.run(main())
# import asyncio
#
# async def func():
#     print(1)
#     await asyncio.sleep(2)
#     print(2)
#     return '返回值'

#报错，原因没有创建事件循环
# task_list = [
#     asyncio.create_task(func(), name = 'n1'),
#     asyncio.create_task(func(), name = 'n2')
# ]
#
# done, pending = asyncio.run(asyncio.wait(task_list))
#修改
# task_list = [
#     func(),
#     func()
# ]
#
# done, pending = asyncio.run(asyncio.wait(task_list))

# import asyncio
#
# async def main() :
#     #获取当前事件循环
#     loop = asyncio.get_running_loop()
#
#     #创建一个任务(Future对象)，这个任务上面都不干
#     fut = loop.create_future()
#
#     #等待任务最终结果(Future对象)，没有结果则一直等待下去
#     await fut
#
# asyncio.run(main())

# import asyncio
#
# async def set_after(fut) :
#     await asyncio.sleep(2)
#     fut.set_result('666')
#
# async def main() :
#     # 获取当前事件循环
#     loop = asyncio.get_running_loop()
#     #创建一个任务(Future对象)
#     fut = loop.create_future()
#     await loop.create_task(set_after(fut))
#
#     data = await fut
#     print(data)
#
# asyncio.run(main())

