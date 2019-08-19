# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv

class DoubanPipeline(object):
    def process_item(self, item, spider):
        with open("xueguanying.csv",'a',newline='') as f:
            filename=['user','time','comment']
            csv.DictReader(f,filenames=filename,item=item)
