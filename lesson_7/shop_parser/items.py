from itemloaders.processors import MapCompose, TakeFirst, Compose
import scrapy

def clean_price(value):
    try:
        if value[0]:
            value = int(value.replace(' ', ''))

    except Exception:
        pass
    return value

def clean_name(value):
    return ''.join(value).strip()


class ShopParserItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(clean_name), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clean_price), output_processor=TakeFirst())
    url = scrapy.Field() 
    all_photo = scrapy.Field()
    _id = scrapy.Field()
