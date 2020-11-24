from scrapy import *
from scrapy.linkextractors import *
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose as Map, Join
from scrapy.crawler import CrawlerProcess


class Model(Item):
    titulo = Field()
    titulo_iframe = Field()


class W3SchoolsCrawler(Spider):
    name = 'W3Schools'

    custom_settings = {
        'LOG_ENABLED': False,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'USER_AGENT': 'Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36',
        'ALLOWED_DOMAINS': ['w3schools.com'],
    }

    start_urls = ['https://www.w3schools.com/html/html_iframe.asp']

    def parse(self, response):
        sel = Selector(response)
        titulo = sel.xpath('//div[@id="main"]//h1/span/text()').get()
        meta_data = {'titulo': titulo}
        iframe_url = sel.xpath(
            '//div[@id="main"]//iframe[@width="99%"]/@src').get()
        iframe_url = "https://www.w3schools.com/html/"+iframe_url
        yield Request(iframe_url, callback=self.parse_iframe, meta=meta_data)

    def parse_iframe(self, rs):
        item = ItemLoader(Model(), rs)
        item.default_input_processor = Map(self.clearText)
        item.default_output_processor = Join()
        item.add_xpath('titulo_iframe', '//div[@id="main"]//h1/span/text()')
        item.add_value('titulo', rs.meta.get('titulo'))
        yield item.load_item()

    def clearText(self, txt):
        return txt.replace('null', '').replace('\n', '').replace('\r', '').replace('\t', '').strip().rstrip().lstrip()

if __name__ == '__main__':
    process = CrawlerProcess(settings={
        'FEEDS': {
            '%(time)s.json': {'format': 'json'},
            '%(time)sjslines.json': {'format': 'jsonlines'},
            '%(time)s.csv': {'format': 'csv'},
            '%(time)s.xml': {'format': 'xml'},
        },
    })
    process.crawl(W3SchoolsCrawler)
    process.start()
