import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pymysql

chrome_options = Options()
chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)

host = '127.0.0.1'
user = 'root'
psd = '123456'
db = 'spiders'
c = 'utf8'
port = 3306


# 插入用户信息
def insert_user_info(user_id, user_name, user_djp, user_lev, event_count, follow_count, fan_count, user_intr,
                     user_base, user_age):
    try:
        cue.execute("insert ignore into music163_user_info "
                    "(user_id, user_name, user_djp, user_lev, event_count, follow_count, fan_count, user_intr, user_base, user_age) "
                    "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [user_id, user_name, user_djp, user_lev, event_count, follow_count, fan_count, user_intr,
                     user_base, user_age])
    except Exception as e:
        print('Insert error:', e)
        con.rollback()
    else:
        con.commit()


def insert_user_song(user_id, song_index, song_title, song_author, song_href, song_hot, unique_key):
    try:
        cue.execute("insert ignore into music163_user_song "
                    "(user_id, song_index, song_title, song_author, song_href, song_hot, unique_key) "
                    "values (%s,%s,%s,%s,%s,%s,%s)",
                    [user_id, song_index, song_title, song_author, song_href, song_hot, unique_key])
    except Exception as e:
        print('Insert error:', e)
        con.rollback()
    else:
        con.commit()


def parse_user(user_id):
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c,
                          port=port)
    cue = con.cursor()

    start_url = 'https://music.163.com/#/user/home?id=' + str(user_id)
    print('parse user:', start_url)
    driver.get(start_url)
    time.sleep(1)
    driver.switch_to.frame('g_iframe')  # 切换到iframe，g_iframe是iframe的id名称
    if '很抱歉，你要查找的网页找不到' in driver.page_source:
        # 把当前user_id标记为已爬取
        cue.execute("update music163_user_id set is_used = 1 where user_id = (%s)", user_id)
        con.commit()
    user_name = driver.find_element_by_xpath('//span[@class="tit f-ff2 s-fc0 f-thide"]').text  # 用户昵称
    user_lev = driver.find_element_by_xpath('//span[@class="lev u-lev u-icn2 u-icn2-lev"]').text  # 用户等级
    try:
        user_djp = driver.find_element_by_xpath('//p[@class="djp f-fs1 s-fc3"]').text  # 用户标签
    except:
        user_djp = ''
    event_count = driver.find_element_by_xpath('//strong[@id="event_count"]').text  # 动态数量
    follow_count = driver.find_element_by_xpath('//strong[@id="follow_count"]').text  # 关注数量
    follow_href = driver.find_elements_by_xpath('//ul[@id="tab-box"]//a')[1].get_attribute('href')  # 关注页面链接
    fan_count = driver.find_element_by_xpath('//strong[@id="fan_count"]').text  # 粉丝数量
    fan_href = driver.find_elements_by_xpath('//ul[@id="tab-box"]//a')[2].get_attribute('href')  # 粉丝页面链接
    try:
        user_intr = driver.find_element_by_xpath('//div[@class="inf s-fc3 f-brk"]').text  # 个人介绍
    except:
        user_intr = ''
    user_info = driver.find_element_by_xpath('//div[@class="inf s-fc3"]').text  # 地点年龄
    user_base = user_info.split('年龄')[0].split('：')[-1]  # 用户地点
    try:
        user_age = user_info.split('年龄')[1].split('：')[-1]  # 用户年龄
    except:
        user_age = -1
    # 插入用户信息
    insert_user_info(user_id, user_name, user_djp, user_lev, event_count, follow_count, fan_count, user_intr,
                     user_base, user_age)

    try:
        driver.find_element_by_xpath('//span[@id="songsall"]').click()
    except:
        # 把follows和fan_href链接保存到数据库
        try:
            cue.execute("insert into music163_follow_href (follow_href)values (%s)", [follow_href])
            cue.execute("insert into music163_follow_href (follow_href)values (%s)", [fan_href])
        except:
            pass
        # 把当前user_id标记为已爬取
        cue.execute("update music163_user_id set is_used = 1 where user_id = (%s)", user_id)
        con.commit()
        return
    time.sleep(1)

    lst_songs = driver.find_elements_by_xpath('//div[@class="j-flag"]//li')
    lst_songs_href = driver.find_elements_by_xpath(
        '//div[@class="j-flag"]//li//div[@class="song"]//span[@class="txt"]/a')
    lst_songs_hot = driver.find_elements_by_xpath(
        '//div[@class="j-flag"]//li//div[@class="tops"]//span')
    count_songs = len(lst_songs)
    print('parse user:', start_url, 'user songs count:', count_songs)
    # 插入最常听歌曲具体信息
    for song_index in range(count_songs):
        song_info = lst_songs[song_index].text.replace('\n', '').split('.')[-1]
        song_title = song_info.split('-')[0]  # 歌曲名称
        song_author = song_info.split('-')[-1]  # 歌曲作者
        song_href = lst_songs_href[song_index].get_attribute('href')  # 歌曲链接
        song_hot = lst_songs_hot[song_index].get_attribute('style').split(': ')[-1].split('%')[0]  # 听歌次数热度%

        unique_key = str(user_id) + '_' + str(song_href.split('=')[-1])
        insert_user_song(user_id, song_index, song_title, song_author, song_href, song_hot, unique_key)

    # 把follows和fan_href链接保存到数据库
    try:
        cue.execute("insert into music163_follow_href (follow_href)values (%s)", [follow_href])
        cue.execute("insert into music163_follow_href (follow_href)values (%s)", [fan_href])
    except:
        pass
    # 把当前user_id标记为已爬取
    cue.execute("update music163_user_id set is_used = 1 where user_id = (%s)", user_id)
    con.commit()


