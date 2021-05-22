# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

#
# class QsbkPipeline:
#     def __init__(self):
#         self.fp=open('qsbk.json','w',encoding='utf-8')
#     def process_item(self, item, spider):
#         item_json=json.dumps(item,ensure_ascii=False)
#         self.fp.write(item_json+'\n')
#         return item
#     def close_spider(self,spider):
#         self.fp.close()
#         print("爬虫接受了")
#优化
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exporters import JsonItemExporter,JsonLinesItemExporter
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class QsbkPipeline:
#     def __init__(self):
#         self.fp=open('qsbk.json','wb')
#         self.exporter=JsonItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
#         self.exporter.start_exporting()
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
#     def close_spider(self,spider):
#         self.exporter.finish_exporting()
#         self.fp.close()
#         print("爬虫over了")
#版本二比较耗内存，下面是版本三
class QsbkPipeline:
    def __init__(self):
        self.fp=open('qsbk.json','wb')
        self.exporter=JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    def close_spider(self,spider):
        self.fp.close()
        print("爬虫over了")