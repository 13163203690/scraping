# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuItem(scrapy.Item):
    author= scrapy.Field()
    title=scrapy.Field()
    content=scrapy.Field()
    #avatar=scrapy.Field()
    publish_time =scrapy.Field()
    letterNumber=scrapy.Field()
    article_id=scrapy.Field()
    likes_count= scrapy.Field()
    views_count= scrapy.Field()
    origin_url=scrapy.Field()