# 解析每个用户的关注用户和粉丝用户
def parse_follows(follow_href):
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c,
                          port=port)
    cue = con.cursor()

    driver.get(follow_href)
    driver.switch_to.frame('g_iframe')
    time.sleep(1)
    lst_user_id = driver.find_elements_by_xpath('//ul[@id="main-box"]//a[@class="s-fc7 f-fs1 nm f-thide"]')
    len_follows = len(lst_user_id)
    print('parse follows:', follow_href, 'follow users count:', len_follows)
    for i in range(len_follows):
        user_id = lst_user_id[i].get_attribute('href').split('=')[-1]
        # 把新的user_id插入数据库
        try:
            cue.execute("insert into music163_user_id (user_id)values (%s)", [user_id])
        except:
            con.rollback()
        else:
            con.commit()

    # 把该链接标记为已爬取
    try:
        cue.execute("update music163_follow_href set is_used = 1 where follow_href = (%s)", follow_href)
    except:
        con.rollback()
    else:
        con.commit()


def thread_parse_user():
    while True:
        try:
            con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c,
                                  port=port)
            cue = con.cursor()
            cue.execute("select user_id from music163_user_id where is_used = 0 limit 1")
            user_id = cue.fetchone()[0]
            parse_user(user_id)
        except:
            print('user id get error...')
            time.sleep(10)
            pass


def thread_parse_href():
    while True:
        try:
            con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c,
                                  port=port)
            cue = con.cursor()
            cue.execute("select follow_href from music163_follow_href where is_used = 0 limit 1")
            follow_href = cue.fetchone()[0]
            parse_follows(follow_href)
        except:
            print('follows href get error...')
            time.sleep(100)
            pass


if __name__ == '__main__':
    try:
        con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c,
                              port=port)
        cue = con.cursor()
        cue.execute("insert into music163_user_id (user_id)values (%s)", '40136303')
        con.commit()
    except:
        pass

    threading.Thread(target=thread_parse_user).start()
    threading.Thread(target=thread_parse_href).start()
