import pandas as pd
import sqlite3


def main():
    xl = pd.read_excel('fuzzy_boyard.xlsx', names=['sku'])
    xlname = []
    cnx = sqlite3.connect('confirmat.db')
    for el in xl.sku:
        name = pd.read_sql_query(f"SELECT name FROM product_data WHERE name LIKE '%{el}%'", cnx)
        if name.empty: name = ''
        else: name = str(name.name[0])
        print(name)
        xlname.append(name)
    xl['name'] = xlname
    xl.to_excel('fuzzy_boyardresult.xlsx')

if __name__ == '__main__':
    main()