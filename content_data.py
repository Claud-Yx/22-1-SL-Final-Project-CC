import datetime

from bs4 import BeautifulSoup
import re
import requests

PERIOD = {'year': 0, 'month': 0, 'date': 0}

CONTENT_KEY = {
    "title": "", "location": "", "begin_day": None, "end_day": None,
    "link": "", "map": "", "poster": "", "reservation": None
}

SEARCH_URL = "https://search.naver.com/search.naver"

PERIOD_RE = re.compile(r"(\d{4})\S(\d{2})\S(\d{2})\S{2}(\d{4})\S(\d{2})\S(\d{2})")

content_list = []


def request_content_data():
    global content_list

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
    }
    keyword = '전시회'
    url = f"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bjBC&qvt=0&query={keyword}"

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    items = soup.find_all(class_='card_item')

    for item in items:
        new_content = CONTENT_KEY.copy()

        # title
        new_content['title'] = item.select_one('div [class="data_area"] div [class="title"]').find('a').string

        # begin_day ~ end_day
        dd = item.select('div [class="info"] dd')
        periods = PERIOD_RE.search(dd[0].string).groups()
        new_content['begin_day'] = datetime.date(
            int(periods[0]),
            int(periods[1]),
            int(periods[2]))
        new_content['end_day'] = datetime.date(
            int(periods[3]),
            int(periods[4]),
            int(periods[5]))

        # location
        new_content['location'] = dd[1].string

        # map
        new_content['map'] = dd[1].find('a').get('href')

        # poster
        new_content['poster'] = item.find('img').get('src')

        # link
        naver_href = item.select_one('div [class="title"] a').get('href')
        naver_link = SEARCH_URL + naver_href
        real_page_soup = BeautifulSoup(requests.get(naver_link, headers=headers).text, 'lxml')
        new_content['link'] = real_page_soup.select_one('div [class="main_pack"] h2 a').get('href')

        # reservation

        content_list.append(new_content)


if __name__ == '__main__':
    request_content_data()

    for c in content_list:
        print("<=================================>")
        for k, v in c.items():
            print(f"{k}: {v}")
