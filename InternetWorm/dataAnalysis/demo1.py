#爬取糗事百科糗图板块下的所有糗图图片
import requests
if __name__ == "__main__" :
    #爬取图片数据
    url = "https://img.zcool.cn/community/01e2b45d2f3490a8012187f4924510.jpg@1280w_1l_2o_100sh.jpg"
    headers = {
        'User-Agent' : "ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36"
    }
    #content返回的是二进制形式的图片数据
    #text(字符串)，json()对象
    img_data = requests.get(url = url, headers = headers).content
    with open('baoerjie.jpg', 'wb') as fp :
        fp.write(img_data)