from model import DataSaver
import asyncio
from selectolax.parser import HTMLParser
import aiohttp

async def fetch(url:str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

def save_data(data):
    data_saver = DataSaver('test.db')
    data_saver.create_table('product_links', ['url TEXT'])
    for item in data:
        print(item)
        data_saver.insert_links('product_links', tuple([item]))
    print('Data saved successfully!')
    data_saver.close_connection()

async def main():
    section = 'https://www.boyard.biz/catalog/kitchen'
    html = await fetch(section)
    parser = HTMLParser(html)
    #imgs = []
    #for img in parser.css('.bd-card-slider__img'):
    #    imgs.append(img.attributes['src'].split('/')[-1:][0])

    # p = ''
    # imgs = parser.css('a.bd-s-bread__a')[-1].text()

    # process_links = [section]
    # pages = parser.css('.bd-pagination__container')
    # if pages: 
    #     pages_num = pages[0].css('.bd-pagination__item')[-1:][0].text(strip=True)
    #     print(f'\tCatalog {section} has {int(pages_num)} pages')
    #     for i in range(2,int(pages_num)+1):
    #         process_links.append(section+'?page='+str(i))

    print(parser)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
