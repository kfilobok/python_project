from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('products.db')
cursor = conn.cursor()




def get_LIME_photos(driver, link):
    driver.get(link)
    # soup = BeautifulSoup(driver.page_source, 'lxml')
    time.sleep(3)
    images = driver.find_elements(By.CSS_SELECTOR, "img")
    image_urls = [img.get_attribute("src") for img in images]
    # print(soup.find("div", "CardProduct__color-article")) #.find("div", "ColorSelector product__colors").find("div", "ColorSelector__title")


    return image_urls


def get_lime_photo_for_db(driver):
    cursor.execute("SELECT id, photo, color, link FROM LIME")
    rows = cursor.fetchall()
    for row in rows:
        product_id, photo0, color0, link = row
        # print(link)
        if link and (not photo0 and not color0):
            photo = ",".join(get_LIME_photos(driver, link))
            cursor.execute("UPDATE LIME SET photo = ? WHERE id = ?", (photo, product_id))
            conn.commit()


def get_LIME_goods(soup, driver):
    """Функция для парсинга карточек продуктов."""
    data = []

    # Ищем все карточки продуктов
    cards = soup.find_all('div', class_='CatalogProduct__content mediaText')

    for card in cards:
        # Извлекаем название товара и ссылку
        title_div = card.find('div', class_='CatalogProduct__title')
        title_link = title_div.find('a') if title_div else None
        name = title_link.text.strip() if title_link else 'Название отсутствует'
        link = "https://lime-shop.com" + title_link['href'] if title_link else 'Ссылка отсутствует'

        # Извлекаем цену товара
        price_div = card.find('div', class_='CatalogProduct__price')
        price = price_div.text.strip() #.replace("руб.", "")

        # Добавляем собранные данные в список
        data.append({
            'name': name,
            'link': link,
            'price': price
        })

        # Вставка записи в таблицу
        cursor.execute('''
        INSERT OR IGNORE INTO LIME (name, price, type, color, photo, link)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, price, None, None, None, link))

        conn.commit()

    return data

