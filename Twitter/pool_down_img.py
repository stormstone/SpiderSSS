import urllib
import urllib.request
import os
import sys
import eventlet
import time
import pymysql
from multiprocessing import Pool as ProcessPool
from config import *


# urllib 获取图片并保存
def save_img(path_img, url, save_name):
    file_name_full = path_img + save_name + '.png'
    if os.path.exists(file_name_full) and os.path.getsize(file_name_full) > 0:
        print('pic:' + save_name + '.png exists')
        return 1
    with eventlet.Timeout(TIME_OUT, False):  # 设置超时时间为10秒
        bytes = urllib.request.urlopen(url)
        f = open(file_name_full, 'wb')
        f.write(bytes.read())
        f.flush()
        f.close()
        print('pic:' + save_name + '.png save success...')
        return 1
    return 0


def save_img_src(username, img_src, path_img):
    if 'profile_banners' in str(img_src):
        save_name = username + '_banner'
    elif 'profile_images' in str(img_src):
        if '400x400' in str(img_src):
            save_name = username + '_avatar'
        else:
            return 1
    elif 'emoji' in str(img_src):
        save_name = 'emoji_' + str(str(img_src).split('/')[-1][:-4])
    else:
        save_name = username + '_' + str(str(img_src).split('/')[-1][:-4])

    return save_img(path_img, img_src, save_name)


def down_img(img_src):
    path_img = PATH_IMGS + username + '/'
    if not os.path.exists(path_img):
        os.makedirs(path_img)
    r = save_img_src(username, img_src, path_img)
    if r:
        # 标记为已爬取
        cue.execute("update twitter_img set is_crawled = 1 where img_src = (%s)", img_src)
        con.commit()


con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c,
                      port=port)
cue = con.cursor()

username = sys.argv[1]

if __name__ == '__main__':
    cue.execute("select username,img_src from twitter_img where is_crawled = 0 and username = '" + username + "';")
    lst_ul = cue.fetchall()
    lst_username = [i[0] for i in lst_ul]
    lst_urls = [i[1] for i in lst_ul]
    print(username, len(lst_urls))

    # 多进程
    pool = ProcessPool(20)
    pool.map(down_img, lst_urls)
    pool.close()
    pool.join()
