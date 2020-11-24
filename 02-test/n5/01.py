import requests as rq
from lxml import html

# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41
hd = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36',
}
login_form_url = 'https://github.com/login'

session = rq.Session()

login_form_rs = session.get(login_form_url, headers=hd)
parser = html.fromstring(login_form_rs.text)
token_especial = parser.xpath('//input[@name="authenticity_token"]/@value')


login_url = 'https://github.com/session'
login_data = {
    'commit': 'Sign in',
    'login': 'fernando_1999_ticona_@hotmail.com',
    'password': '<PWD>',
    'authenticity_token': token_especial
}

session.post(login_url, headers=hd, data=login_data)

data_url = 'https://github.com/NixRoYal?tab=repositories'
request = session.get(data_url, headers=hd)
parser = html.fromstring(request.text)
repos = parser.xpath('//h3[@class="wb-break-all"]/a/text()')
for repo in repos:
    print(repo)
