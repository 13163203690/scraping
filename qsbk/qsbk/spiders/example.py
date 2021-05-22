import scrapy
from qsbk.items import QsbkItem

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    base_url='https://www.qiushibaike.com'

    def parse(self, response):
        outerbox = response.xpath("//div[@class='col1 old-style-col1']/div")
        #items = []
        for box in outerbox:
            author = box.xpath(".//h2/text()").get().strip()
            content=box.xpath(".//div[@class='content']//text()").getall()
            content="".join(content).strip()
            item = QsbkItem(author=author,content=content)
            # item["author"] = author
            # item["content"] = content
            #items.append(item)
            yield item
        next_url=response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return
        else:
            yield  scrapy.Request(self.base_url+next_url,callback=self.parse)

        #     content = box.xpath(".//div[@class='content']/span/text()").extract_first().strip()
        #     item = QsbkItem()
        #     item["author"] = author
        #     item["content"] = content
        #     items.append(item)
        # return items