import asyncio
from selectolax.parser import HTMLParser
import aiohttp
import json
import pprint
from model import DataSaver


async def fetch(url:str) -> str:
    """
    Asynchronously fetches the content of a given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The content of the URL.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def get_urls():
    data_saver = DataSaver('data.db')
    urls = data_saver.get_urls()
    data_saver.close_connection()
    return urls

async def save_data(data:list):
    data_saver = DataSaver('confirmat.db')
    data_saver.create_table('one',
                            ['id INTEGER PRIMARY KEY',
                             'url TEXT',
                             'name TEXT',
                             'price TEXT',
                             'imgs TEXT',
                             'prop TEXT',
                             'desc TEXT',
                             'docs TEXT'
                             ])
    for item in data:
        data_saver.insert_data('one', item)
    print('Data saved successfully!')
    data_saver.close_connection()

async def main():
    #urls = ['https://www.boyard.biz/catalog/handles/rt115sc_1_224_400.html', 'https://www.boyard.biz/catalog/handles/rz050_04bl.html']
    urls = await get_urls()
    result = []
    counter = 1
    length = len(urls)
    #print(str(urls[0][0]))
    for u in urls:
        print(f'\t\tProcessing {counter}/{length} products', end='\r')
        html = await fetch(u[0])
        parser = HTMLParser(html)
        page = {}
        # Name
        name = parser.css('.bd-card-head__title')[0].text()
        page.update({'name': name})
         # Price
        price = parser.css('li.bd-price__current')[1].text(strip=True)[:-4].replace(' ', '')
        page.update({'price': price})
        # Images
        imgs = []
        for img in parser.css('.bd-card-slider__img'):
            imgs.append(img.attributes['src'])
        page.update({'imgs': ', '.join(imgs)})
        # Properties
        prop = {}
        for li in parser.css('.bd-product-list__item'):
            key = li.css(".bd-product-list__prop")[0].text(strip=True)
            value = li.css(".bd-product-list__value")[0].text(strip=True)
            prop.update({key: value})
        page.update({'prop': json.dumps(prop)})
        # Description
        p = ''
        node = parser.css('.bd-card-tabs__body')[1]
        for cnode in node.iter():
            p += cnode.html
            #desc = parser.css('.bd-card-tabs__body')[1].text(strip=True)
        page.update({'desc': p})
        # Documents
        docs = []
        for doc in parser.css('.bd-download-files__item'):
            docs.append(doc.attributes['href'])
        page.update({'docs': ', '.join(docs)})
        result.append(page)
        #pprint.PrettyPrinter().pprint(page)
        page.update({'url': u})
        page.update({'id': counter})
        counter += 1
    await save_data(result)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())