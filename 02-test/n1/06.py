from scrapy import *
from scrapy.linkextractors import *
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose as Map


class Hotel(Item):
    nom = Field()
    des = Field()
    pre = Field()
    reg = Field()


class TipAdVisor(CrawlSpider):
    name = "Hoteles"

    custom_settings = {
        # 'LOG_ENABLED': False,
        # 'LOG_FILE': 'dt.txt',
        "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        'DOWNLOAD_DELAY': 2,
        'CLOSESPIDER_PAGECOUNT': 2,
        # 'CONCURRENT_REQUESTS': 0,
        # 'CONCURRENT_REQUESTS_PER_DOMAIN': 0,
        # 'CONCURRENT_REQUESTS_PER_IP': 0,
        # 'RANDOMIZE_DOWNLOAD_DELAY': 0,
        # 'ALLOWED_DOMAINS': ['tripadvisor.com.pe']
        # 'DOWNLOAD_DELAY': 5.0,
    }

    start_urls = [
        'https://www.tripadvisor.com.pe/Tourism-g294316-Lima_Lima_Region-Vacations.html']

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/VacationRentalReview-'
            ), follow=True, callback='parse_hotel'
        ),
    )

    def quitarSimboSol(self, texto):
        return texto.replace('S/.', '')

    def parse_hotel(self, rs):
        sel = Selector(rs)
        item = ItemLoader(Hotel(), sel)
        item.add_xpath(
            'nom', '/h1[contains(@class, "propertyHeading")]/text()')
        item.add_xpath('des', './/div[@class="VGN0nqph"]/text()')
        item.add_xpath(
            'pre', '//span[@class="_3z9G8Gio"]/text()', Map(self.quitarSimboSol))
        item.add_xpath('reg', '//div[contains(@class, "VARqlzzo")]/text()')
        yield item.load_item()
