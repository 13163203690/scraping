'''
from selenium import webdriver
# chromedriver的绝对路径
driver_path = r'F:\Anaconda3\Scripts\chromedriver.exe'
# 初始化一个driver，并且指定chromedriver的路径
driver = webdriver.Chrome(executable_path=driver_path)
# 请求网页
driver.get("https://www.baidu.com/")
# 通过page_source获取网页源代码
print(driver.page_source)
# hide browser window
'''

# Simple assignment
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
driver = Chrome()
driver.get("https://www.baidu.com/")
# rememberBtn =driver.find_element_by_name('remember')
# rememberBtn.click()#但现在豆瓣好像没有记住登录这一选项
# your code inside this indent
# from selenium.webdriver.support.ui import Select
#
# # 选中这个标签，然后使用Select创建对象
# selectTag = Select(driver.find_element_by_name("jumpMenu"))
# # 根据索引选择
# selectTag.select_by_index(1)
# # 根据值选择
# selectTag.select_by_value("http://www.95yueba.com")
# # 根据可视的文本选择
# selectTag.select_by_visible_text("95秀客户端")
# # 取消选中所有选项
# selectTag.deselect_all()

#操作行为链
# inputTag = driver.find_element_by_id('kw')
# submitTag = driver.find_element_by_id('su')
#
# actions = ActionChains(driver)
# actions.move_to_element(inputTag)
# actions.send_keys_to_element(inputTag,'python')
# actions.move_to_element(submitTag)
# actions.click(submitTag)
# actions.perform()
#cookie
# for cookie in driver.get_cookies():
#      print(cookie)
# print('*'*30)
# print(driver.get_cookie('BAIDUID'))
# driver.delete_cookie('BAIDUID')
# driver.delete_all_cookies()

# 打开一个新的页面
driver.execute_script("window.open('https://baike.baidu.com/')")
# 切换到这个新的页面中
driver.switch_to.window(driver.window_handles[1])
print (driver.current_url)
print (driver.page_source)

#虽然在窗口中切换到了新的页面。但是driver中还没有切换。
#如果想要在代码中切换到新的页面,并且做一些爬虫。
#那么应该使用driver.switch_to_window来切换到指定的窗口·从driver.window_handles中取出具体第几个窗口
#driver.window_handler提一个列表,里面装的都是窗口句柄。手他会按照打开页面的顺序来存储窗口的句柄。
