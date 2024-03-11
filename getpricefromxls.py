import pandas as pd
import sqlite3


def addprice_to_product():
    db = sqlite3.connect('confirmat.db')
    cur = db.cursor()
    curva = db.cursor()
    cur.execute('SELECT art, name, opt, price FROM pricelist')
    counter = 1
    for row in cur:
        #curva.execute(f"SELECT name FROM product_data WHERE name LIKE '%{row[0]}%'")
        curva.execute(f"UPDATE product_data SET ours_price = '{row[3]}', art = '{row[0]}' WHERE name LIKE '%{row[0]}%'")
        db.commit()
        print(f'Updated {counter} rows in table', end='\r')
        counter += 1
        #for r in curva:
            #cur.execute(f"UPDATE product_data SET cprice = '{row[3]}' WHERE name = '{r[2]}'")
            #print(r)
    curva.close()
    cur.close()
    db.close()
    print(f'Done! Updated {counter} rows in table')

def main():
    data = pd.read_excel('pricelist.xls', usecols=[0, 5, 13, 14], names=['art', 'name', 'opt','price'], skiprows=6)
    f = ['В', 'Арт', 'АРТ', 'Метиз Астана', 'МетизАстана', 'КонфАлм', 'Дима', 'МФ', 'NaN', 'B', 'АлК',
         'Арт 1', 'Арт 2', 'Арт 3', 'Арт 1, 3', 'ФМС', 'Ал Конф', 'Б', 'Шоса', 'MS', 'Арт (брючница)',
         'Арт (обувница)', 'Арт (для белья)', 'Арт (для брюк)', 'АМБ', 'Кур-Астана', 'А-MAРКА', 'МФ']
    data = data[~data['art'].isin(f)]
    data = data.astype("string")
    data['art'] = data['art'].apply(lambda x: str(x).strip())

    db = sqlite3.connect('confirmat.db')
    data.to_sql('pricelist', db, if_exists='replace', index=False)
    db.close()

    print('Done! Pricelist added to database')
    #addprice_to_product()


if __name__ == "__main__":
    #addprice_to_product()
    main()