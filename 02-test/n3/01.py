import random
from selenium import webdriver
from threading import Timer
from time import sleep
# from msedge.selenium_tools import Edge, EdgeOptions
# options = EdgeOptions()
# options.use_chromium = True
# options.binary_location='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
# driver = Edge(options=options, executable_path='./edge.exe')

driver = webdriver.Edge('./edge3.exe')
# driver.implicitly_wait(100)
driver.get('https://www.olx.com.pe/autos_c378')
# sleep(1)
print(driver.title)
driver.maximize_window()
btn = driver.find_element_by_xpath('//button[@data-aut-id="btnLoadMore"]')
for i in range(3):
    btn.click()
    sleep(random.uniform(8.0, 10.0))

autos = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')
for auto in autos:
    pre = auto.find_element_by_xpath(
        './/span[@data-aut-id="itemPrice"]').text
    nom = auto.find_element_by_xpath(
        './/span[@data-aut-id="itemTitle"]').text
    des = auto.find_element_by_xpath(
        './/span[@data-aut-id="itemDetails"]').text
    dir = auto.find_element_by_xpath(
        './/span[@data-aut-id="item-location"]').text
    print(pre, nom, des, dir)

print(len(autos))
driver.close()

# def fun():
#     btn = driver.find_element_by_xpath('//button[@data-aut-id="btnLoadMore"]')
#     btn.click()
#     print(driver.title)
#     autos = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')
#     for auto in autos:
#         pre = auto.find_element_by_xpath(
#             './/span[@data-aut-id="itemPrice"]').text
#         nom = auto.find_element_by_xpath(
#             './/span[@data-aut-id="itemTitle"]').text
#         des = auto.find_element_by_xpath(
#             './/span[@data-aut-id="itemDetails"]').text
#         dir = auto.find_element_by_xpath(
#             './/span[@data-aut-id="item-location"]').text
#         print(pre, nom, des, dir)


# r = Timer(1.0, fun).start()

# QUE HIJO DE PUTA, JAJAJAJAJA PRACTICAMENTE TIENE QUE HABER UN ASYNC SI NO NO CAPTURA LA DATA CSM jsjsjs
