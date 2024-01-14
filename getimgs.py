from model import DataSaver


def main():
    ds = DataSaver('confirmat.db') 
    links = ds.get_imglinks()
    for link in links:
        pass


if __name__ == '__main__':
    main()