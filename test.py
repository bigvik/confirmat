#from model import DataSaver
import sqlite3

def main():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    query = "SELECT url FROM 'data'"
    cursor.execute(query)
    urls = cursor.fetchall()
    for url in urls:
        print(url[0])

    conn.close()


if __name__ == "__main__":
    main()
