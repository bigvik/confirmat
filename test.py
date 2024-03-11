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
    html = await fetch('https://artmebel.kz/catalog/724/82984/')
    parser = HTMLParser(html)
    #imgs = []
    #for img in parser.css('.bd-card-slider__img'):
    #    imgs.append(img.attributes['src'].split('/')[-1:][0])
    p = ''
    imgs = parser.css('div[data-value="description"]')[0]
    for i in imgs.iter():
        p += i.html
    print(p)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
