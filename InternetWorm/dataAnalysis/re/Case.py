import requests
import re
import os

if __name__ == "__main__" :
    if not os.path.exists('qiutuLibs') :
        os.mkdir('qiutuLibs')
    count = 0
    for pageNum in range(1, 31) :
        url = f"https://xiaohua.zol.com.cn/qutu/qiushi/{pageNum}.html"
        headers = {
            'User-Agent': "ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36"
        }
        #爬取一整张页面
        page_text = requests.get(url = url, headers = headers).text
        #使用聚焦爬虫将页面中的图片进行解析提取
        ex = re.compile(r'<div class="summary-text">.*?<img src="(?P<src>.*?)" alt.*?</div>')
        s = '<div class="summary-text"><p><a target="_blank" href="/detail59/58636.html"><img src="https://xiaohua-fd.zol-img.com.cn/t_s300x2000/g5/M00/04/0E/ChMkJ1mvdSaIViq4ADYK5g0qldQAAgOcgAF2PYANgr-558.gif" alt="因为电击，手的肌肉收紧，也无法松开导电的东西..." title="点击查看大图"></a></p></div>'
        # img_src_list = re.findall(ex, page_text, re.S)
        # res = ex.finditer(s)
        # for sr in res :
        #     print(sr.group("src"))
        img_src_iter = ex.finditer(page_text)
        print(img_src_iter)
        for src in img_src_iter :
            print(src.group("src"))
            count += 1
            #请求图片的二进制数据
            img_data = requests.get(url = src.group("src"), headers = headers).content
            name = src.group("src").split("/")[-1]
            img_path = 'qiutuLibs/' + name
            with open(img_path, 'wb') as fp :
                fp.write(img_data)
    print(count)