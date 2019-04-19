from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")  # 根据name查找元素
elem.send_keys("pycon")  # 输入内容
elem.send_keys(Keys.RETURN)  # 回车
print(driver.page_source)  # 返回浏览器渲染后页面
