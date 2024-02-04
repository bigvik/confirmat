from model import DataSaver


def main():
    ds = DataSaver('confirmat.db')
    data = ds.get_all()
    ds.close_connection()
    with open('update.sql', 'w', encoding='utf-8') as f:
        for d in data:
            f.write(f"UPDATE product_data SET prop='{d[7]}', des='{d[8]}' WHERE url='{d[1]}';\n")
    print('Done!')  


if __name__ == "__main__":
    main()