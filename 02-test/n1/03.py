from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

class Pregunta(Item):
    id = Field()
    pregunta = Field()
    # descripcion = Field()


class StackOverFlowSpider(Spider):
    name = "MiPrimerSpider"
    custom_settings = {
        "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }

    start_urls = ['https://stackoverflow.com/questions']

    def parse(self, rs):
        i = 0
        sel = Selector(rs)
        preguntas = sel.xpath(
            '//div[@id="questions"]//div[@class="question-summary"]')
        for vpregu in preguntas:
            item = ItemLoader(Pregunta(), vpregu)
            item.add_value('id', i)
            item.add_xpath('pregunta', './/h3/a/text()')
            # item.add_xpath('descripcion', './/div[@class="excerpt"]/text()')
            i += 1

            yield item.load_item()

