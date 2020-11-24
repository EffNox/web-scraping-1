from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from msedge.selenium_tools import Edge
from selenium.webdriver.support.ui import WebDriverWait
from pymongo import MongoClient

driver = Edge(executable_path='./edgeDriver.exe')
wait = WebDriverWait(driver, 10)
driver.get('https://www.olx.com.pe')

client = MongoClient('localhost')
db = client['web-scraping']
collection = db['anuncios_olx_selenium']

for i in range(2):
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@data-aut-id="btnLoadMore"]')))
    btn.click()
    wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]')))

driver.execute_script("window.scrollTo({top:20000, behavior:'smooth'});")

anuncios = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')
print(len(anuncios))
for anuncio in anuncios:
    try:
        pre = anuncio.find_element_by_xpath(
            './/span[@data-aut-id="itemPrice"]').text
        nom = anuncio.find_element_by_xpath(
            './/span[@data-aut-id="itemTitle"]').text
        collection.insert_one({'precio': pre, 'titulo': nom})
    except:
        None

# driver.close()
