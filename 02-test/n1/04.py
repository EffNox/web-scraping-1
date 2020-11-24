# from scrapy.item import Field
# from scrapy.item import Item
# from scrapy.spiders import Spider
# from scrapy.selector import Selector
# from scrapy.loader import ItemLoader
from scrapy import *

from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess


class Noticia(Item):
    titular = Field()
    descripcion = Field()


class ElUniversoSpider(Spider):
    name = "MiSegundoSpider"

    custom_settings = {
        'LOG_ENABLED': False,
        "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }

    start_urls = ['https://www.eluniverso.com/deportes']

    def parse(self, rs):
        sel = Selector(rs)
        noticias = sel.xpath(
            '//div[@class="view-content"]/div[@class="posts"]')
        for noticia in noticias:
            item = ItemLoader(Noticia(), noticia)
            item.add_xpath('titular', './/h2/a/text()')
            item.add_xpath('descripcion', './/p/text()')
            yield item.load_item()


if __name__ == '__main__':
    process = CrawlerProcess(settings={
        "FEEDS": {
            "%(time)sdt.json": {"format": "json"},
            "%(time)sjsonlines.json": {"format": "jsonlines"},
            "%(time)sdt.csv": {"format": "csv"},
            "%(time)sdt.xml": {"format": "xml"},
        },
    })
    process.crawl(ElUniversoSpider)
    process.start()
