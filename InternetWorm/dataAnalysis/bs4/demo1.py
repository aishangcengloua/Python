from bs4 import BeautifulSoup

if __name__ == "__main__" :
    # 将本地的html文档中的数据加载到该对象中
    with open('response.html', 'r') as fp :

        soup = BeautifulSoup(fp, 'lxml')
        # print(soup)
        # print(soup.a)#soup.tagName返回的是html第一次出现的tagName标签
        # print(soup.div)
        # print(soup.find('div').string) #相当于soup.div
        # print(soup.find('div', class_ = 'sub-links'))
        # print(soup.find_all('a'))
        #
        print(soup.select("div > ul > li > span > a"))