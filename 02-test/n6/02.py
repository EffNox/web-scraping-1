import requests as rq
from bs4 import BeautifulSoup

url = 'https://file-examples.com/index.php/sample-documents-download/sample-xls-download/'

rs = rq.get(url)
soup = BeautifulSoup(rs.text)
urls = []

descargas = soup.find_all('a', class_='download-button')

for descarga in descargas:
    urls.append(descarga['href'])

i = 1
for url in urls:
    v = rq.get(url, allow_redirects=True)
    file_name = './02-files/excel-file-'+str(i)+'.'+url.split('.')[-1]
    output = open(file_name, 'wb')
    output.write(v.content)
    output.close()
    i += 1
