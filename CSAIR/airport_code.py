# -*- coding: utf-8 -*-
import requests
import pandas as pd
from lxml import etree

base_url = "http://www.6qt.net/index.asp?Field=&keyword=&MaxPerPage=50&page={}"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
}

df_airport = pd.DataFrame()
for page in range(49):
    page_url = base_url.format(page + 1)
    page_response = requests.get(page_url, headers=header)
    page_response.encoding = page_response.apparent_encoding
    page_txt = page_response.text
    page_html = etree.HTML(page_txt)
    lst_tr = page_html.xpath('//tr[@onmouseout="this.className=\'tdbg\'"]')
    print('===page:', page + 1, len(lst_tr))
    for tr in lst_tr:
        lst_td = tr.xpath('td')
        city = lst_td[0].xpath('a//text()')[0].strip()
        code = lst_td[1].xpath('a//text()')[0].strip()
        try:
            country = lst_td[2].xpath('a//text()')[0].strip()
        except:
            country = ''
        try:
            country_code = lst_td[3].xpath('a//text()')[0].strip()
        except:
            country_code = ''
        try:
            code_4 = lst_td[4].xpath('a//text()')[0].strip()
        except:
            code_4 = ''
        airport = lst_td[5].text.strip()
        airport_eng = lst_td[6].text.strip()
        print(city, code, country, country_code, code_4, airport, airport_eng)
        df_airport = df_airport.append([[city, code, country, country_code, code_4, airport, airport_eng]])
df_airport.columns = ['city', 'code', 'country', 'country_code', 'code_4', 'airport', 'airport_eng']
print('df_airport shape:', df_airport.shape)
df_airport.to_csv('./data/df_airport.csv', index=False)
