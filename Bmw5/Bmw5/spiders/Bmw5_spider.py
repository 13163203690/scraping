import scrapy
from Bmw5.items import Bmw5Item

class Bmw5SpiderSpider(scrapy.Spider):
    name = 'Bmw5_spider'
    allowed_domains = ['autohome.com']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html#pvareaid=2042194']
    # 其中start_urls需要我们修改，打开汽车之家官网，按品牌找车--> 宝马 --> 宝马--> 图片
    # 然后复制其地址，与原来的start_urls的参数替换即可

    def parse(self, response):
        uiboxs = response.xpath("//div[@class='uibox']")[1:]
        for uibox in uiboxs:
            title = uibox.xpath(".//div[@class='uibox-title']/a/text()").get()
            urls = uibox.xpath(".//ul/li/a/img/@src").getall()
            urls = list(map(lambda url: response.urljoin(url), urls))
            #print(urls)
            # # 后面这两行代码是需要编写完items.py后，才写的。
            item = Bmw5Item(title=title,image_urls=urls)
            yield item
