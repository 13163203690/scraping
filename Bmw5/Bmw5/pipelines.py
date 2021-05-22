# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
from urllib import request
from scrapy.pipelines.images import  ImagesPipeline
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from Bmw5 import settings

class Bmw5Pipeline:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def process_item(self, item, spider):
        title = item['title']
        urls = item['urls']
        title_path = os.path.join(self.path, title)
        if not os.path.exists(title_path):
            os.mkdir(title_path)
        for url in urls:
            # 这行代码是给每一种图片以它的地址命名，你仔细分析每一张图的图片地址前面的都一样，所以以下划线分割，取到最后一位字符就是名字。
            image_name = url.split("_")[-1]
            # 利用request库的urlretrieve将图片下载到title_path绝对路径。
            request.urlretrieve(url, os.path.join(title_path, image_name))
        return item

class Bmw5ImangePipeline( ImagesPipeline ):
    def get_media_requests(self, item, info):
        request_objs = super(Bmw5ImangePipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item=item
        return request_objs

            #发送下载请求
    def file_path(self, request, response=None, info=None, *, item=None):
        path = super(Bmw5ImangePipeline,self).file_path(request, response,info)
        title=request.item.get("title")
        images_store =settings.IMAGES_STORE
        category_path = os.path.join(images_store, title)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        image_name=path.replace("full/","")
        image_path=os.path .join(category_path,image_name)
        return image_path

