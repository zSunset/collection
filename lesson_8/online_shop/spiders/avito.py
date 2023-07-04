'''По каждому объявлению собрать наименование, ссылку, цену, описание и фотографии.
Фотографии можно взять одну большую, которая загрузится первой и остальные маленькие.'''
from scrapy.http import HtmlResponse
from scrapy_splash import SplashRequest
from online_shop.items import OnlineShopItem
from scrapy.loader import ItemLoader
import scrapy


class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["avito.ru"]
    start_urls = ["https://www.avito.ru/all/noutbuki/apple-ASgCAQICAUCo5A0U9Nlm?cd=1&d=1&f=ASgCAQECA0Co5A0U9Nlm8ooOFKSClAGUoRIUAgFFxpoMFXsiZnJvbSI6NTAwMDAsInRvIjowfQ&q=macbook"]
    page_number = 1

    def start_requests(self):
        if not self.start_urls and hasattr(self, "start_url"):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)"
            )
        for url in self.start_urls:
            yield SplashRequest(url)


    def parse(self, response: HtmlResponse, **kwargs):
        link = response.xpath('//h3[@itemprop="name"]/../@href').getall()
        for links in link:
            yield SplashRequest("https://avito.ru" + links, callback=self.shop_parse)
        self.page_number += 1
        next_page = f'https://www.avito.ru/all/noutbuki/apple-ASgCAQICAUCo5A0U9Nlm?cd=1&d=1&f=ASgCAQECA0Co5A0U9Nlm8ooOFKSClAGUoRIUAgFFxpoMFXsiZnJvbSI6NTAwMDAsInRvIjowfQ&p={self.page_number}&q=macbook'
        yield response.follow(next_page, callback=self.parse)
            
    
    def shop_parse(self, response: HtmlResponse):
        name = response.xpath('//span[@class="title-info-title-text"]/text()').get()
        price = response.xpath('//span[@class="styles-module-size_xxxl-A2qfi"]/@content').get()
        link = response.url
        description = response.xpath('//div[@itemprop="description"]/p/text()').getall()
        photo_big = response.xpath('//div[@class="image-frame-wrapper-_NvbY"]/img/@src').get()
        photo_smalls = response.xpath('//li[@class="images-preview-previewImageWrapper-RfThd"]/img/@src').getall()
        yield OnlineShopItem(name=name, link=link, price=price, description=description, photo_big=photo_big, photo_smalls=photo_smalls)