import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import eventlet
import os

eventlet.monkey_patch()

base_url = 'http://www.happycamp.cc'
start_url = 'http://www.happycamp.cc/list'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
}

path_df_links = 'df_links.csv'
path_df_authors = 'df_authors.csv'


# 解析每一期节目参加的嘉宾名字
def parse_v(href):
    df_tmp = pd.DataFrame()
    r = requests.get(href, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find('h1').text
    try:
        lst_authors_a = soup.find_all('a', class_="author")
    except:
        lst_authors_a = []
        pass
    if len(lst_authors_a) != 0:
        for a in lst_authors_a:
            author = a.text
            df_tmp = df_tmp.append([[title, author, href]])
    else:
        df_tmp = df_tmp.append([[title, 'None', href]])
    df_tmp.columns = ['title', 'author', 'href']
    return df_tmp


# 获取所有期节目的链接
def get_links_v():
    r = requests.get(start_url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    v_ul = soup.find('ul', class_="list-by-year")
    lst_v_a = v_ul.find_all('a')
    df_links = pd.DataFrame()
    for a in lst_v_a:
        href = base_url + a.get('href')
        df_links = df_links.append([[href, False]])
    df_links.columns = ['href', 'is_spider']
    df_links.to_csv(path_df_links, index=False)


# 循环获取每一期的嘉宾
def get_authors():
    if os.path.exists(path_df_authors):
        df_authors = pd.read_csv(path_df_authors)
    else:
        df_authors = pd.DataFrame()
    df_links = pd.read_csv(path_df_links)
    count_to_spider = df_links[df_links['is_spider'] == False].shape[0]
    while count_to_spider:
        for i in range(df_links.shape[0]):
            href = df_links.loc[i, 'href']
            is_spider = df_links.loc[i, 'is_spider']
            if is_spider:
                continue
            print(href, is_spider)
            with eventlet.Timeout(10, False):  # 设置超时时间为10秒
                df_tmp = parse_v(href)
                df_authors = df_authors.append(df_tmp)
                df_links.loc[i, 'is_spider'] = True
                print(href, 'success\n')
            df_authors.to_csv(path_df_authors, index=False, encoding='utf8')
            count_to_spider = df_links[df_links['is_spider'] == False].shape[0]
            df_links.to_csv(path_df_links, index=False)


if __name__ == '__main__':
    if os.path.exists(path_df_links):
        pass
    else:
        get_links_v()
    get_authors()
