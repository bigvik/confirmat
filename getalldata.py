import asyncio
from selectolax.parser import HTMLParser
import aiohttp
import json
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

async def parse_catalog() -> list:
    """
    Parses the catalog by fetching the HTML from the specified URL and extracting the links of the product cards.

    Returns:
        list: A list of strings representing the links of the product cards.
    """
    html = await fetch('https://www.boyard.biz/catalog')
    parser = HTMLParser(html)
    links = [a.attrs['href'] for a in parser.css('.product-card')]
    return links

async def parse_links(link:str) -> dict:
    """
    Asynchronously parses the links of a given webpage.

    Args:
        link (str): The URL of the webpage to be parsed.

    Returns:
        dict: A dictionary containing the parsed links.

    """
    html = await fetch(link)
    parser = HTMLParser(html)
    process_links = [link]
    #title = parser.css('bd-m-catalog__title bd-wrap')[0].text(strip=True)
    pages = parser.css('.bd-pagination')
    if pages: 
        pages_num = pages[0].css('.bd-pagination__item')[-1:][0].text(strip=True)
        print(f'\tCatalog {link} has {int(pages_num)} pages')
        for i in range(2,int(pages_num)+1):
            process_links.append(link+'?page='+str(i))
    
    links = await process_parse_links(process_links)
    return links

async def process_parse_links(links:list) -> dict:
    product_links = {}
    counter = 1
    for link in links:
        print(f'\t\tProcessing {counter}/{len(links)} links:', end='\r')
        counter += 1
        html = await fetch(link)
        parser = HTMLParser(html)
        for a in parser.css('.bd-product__link'):
            product_links.update({a.attributes['title']: a.attributes['href']})
    return product_links

async def collect_links():
    catalog = await parse_catalog()
    print(f'{len(catalog)} sections in catalog:')
    for section in catalog:
        product_links = await parse_links(section)


async def get_urls():
    data_saver = DataSaver('confirmat.db')
    urls = data_saver.get_urls()
    data_saver.close_connection()
    return urls

async def save_data(data:list):
    data_saver = DataSaver('confirmat.db')
    data_saver.create_table('product_data',
                            ['id INTEGER PRIMARY KEY',
                             'url TEXT',
                             'name TEXT',
                             'art TEXT',
                             'price TEXT',
                             'ours_price TEXT',
                             'imgs TEXT',
                             'prop TEXT',
                             'desc TEXT',
                             'docs TEXT'
                             ])
    for item in data:
        data_saver.insert_data('product_data', item)
    #print('Data saved successfully!')
    data_saver.close_connection()

async def main():
    #urls = ['https://www.boyard.biz/catalog/handles/rt009cp_1_000_500.html', 'https://www.boyard.biz/catalog/handles/rz050_04w.html']
    urls = await get_urls()
    result = []
    counter = 1
    length = len(urls)
    for u in urls:
        try:
            print(f'\t\tProcessing {counter}/{length} url: {u[0]}', end='\r')
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
            page.update({'prop': json.dumps(prop, ensure_ascii=False)})
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
            
            page.update({'url': u[0]})
            page.update({'id': counter})

            page.update({'art': ''})
            page.update({'ours_price': '0'})

            result.append(page)
            counter += 1
        except:
            print(f'Error!: {counter}/ {u[0]}')
            continue
    await save_data(result)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())