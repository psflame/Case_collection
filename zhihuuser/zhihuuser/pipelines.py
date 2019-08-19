# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class MongoPipeline(object):
    collection_name = 'users'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.setting.get('MONGO_URI'),
            mongo_db=crawler.setting.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        """update方法，第一个参数传入查询条件，这里使用的是url_token，第二个参数传入字典类型的对象，
        就是我们的item，第三个参数传入True，这样就可以保证，如果查询数据存在的话就更新，不存在的话就插入。
        这样就可以保证去重了"""
        self.db[self.collection_name].update({'url_token': item['url_token']}, {'$set': dict(item)}, True)
        return item
