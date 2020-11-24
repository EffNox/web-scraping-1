from scrapy import *
from scrapy.linkextractors import *
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose as Map


class Articulo(Item):
    tit = Field()
    cont = Field()


class Review(Item):
    tit = Field()
    cal = Field()


class Video(Item):
    tit = Field()
    fec = Field()


class IGNCrawler(CrawlSpider):
    name = "IGN"

    custom_settings = {
        'LOG_ENABLED': False,
        'USER_AGENT': 'Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36',
        'DOWNLOAD_DELAY': 2,
        'CLOSESPIDER_PAGECOUNT': 10,
        'ALLOWED_DOMAINS': ['latam.ign.com'],
        'FEED_EXPORT_ENCODING': 'utf-8',
    }
    start_urls = [
        'https://latam.ign.com/se/?model=article&q=ps5']

    rules = (
        Rule(
            LinkExtractor(
                allow=r'type='
            ), follow=True
        ),
        Rule(
            LinkExtractor(
                allow=r'&page=\d+'  # \d+ es para verificar que sean números
            ), follow=True
        ),
        # REVIEWS
        Rule(
            LinkExtractor(
                allow=r'/review/'
            ), follow=True, callback="parse_review"
        ),
        # VIDEOS
        Rule(
            LinkExtractor(
                allow=r'/video/'
            ), follow=True, callback="parse_video"
        ),
        # ARTICULOS
        Rule(
            LinkExtractor(
                allow=r'/news/'
            ), follow=True, callback="parse_new"
        ),
    )

    def parse_new(self, rs):
        item = ItemLoader(Articulo(), rs)
        item.add_xpath('tit', '//h1[@id="id_title"]/text()',Map(self.clearText))
        item.add_xpath('cont', '//div[@id="id_text"]//*/text()',Map(self.clearText))
        yield item.load_item()

    def parse_review(self, rs):
        item = ItemLoader(Review(), rs)
        item.add_xpath('tit', '//h1/text()',Map(self.clearText))
        item.add_xpath(
            'cal', '//span[@class="side-wrapper side-wrapper hexagon-content"]/text()')
        yield item.load_item()

    def parse_video(self, rs):
        item = ItemLoader(Video(), rs)
        item.add_xpath('tit', '//h1/text()',Map(self.clearText))
        item.add_xpath('fec', '//span[@class="publish-date"]/text()',Map(self.clearText))
        yield item.load_item()

    def clearText(self, txt):
        return txt.replace(
            '\n', '').replace('\r', '').replace('\t', '').strip()
