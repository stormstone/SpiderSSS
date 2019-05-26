import urllib
import os
import eventlet
import time
import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

eventlet.monkey_patch()

chrome_options = Options()
chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--proxy-server=http://127.0.0.1:2080")
driver = webdriver.Chrome(options=chrome_options)

host = '127.0.0.1'
user = 'root'
psd = '123456'
db = 'spiders'
c = 'utf8'
port = 3306

path_img = './imgs/'
base_url = 'https://twitter.com/'


# urllib 获取图片并保存
def save_img(path_img, url, save_name):
    file_name_full = path_img + save_name + '.png'
    if os.path.exists(file_name_full):
        print('pic:' + save_name + '.png exists')
        return 1
    with eventlet.Timeout(10, False):  # 设置超时时间为10秒
        bytes = urllib.request.urlopen(url)
        f = open(file_name_full, 'wb')
        f.write(bytes.read())
        f.flush()
        f.close()
        print('pic:' + save_name + '.png save success...')
        return 1
    return 0


# 图片保存命名
def save_img_src(img_src):
    print(img_src)
    if 'profile_banners' in str(img_src):
        save_name = username + '_banner'
    elif 'profile_images' in str(img_src):
        if '400x400' in str(img_src):
            save_name = username + '_avatar'
        else:
            return
    elif 'emoji' in str(img_src):
        save_name = 'emoji_' + str(str(img_src).split('/')[-1][:-4])
    else:
        save_name = username + '_' + str(str(img_src).split('/')[-1][:-4])

    return save_img(path_img, img_src, save_name)


# 插入图片src到数据库
def insert_user_info(username, img_src):
    try:
        cue.execute("insert ignore into twitter_img "
                    "(username, img_src) "
                    "values (%s,%s)",
                    [username, img_src])
    except Exception as e:
        print('Insert error:', e)
        con.rollback()
    else:
        con.commit()


# selenium driver 获取用户meida下图片链接
def get_users_media_driver(username):
    start_url = base_url + username + '/media'
    print('driver get url:', start_url)
    driver.get(start_url)

    # 判断是否滑到最后了
    lst_end = driver.find_elements_by_xpath('//div[@class="timeline-end has-items"]')
    lst_no_end = driver.find_elements_by_xpath('//div[@class="timeline-end has-items has-more-items"]')

    count_scroll = 0
    while len(lst_end) < 1 or len(lst_no_end) > 0:
        # 滑倒底
        js = "window.scrollTo(0,document.body.scrollHeight)"
        driver.execute_script(js)
        count_scroll += 1
        print('scroll:', count_scroll)
        time.sleep(2)
        lst_end = driver.find_elements_by_xpath('//div[@class="stream-end-inner"]')
        lst_no_end = driver.find_elements_by_xpath('//div[@class="timeline-end has-items has-more-items"]')

    lst_img = [img.get_attribute('src') for img in driver.find_elements_by_xpath('//img')]
    lst_img = list(set(lst_img))
    count_all = len(lst_img)
    print(username, 'unique img count:', count_all)
    for count in range(count_all):
        img_src = lst_img[count]
        print(username, count, '/', count_all, img_src)
        if img_src != None:
            insert_user_info(username, img_src)


def down_img(username=None):
    if username:
        cue.execute("select count(*) from twitter_img where username = '" + username + "' and is_crawled = 0")
    else:
        cue.execute("select count(*) from twitter_img where is_crawled = 0")
    count_all = cue.fetchone()[0]
    print('down img count all:', count_all)
    for i in range(count_all):
        if username:
            cue.execute(
                "select img_src from twitter_img where username = '" + username + "' and is_crawled = 0 limit 1")
        else:
            cue.execute("select img_src from twitter_img where is_crawled = 0 limit 1")
        img_src = cue.fetchone()[0]
        r = save_img_src(img_src)
        if r:
            cue.execute("update twitter_img set is_crawled = 1 where img_src = (%s)", img_src)
            con.commit()


if __name__ == '__main__':
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c,
                          port=port)
    cue = con.cursor()

    username = 'kaifulee'
    get_users_media_driver(username)
    down_img(username)