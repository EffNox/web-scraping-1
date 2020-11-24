from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
opts = EdgeOptions()
opts.add_argument(
    'user-agent=Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36'
)
driver = Edge(executable_path='./edgeDriver.exe', options=opts)
wait = WebDriverWait(driver, 10)
driver.get('https://www.google.com/recaptcha/api2/demo')
print(driver.title)

try:
    driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))

    captcha=driver.find_element_by_xpath('//div[@class="recaptcha-checkbox-border"]')
    captcha.click()
    input('====>PRESIONE ENTER DESPUES DE VERIFIQUE CAPTCHA\n')

    driver.switch_to.default_content()
    
    submit=driver.find_element_by_xpath('//input[@id="recaptcha-demo-submit"]')
    submit.click()
except Exception as e:
    print(e)

# Siguiente Página
contenido=driver.find_element_by_class_name('recaptcha-success')
print(contenido.text)
