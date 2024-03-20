import asyncio
from selectolax.parser import HTMLParser
import aiohttp
from model import DataSaver
import pandas as pd


async def fetch(session, url:str) -> str:
    async with session.get(url) as response:
        return await response.text()

async def main():
    db = DataSaver('confirmat.db')
    urls = db.get_urls()
    result = []
    counter = 1
    length = len(urls)
    async with aiohttp.ClientSession() as session:
        for url in urls:
            print(f'\t\tProcessing {counter}/{length}', end='\r')
            try:
                html = await fetch(session, url[0])

                parser = HTMLParser(html)
                #'.bd-product-label--action'
                if parser.css('.bd-product-label--liquidation'):
                    name = parser.css('.bd-card-head__title')[0].text()
                    label = 'liquidation'
                    result.append({'name':name, 'label':label, 'url':url[0]})
                if parser.css('.bd-product-label--action'):
                    name = parser.css('.bd-card-head__title')[0].text()
                    label = 'action'
                    result.append({'name':name, 'label':label, 'url':url[0]})
                counter += 1
            except Exception:
                continue
    print(f'{counter} from {length} is OK')
    df = pd.DataFrame(result)
    df.to_excel('booyard_labels.xlsx')



if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())