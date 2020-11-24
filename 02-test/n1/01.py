import requests as http
from lxml import html

hd = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
}
url = "https://www.wikipedia.org/"

rs = http.get(url, headers=hd)
rs.encoding = 'utf-8'

parsed = html.fromstring(rs.text)
# inglesTxt=parsed.get_element_by_id("js-link-box-en")
idiomas = parsed.xpath("//div[contains(@class,'central-featured-lang')]//strong/text()")
# idiomas = parsed.find_class('central-featured-lang')

for idioma in idiomas:
    print(idioma)
    # print(idioma.text_content())
