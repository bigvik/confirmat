from docx import Document
from docx.shared import Pt

from model import DataSaver


def get_data():
    '''
    Return id, url from product_data
    '''
    data_saver = DataSaver('confirmat.db')
    data = data_saver.get_urls_product()
    data_saver.close_connection()
    return data

def main():
    doc = Document()
    doc.add_heading('QR Каталог', 0)
    data = get_data()
    counter = 1
    l = len(data)
    for d in data:
        print(f'Processing {counter}/{l}', end='/r')
        name = d[0].split('/')[-1:][0].replace('*', '_')
        path = 'qr/'+name+'.png'
        doc.add_paragraph(d[1])
        doc.add_picture(path, width=Pt(100))
        counter += 1
    doc.save('QRcatalog.docx')
    print('Done!')


if __name__ == '__main__':
    main()