# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from online_shop import settings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class OnlineShopPipeline:

    def __init__(self) -> None:
        uri = f"mongodb+srv://{settings.LOGIN_MDB}:{settings.PASSWORD_MDB}@cluster0.dqkosbc.mongodb.net/"
        client = MongoClient(uri, server_api=ServerApi('1'))
        client.admin.command('ping')
        mydb = client['lesson_8']
        self.mycol = mydb['collection']

    def process_item(self, item, spider):
        collection = self.mycol[spider.name]
        collection.insert_one(item)
        return item
    
    


class OnlineShopParserPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        link_photo = []
        link_big_photo = []
        
        for all_photos in item['photo_smalls']:
            link_photo.append(all_photos)
        
        for img in link_photo:
            try:
                yield scrapy.Request(img)
            except Exception as misstake:
                print(misstake)

        for all_photos_big in item['photo_big']:
            link_big_photo.append(all_photos_big)
        
        for img_big in link_big_photo:
            try:
                yield scrapy.Request(img_big)
            except Exception as misstake:
                print(misstake)
