# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OnlineShopItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    photo_big = scrapy.Field()
    photo_smalls = scrapy.Field()
    _id = scrapy.Field()
