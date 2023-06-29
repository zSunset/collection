from scrapy.http import HtmlResponse
from shop_parser.items import ShopParserItem
from scrapy.loader import ItemLoader
import scrapy


class CastoramaSpider(scrapy.Spider):
    name = "castorama"
    allowed_domains = ["castorama.ru"]
    start_urls = ["https://www.castorama.ru/windows-and-doors/exterior-doors/"]

    def parse(self, response: HtmlResponse, **kwargs):
        link = response.xpath('//a[@class="product-card__name ga-product-card-name"]/@href').getall()
        for links in link:
            yield response.follow(links, callback=self.product_parse)
        
        next_page = response.xpath('//a[@class="next i-next"]/@href').get()
                
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def product_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=ShopParserItem(), response=response)
        loader.add_xpath('name', '//h1[@class="product-essential__name hide-max-small"]/text()')
        loader.add_xpath('price', '//span[@class="regular-price"]/span[@class="price"]/span/span/text()')
        loader.add_value('url', response.url)       
        loader.add_xpath('all_photo', '//div[@class="js-zoom-container"]/img/@data-src')
        yield loader.load_item()