from scrapy import *
from scrapy.linkextractors import *
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose as Map, Join
from scrapy.crawler import CrawlerProcess


class Departamento(Item):
    nom = Field()
    dir = Field()


class UrbaniaCrawler(CrawlSpider):
    name = 'Urbania'

    custom_settings = {
        'LOG_ENABLED': False,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'USER_AGENT': 'Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36',
        # 'DOWNLOAD_DELAY': 2,
        'CLOSESPIDER_PAGECOUNT': 2,
        'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_APIKEY': '9d35c06c62584a1993030871bfbbf8d5',
        # 'COOKIES_ENABLED': False,
    }

    start_urls = [
        'https://urbania.pe/buscar/proyectos-propiedades?page=1',
        'https://urbania.pe/buscar/proyectos-propiedades?page=2',
        'https://urbania.pe/buscar/proyectos-propiedades?page=3',
        'https://urbania.pe/buscar/proyectos-propiedades?page=4',
        'https://urbania.pe/buscar/proyectos-propiedades?page=5',
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/proyecto-',
            ), follow=True, callback='parse'
        ),
    )

    def parse(self, rs):
        sel = Selector(rs)
        item = ItemLoader(Departamento(), sel)
        item.default_input_processor = Map(self.clearText)
        item.default_output_processor = Join()
        item.add_xpath('nom', '//h2[@class="left-title"]/text()')
        item.add_xpath('dir', '//h2[@class="left-subtitle"]/b/text()')
        yield item.load_item()

    def clearText(self, txt):
        return txt.replace('null', '').replace('\n', '').replace('\r', '').replace('\t', '').strip().rstrip().lstrip()


if __name__ == '__main__':
    process = CrawlerProcess(settings={
        'FEEDS': {
            '%(time)s.json': {'format': 'json'}, '%(time)s.jsonl': {'format': 'jsonlines'},
            '%(time)s.csv': {'format': 'csv'}, '%(time)s.xml': {'format': 'xml'},
        },
    })
    process.crawl(UrbaniaCrawler)
    process.start()
