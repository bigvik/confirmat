import asyncio
from selectolax.parser import HTMLParser
import aiohttp
import qrcode
from docx import Document
from docx.shared import Pt

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        
async def parse_catalog():
    html = await fetch('https://www.boyard.biz/catalog')
    parser = HTMLParser(html)
    links = [a.attrs['href'] for a in parser.css('.product-card')]
    return links

async def parse_links(link):
    html = await fetch(link)
    parser = HTMLParser(html)
    links = {}
    for a in parser.css('.bd-product__link'):
        links.update({a.attributes['title']: a.attributes['href']})
    return links

async def main():
    catalog = await parse_catalog()
    doc = Document()
    doc.add_heading('QR-коды продуктов Boyard', 0)
    for link in catalog:
        links = await parse_links(link)
        for k in links:
            qr = qrcode.make(links[k])
            name = links[k].split('/')[-1:][0]
            qr.save('qr/'+name+'.png')
            doc.add_paragraph(k)
            doc.add_picture('qr/'+name+'.png', width=Pt(100))
            print(name+'.png')
    doc.save('catalog.docx')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())