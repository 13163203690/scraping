import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wxapp.items import WxappItem


class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp.dreawer.com']
    start_urls = ['http://wxapp.dreawer.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+?mod=list&catid=2&page=\d'), follow=True),#设置全部固定完就不能爬取到其他页面
        Rule(LinkExtractor(allow=r'.+article-.+\.html'), callback="parse_detail", follow=False),
    )


    def parse_detail(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        title=response.xpath('//h1[@class ="ph"]//text()').get()
        print(title)
        p=response.xpath('//p[@class ="authors"]')
        author=p.xpath('.//a/text()').get()
        pub_time = p.xpath('.//span/text()').get()
        content1=response.xpath('//td[@id="article_content"]//text()').getall()
        content="".join(content1).strip()#转变成字符类型并去掉首位空字符
        item=WxappItem(title=title,author=author,pub_time=pub_time,content=content)
        yield  item

