import re
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from selenium.webdriver import Chrome
import xlwings as xw
class  LagouSpider(object):

    def __init__(self):
        self.driver =Chrome()
        self.url = 'https://www.lagou.com/jobs/list_python%E5%AE%9E%E4%B9%A0'
        self.positions = []
        self.count_num = 1
        self.save_count = 0
        self.app = xw.App(visible=True, add_book=False)
        self.position_file = self.app.books.open('lagou_positions.xlsx')
        self.sheet = self.position_file.sheets[0]

    def run(self):
        # 打开网页
        self.driver.get(self.url)
        # 登录操作
        self.login()
        # 输入从第几页开始爬取
        spider_page = int(input("输入从第几页开始爬取，输入整数："))
        if spider_page > 1:
            # 翻页操作（爬取中断后输入页码继续爬取操作，从第一页开始爬则输入1，从第二页开始爬则输入2）
            self.continue_spider(spider_page)
        # 数据爬取部分
        while True:
            # 等待网页加载完毕再返回源码(下一页按钮)
            WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="pager_container"]/span[last()]')))
            # 获取网页源代码
            source = self.driver.page_source
            # 获取详细职位信息网址
            self.parse_page_url(source)
            nextpage_btn = self.driver.find_element_by_xpath('//div[@class="pager_container"]/span[@action="next"]')
            # 若没有下一页则跳出循环，完成爬取
            if re.search(r'action="next" class="pager_next pager_next_disabled"',self.driver.page_source):
                print("爬取完成！")
                break
            else:
                nextpage_btn.click()
                time.sleep(1)

    def login(self):
        loginTag = self.driver.find_element_by_css_selector('.login')
        usernameTag = self.driver.find_element_by_xpath("//input[@type='text']")
        passwordTag = self.driver.find_element_by_xpath("//input[@type='password']")
        login = self.driver.find_element_by_xpath(
            "//div[@class='login-btn login-password sense_login_password btn-green']")

        actions = ActionChains(self.driver)
        actions.move_to_element(loginTag)
        actions.click(loginTag)
        actions.send_keys_to_element(usernameTag, '13163203690')
        actions.send_keys_to_element(passwordTag, '13163203690Aa')
        actions.move_to_element(login)
        actions.click(login)
        actions.perform()
        # 15秒内输入验证码
        time.sleep(15)

    def continue_spider(self, num):
        self.count_num = 15 * (num - 1) + 1
        self.save_count = num - 1
        # 当前页面页码
        current_page = 1
        # 循环-翻页操作
        while True:
            if current_page == num:
                break
            else:
                # 下一页按钮
                next_page_Btn = self.driver.find_element_by_xpath("//div[@class='pager_container']/span[last()]")
                actions = ActionChains(self.driver)
                actions.move_to_element(next_page_Btn)
                actions.click(next_page_Btn)
                actions.perform()

                current_page += 1
                time.sleep(1)

    def parse_page_url(self, source):
        html = etree.HTML(source)
        detail_links = html.xpath('//a[@class="position_link"]/@href')
        for link in detail_links:
            # 打开详细职位信息网址
            self.request_detail_page(link)
            # 暂停一秒，以免爬取过快
            time.sleep(1)
    def request_detail_page(self, url):
        # 新建一个窗口，打开详细页面
        self.driver.execute_script("window.open('%s')" % url)
        # 切换到详情页面窗口
        self.driver.switch_to.window(self.driver.window_handles[1])
        # 等待页面加载完毕再返回源码
        WebDriverWait(self.driver, timeout=20).until(
             EC.presence_of_element_located((By.XPATH, '//span[@class="position-head-wrap-name"]')))
        page_source = self.driver.page_source
        self.parse_detail_page(page_source)
        # 暂停一秒，防止爬取过快
        time.sleep(1)
        # 关闭挡墙详情页面，并回到上一个页面窗口
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
    def parse_detail_page(self,source):
        detail_url = etree.HTML(source)  # 解析详情页
        name = re.findall(r'<span class="position-head-wrap-name">([^<]*)', self.driver.page_source)[0]  # 得到职位名称
        advantage = re.findall(r'职位诱惑：.*?<p>([^<]*)', self.driver.page_source, re.DOTALL)[0]  # 得到职位诱惑内容
        job_request = detail_url.xpath('//dd[@class="job_request"]//span/text()')
        salary = job_request[0]  # 获取薪资
        request = re.sub('[/]', '', ','.join(job_request[1:]))
        job_descript = detail_url.xpath('//div[@class="job-detail"]/text()')  # 获取职位描述
        job_descript = ' '.join(job_descript)
        address = re.findall(r'<input type="hidden" name="positionAddress" value="([^"]*)', self.driver.page_source)[
            0].strip()  # 获取工作地点
        company = detail_url.xpath('//h4[@class="company"]/text()')
        position = {  # 将获取到的数据存入字典
            'name': name,
            'address': address,
            'advantage': advantage,
            'salary': salary,
            'request': request,
            'job_descript': job_descript,
            'company': company
        }
        time.sleep(1)  # 睡一下 以防开启太快被临时封ip
        self.positions.append(position)  # 将存放数据的字典添加到列表中
        self.positions.append(position)
        self.count_num += 1
        print("已爬取%d条数据" % (self.count_num - 1))
        if self.count_num % 15 == 1:
            self.save_positions()
    def save_positions(self):
        save_positions = pd.DataFrame(self.positions)
        # 重新开始保存下一页
        self.positions = []
        row = 1 + 16 * self.save_count
        self.save_count += 1
        print('已保存%d页' % self.save_count)
        print('*' * 30)
        self.sheet.range('A' + str(row)).value = save_positions
        self.position_file.save()



if __name__ == '__main__':
    spider = LagouSpider()
    spider.run()
