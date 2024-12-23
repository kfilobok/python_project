from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sqlite3


# Подключение к базе данных
conn = sqlite3.connect('products.db')
cursor = conn.cursor()


def get_AWN_goods(soup):
    data = []
    cards = soup.find('div', class_='catalog catalog--items-3')  # .find('div', class_='product-item catalog__product')
    # print(len(cards))

    for card in cards:
        if card != None and str(card).rstrip():
            name = card.find('a', class_='product-item--link').find('span', class_='product-item--name').get_text(
                strip=True)  # .get('product-item--nam')
            # print(item_name)
            price = card.find('div', class_='product-item--price').find('div', class_='price').find('span').get_text(
                strip=True).split(' / ')[0].replace(' ', '').replace('₽', ' руб.')
            # print(price)
            link = "https://allweneed.ru" + card.find('a', class_='product-item--image-wrapper').get('href')
            # print(link)

            data.append({
                'name': name,
                'link': link,
                'price': price
            })

            # Вставка записи в таблицу
            cursor.execute('''
                    INSERT OR IGNORE INTO AWN (name, price, type, color, photo, link)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (name, price, None, None, None, link))
            conn.commit()

    return data


def get_AWN_photos(driver, link):
    dictionary = {'beige': 'бежевый', 'black': 'черный', 'blue': 'синий', 'brown': 'коричневый', 'camel': 'верблюд',
                  'coffee': 'кофе', 'dark green': 'темно-зеленый', 'dark grey': 'темно-серый', 'green': 'зеленый',
                  'greige': 'серый', 'grey': 'серый', 'grey-blue': 'серо-синий', 'ink navy': 'темно-синий',
                  'khaki': 'хаки', 'light-grey': 'светло-серый', 'milky': 'молочный', 'olive': 'оливковый',
                  'red': 'красный', 'white': 'белый', 'white blue': 'белый синий'}

    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    time.sleep(2)
    # images = driver.find_elements(By.CSS_SELECTOR, "img")
    # image_urls = [img.get_attribute("src") for img in images]

    colour = soup.find('div', class_='product-page--color').find('div', class_='product-page--color-header').get_text(
        strip=True).split(':')[1]
    # print(colour)
    photo = soup.find('div', class_='product-gallery__image').find_all('img')[1]['src']
    if colour in dictionary.keys():
        colour = dictionary[colour]

    return colour, photo


def get_AWN_photo_for_db(driver, soup):
    cursor.execute("SELECT id, photo, color, link FROM AWN")
    rows = cursor.fetchall()
    for row in rows:
        product_id, photo0, color0, link0 = row
        # print(link)
        if link0 and not photo0 and not color0:
            col, photo = get_AWN_photos(driver, link0)

            cursor.execute('''
                UPDATE AWN
                SET photo = ?, color = ?
                WHERE id = ?
            ''', (photo, col, product_id))

            conn.commit()
