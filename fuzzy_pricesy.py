import pandas as pd
from thefuzz import fuzz
from thefuzz import process
import sqlite3


def main():
    pricelist = pd.read_excel('D:\\Documents\\pricelist_14_03_24.xls', names=['sku','name','wholesale','retail','balance','available'])
    pricelist = pricelist.astype('string')
    pricelist['sku'] = pricelist['sku'].apply(lambda x: str(x).strip())
    pricelist['name'] = pricelist['name'].apply(lambda x: str(x).strip())
    pricelist['name'] = pricelist['name'].apply(lambda x: x.replace(', Шт', ''))
    pricelist['name'] = pricelist['name'].apply(lambda x: x.replace(', лист', ''))
    pricelist['name'] = pricelist['name'].apply(lambda x: x.replace(', компл', ''))

    cnx = sqlite3.connect('confirmat.db')
    data = pd.read_sql_query("SELECT * FROM product_data", cnx)
    data['name'] = data['name'].astype('string')
    data['name'] = data['name'].apply(lambda x: str(x).strip())
    data['articul'] = data['articul'].astype('string')

    boyard = data[data['manufacturer']=='BOYARD']
    boyard.drop(columns=['id', 'url', 'articul', 'catalog', 'price', 'ours_price', 'imgs', 'properties', 'description', 'docs'])

    '''ln = len(pricelist)
    counter = 0
    actual = []
    similarity =[]
    for i in pricelist['name']:
        print(f'Processing {counter}/{ln}', end='\r')
        ratio = process.extract(i, data['name'], limit=2, scorer=fuzz.token_set_ratio)
        actual.append(ratio[0][0])
        similarity.append(ratio[0][1])
        pricelist['FOUND'] = pd.Series(actual)
        pricelist['SIM'] = pd.Series(similarity)

        counter += 1
    pricelist.to_excel('fuzzy_pricezy.xlsx')'''

    ln = len(boyard)
    counter = 0
    actual = []
    similarity = []
    for i in boyard.name:
        print(f'Processing {counter}/{ln}', end='\r')
        ratio = process.extract(i, pricelist['sku'], limit=2, scorer=fuzz.token_set_ratio)
        actual.append(ratio[0][0])
        similarity.append(ratio[0][1])
        boyard['articul'] = pd.Series(actual)
        boyard['SIM'] = pd.Series(similarity)
        counter += 1
    boyard.to_excel('fuzzy_datazy.xlsx')




if __name__ == '__main__':
    main()