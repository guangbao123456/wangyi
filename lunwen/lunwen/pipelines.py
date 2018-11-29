# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class LunwenPipeline(object):
    def __init__(self):
        myconn=MongoClient('127.0.0.1',27017)
        mydb=myconn['wurenji']
        self.mycol=mydb['wangyi']
    def process_item(self, item, spider):
        self.mycol.insert(dict(item))
        return item
