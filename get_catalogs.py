import pprint
import asyncio
import aiohttp
from selectolax.parser import HTMLParser as hp



async def fetch(session, url:str)->str:
	async with session.get(url) as response:
            return await response.text()

async def get_data(session, url:str)->list:
	data = []
	html = await fetch(session, url)
	parser = hp(html)
	#data.append(parser.css('.bd-m-catalog__title')[0].text())
	data.append(parser.css('.bd-category-info__text'))
	return data

async def main()->None:
	async with aiohttp.ClientSession() as session:
		catalog_html = await fetch(session, 'https://www.boyard.biz/catalog')
		parser = hp(catalog_html)
		links = [a.attrs['href'] for a in parser.css('.product-card')]
		data_tasks = [asyncio.ensure_future(get_data(session, link))for link in links]
		data = await asyncio.gather(*data_tasks)
		print(data)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())