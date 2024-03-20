import sqlite3

class DataSaver:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
    
    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.cursor.execute(query)
    
    def insert_data(self, table_name, data):
        #placeholders = ', '.join(['?' for _ in data])
        #print(placeholders)
        query = f"INSERT OR IGNORE INTO {table_name} (url, name, sku, manufacturer, catalog, price, ours_price, imgs, properties, description, docs) VALUES (:url, :name, :sku, :manufacturer, :catalog, :price, :ours_price, :imgs, :properties, :description, :docs)"
        #query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        #print(query)
        self.cursor.execute(query, data)
        self.conn.commit()

    def update_info(self, table_name, url, prop, desc):
        query = f"UPDATE {table_name} SET prop = '{prop}', desc = '{desc}' WHERE url = '{url}'"
        self.cursor.execute(query)
        self.conn.commit()

    def insert_links(self, table_name, data):
        query = f"INSERT OR IGNORE INTO {table_name} VALUES (?)"
        print(data)
        self.cursor.execute(query, data)
        self.conn.commit()

    def get_all(self):
        query = "SELECT * FROM 'product_data'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_urls(self):
        query = "SELECT url FROM 'product_links'"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def url_exist(self, url):
        query = "SELECT name FROM product_data WHERE url == ?"
        self.cursor.execute(query, (url,))
        if self.cursor.fetchone(): return True
        else: return False

    def name(self, url):
        query = "SELECT name FROM product_data WHERE url == ?"
        self.cursor.execute(query, (url,))
        return self.cursor.fetchone()

    def get_urls_product(self):
        query = "SELECT url, name FROM 'product_data'"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_where(self, art):
        query = f"SELECT url, sku FROM 'product_data' WHERE sku LIKE '%{art}%'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_imglinks(self):
        query = "SELECT imgs FROM 'product_data'"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    pass