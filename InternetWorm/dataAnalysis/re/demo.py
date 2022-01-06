import re

# findall 在字符串中找到正则表达式所匹配的所有子串，并返回一个列表，
# 如果有多个匹配模式，则返回元组列表，如果没有找到匹配的，则返回空列表。
#在字符串中找到所有匹配的数字
lst = re.findall("\d+", "我今年18岁了，我喜欢5个妹子")
print(lst)

# search 扫描整个字符串并返回第一个成功的匹配。
#判断一句话中是否有数字
res = re.search("\d+", string = "我今年18岁了，我喜欢5个妹子")
print(res.group())

# re.finditer 和 findall 类似，在字符串中找到正则表达式所匹配的所有子串，并把它们作为一个迭代器返回。
# 用于爬虫
it = re.finditer("\d+", string = "我今年18岁了，我喜欢5个妹子")
for item in it :
    print(item.group())

#re.match 尝试从字符串的起始位置匹配一个模式，如果不是起始位置匹配成功的话，match() 就返回 none
#默认加上^
res = re.match("\d+", "18岁了，我喜欢5个妹子")
print(res.group())

res = re.split("[喜欢]", "你好18岁先生， 喜欢5个妹子")
print(res)

res = re.sub("\d+", "sb", "喜欢18岁的妹子")
print(res)

res = re.subn("\d+", "sb", "喜欢18岁的妹子")
print(res)

ojb = re.compile("\d+") #先加载这个正则，后面直接追使用这正则去匹配内容
lst = ojb.findall("喜欢18岁的妹子")
print(lst)

#爬虫必须会的重点
#1.()括起来的内容是最终想要的结果
#2.(?P<name>正则)把正则匹配到的内容直接放到name组里面，后面取数据时直接group(name)
obj = re.compile(r"今天喜欢(?P<meizi>\d+)岁的妹子") #使用?P<main>进行标记，匹配到的数据填入标记处
it = obj.finditer("今年18，昨天喜欢17岁的妹子， 今天喜欢16岁的妹子")
for item in it :
    print(item.group("meizi")) #拿标注的分组数据
    print(item.groupdict())

s = "今年18，昨天喜欢17岁的妹子， 今天喜欢16岁的妹子"
ex = '今年.*?喜欢.*?喜欢.*?的妹子'
res = re.finditer(ex, s)
for temp in res :
    print(temp.group())