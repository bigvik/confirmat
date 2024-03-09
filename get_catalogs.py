import asyncio
import aiohttp
from selectolax.parser import HTMLParser as hp
from transliterate import slugify
import csv
import pprint



async def fetch(session, url:str)->str:
	async with session.get(url) as response:
            return await response.text()

async def get_data(session, url:str, index)->dict:
	data = {}
	html = await fetch(session, url)
	parser = hp(html)
	data['Category ID'] = index
	data['Active (0/1)'] = 1
	title = parser.css('.bd-m-catalog__title')[0].text()
	data['Name *'] = title
	data['Parent category'] = 'Home'
	data['Root category (0/1)'] = 0
	data['URL rewritten'] = slugify(title)
	try:
		data['Description'] = parser.css('.bd-category-info__text')[0].html
	except: data['Description'] = ''
	data['Meta title'] = ''
	data['Meta keywords'] = ''
	data['Meta description'] = ''
	data['Image URL'] = ''
	return data

async def main()->None:
	async with aiohttp.ClientSession() as session:
		catalog_html = await fetch(session, 'https://www.boyard.biz/catalog')
		parser = hp(catalog_html)
		links = [a.attrs['href'] for a in parser.css('.product-card')]
		data_tasks = [asyncio.ensure_future(get_data(session, link, links.index(link)+3))for link in links]
		data = await asyncio.gather(*data_tasks)
		with open('categories_import.csv', 'w', newline='', encoding='utf-8') as f:
			fieldnames = ['Category ID', 'Active (0/1)','Name *', 'Parent category', 'Root category (0/1)', 'Description', 'Meta title', 'Meta keywords', 'Meta description', 'URL rewritten', 'Image URL']
			writer = csv.DictWriter(f, delimiter=';',fieldnames=fieldnames)
			writer.writeheader()
			for d in data:
				pprint.pprint(d)
				writer.writerow(d)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())