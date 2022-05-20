import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'
#HOST - Адрес сайта
HOST = 'https://minfin.com.ua/'
#URL - Адрес страницы для парсинга
URL = 'https://minfin.com.ua/cards/'
#HEADERS - константа для того чтобы наш парсинг не посчитали за бота 2 параметра смотрятся в браузере на странице сайта ф12- сеть- обновляем страницу - cards - заголовки там эти параметры
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r 

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='sc-182gfyr-0 jmBHNg')
    cards = []

    for item in items:
        cards.append(
            {
               'title':item.find('a', class_='cpshbz-0 eRamNS').get_text(strip=True),
               'link_product': HOST + item.find('a', class_='cpshbz-0 eRamNS').get('href'),
               'bank_name': item.find('span', class_='be80pr-21 dksWIi').get_text(),
               'card_images': item.find('div', class_='be80pr-9 fJFiLL').find('a').find('img').get('src')
                #be80pr-15 kwXsZB
            }
        )
    return cards
#ф-ия ниже делает тоже самое для всех или многих страниц

def save_doc(items, path):
    #открыть прочесть файл
    with open(path, 'w', newline='',  encoding="utf-8") as file: 
        writer = csv.writer(file, delimiter=';')
        #Задаем в файле 1ую строку (колонки)
        writer.writerow(['Название карты','Ссылка на продукт','Банк','Изображение карты'])
        #Разбирает item
        for item in items:
            writer.writerow([item['title'],item['link_product'],item['bank_name'],item['card_images']])


            

def parsing():
    #PAGENATION = input('Укажите кол-во страниц для парсинга: ')
    #PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = [] 
        print(get_content(html.text)) 
        save_doc(get_content(html.text), CSV)
        #for page in range(1, PAGENATION):
                #print(f'Парсим страницу: {page}')
                #page ниже тянется из строки браузера типо 1 страница 2ая
                #html = get_html(URL, params={'page': page})
                #cards.extend(get_content(html.text))
        #pass
        #print(cards)
    else:
        print('error')
parsing()