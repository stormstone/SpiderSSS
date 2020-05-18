import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

driver = webdriver.Chrome(options=chrome_options)

start_url = "https://www.zhihu.com/search?type=content&q=%E6%B1%89%E5%BE%97"
driver.get(start_url)