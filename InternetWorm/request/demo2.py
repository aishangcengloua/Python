# 简易网页采集器(指定词条对应的搜索页面)
# import requests

# UA：User-Agent(请求载体的身份标识)
# UA检测：门户网站的服务器会检测对应请求的载体身份标识，如果是浏览器则是正常的请求，
# 如果载体身份标识表示浏览器，则表示该请求不是正当的请求(爬虫)，那服务器就可能拒绝此次请求

# UA伪装：让爬虫对应的请求载体身份标识伪装成某一浏览器
# if __name__ == "__main__" :
#     # UA伪装将对应的User-Agent封装到一个字典中
#     headers = {
#         'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36'
#     }
#     url = "https://www.sogou.com/web"
#     # 处理url携带的参数：封装到字典中
#     kw = input('enter a word :')
#     param = {
#         'query' : kw
#     }
#     response = requests.get(url = url, params = param, headers = headers)
#     page_text = response.text
#     fileName = kw + '.html'
#     with open(fileName, 'w', encoding = 'utf-8') as fp :
#         fp.write(page_text)
#
#     print('Successful!')

# 破解百度翻译
# import requests
# import json

# post请求(携带参数)
# 响应数据是一组json数据
# if __name__ == "__main__" :
#     # 指定url
#     post_url = "https://fanyi.baidu.com/sug"
#     word = input("enter a word : ")
#     data = {
#         'kw' : word
#     }
#     # UA伪装
#     headers = {
#         'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36"
#     }
#     # 发起请求
#     response = requests.post(url = post_url, data = data, headers = headers, )
#     # 获取响应数据，json方法返回的对象是obj，只有确定响应数据是json才不会报错
#     dic_obj = response.json()
#     print(dic_obj)
#     fileName = word + '.json'
#     # 持久存储
#     with open(fileName, 'w', encoding = 'utf-8') as fp :
#         json.dump(dic_obj, fp = fp, ensure_ascii = False)
#     print("over")

# 豆瓣电影分类排行榜
import requests
import json

# if __name__ == "__main__" :
#     url = "https://movie.douban.com/j/chart/top_list"
#     headers = {
#         "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36"
#     }
#     params = {
#         'type': 24,
#         'interval_id' : '100:90' ,
#         'action' : '',
#         'start' : 1,# 从第几部电影开始取，索引从零开始
#         'limit' : 20 # 取多少部电影
#     }
#     response = requests.get(url = url, params = params, headers = headers)
#     list_data = response.json()
#     with open('douban.json', 'w', encoding = 'utf-8') as fp :
#         json.dump(list_data, fp = fp, ensure_ascii = False)
#     print("over!")

# 肯德基餐厅查询
# import requests
# import json

# if __name__ == "__main__" :
#     url = "http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword"
#     headers = {
#         "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36"
#     }
#     params = {
#         'cname': '',
#         'pid': '',
#         'keyword': '湛江',
#         'pageIndex': 1,
#         'pageSize': 10
#     }
#     response = requests.post(url = url, data = params, headers = headers)
#     dic_json = response.json()
#     fileName = params['keyword'] + 'KFC' + '.json'
#     with open(fileName, 'w', encoding = 'utf-8') as fp :
#         json.dump(dic_json, fp = fp, ensure_ascii = False)
#     print('over!')

#药监总局化妆生产许可证
#动态加载数据
#首页对应的企业信息是通过ajax动态请求得到的
#详情页的数据也是动态加载出来的
import requests
import json

if __name__ == "__main__" :
    #批量获取不同企业的id值
    url = "http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList"
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36"
    }
    #获取所有叶的数据
    id_list = []
    for page in range(1, 51) :
        data = {
            'on': 'true',
            'page': page,
            'pageSize': 15,
            'productName':'',
            'conditionType': 1,
            'applyname':'',
            'applysn':''
        }
        json_ids = requests.post(url = url, headers = headers, data = data).json()
        for dic in json_ids["list"] :
            id_list.append(dic["ID"])
    # print(id_list)

    #获取企业详情数据
    all_detail_data = []
    post_url = "http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById"
    for id in id_list :
        data = {
            "id" : id
        }
        detail_json = requests.post(url = post_url, data = data, headers = headers).json()
        # print(detail_json)

        all_detail_data.append(detail_json)
    with open("allData.json", "w", encoding = "utf-8") as fp :
        json.dump(all_detail_data, fp = fp, ensure_ascii = False)

    print("end!")