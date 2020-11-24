from scrapy import *
from scrapy.linkextractors import *
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose as Map, Join


class Farmacia(Item):
    nom = Field()
    pre = Field()


class CruzVerdeCrawler(CrawlSpider):
    name = "Data"

    custom_settings = {
        'LOG_ENABLED': False,
        'USER_AGENT': 'Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36',
        'DOWNLOAD_DELAY': 2,
        'CLOSESPIDER_PAGECOUNT': 10,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'ALLOWED_DOMAINS': ['cruzverde.cl'],
    }
    start_urls = ['https://www.cruzverde.cl/medicamentos/']

    rules = (
        Rule(
            LinkExtractor(
                allow=r'start=\d+',
                tags=('a', 'button'),
                attrs=('href', 'data-url')
            ), follow=True, callback="parse_farmacia"
        ),
    )

    def parse_farmacia(self, rs):
        sel = Selector(rs)
        productos = sel.xpath('//div[@class="col-12 col-lg-4"]')
        for producto in productos:
            item = ItemLoader(Farmacia(), producto)
            item.default_input_processor = Map(self.clearText)#Map para todos por defecto
            item.default_output_processor = Join()  # Juntar todo en un solo textoi
            item.add_xpath('nom', './/div[@class="pdp-link"]/a/text()')
            item.add_xpath('pre', './/span[@class="value"]/text()')
            # 'pre', '//div[contains(@class, "large-price")]/span[@class="value"]/text()')
            # 'pre', 'normalize-space(.//span[@class="value"]/text())')
            yield item.load_item()

    def clearText(self, txt):
        return txt.replace('null', '').replace('(Oferta)', '').replace(
            '\n', '').replace('\r', '').replace('\t', '').replace('   ', '').replace('   $', '').replace('$', '').replace('  ', '').strip().rstrip().lstrip()
