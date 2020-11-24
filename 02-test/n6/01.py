from time import sleep
import requests as rq
from PIL import Image
import io
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait

opts = EdgeOptions()
opts.add_argument(
    'user-agent=Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36'
)
driver = Edge(executable_path='./edgeDriver.exe', options=opts)
wait = WebDriverWait(driver, 10)
driver.get('https://www.olx.com.pe')
print(driver.title)

for i in range(2):
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@data-aut-id="btnLoadMore"]')))
    btn.click()
    wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]')))

driver.execute_script("window.scrollTo({top:0, behavior:'smooth'});")
sleep(5)
driver.execute_script("window.scrollTo({top:20000, behavior:'smooth'});")
sleep(5)

anuncios = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')
i = 1
for anuncio in anuncios:
    try:
        pre = anuncio.find_element_by_xpath(
            './/span[@data-aut-id="itemPrice"]').text
        nom = anuncio.find_element_by_xpath(
            './/span[@data-aut-id="itemTitle"]').text
        print(pre, nom)

        url = anuncio.find_element_by_xpath('.//img').get_attribute('src')
        img_content = rq.get(url).content

        img_file = io.BytesIO(img_content)
        img = Image.open(img_file).convert('RGB')
        path = './01-imgs/'+str(i)+'.jpg'
        with open(path, 'wb') as f:
            img.save(f, 'JPEG', quality=85)
    except:
        print('ERROR')
    i += 1

print(len(anuncios))

# driver.close()
