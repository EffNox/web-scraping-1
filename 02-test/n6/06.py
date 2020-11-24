import time
import schedule
from schedule import every
from msedge.selenium_tools import Edge, EdgeOptions
from pymongo import MongoClient

client = MongoClient('localhost')
db = client['web-scraping']
collection = db['clima_selenium']

opts = EdgeOptions()
opts.add_argument(
    'user-agent=Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36'
)

start_urls = [
    'https://www.accuweather.com/es/pe/lima/264120/current-weather/264120',
    'https://www.accuweather.com/es/ar/buenos-aires/7894/current-weather/7894',
    'https://www.accuweather.com/es/cr/chile/115164/current-weather/115164'
]

def extraer_datos():
    driver = Edge(executable_path='./edgeDriver.exe', options=opts)
    for url in start_urls:
        driver.get(url)
        ciudad = driver.find_element_by_xpath('//h1[@class="header-loc"]').text
        current = driver.find_element_by_xpath(
            '//div[@class="display-temp"]').text
        real_feel = driver.find_elements_by_xpath(
            '//div[@class="current-weather-extra"]/div')[1].text
        ciudad = clearText(ciudad)
        current = clearText(current)
        real_feel = clearText(real_feel)

        collection.update_one({
            'ciudad': ciudad
        }, {
            "$set": {
                'current': current,
                'real_feel': real_feel,
                'ciudad': ciudad
            }
        }, upsert=True)

    driver.close()


def clearText(v):
    return v.replace('RealFeel Shade™', '').replace('°', '').strip()


if __name__ == '__main__':
    extraer_datos()
    schedule, every(1).minutes.do(extraer_datos)
    while True:
        schedule.run_pending()
        time.sleep(1)
