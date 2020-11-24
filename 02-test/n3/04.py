import random as rnd
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
opts = EdgeOptions()
opts.add_argument(
    'user-agent=Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36'
)
driver = Edge(executable_path='./edge1.exe', options=opts)
driver.get('https://www.google.com.pe/maps/place/Real+Plaza+Centro+C%C3%ADvico/@-12.0567891,-77.039606,17z/data=!4m7!3m6!1s0x9105c8c6c76e03e5:0x3e12ff686b901453!8m2!3d-12.0567891!4d-77.0374173!9m1!1b1?hl=es-419')


wait = WebDriverWait(driver, 10)
scrollingScript = """ 
    document.getElementsByClassName('section-layout section-scrollbox scrollable-y scrollable-show')[0].scroll(0, 10000)
"""
sleep(rnd.randint(4, 5))
SCROLLS = 0
while SCROLLS != 3:
    driver.execute_script(scrollingScript)
    sleep(rnd.randint(5, 6))
    SCROLLS += 1

reviws_real_plaza = driver.find_elements_by_xpath(
    '//div[@class="section-review-content"]')

for review in reviws_real_plaza:
    user_link = review.find_element_by_xpath(
        './/div[@class="section-review-title"]')
    try:
        user_link.click()
        driver.switch_to_window(driver.window_handles[1])
        btn_Opiniones = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@class="section-tab-bar-tab ripple-container section-tab-bar-tab-selected"]'))
        )
        btn_Opiniones.click()
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="section-layout section-scrollbox scrollable-y scrollable-show"]'))
        )
        USER_SCROLLS = 0
        while USER_SCROLLS != 3:
            driver.execute_script(scrollingScript)
            USER_SCROLLS += 1
        
        userReviews = driver.find_elements_by_xpath('//div[@class="section-review-content"]')
        for userReview in userReviews:
            comentario=userReview.find_element_by_xpath('.//span[@class="section-review-text"]').text
            rating=userReview.find_element_by_xpath('.//span[@class="section-review-stars"]').get_attribute('aria-label')
            print(comentario,rating)
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
    except Exception as e:
        print(e)
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
