import sqlite3

class DataSaver:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.cursor.execute(query)
    
    def insert_data(self, table_name, data):
        #placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table_name} VALUES (:name, :url, :prop)"
        self.cursor.execute(query, data)
        self.conn.commit()
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    pass