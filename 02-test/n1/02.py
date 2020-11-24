import requests as http
from bs4 import BeautifulSoup

hd = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
}
url = "https://www.wikipedia.org/"

rs = http.get(url, headers=hd)
# rs.encoding = 'utf-8'
soup = BeautifulSoup(rs.text)

contenedor_de_preguntas = soup.find(id="questions")
lista_de_preguntas = contenedor_de_preguntas.find_all("div", class_="question-summary")

for pregunta in lista_de_preguntas:
    txt = pregunta.find('h3').text
    print(txt)
