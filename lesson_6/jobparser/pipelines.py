# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from jobparser import settings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class JobparserPipeline:
    def __init__(self) -> None:
        uri = f"mongodb+srv://{settings.LOGIN_MDB}:{settings.PASSWORD_MDB}@cluster0.dqkosbc.mongodb.net/"
        client = MongoClient(uri, server_api=ServerApi('1'))
        client.admin.command('ping')
        mydb = client['lesson_6']
        self.mycol = mydb['collection']

    def process_item(self, item, spider):
        item['salary'] = self.process_salary(item['salary'])
        collection = self.mycol[spider.name]
        collection.insert_one(item)
        return item

    def process_salary(self, salary):
        dec = {}
        dec['от'] = int(salary[1].replace(u'\xa0', u''))
        dec['до'] = int(salary[3].replace(u'\xa0', u''))
        dec['валюта'] = salary[5]
        return dec