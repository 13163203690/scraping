import threading
import requests
from lxml import etree
from urllib import request
import os
import re
from queue import Queue
i = 0
class Producer(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    }
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Producer, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self,url):
        response = requests.get(url, headers=self.headers)
        text = response.text
        html = etree.HTML(text)
        imgs = html.xpath('//div[@class="page-content text-center"]//img[@class!="gif"]')
        global i
        for img in imgs:
            # print(etree.tostring(img,encoding='utf-8').decode('utf-8'))
            img_url = img.xpath(".//@data-original")[0]
            suffix = os.path.splitext(img_url)[1]
            alt = img.xpath(".//@alt")[0]
            alt = re.sub(r'[，。？?,/\\·]', '', alt)
            if alt == '':
                i = i + 1
                alt = 'image%d' % i
            img_name = alt + suffix
            #print(img_name)
            self.img_queue.put((img_url, img_name))
            # request.urlretrieve(img_url, 'images/'+img_name)

class Consumer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
    def run(self):
        while True:
            print("xiaofeiz")
            if self.page_queue.empty() and self.img_queue.empty():
                return
            img = self.img_queue.get(block=True)
            url,filename = img
            #request.urlretrieve(url,'images/'+filename)
            print(filename+'  下载完成！')

def spider():
    page_queue = Queue(5)#队列数目一定要和你爬取页数一样否则可能出错
    img_queue = Queue(40)
    for x in range(1, 6):
        url = "http://www.doutula.com/photo/list/?page=%d" % x
        page_queue.put(url)
    for x in range(4):
        t = Producer(page_queue,img_queue)
        t.start()

    for x in range(2):
        t = Consumer(page_queue,img_queue)
        t.start()
if __name__ == '__main__':
    spider()
