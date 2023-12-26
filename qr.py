import time
import qrcode


def timer(function):
    '''
    Функция декоратор для измерения времени выполнения функции
    '''
    def wrapped(*args):
        start_time = time.perf_counter()
        res = function(*args)
        print(time.perf_counter() - start_time)
        return res
    return wrapped

def get_urls():
    from model import DataSaver
    data_saver = DataSaver()
    urls = data_saver.get_urls()
    data_saver.close_connection()
    return urls


def make_qr(url: str) -> None:
    """
    Generate a QR code image from a given text and save it with a specified name.

    Args:
        url (str): The url to be encoded in the QR code.

    Returns:
        None
    """
    qr = qrcode.make(url)
    name = url.split('/')[-1:][0].replace('*', '_')
    qr.save('qr/'+name+'.png')

@timer
def main():
    counter = 1
    urls = get_urls()
    for url in urls:
        print(f'\t\tProcessing {counter}/{len(urls)} QR:{url[0]}', end='\r')
        make_qr(url[0])
        counter += 1
    print('Done!')


if __name__ == "__main__":
    main()