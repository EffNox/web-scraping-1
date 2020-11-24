import requests as rq

hd = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36',
    # 'authorization': 'Bearer qOpbYoGEx5KwGiWIMDWrYadgSe5B43ydVh5mK7yH',
    # 'x-udemy-authorization': 'Bearer qOpbYoGEx5KwGiWIMDWrYadgSe5B43ydVh5mK7yH',
    'referer': 'https://www.udemy.com/courses/search/?src=ukw&q=web+scraping',
    # 'referer': 'https://www.udemy.com/courses/search/',
}

for n in range(1, 4):
    api = 'https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=web%20scraping&skip_price=true&p=' +  str(n)
    print('PAGINA '+str(n))
    print('---------------------------------------------------------------------')
    rs = rq.get(api, headers=hd)
    dt = rs.json()
    courses = dt['courses']
    for curso in courses:
        print(curso['title'], curso['num_reviews'], curso['rating'])
    print('---------------------------------------------------------------------')
