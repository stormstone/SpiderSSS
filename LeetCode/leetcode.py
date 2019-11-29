import pandas as pd
import os
import eventlet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

path_df_links = 'df_links_01.csv'
path_df_problems = 'df_problems_01.csv'

chrome_options = Options()
chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)


def parse_links():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)

    start_url = 'https://leetcode-cn.com/problemset/all/'
    print('driver get url...')
    try:
        driver.get(start_url)
    except:
        driver.close()
        parse_links()
    print('click row select to all...')
    driver.find_element_by_xpath('//select[@class="form-control"]//option[4]').click()

    lst_ids = driver.find_elements_by_xpath('//tbody[@class="reactable-data"]//tr//td[2]')
    lst_problems = driver.find_elements_by_xpath('//tbody[@class="reactable-data"]//tr//td[3]//a')
    print(len(lst_problems))
    df_links = pd.DataFrame()
    for id, a in zip(lst_ids, lst_problems):
        href = a.get_attribute('href')
        title = a.text.strip()
        df_links = df_links.append([[id.text, title, href, False]])

    df_links.columns = ['id', 'title', 'href', 'is_crawled']
    df_links.to_csv(path_df_links, index=False, encoding='utf8')
    driver.close()


def parse_problem(title, href):
    driver.get(href)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="css-nj515r-Tools e5i1odf4"]')))
    # driver.implicitly_wait(10)

    difficult = driver.find_element_by_xpath('//div[@class="css-nj515r-Tools e5i1odf4"]//span[2]').text
    count_star = driver.find_element_by_xpath('//button[@class="css-atw98h-Button e5i1odf1"]//span').text
    # count_review = driver.find_element_by_xpath(
    #     '//*[@id="question-detail-main-tabs"]/div[1]/div/div[2]/a/div/span/div').text
    # count_review = driver.find_element_by_css_selector('.css-pusovc-TabHeader').text
    lst_count_pc = driver.find_elements_by_xpath('//p[@class="css-1onqcw6-Count e5i1odf10"]')
    count_pass = lst_count_pc[0].text
    count_commit = lst_count_pc[1].text
    # 标签
    lst_labels = driver.find_elements_by_xpath('//a[@class="topic-tag__1z4-"]')
    labels = [label.get_attribute('href') for label in lst_labels]
    labels = [label.split('/')[-2] for label in labels]
    # print(difficult, count_star, count_pass, count_commit, labels)
    df_tmp = pd.DataFrame()
    df_tmp = df_tmp.append([[title, difficult, count_star, count_pass, count_commit, labels, href]])
    df_tmp.columns = ['title', 'difficult', 'count_star', 'count_pass', 'count_commit', 'labels', 'href']
    return df_tmp


def get_all():
    if os.path.exists(path_df_problems):
        df_problems = pd.read_csv(path_df_problems)
    else:
        df_problems = pd.DataFrame()
    df_links = pd.read_csv(path_df_links)
    count_no_spider = df_links[df_links['is_crawled'] == False].shape[0]
    while count_no_spider:
        for i in range(df_links.shape[0]):
            is_crawled = df_links.loc[i, 'is_crawled']
            if is_crawled:
                continue
            title = df_links.loc[i, 'title']
            href = df_links.loc[i, 'href']
            print(href)

            # df_tmp = parse_problem(title, href)
            # df_problems = df_problems.append(df_tmp)
            # df_links.loc[i, 'is_crawled'] = True
            # print(href, 'success\n')

            with eventlet.Timeout(20, False):  # 设置超时时间为10秒
                try:
                    df_tmp = parse_problem(title, href)
                    df_problems = df_problems.append(df_tmp)
                    df_links.loc[i, 'is_crawled'] = True
                    print(href, 'success\n')
                except:
                    print(href, 'False\n')
                    continue

            df_problems.to_csv(path_df_problems, index=False, encoding='utf8')
            df_links.to_csv(path_df_links, index=False, encoding='utf8')
            count_no_spider = df_links[df_links['is_crawled'] == False].shape[0]


if __name__ == '__main__':
    if os.path.exists(path_df_links):
        pass
    else:
        parse_links()
    get_all()
