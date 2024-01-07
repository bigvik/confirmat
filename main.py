import asyncio
from selectolax.parser import HTMLParser
import aiohttp
import qrcode
# from docx import Document
# from docx.shared import Pt
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

async def parse_properties(link:str) -> dict:
    """
    Parses the properties of a given link and returns a dictionary containing the key-value pairs.

    Parameters:
    link (str): The link to fetch and parse the properties from.

    Returns:
    dict: A dictionary containing the key-value pairs of the parsed properties.
    """
    html = await fetch(link)
    parser = HTMLParser(html)
    prop = {}
    for li in parser.css('.bd-product-list__item'):
        key = li.css(".bd-product-list__prop")[0].text(strip=True)
        value = li.css(".bd-product-list__value")[0].text(strip=True)
        prop.update({key: value})
    return prop

async def parse_one(url:str) -> dict:
    """
    Parses the properties of a given link and returns a dictionary containing the key-value pairs.

    Parameters:
    link (str): The link to fetch and parse the properties from.

    Returns:
    dict: A dictionary containing the key-value pairs of the parsed properties.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            parser = HTMLParser(html)
            page = {}
            # Name
            #name = parser.css('.bd-card-head__title')[0].text()
            page.update({'name': 'name'})
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
            return page

async def make_qr(text: str, name:str) -> None:
    """
    Generate a QR code image from a given text and save it with a specified name.

    Args:
        text (str): The text to be encoded in the QR code.
        name (str): The name of the QR code image file.

    Returns:
        None
    """
    qr = qrcode.make(text)
    name = text.split('/')[-1:][0]
    qr.save('qr/'+name+'.png')

async def save_data(data):
    """
    Saves the given data to the 'data.db' database.

    Args:
        data: A list of dictionaries representing the data to be saved. Each dictionary
            should have the following keys: 'name', 'url', 'prop'.

    Returns:
        None
    """
    data_saver = DataSaver()
    data_saver.create_table('data',
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
        #print(item)
        data_saver.insert_data('data', item)
    print('Data saved successfully!')
    data_saver.close_connection()

async def main():
    """
    parse_catalog -> parse_links -> parse_properties
    """
    catalog = await parse_catalog()
    print(f'{len(catalog)} sections in catalog:')
    #doc = Document()
    #doc.add_heading('QR-коды продуктов Boyard', 0)
    for sections in catalog:
        product_links = await parse_links(sections)
        counter = 1
        length = len(product_links)
        data = []
        for key in product_links:
            #properties = await parse_properties(product_links[key])
            properties = await parse_one(product_links[key])
            properties.update({'id': counter})
            properties.update({'name': key})
            properties.update({'url': product_links[key]})
            print(f'\t\tProcessing {counter}/{length} products', end='\r')
            counter += 1
            #print({'name':key, 'url':product_links[key], 'prop':properties})
            #name = links[k].split('/')[-1:][0][:-5]
            #await make_qr(links[k], name)
            #doc.add_paragraph(k)
            #doc.add_picture('qr/'+name+'.png', width=Pt(100))
            data.append(properties)
        await save_data(data)
        counter = 1
    #doc.save('catalog.docx')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())