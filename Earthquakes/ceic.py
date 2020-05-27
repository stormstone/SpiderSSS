import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

start_url = "http://www.ceic.ac.cn/history"
driver.get(start_url)
driver.find_element_by_id("search").click()
time.sleep(3)

df_ceic = pd.DataFrame()
max_pages = 1  # 翻页次数，爬取最新只需爬取第一页数据
page = 1
tmp_gap = 6
while page <= max_pages:
    page += 1
    df_tmp = pd.DataFrame()
    lst_trs = driver.find_elements_by_xpath("//tr")
    tds = [td.text for td in lst_trs[0].find_elements_by_xpath("//td")]
    print(len(lst_trs), len(tds))
    i = 0
    while (i < len(tds)):
        print(tds[i:i + tmp_gap])
        df_tmp = df_tmp.append([tds[i:i + tmp_gap]])
        i += tmp_gap
    df_ceic = df_ceic.append(df_tmp)
    driver.find_element_by_xpath('//a[@title="下一页"]').click()
    time.sleep(0.5)

driver.close()
df_ceic.columns = ['震级', '发震时刻', '纬度', '经度', '深度', '参考位置']
df_ceic.to_csv('./data/df_ceic_tmp.csv', index=False)
