import pandas as pd
import requests as rq

hd = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36',
    'referer': 'https://www.udemy.com/courses/search/?src=ukw&q=web+scraping',
}

cursos_totales = []

for n in range(1, 2):
    url = 'https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=web%20scraping&skip_price=true&p=' + \
        str(n)
    rs = rq.get(url, headers=hd)
    dt = rs.json()
    courses = dt['courses']
    for curso in courses:
        cursos_totales.append({
            'title': curso['title'],
            'num_reviews': curso['num_reviews'],
            'rating': curso['rating'],
        })


data_frame = pd.DataFrame(cursos_totales)
print(data_frame)
data_frame.to_csv('cursos_udemy.csv')
