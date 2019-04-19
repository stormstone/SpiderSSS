from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

# 创建 beautifulsoup 对象
soup = BeautifulSoup(html)
# 打印一下 soup 对象的内容，格式化输出
print(soup.prettify)

# 结构化数据解析
print(soup.title)  # 获取title
print(soup.title.name)  # title标签名称
print(soup.title.string)  # title标签内容
print(soup.title.parent.name)  # 父标签
print(soup.p['class'])  # 属性获取
print(soup.find_all('a'))  # 查找所有标签
print(soup.find(id="link3"))  # 通过id查找
for link in soup.find_all('a'):  # 遍历获取所有a标签
    print(link.get('href'))  # 获取a标签href属性
