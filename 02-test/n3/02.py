from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

driver = webdriver.Edge('./edge3.exe')
# driver.implicitly_wait(10) # seconds
driver.get('https://www.olx.com.pe')

print(driver.title)
driver.maximize_window()
wait = WebDriverWait(driver, 10)
for i in range(4):
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@data-aut-id="btnLoadMore"]')))
    btn.click()
    wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]')))

# sleep(6)
anuncios = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')
for anuncio in anuncios:
    try:
        pre = anuncio.find_element_by_xpath(
            './/span[@data-aut-id="itemPrice"]').text
        nom = anuncio.find_element_by_xpath(
            './/span[@data-aut-id="itemTitle"]').text
        # dir = anuncio.find_element_by_xpath(
        # './/span[@data-aut-id="item-location"]').text
        print(pre, nom)
    except:
        None

print(len(anuncios))

# driver.close()
