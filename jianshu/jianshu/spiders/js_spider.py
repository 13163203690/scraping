import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu.items import JianshuItem
import json

class JsSpiderSpider(CrawlSpider):
    name = 'js_spider'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        script = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        process_url=response.url.split('?')[0]#  以问号分割取前一部分
        article_id=process_url.split('/')[-1] #  以 ‘/’ 分割获取最后一个字符串即为文章的id
        origin_url=response.url
        print( '1' * 100)
        data = json.loads(script)  # 传进来的数据转换成字典的格式
        # 开始解析data
        props = data.get('props')
        initialState = props.get('initialState')
        note = initialState.get('note')
        data_ = note.get('data')
        title = data_.get('public_title')
        content = data_.get('free_content')

        author = data_.get('user').get('nickname')  # 防止出错的话，可以使用if判断一下
        letterNumber = data_.get('wordage')
        likes_count = data_.get("likes_count")
        views_count = data_.get('views_count')

        # first_shared_at = data_.get('first_shared_at')  # 发布时间
        publish_time = data_.get('last_updated_at')  # 最近更改时间
        item = JianshuItem(title=title, content=content, author=author, letterNumber=letterNumber,
                           article_id=article_id, publish_time=publish_time, likes_count=likes_count,
                           views_count=views_count, origin_url=origin_url)
        print('y' * 100)
        print(item)
        print('y' * 100)
        yield item



