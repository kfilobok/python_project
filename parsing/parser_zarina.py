from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('products.db')
cursor = conn.cursor()



def get_ZRN_goods(soup):
    data = []
    cards = soup.find_all('div', class_='catalog__item')  # .find('div', class_='product-item catalog__product')
    # print(len(cards))

    for card in cards:
        if card != None and str(card).rstrip():
            # price = card.find('div', class_='product-item--price').find('div', class_='price').find('span').get_text(
            #     strip=True).split(' / ')[0].replace(' ', '').replace('₽', ' руб')
            # # print(price)

            name = card.find('div', class_='catalog__product-info').find("div",
                                                                         class_='catalog__product-title').get_text()
            link = "https://zarina.ru" + card.find('div', class_='catalog__product-info').find("div",
                                                                                               class_='catalog__product-title').find(
                "a").get('href')
            price = card.find('div', class_='catalog__product-info').find("div",
                                                                          class_="catalog__product-price_current").get_text(
                strip=True).replace('₽', 'руб.').rstrip()
            # print(price)
            data.append({
                'name': name,
                'link': link,
                'price': price
            })

            cursor.execute('''
                    INSERT OR IGNORE INTO ZRN (name, price, type, color, photo, link)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (name, price, None, None, None, link))
            conn.commit()

    return data


def get_ZRN_photos(driver, link):
    try:
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        time.sleep(2)
        # images = driver.find_elements(By.CSS_SELECTOR, "img")
        # image_urls = [img.get_attribute("src") for img in images]
        # print(link)

        colour = soup.find('div', class_='product__colors').find('div', class_='product__colors-title').get_text(
            strip=True)
        # print(colour)
        photos = soup.find('div', class_='product__media').find_all('div', "product__media-preview_item swiper-slide")
        photo = [myimg.find("img").get('src') for myimg in photos]
        # print(photo)
        return colour, photo
    except AttributeError:
        return "", []


def get_ZRN_photo_for_db(driver, soup):
    cursor.execute("SELECT id, photo, color, link FROM ZRN")
    rows = cursor.fetchall()
    for row in rows:
        product_id, photo0, color0, link0 = row
        # print(link)
        if link0 and not photo0 and not color0:
            col, photo = get_ZRN_photos(driver, link0)
            photo = ",".join(photo)
            cursor.execute('''
                UPDATE ZRN
                SET photo = ?, color = ?
                WHERE id = ?
            ''', (photo, col, product_id))

            conn.commit()
