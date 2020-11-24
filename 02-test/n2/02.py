from scrapy import *
from scrapy.linkextractors import *
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose as Map


class Opinion(Item):
    titulo = Field()
    calificacion = Field()
    contenido = Field()
    autor = Field()


class TripAdVisorCrawler(CrawlSpider):
    name = "OpinionesTripAdVisor"

    custom_settings = {
        'LOG_ENABLED': False,
        'USER_AGENT': 'Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36',
        'DOWNLOAD_DELAY': 2,
        'CLOSESPIDER_PAGECOUNT': 50,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'ALLOWED_DOMAINS': ['tripadvisor.com.pe/'],
    }
    start_urls = [
        'https://www.tripadvisor.com.pe/Hotels-g294316-Lima_Lima_Region-Hotels.html']

    rules = (
        Rule(
            LinkExtractor(
                allow=r'-oa\d+-'
            ), follow=True
        ),
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-',
                # Reduce el expectro de la busqueda
                restrict_xpaths=[
                    '//div[@id="taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0"]//a[@data-clicksource="HotelName"]']
            )
        ),
        Rule(
            LinkExtractor(
                allow=r'-or\d+-'
            ), follow=True
        ),
        Rule(
            LinkExtractor(
                allow=r'/Profile/',
                restrict_xpaths=[
                    '//div[@data-test-target="reviews-tab"]//a[contains(@class, "ui_header_link")]']
            ), follow=True, callback="parse_opinion"
        )
    )

    def parse_opinion(self, rs):
        sel = Selector(rs)
        opiniones = sel.xpath('//div[@id="content"]/div/div')
        autor = sel.xpath('//h1/span[@class="_2wpJPTNc"]/text()').get()
        for opinion in opiniones:
            item = ItemLoader(Opinion(), opinion)
            item.add_value('autor', autor)
            item.add_xpath(
                'titulo', '//div[contains(@class, "_3IEJ3tAK")]//text()')
            item.add_xpath(
                'calificacion', '//div[contains(@class,"_1VhUEi8g")]/span/@class', Map(self.getCalificacion))
            item.add_xpath('contenido', '//q[@class="_tZZyFcY"]/text()')
            # item.add_xpath('autor', '//a[contains(@class, "ui_link")]//text()')
            yield item.load_item()

    def getCalificacion(self, txt):
        return txt.split('_')[-1]

    def clearText(self, txt):
        return txt.replace(
            '\n', '').replace('\r', '').replace('\t', '').strip()
