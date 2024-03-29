import pandas as pd
import sqlite3


def main():
    price_in = pd.read_excel('pricetest.xls', names=['sku','name','wholesale','retail'])
    price_in['sku'] = price_in['sku'].apply(lambda x: str(x).strip())
    price_in['name'] = price_in['name'].apply(lambda x: str(x).strip())
    price_in['name'] = price_in['name'].apply(lambda x: x.replace(', Шт', ''))
    price_in['name'] = price_in['name'].apply(lambda x: x.replace(', лист', ''))
    price_in['name'] = price_in['name'].apply(lambda x: x.replace(', компл', ''))
    cnx = sqlite3.connect('confirmat.db')
    #data = pd.read_sql_query("SELECT * FROM pricelist", cnx)
    names = []
    for x in price_in.sku:
        name = pd.read_sql_query(f"SELECT name FROM pricelist WHERE sku == '{x}'", cnx)
        if not name['name'].empty:
            n = name['name'].iloc[0]
            print(n)
        else:
            n = x
        names.append(n)
    price_in.name = names
    #df = pd.DataFrame(result)
    price_in.to_excel('pricelist_in.xlsx')


if __name__ == '__main__':
    main()