from scrapy import *
from scrapy.linkextractors import *
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose as Map


class Articulo(Item):
    titulo = Field()
    descripcion = Field()
    precio = Field()


class MercadoLibreCrawler(CrawlSpider):
    name = 'Mercado Libre'

    custom_settings = {
        # 'LOG_ENABLED': False,
        'USER_AGENT': 'Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36',
        'DOWNLOAD_DELAY': 2,
        'CLOSESPIDER_PAGECOUNT': 2,
        'ALLOWED_DOMAINS': ['listado.mercadolibre.com.pe', 'articulo.mercadolibre.com.pe'],
    }
    start_urls = [
        'https://listado.mercadolibre.com.pe/animales-mascotas/perros/']

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/_Desde_'
            ), follow=True
        ),
        Rule(
            LinkExtractor(
                allow=r'/MPE-'
            ), follow=True, callback='parse_items'
        ),
    )

    def parse_items(self, rs):
        item = ItemLoader(Articulo(), rs)
        item.add_xpath(
            'titulo', '//h1[@class="ui-pdp-title"]/text()', Map(self.clearText))
        item.add_xpath(
            'descripcion', '//p[@class="ui-pdp-description__content"]/text()')
        item.add_xpath(
            'precio', '//span[contains(@class, "price-tag")]/span[@class="price-tag-fraction"]/text()', Map(lambda i: "S/. "+i))
        yield item.load_item()

    def clearText(self, txt):
        return txt.replace(
            '\n', '').replace('\r', '').replace('\t', '').strip()
