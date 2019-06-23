# Pinterest 图片爬虫

![show](zzf.png)

妹妹太漂亮太可爱了！:heart_eyes: :heart_eyes: :heart_eyes:


![show](show.png)



    selenium
    urllib
    mysql

首先把图片链接存入MySQL，然后下载每张图片。



配置文件内容：config.py

```python
# Pinterest 用户名密码
LOGIN_EMAIL = '邮箱'
LOGIN_PASSWORD = '密码'

# 待爬取用户名
lst_search_text = ['张子枫']

# {1: '图片链接保存DB', 2: '下载图片'}
TYPE_DB_OR_IMG = 1

# 图片存储路径
PATH_IMGS = './imgs/'

# 代理
proxy_server = 'http://127.0.0.1:2080'

# 下载图片超时时间（s）
TIME_OUT = 20

# MySQL配置
host = '127.0.0.1'
user = 'root'
psd = '123456'
db = 'spiders'
c = 'utf8'
port = 3306
```
