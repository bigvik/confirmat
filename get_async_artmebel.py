from bs4 import BeautifulSoup as bs
from selectolax.parser import HTMLParser
from icecream import ic
import asyncio
import aiohttp
import csv


#ic.disable()

urls: list = [
    'https://artmebel.kz/catalog/811?SHOWALL_1=1',
    'https://artmebel.kz/catalog/741?SHOWALL_1=1'#,
    #'https://artmebel.kz/catalog/954?SHOWALL_1=1'
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
    
    counter = 1
    ln = len(links)
    for link in links:
        dic: dict = {}
        print(f'Processing {counter} from {ln} ...', end='\r')
        parser = HTMLParser(await fetch(session, link))
        #dic.update({'url': link})
        name = parser.css('#pagetitle')[0].text()
        dic.update({'Name *': name})
        try:
            catalog = parser.css('.bx-breadcrumb div:nth-last-child(2) span')[0].text()
            dic.update({'Categories (x,y,z...)': catalog})
        except:
            dic.update({'Categories (x,y,z...)': ''})
        price = parser.css('.product-item-detail-price-current')[0].text()
        dic.update({'Price tax excluded': price.strip()[:-6].replace(' ', '')})
        img = parser.css('.product-item-detail-slider-image img')[0].attributes['src']
        dic.update({'Image URLs (x,y,z...)': base+img})
        desc = parser.css('div[data-value="description"]')[0]
        description = ''
        for p in desc.iter():
            description += p.html
        dic.update({'Description': description})
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
                if prop[0] == 'Производитель':
                    dic.update({'Manufacturer': prop[1]})
                prop = []
        #dic.update({'prop':prop_dic})
        ic(dic)
        data.append(dic)

        counter += 1
        ic(counter, data)
    return data

async def main()->None:
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(get_links(session, url)) for url in urls]
        responses = await asyncio.gather(*tasks)
        ic(responses)
        datatasks = [asyncio.ensure_future(get_data(session, response))for response in responses]
        data = await asyncio.gather(*datatasks)
        #ic(data)
        with open('products_import.csv', 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Product ID', 'Active (0/1)', 'Name *', 'Categories (x,y,z...)', 'Price tax excluded', 'Tax rules ID', 'Wholesale price', 'On sale (0/1)', 'Discount amount', 'Discount percent', 'Discount from (yyyy-mm-dd)', 'Discount to (yyyy-mm-dd)', 'Reference #', 'Supplier reference #', 'Supplier', 'Manufacturer', 'EAN13', 'UPC', 'Ecotax', 'Width', 'Height', 'Depth', 'Weight', 'Delivery time of in-stock products', 'Delivery time of out-of-stock products with allowed orders', 'Quantity', 'Minimal quantity', 'Low stock level', 'Receive a low stock alert by email', 'Visibility', 'Additional shipping cost', 'Unity', 'Unit price', 'Summary', 'Description', 'Tags (x,y,z...)', 'Meta title', 'Meta keywords', 'Meta description', 'URL rewritten', 'Text when in stock', 'Text when backorder allowed', 'Available for order (0 = No, 1 = Yes)', 'Product available date', 'Product creation date', 'Show price (0 = No, 1 = Yes)', 'Image URLs (x,y,z...)', 'Image alt texts (x,y,z...)', 'Delete existing images (0 = No, 1 = Yes)', 'Feature(Name:Value:Position)', 'Available online only (0 = No, 1 = Yes)', 'Condition', 'Customizable (0 = No, 1 = Yes)', 'Uploadable files (0 = No, 1 = Yes)', 'Text fields (0 = No, 1 = Yes)', 'Out of stock action', 'Virtual product', 'File URL', 'Number of allowed downloads', 'Expiration date', 'Number of days', 'ID / Name of shop', 'Advanced stock management', 'Depends On Stock', 'Warehouse', 'Acessories  (x,y,z...)']
            writer = csv.DictWriter(f, delimiter=';',fieldnames=fieldnames)
            writer.writeheader()
            #print(data)
            #writer.writerows(data[0])
            for d in data:
                #print(d[])
                writer.writerows(d)
                


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())