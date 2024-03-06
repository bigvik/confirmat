from bs4 import BeautifulSoup as bs
from selectolax.parser import HTMLParser
from icecream import ic
import asyncio
import aiohttp


urls: list = [
    'https://artmebel.kz/catalog/811?SHOWALL_1=1',
    'https://artmebel.kz/catalog/741?SHOWALL_1=1'
    ]


async def fetch(session, url:str)->str:
    async with session.get(url) as response:
        return await response.text()

async def get_links(session, url:str)->list:
    base: str = 'https://artmebel.kz'
    links: list = []
    soup = bs(await fetch(session, url), 'html.parser')
    all_links = soup.findAll('div', class_='product-item-title')
    for link in all_links:
        a = link.find('a').get('href')
        links.append(base+a)
    return links

async def get_data(session, links:list)->list:
    base: str = 'https://artmebel.kz'
    data: list = []
    dic: dict = {}
    counter = 1
    ln = len(links)
    for link in links:
        print(f'Processing {counter} from {ln} ...', end='\r')
        parser = HTMLParser(await fetch(session, link))
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

async def main()->None:
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(get_links(session, url)) for url in urls]
        responses = await asyncio.gather(*tasks)
        datatasks = [asyncio.ensure_future(get_data(session, response))for response in responses]
        data = await asyncio.gather(*datatasks)
        for d in data:
            print(d)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())