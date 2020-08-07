# -*- coding: utf-8 -*-
import os

import requests
from lxml import etree


# 下载图片
def downloadfile(img_src, img_name):
    print('start download:', img_src)
    text = requests.get(img_src).content
    f = open('pic/' + img_name, 'wb+')
    f.write(text)
    f.close()


def main():
    base_url = 'https://www.nbfox.com/topics/'
    lst_category = ['world-famous-paintings', '超高清', 'laogui-favorites']
    lst_pages = [5, 18, 6]

    for category, page_size in zip(lst_category, lst_pages):
        for page in range(page_size):
            txt = requests.get(base_url + category + '/page/' + str(page + 1)).text
            html = etree.HTML(txt)
            lst_links = html.xpath('//a[@class="czr-title"]//@href')
            print(category, page + 1, lst_links)
            for link in lst_links:
                page_txt = requests.get(link).text
                page_html = etree.HTML(page_txt)
                img_src = page_html.xpath('//div[@class="czr-wp-the-content"]//img//@data-src')
                for img in img_src:
                    if os.path.exists('pic/' + img.split('/')[-1]):
                        continue
                    downloadfile(img, img.split('/')[-1])


if __name__ == '__main__':
    main()
