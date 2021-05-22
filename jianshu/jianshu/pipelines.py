# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from twisted.enterprise import adbapi # 使用异步数据库处理连接池
from pymysql import cursors # 数据库游标类

class JianshuPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'jianshu',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['title'], item['content'],
                                       item['author'], item['letterNumber'],
                                       item['article_id'],
                                       item['publish_time'],
                                       item['likes_count'], item['views_count'],
                                       item['origin_url']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id,title,content,author,letterNumber,
            article_id,publish_time,likes_count,views_count,origin_url) values (null,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql


class JianshuTwistedPipeline(object):
    def __init__(self):
        params = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'jianshu',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        # 调用异步连接池实现异步插入数据库
        self.dbpool = adbapi.ConnectionPool("pymysql", **params)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''insert into article(id,title,content,author,letterNumber,
            article_id,publish_time,origin_url,likes_count,views_count) values (null,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        # 异步插入数据
        defer = self.dbpool.runInteraction(self.insert_item, item)
        # 错误处理
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, item, cursor):
        cursor.execute(self.sql, (item['title'], item['content'],
                                       item['author'], item['letterNumber'],
                                       item['article_id'],
                                       item['publish_time'],
                                       item['likes_count'], item['views_count'],
                                       item['origin_url']))

    def handle_error(self, item, error, spider):
        print('+' * 30 + 'error' + '+' * 30)
        print(error)
        print('+' * 30 + 'error' + '+' * 30)











