import requests
import json
import time
from bs4 import BeautifulSoup

#Адреса страниц исходя из сделанной структуры(жилые)
ADVERTS_TYPE_0 = {
    'Продажа квартиры': 'kupit-kvartiru/?page=\t',
    'Аренда квартиры': 'sniat-kvartiru/?page=\t',
    'Посуточная аренда квартиры': 'kvartiri-posutochno/?page=\t',
    'Продажа комнаты': 'kupit-komnatu/?page=\t',
    'Аренда комнаты': 'sniat-komnatu/?page=\t',
    'Продажа таунхауса': 'kupit-taunhaus/?page=\t',
    'Аренда таунхауса': 'sniat-taunhaus/?page=\t',
    'Продажа дома': 'kupit-dom/?page=\t',
    'Аренда дома': 'sniat-dom/?page=\t',
    'Посуточная аренда дома': 'sniat-kottedji-posutochno/?page=\t',
    'Продажа участка': 'zemelnie-uchastki/?page=\t'
}
#Адреса страниц исходя из сделанной структуры(нежилые)
ADVERTS_TYPE_1 = {
    'Продажа гаража': 'prodaja-garajey-i-mashinomest/?page=\t',
    'Аренда гаража': 'garaji-i-mashinomesta-v-arendu/?page=\t',
    'Продажа офисов': 'prodaja-ofisov/?page=\t',
    'Аренда офисов': 'arenda-ofisov/?page=\t',
    'Продажа торговой площади': 'prodaja-torgovih-ploshadey/?page=\t',
    'Аренда торговой площади': 'arenda-torgovih-ploshadey/?page=\t',
    'Продажа складов': 'prodaja-slkadov/?page=\t',
    'Аренда складов': 'arenda-skladov/?page=\t',
    'Продажа помещения общественного питания': 'prodaja-pomesheniy-obshestvennogo-pitaniya/?page=\t',
    'Аренда помещения общественного питания': 'arenda-pomesheniy-obshestvennogo-pitaniya/?page=\t',
    'Продажа готового бизнеса': 'prodaja-gotovogo-biznesa/?page=\t',
    'Аренда готового бизнеса': 'gotoviy-biznes-v-arendu/?page=\t',
    'Продажа ПСН': 'prodaja-psn/?page=\t',
    'Аренда ПСН': 'arenda-psn/?page=\t',

}


#Основная(верхняя) информация с объявлений(жилые)
def get_residential(url, type):
    advert = {}
    advert['Тип объявления'] = type    # Тип задается при вызове исходя из заданного раздела

    html = requests.get(url)
    soup = BeautifulSoup(html.text,'html.parser')

    # Дата подачи объявления
    date = soup.find_all('span', 'ob2_obj_inf__left')
    if(len(date)>1):
        advert['Дата подачи'] = date[1].text.strip()

    # Кол-во комнат в квартире(при учете выбора квартиры)
    if(type.split().count('квартиры') == 1):
        rooms = soup.find_all('ul', 'u_ob2_dot_list').find('li').text.strip()
        if(len(rooms)>0):
            rooms = rooms[0].text.split('-')
            advert['Количество комнат'] = rooms[0].strip()

    # Адрес
    address = soup.find_all('ul', 'ob2_obj_adress').find_all('li').text.strip()
    if(len(address) > 0):
        address = address[0].find_all('a')
        advert['Адрес'] = ', '.join([address[elem].text for elem in range(len(address))])

    # Указание на метро или название жилого комплекса( последнее знач. перед переходом на карту)
    metro = soup.find_all('ul', 'ob2_obj_adress').find_all('li', 'no_dot').text.strip()
    if(len(metro) > 0):
        metro = metro[0].find_all('a')
        advert['Метро'] = ', '.join([metro[elem].text for elem in range(len(metro))])

    # Цена
    price = soup.find('div', 'ob2_obj_price__number')
    advert['Цена'] = ' '.join(price.text.split())

    # Парсинг основных свойств объекта
    properties = soup.find_all('ul', 'u_ob2_dot_list')
    if(len(properties) > 0):
        properties = properties[0].find_all('li')
        advert[properties] = ' '.join(properties.find('td').text.split())

    # Текстовое описание квартиры
    text = str(soup.find_all('div', '!js_slice_text')[0])
    text = text.split('<div class="!js_slice_text" itemprop="description">')[1]
    advert['Описание квартиры'] = (' '.join(text.split('<br/>'))).strip()

    # Контакты(имя)
    realtor = soup.find('div', 'ob2_cts__person__info')
    if(len(realtor.find_all('a')) == 0):
        advert['Продавец'] = realtor.contents[0].strip()
    else:
        advert['Продавец'] = realtor.find('a').text.strip()

    # Контакты(номер телефона)
    phone = phone.split('<span class="u_btn js_show_all_phone" data-link-tel=" ">')[1]
    if(len(phone) > 0):
        advert['Телефон продавца'] = (' '.join(phone.split(' '))).strip()

