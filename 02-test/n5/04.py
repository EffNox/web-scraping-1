from time import sleep
import requests as rq
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait

opts = EdgeOptions()
opts.add_argument(
    'user-agent=Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36'
)
driver = Edge(executable_path='./edgeDriver.exe', options=opts)
wait = WebDriverWait(driver, 10)
url_i = 'https://www.google.com/recaptcha/api2/demo'
driver.get(url_i)
print(driver.title)


try:
    captcha_key = driver.find_element_by_id(
        'recaptcha-demo').get_attribute('data-sitekey')
    url = 'https://2captcha.com/in.php?'
    url += 'key=f300d3f245f9820efaced256a2b5c942'
    url += '&method=userrecaptcha'
    url += '&googlekey='+captcha_key
    url += '&pageurl='+url_i
    url += '&json=0'
    print(url)
    rs_requerimiento = rq.get(url)
    captcha_service_key = rs_requerimiento.text
    print(captcha_service_key)
    captcha_service_key = captcha_service_key.split('|')[-1]

    url_rs = "https://2captcha.com/res.php?"
    url_rs += 'key=f300d3f245f9820efaced256a2b5c942'
    url_rs += '&action=get'
    url_rs += '&id='+captcha_service_key
    url_rs += '&json=0'
    print(url_rs)
    sleep(20)
    while True:
        respuesta_solver = rq.get(url_rs)
        respuesta_solver = respuesta_solver.text
        print(respuesta_solver)
        if respuesta_solver == 'CAPTCHA_NOT_READY':
            sleep(5)
        else:
            break

        respuesta_solver = respuesta_solver.split('|')[-1]
        print()
        insertar_solucion = 'document.getElementById("g-recaptcha-response").innerHTML='+respuesta_solver
        print(insertar_solucion)
        driver.execute_script(insertar_solucion)
        submit_button=driver.find_element_by_xpath('//input[@id="recaptcha-demo-submit"]')
        submit_button.click()
except Exception as e:
    print(e)

print('YA DEBO DE ESTAR EN LA PÁGINA PRINCIPAL...')


contenido = driver.find_element_by_class_name('recaptcha-success')

print(contenido.text)
