from selectolax.parser import HTMLParser
from icecream import ic
import asyncio
import aiohttp
from model import DataSaver as ds
import pickle
import os
import json


#ic.disable()

urls: list = []

async def fetch(session, url:str)->str:
    async with session.get(url) as response:
        return await response.text()
    
async def get_catalog(session, url:str, links, counter)->list:
    base: str = 'https://artmebel.kz'
    parser = HTMLParser(await fetch(session, url))
    for link in parser.css('.bx_catalog_tile_img'):
        a = link.attributes['href']
        href = base+a
        if href not in links:
            links.append(href+'?SHOWALL_1=1')
            await get_catalog(session, href, links, counter+1)

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
        dic.update({'sku': ''})

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
                        dic.update({'sku': prop[1]})
                        
                    prop = []
        except Exception:
            pass
        dic.update({'properties': json.dumps(prop_dic, ensure_ascii=False)})

        # Components
        try:
            for a in parser.css('.samecomp a'):
                links.append(base+a.attributes['href'])
        except Exception:
            pass

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
                             'url TEXT UNIQUE',
                             'name TEXT',
                             'sku TEXT',
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
            await get_catalog(session, 'https://artmebel.kz/catalog/', urls, 1)
            print(f'Links quantity: {len(urls)}')

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
        os.remove('data.pickle')

                


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())