#Основная(верхняя) информация с объявлений(нежилые)
def get_commercial(url, type):
    advert = {}
    advert['Тип объявления'] = type  # Тип задается при вызове исходя из заданного раздела

    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    # Дата подачи объявления
    date = soup.find_all('span', 'ob2_obj_inf__left')
    if (len(date) > 1):
        advert['Дата подачи'] = date[1].text.strip()

    # Адрес
    address = soup.find_all('ul', 'ob2_obj_adress').find_all('li').text.strip()
    if (len(address) > 0):
        address = address[0].find_all('a')
        advert['Адрес'] = ', '.join([address[elem].text for elem in range(len(address))])

    # Указание на метро или название жилого комплекса( последнее знач. перед переходом на карту)
    metro = soup.find_all('ul', 'ob2_obj_adress').find_all('li', 'no_dot').text.strip()
    if (len(metro) > 0):
        metro = metro[0].find_all('a')
        advert['Метро'] = ', '.join([metro[elem].text for elem in range(len(metro))])

    # Цена
    price = soup.find('div', 'ob2_obj_price__number')
    advert['Цена'] = ' '.join(price.text.split())

    # Парсинг основных свойств объекта
    properties = soup.find_all('ul', 'u_ob2_dot_list')
    if (len(properties) > 0):
        properties = properties[0].find_all('li')
        advert[properties] = ' '.join(properties.find('td').text.split())

    # Текстовое описание квартиры
    text = str(soup.find_all('div', '!js_slice_text')[0])
    text = text.split('<div class="!js_slice_text" itemprop="description">')[1]
    advert['Описание'] = (' '.join(text.split('<br/>'))).strip()

    # Контакты(имя)
    realtor = soup.find('div', 'ob2_cts__person__info')
    if (len(realtor.find_all('a')) == 0):
        advert['Продавец'] = realtor.contents[0].strip()
    else:
        advert['Продавец'] = realtor.find('a').text.strip()

    # Контакты(номер телефона)
    phone = phone.split('<span class="u_btn js_show_all_phone" data-link-tel=" ">')[1]
    if (len(phone) > 0):
        advert['Телефон продавца'] = (' '.join(phone.split(' '))).strip()

    return advert

def parse_one_page(page_url, prop_type, ad_type):
    # print('Начал парсить страницу')
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text,'html.parser')
    ad_list = soup.find_all('div', 'serp-item')
    for ad in ad_list:
        if(prop_type == 0): # жилая недвижимость
            adverts_mas.append(get_residential(ad['href'], ad_type))
            # print('Я добавил жилое объявление')
        else: # не жилая недвижимость
            adverts_mas.append(get_commercial(ad['href'], ad_type))
            # print('Я добавил не жилое объявление')

    # возвращаем номер последней доступной отсюда страницы или -1, если страниц еще очень много
    pages = soup.find_all('div', 'pagination_block')
    if(len(pages) > 0):
        pages = pages[0].contents
        last_page_number = pages[len(pages)-2].text
        try:
            last_page_number = int(last_page_number)
        except:
            last_page_number = -1
    else:
        last_page_number = 1 # Если нет списка страниц, то страница одна
    # print("Закончил")
    return last_page_number

def parse():
    # Жилая недвижимость
    prop_type = 0
    for key in ADVERTS_TYPE_0.keys():
        page_number = 1
        while True:
            page_url = base_url + str(page_number).join(ADVERTS_TYPE_0.get(key).split('\t'))
            last_page = parse_one_page(page_url, prop_type, key)
            time.sleep(5)
            if(last_page == page_number):
                break
            else:
                page_number += 1

    # Не жилая недвижимость
    prop_type = 1
    for key in ADVERTS_TYPE_1.keys():
        page_number = 1
        while True:
            page_url = base_url + str(page_number).join(ADVERTS_TYPE_1.get(key).split('\t'))
            last_page = parse_one_page(page_url, prop_type, key)
            time.sleep(5)
            if (last_page == page_number):
                break
            else:
                page_number += 1

if __name__ == '__main__':
    base_url = 'https://www.kvadroom.ru/'
    adverts_mas = []
    print('Начинаю работу')
    parse()
    print('Я все сделал, готовлю отчет')

    with open('exit.json', 'w', encoding='utf-8') as file:
        json.dump(adverts_mas, file, indent=2, ensure_ascii=False)

    print('Результаты в файле exit.json')