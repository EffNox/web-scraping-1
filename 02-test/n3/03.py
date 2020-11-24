from selenium.webdriver.common.by import By
from msedge.selenium_tools import Edge, EdgeOptions
opts = EdgeOptions()
opts.add_argument(
    'user-agent=Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36'
)
driver = Edge(options=opts, executable_path='./edge1.exe')

driver.get('https://listado.mercadolibre.com.pe/aviones-guerra')

while True:
    links_productos = driver.find_elements(
        By.XPATH, '//a[@class="ui-search-item__group__element ui-search-link"]')
    links_de_la_pagina = []
    for tag_a in links_productos:
        links_de_la_pagina.append(tag_a.get_attribute('href'))

    for link in links_de_la_pagina:
        try:
            driver.get(link)
            titulo = driver.find_element_by_xpath(
                '//h1[@class="ui-pdp-title"]').text
            precio = driver.find_element_by_xpath(
                '//span[@itemprop="offers"]/span[@class="price-tag-fraction"]').text
            print(titulo, precio)
            driver.back()
        except:
            driver.back()

    try:
        btn_siguiente = driver.find_element_by_xpath('//span[text()="Siguiente"]')
        btn_siguiente.click()
    except:
        break
