from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup


class Noticia(Item):
    titular = Field()
    descripcion = Field()


class ElUniversoSpider(Spider):
    name = "MiSegundoSpider"
    custom_settings = {
        "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }
    start_urls = ['https://www.eluniverso.com/deportes']

    def parse(self, rs):
        soup = BeautifulSoup(rs.body)
        contenedor_noticias = soup.find_all('div', class_='view-content')

        for contenedor in contenedor_noticias:
            noticias = contenedor.find_all(
                'div', class_='posts', recursive=False)
            for noticia in noticias:
                item = ItemLoader(Noticia(), rs.body)
                titular = noticia.find('h2').text
                descripcion = noticia.find('p').text
                item.add_value('titular', titular)
                item.add_value('descripcion', descripcion)
                yield item.load_item()
