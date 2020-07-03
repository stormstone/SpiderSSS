# -*- coding: utf-8 -*-

import requests
import json
from multiprocessing.pool import Pool as ThreadPool


# 发起请求获得json数据
def get_json(url):
    try:
        res = requests.get(url).text
        return res
    except:
        print('cannot read %s' % url)
        return None


# 获取图片url
def get_url(url):
    try:
        pase = json.loads(get_json(url))
        img_url = 'https://cn.bing.com/' + pase['images'][0]['url']
        return img_url
    except:
        print('cannot load', get_json(url), ',url:', url)
        return None


# 每日请求图片路径json的url
def bingDayUrl(day):
    return 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=%d&n=1&mkt=en-US' % day


# 获取图片url
def get_pic_name(url):
    if url == None:
        return ''
    name = json.loads(get_json(url))['images'][0]['copyright'].split(None, 1)[0] + '.jpg'
    return name


# 下载图片
def downloadfile(tup_nu):
    name, url = tup_nu
    print('start download:', name, url)
    if url == None or name == None:
        return None

    text = requests.get(url).content
    name = name.replace('/', '_')
    f = open('pic/' + name, 'wb+')
    f.write(text)
    f.close()


# 多线程
def download_pic_range(i, j):
    pool = ThreadPool()
    links = pool.map(bingDayUrl, range(i, j + 1))
    pic_urls = pool.map(get_url, links)
    pic_name = pool.map(get_pic_name, links)
    pool.map(downloadfile, zip(pic_name, pic_urls))


if __name__ == '__main__':
    download_pic_range(-1, 7)
