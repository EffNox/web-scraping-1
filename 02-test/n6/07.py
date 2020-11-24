from scrapy.spiders import Spider
from scrapy.crawler import CrawlerRunner
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from pymongo import MongoClient


class ExtractorClima(Spider):
    client = MongoClient('localhost')
    db = client['web-scraping']
    collection = db['clima_scrapy']

    name = 'Clima'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36',
        'LOG_ENABLED': False,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DOWNLOAD_DELAY': 2,
        'CLOSESPIDER_PAGECOUNT': 10,
        'ALLOWED_DOMAINS': [''],
    }
    start_urls = [
        'https://www.accuweather.com/es/pe/lima/264120/current-weather/264120',
        'https://www.accuweather.com/es/ar/buenos-aires/7894/current-weather/7894',
        'https://www.accuweather.com/es/cr/chile/115164/current-weather/115164'
    ]

    def parse(self, rs):
        ciudad = rs.xpath('//h1[@class="header-loc"]/text()').get()
        current = rs.xpath('//div[@class="display-temp"]/text()').get()
        real_feel = rs.xpath(
            '//div[@class="current-weather-extra"]/div[1]/text()').get()
        real_feel = self.clearText(real_feel)
        ciudad = self.clearText(ciudad)
        current = self.clearText(current)
        print(ciudad, current, real_feel)
        self.collection.update_one({
            'ciudad': ciudad
        }, {
            "$set": {
                'current': current,
                'real_feel': real_feel,
                'ciudad': ciudad
            }
        }, upsert=True)
      

    def clearText(self, v):
        return v.replace('RealFeel®','').replace('RealFeel Shade™', '').replace('°', '').strip()

# process = CrawlerProcess()
# process.crawl(ExtractorClima)
# process.start()


runner = CrawlerRunner()
task = LoopingCall(lambda: runner.crawl(ExtractorClima))
task.start(20, now=True)
reactor.run()
