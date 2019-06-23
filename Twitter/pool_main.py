import os
import pymysql
from multiprocessing import Pool as ProcessPool
from config import *

con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c,
                      port=port)
cue = con.cursor()


def pool_main(username):
    os.system('python pool_down_img.py ' + username)


if __name__ == '__main__':
    cue.execute("select distinct username from twitter_img where is_crawled = 0;")
    lst_users = [i[0] for i in cue.fetchall()]

    # 多进程
    pool = ProcessPool(2)
    pool.map(pool_main, lst_users)
    pool.close()
    pool.join()
