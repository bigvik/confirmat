import sqlite3


def main():
    db = sqlite3.connect('confirmat.db')
    cur = db.cursor()
    curva = db.cursor()
    cur.execute('SELECT art, price FROM pricelist')
    counter = 1
    for row in cur.fetchall():
        #curva.execute(f"SELECT name FROM product_data WHERE name LIKE '%{row[0]}%'")
        
        curva.execute(f"SELECT id, name FROM product_data WHERE name LIKE '%{row[0]}%'")
        result = curva.fetchall()
        if result:
            print(row[0])
            print(result, end='   ')
            print(row[1])
        #db.commit()
        # print(f'Updated {counter} rows in table', end='\r')
        # counter += 1
        #for r in curva:
            #cur.execute(f"UPDATE product_data SET cprice = '{row[3]}' WHERE name = '{r[2]}'")
            #print(r)
    curva.close()
    cur.close()
    db.close()
    print(f'Done! Updated {counter} rows in table')


if __name__ == '__main__':
    main()