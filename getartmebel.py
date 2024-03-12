from selectolax.parser import HTMLParser
from icecream import ic
import asyncio
import aiohttp
from model import DataSaver as ds
import pickle
import os
import json


#ic.disable()

urls: list = [
    'https://artmebel.kz/catalog/781?SHOWALL_1=1', # Ножки
    'https://artmebel.kz/catalog/953?SHOWALL_1=1', # Колеса
    'https://artmebel.kz/catalog/954?SHOWALL_1=1', # Подпятники
    'https://artmebel.kz/catalog/711', # Шпингалеты
    'https://artmebel.kz/catalog/710', # Демпфера, магниты, доводчики
    'https://artmebel.kz/catalog/755?SHOWALL_1=1', # Газлифты
    'https://artmebel.kz/catalog/970?SHOWALL_1=1', # Шурупы
    'https://artmebel.kz/catalog/811?SHOWALL_1=1', # Штанги
    'https://artmebel.kz/catalog/741?SHOWALL_1=1', # Уголки
    'https://artmebel.kz/catalog/747?SHOWALL_1=1' # Полкодержатели
    ]


async def fetch(session, url:str)->str:
    async with session.get(url) as response:
        return await response.text()

async def get_links(session, url:str)->list:
    base: str = 'https://artmebel.kz'
    links: list = []
    parser = HTMLParser(await fetch(session, url))
    for link in parser.css('.product-item-title a'):
        a = link.attributes['href']
        links.append(base+a)
    return links

async def get_data(session, links:list)->list:
    base: str = 'https://artmebel.kz'
    data: list = []
    
    counter = 1
    ln = len(links)
    for link in links:
        dic: dict = {}
        print(f'Processing {counter} from {ln} ...', end='\r')
        parser = HTMLParser(await fetch(session, link))

        # URL
        dic.update({'url': link})

        # Name
        name = parser.css('#pagetitle')[0].text()
        dic.update({'name': name})

        # Catalog
        try:
            catalog = parser.css('.bx-breadcrumb div:nth-last-child(2) span')[0].text()
            dic.update({'catalog': catalog})
        except Exception:
            dic.update({'catalog': ''})

        # Price
        price = parser.css('.product-item-detail-price-current')[0].text()
        dic.update({'price': price.strip()[:-6].replace(u'\xa0', '')})

        # Image
        img = parser.css('.product-item-detail-slider-image img')[0].attributes['src']
        dic.update({'imgs': base+img})

        # Description
        description = ''
        try:
            desc = parser.css('div[data-value="description"]')[0]
            for p in desc.iter():
                description += p.html
        except Exception:
            pass
        dic.update({'description': description})

        # Articul & Manufacturer
        dic.update({'manufacturer': ''})
        dic.update({'articul': ''})

        # Properties
        prop = []
        prop_dic = {}
        c = 0
        try:
            for el in parser.css('.product-item-detail-properties > *'):
                p = el.text(strip=True)
                if c == 0:
                    p = p.capitalize()
                    prop.append(p)
                    c += 1
                else:
                    prop.append(p)
                    c = 0
                    prop_dic.update({prop[0]:prop[1]})

                    # Manufacturer
                    if prop[0] == 'Производитель':
                        dic.update({'manufacturer': prop[1]})

                    # Articul
                    if prop[0] == 'Артикул':
                        dic.update({'articul': prop[1]})
                        
                    prop = []
        except Exception:
            pass
        dic.update({'properties': json.dumps(prop_dic, ensure_ascii=False)})

        dic.update({'docs': ''})
        dic.update({'ours_price': '0'})
        #ic(dic)
        data.append(dic)

        counter += 1
        ic(counter, data)
    return data

async def save_data(data:list):
    data_saver = ds('confirmat.db')
    data_saver.create_table('product_data',
                            ['id INTEGER PRIMARY KEY',
                             'url TEXT',
                             'name TEXT',
                             'articul TEXT',
                             'manufacturer TEXT',
                             'catalog TEXT',
                             'price TEXT',
                             'ours_price TEXT',
                             'imgs TEXT',
                             'properties TEXT',
                             'description TEXT',
                             'docs TEXT'
                             ])
    for item in data:
        try:
            data_saver.insert_data('product_data', item)
        except Exception as e:
            print(e)
            raise
        print('Data saved successfully!')
    
    data_saver.close_connection()

async def main()->None:
    if os.path.isfile('data.pickle'):
        print('Load data from pickle..')
        with open('data.pickle', 'rb') as f:
            data = pickle.load(f)
    else:
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(get_links(session, url)) for url in urls]
            responses = await asyncio.gather(*tasks)

            datatasks = [asyncio.ensure_future(get_data(session, response))for response in responses]
            data = await asyncio.gather(*datatasks)
        with open('data.pickle', 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
    try:
        for d in data:
            await save_data(d)
        os.remove('data.pickle')
    except Exception:
        print('FAIL')

                


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())