# import time

#使用单线程串行进行执行
# def get_page(str) :
#     print("正在下载: ", str)
#     time.sleep(2)
#     print('下载成功: ', str)
#
# name_list = ['xiaozi', 'aa', 'bb', 'cc']
# start_time = time.time()
# for i in range(len(name_list)) :
#     get_page(name_list[i])
# end_time = time.time()
# print(f'{end_time - start_time} second')

#线程池方式执行
import time
from multiprocessing.dummy import Pool#导入多线程对应的类

start_time = time.time()
def get_page(str) :
    print("正在下载: ", str)
    time.sleep(2)
    print('下载成功: ', str)

name_list = ['xiaozi', 'aa', 'bb', 'cc']

#实例化一个线程池的对象
pool = Pool(4) #4个url，4个阻塞操作
pool.map(get_page, name_list)
end_time = time.time()

print(f'{end_time - start_time} second')