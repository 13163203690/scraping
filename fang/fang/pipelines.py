# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter
from fang.items import NewHouseItem,ESFHouseItem
import csv
class FangPipeline:
    def __init__(self):
        self.newhouse_fp = open('newhouse.json', 'wb')
        self.esfhouse_fp = open('esfhouse.json', 'wb')
        self.newhouse_exporter = JsonLinesItemExporter(self.newhouse_fp, ensure_ascii=False)
        self.esfhouse_exporter = JsonLinesItemExporter(self.esfhouse_fp, ensure_ascii=False)

    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            self.newhouse_exporter.export_item(item)
        elif isinstance(item, ESFHouseItem):
            self.esfhouse_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.newhouse_fp.close()
        self.esfhouse_fp.close()

class FangCSVPipeline(object):
    def __init__(self):
        print("开始写入...")
        self.f1 = open('new_house.csv', 'w', newline='')
        self.write1 = csv.writer(self.f1)
        self.write1.writerow(["城市", "小区名称", "价格", "几居",
                              "面积", "地址", "行政区", "是否在售", "详细url"])

        self.f2 = open('esf_house1.csv', 'w', newline='')
        self.write2 = csv.writer(self.f2)
        self.write2.writerow(["城市", "小区的名字", "几居", "层", "朝向",
                              "年代", "地址", "建筑面积", "总价", "单价", "详细的url"])

        self.f3 = open('rent_house.csv', 'w', newline='')
        self.write3 = csv.writer(self.f3)
        self.write3.writerow(['城市', '标题', '房间数', '平方数',
                              '价格', '地址', '交通描述', '区', '房间朝向'])



    def process_item(self, item, spider):
        print("正在写入...")
        if isinstance(item, NewHouseItem):
            self.write1.writerow([item['city'], item['name'], item['price'],
                                  item['rooms'], item['area'], item['address'], item['district'], item['sale']
                                     , item['origin_url']])
        elif isinstance(item, ESFHouseItem):
            self.write2.writerow([item['city'], item['name'], item['rooms'],
                                  item['floor'], item['toward'], item['year'], item['address'], item['area']
                                     , item['price'], item['unit'], item['origin_url']])
        return item# elif isinstance(item, RenthousescrapyItem):
        #     self.write3.writerow([item['city'], item['title'], item['rooms'], item['area'], item['price']
        #                              , item['address'], item['traffic'], item['region'],
        #                           item['direction']])

    def close_spider(self, item, spider):
        print("写入完成...")
        self.f1.close()
        self.f2.close()
        #self.f3.close()
import pymysql
class FangSqlPipeline(object):
    def __init__(self):
        dbparams = {
            'host':'127.0.0.1',
            'port':3306,
            'user':'root',
            'password':'root',
            'database':'fang',
            'charset':'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None
    def process_item(self, item, spider):
        self.cursor.execute(self.sql,(item["province"],item['city'],item['name'],item['room'],item['address'],item['price'],item['area'],item['on_sale'],item['dateil_url']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into fang_info(id, province, city, name, room, address, price, area, on_sale, dateil_url) values(null, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            return self._sql
        return self._sql






