import requests
from bs4 import BeautifulSoup
import pandas as pd

# from lxml import etree

start_url = 'https://www.biendata.com/competition/'
header = {
    'Referer': 'https://www.biendata.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
res = requests.get(start_url, headers=header)
res_html = res.text
soup = BeautifulSoup(res_html, 'lxml')
print(soup)

# tree = etree.fromstring(res_html)
# print(tree)
