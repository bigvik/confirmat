import qrcode
from model import DataSaver


def get_urls():
    data_saver = DataSaver('confirmat.db')
    urls = data_saver.get_urls_product()
    data_saver.close_connection()
    return urls

def make_qr(id, url: str) -> None:
    qr = qrcode.make('http://bigvik.alwaysdata.net/?id='+str(id))
    name = url.split('/')[-1:][0].replace('*', '_')
    qr.save('qr/'+name+'.png')

def main():
    urls = get_urls()
    for url in urls:
        make_qr(url[0], url[1])



if __name__ == '__main__':
    main()