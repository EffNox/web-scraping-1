import random as rnd
from time import sleep
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
opts = EdgeOptions()
opts.add_argument(
    'user-agent=Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36'
)
driver = Edge(executable_path='./edge1.exe', options=opts)
wait = WebDriverWait(driver, 10)
driver.get('https://twitter.com')
# driver.maximize_window()
print(driver.title)

user = 'fernandoft1999@gmail.com'
pwd = open('05-pwd.txt').readline().strip()

input_user = driver.find_element_by_xpath(
    '//input[@name="session[username_or_email]"]')
input_pwd = driver.find_element_by_xpath('//input[@name="session[password]"]')

input_user.send_keys(user)
input_pwd.send_keys(pwd)

btnLogin = wait.until(
    EC.presence_of_element_located((By.XPATH, '//*[@data-testid="LoginForm_Login_Button"]'))
)
btnLogin.click()

tweets = wait.until(
    EC.presence_of_all_elements_located((By.XPATH,'//section//article//div[@dir="auto"]/span'))
)

tweets_text=[]

for tweet in tweets:
    tweets_text.append(tweet.text)
    print(tweet.text)

with open('05-data.json', "w", encoding='utf-8') as f:
    json.dump(tweets_text, f,ensure_ascii=False)
