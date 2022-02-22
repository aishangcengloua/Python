from lxml import etree

if __name__ == "__main__" :
    #实例化etree对象，加载了解析的源码
    parse = etree.HTMLParser(encoding = 'utf-8')
    tree = etree.parse('response.html', parser = parse)
    # r = tree.xpath('/html/body/div')
    # r = tree.xpath('//div[@id="top_left_menu"]')
    r = tree.xpath('//div[@id = "top_left_menu"]/ul/li[3]/a//text()')[0]
    r = tree.xpath('//div[@id = "top_left_menu"]/ul/li[3]/a')
    r = tree.xpath('//div[@id = "top_left_menu"]/text()')
    #取属性值
    r = tree.xpath('//div[@id = "top_left_menu"]/ul/li[3]/a/@href')
    # print(len(r))
    print(r)