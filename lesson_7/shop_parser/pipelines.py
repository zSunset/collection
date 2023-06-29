# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from shop_parser import settings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class ShopParserPipeline:

    def __init__(self) -> None:
        uri = f"mongodb+srv://{settings.LOGIN_MDB}:{settings.PASSWORD_MDB}@cluster0.dqkosbc.mongodb.net/"
        client = MongoClient(uri, server_api=ServerApi('1'))
        client.admin.command('ping')
        mydb = client['lesson_7']
        self.mycol = mydb['collection']

    def process_item(self, item, spider):
        collection = self.mycol[spider.name]
        collection.insert_one(item)
        return item

class ShopPhotosParserPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        link_photo = []
        
        for all_photos in item['all_photo']:
            data = f'https://www.castorama.ru{all_photos}'
            link_photo.append(data)
        
        for img in link_photo:
            try:
                yield scrapy.Request(img)
            except Exception as misstake:
                print(misstake)
    
    def item_completed(self, results, item, info):
        if results:
            item['all_photo'] = [itm[1] for itm in results if itm[0]]
        return item
    
    