import asyncio
import aiohttp
from selectolax.parser import HTMLParser


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
    #return links

async def main():
    links = []
    async with aiohttp.ClientSession() as session:
        await get_catalog(session, 'https://artmebel.kz/catalog/', links, 1)
        print(f'Links quantity: {len(links)}')
        print(links)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())