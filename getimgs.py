import requests

from model import DataSaver

def main():
    ds = DataSaver('confirmat.db') 
    links = ds.get_imglinks()
    l = len(links)
    counter = 1
    for link in links:
        print(f'Getting {counter} / {l}', end='\r')
        counter = counter + 1
        for img in link[0].split(','):
            if img.find('slider_small') == -1:
                try:
                    #print(img)
                    i = requests.get(img)
                    name = img.split('/')[-1:][0].replace('*', '_')
                    open('imgs/' + name, 'wb').write(i.content)
                except:
                    print('Error!')
                    continue

def test():
    img = 'https://www.boyard.biz/thumbs/slider_big/nThErcmI3wpDjGNBV9nZLsTvz8WJmLDyh6cbsSnq.jpg'
    r = requests.get(img)
    name = img.split('/')[-1:][0].replace('*', '_')
    open('imgs/' + name, 'wb').write(r.content)



if __name__ == '__main__':
    main()