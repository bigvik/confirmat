import sqlite3

class DataSaver:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()
    
    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.cursor.execute(query)
    
    def insert_data(self, table_name, data):
        #placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table_name} VALUES (:name, :url, :prop)"
        self.cursor.execute(query, data)
        self.conn.commit()

    def get_urls(self):
        query = "SELECT url FROM 'data'"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    pass