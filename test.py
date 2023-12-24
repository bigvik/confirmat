import aiohttp
import asyncio
from selectolax.parser import HTMLParser

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(response.status)
            return await response.text()

def parse_html(html):
    print(len(html))
    soup = HTMLParser(html)
    product_items = soup.css(".bd-product-list__item")
    print(product_items)

    data_dict = {}

    for item in product_items:
        keyclass = item.css(".bd-product-list__prop")
        valueclass = item.css(".bd-product-list__value")
        key = keyclass[0].text(strip=True)
        value = valueclass[0].text(strip=True)
        data_dict[key] = value

    return data_dict

async def main():
    url = "https://www.boyard.biz/catalog/handles/rz050_04bl.html"
    html = await fetch_data(url)
    data_dict = parse_html(html)
    print(data_dict)

async def ifpages():
    urls = ["https://www.boyard.biz/catalog/handles/", "https://www.boyard.biz/catalog/locks"]
    for url in urls:
        html = await fetch_data(url)
        soup = HTMLParser(html)
        pages = soup.css(".bd-pagination")
        if pages:
            print(f'{url} has pages')
        else:
            print(f'{url} has NO pages')

if __name__ == "__main__":
    asyncio.run(ifpages())
