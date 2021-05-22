from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
class  Qiangpiao(object):

    def __init__(self):
        self.driver =Chrome()
        self.login_url='https://kyfw.12306.cn/otn/resources/login.html'
        self.initmy_ur1=''
    def login(self):
        self.driver.get(self.login_url)
        WebDriverWait(self.driver, 1000).until(
            EC.url_to_be(self.initmy_ur1))
        print("登录成功!")

    def order_ticket(self):
        pass
    def run(self):
        self.login()
        self.order_ticket()
if __name__ == '__main__':
    spider=Qiangpiao()
    spider.run()

