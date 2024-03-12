import asyncio
from selectolax.parser import HTMLParser
import aiohttp
from model import DataSaver

async def fetch(url:str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        
async def parse_catalog() -> list:
    html = await fetch('https://www.boyard.biz/catalog')
    parser = HTMLParser(html)
    sections = [a.attrs['href'] for a in parser.css('.product-card')]
    return sections

async def parse_links(section:str) -> dict:
    html = await fetch(section)
    parser = HTMLParser(html)
    process_links = [section]
    pages = parser.css('.bd-pagination__container')
    if pages: 
        pages_num = pages[0].css('.bd-pagination__item')[-1:][0].text(strip=True)
        print(f'\tCatalog {section} has {int(pages_num)} pages')
        for i in range(2,int(pages_num)+1):
            process_links.append(section+'?page='+str(i)) 
    else:
        print(f'\tCatalog {section} has 1 page')
    links = await process_parse_links(process_links)
    return links

async def process_parse_links(links:list) -> list:
    product_links = []
    counter = 1
    for link in links:
        print(f'\t\tProcessing {counter}/{len(links)} page:', end='\r')
        counter += 1
        html = await fetch(link)
        parser = HTMLParser(html)
        for a in parser.css('.bd-product__link'):
            product_links.append(a.attributes['href'])
    return product_links

async def save_data(data):
    data_saver = DataSaver('confirmat.db')
    data_saver.create_table('product_links', ['url TEXT UNIQUE'])
    for item in data:
        data_saver.insert_links('product_links', tuple([item]))
    print('Data saved successfully!')
    data_saver.close_connection()

async def main():
    catalog = await parse_catalog()
    print(f'{len(catalog)} sections in catalog:')
    for section in catalog:
        product_links = await parse_links(section)
        await save_data(product_links)



if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())