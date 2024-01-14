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
    html = await fetch('https://www.boyard.biz/catalog/handles/rt009cp_1_000_500.html')
    parser = HTMLParser(html)
    imgs = []
    for img in parser.css('.bd-card-slider__img'):
        imgs.append(img.attributes['src'].split('/')[-1:][0])
    print(imgs)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
