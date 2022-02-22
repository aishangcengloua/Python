#爬取58同城二手房的相关信息
import requests
import pandas as pd
from lxml import etree

if __name__ == "__main__" :
    headers = {
        'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36"
    }
    url = "https://bj.58.com/ershoufang/"
    page_text = requests.get(url = url, headers = headers).text
    #数据解析
    parse = etree.HTMLParser(encoding='utf-8')
    tree = etree.HTML(page_text, parser = parse)
    div_list = tree.xpath('//section[@ class = "list"]/div[@ class = "property"]')
    # print(div_list)
    title, fangxing, area, chaoxiang, louceng, time, total_price, one_price, address = [], [], [], [], [], [], [], [], []
    for div in div_list :
        #标题
        title.append(div.xpath('./a/div[2]//h3/@title')[0])#./表示最左边的div
        #房型
        fangxing_temp = div.xpath('./a//div[@ class = "property-content-info"]/p[1]//text()')
        s = ""
        for str in fangxing_temp :
            if str != ' ' :
                s += str
        fangxing.append(s)
        #面积
        area_temp = div.xpath('./a//div[@ class = "property-content-info"]/p[2]/text()')
        s = area_temp[0].strip(' \n')
        area.append(s)
        #朝向
        chaoxiang.append(div.xpath('./a//div[@ class = "property-content-info"]/p[3]/text()')[0])
        #楼层
        louceng.append(div.xpath('./a//div[@ class = "property-content-info"]/p[4]/text()')[0].strip(' \n'))
        #建造时间
        time.append(div.xpath('./a//div[@ class = "property-content-info"]/p[5]/text()')[0].strip(' \n'))
        #总房价
        total_price.append(div.xpath('./a//div[@ class = "property-price"]/p[1]//text()')[0] + '万')
        #单价
        one_price.append(div.xpath('./a//div[@ class = "property-price"]/p[2]//text()')[0])
        #地址
        address.append('-'.join(div.xpath('./a//section/div[2]/p[2]//text()')))

    df = pd.DataFrame({"标题" : title, "房型" : fangxing, "面积" : area, "朝向" : chaoxiang, "楼层" : louceng
                       , "建造时间" : time, "每平方米/万元" : one_price, "总房价" : total_price, "地址" : address})
    df.to_csv("58同城房价.csv", encoding = "utf-8", index = True, index_label = "序号")