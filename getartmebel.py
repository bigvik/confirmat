from bs4 import BeautifulSoup as bs
from selectolax.parser import HTMLParser
from icecream import ic
import requests


urls: list = [
    'https://artmebel.kz/catalog/811?SHOWALL_1=1',
    'https://artmebel.kz/catalog/741?SHOWALL_1=1'
    ]


def fetch(url:str)->str:
    page = requests.get(url)
    return page.text

def get_links(urls:list)->list:
    base: str = 'https://artmebel.kz'
    links: list = []
    for url in urls:
        soup = bs(fetch(url), 'html.parser')
        all_links = soup.findAll('div', class_='product-item-title')
        for link in all_links:
            a = link.find('a').get('href')
            links.append(base+a)
    return links

def get_data(links:list)->list:
    base: str = 'https://artmebel.kz'
    data: list = []
    dic: dict = {}
    counter = 1
    ln = len(links)
    for link in links:
        print(f'Processing {counter} from {ln} ...', end='\r')
        parser = HTMLParser(fetch(link))
        dic.update({'url': link})
        name = parser.css('#pagetitle')[0].text()
        dic.update({'name': name})
        price = parser.css('.product-item-detail-price-current')[0].text()
        dic.update({'price': price.strip()})
        img = parser.css('.product-item-detail-slider-image img')[0].attributes['src']
        dic.update({'img': base+img})
        prop = []
        prop_dic = {}
        c = 0
        for el in parser.css('.product-item-detail-properties > *'):
            p = el.text(strip=True)
            if c == 0:
                p = p.capitalize()
                prop.append(p)
                c += 1
            else:
                prop.append(p)
                c = 0
                ic(prop)
                prop_dic.update({prop[0]:prop[1]})
                prop = []
        dic.update({'prop':prop_dic})
        ic(dic)
        data.append(dic)

        counter += 1
    return data

def main()->None:
    links = get_links(urls)
    data = get_data(links)
    print(data)


if __name__ == '__main__':
    main()