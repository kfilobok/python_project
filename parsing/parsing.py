from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import sqlite3
from parser_lime import get_LIME_goods, get_lime_photo_for_db, get_LIME_photos
from parser_allweneed import get_AWN_goods, get_AWN_photo_for_db, get_AWN_photos
from parser_zarina import get_ZRN_goods, get_ZRN_photo_for_db, get_ZRN_photos

# Подключение к базе данных
conn = sqlite3.connect('products.db')
cursor = conn.cursor()


def scroll_to_load(driver):
    """Функция для плавного скроллинга страницы вниз, чтобы загрузить все элементы."""
    scroll_pause_time = 1  # Время ожидания после каждой прокрутки
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Прокручиваем страницу вниз
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        # Получаем новую высоту страницы
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Если высота больше не меняется, значит мы дошли до конца
        if new_height == last_height:
            break
        last_height = new_height


def main():
    driver = webdriver.Safari()
    driver.maximize_window()

    # LIME
    try:
        driver.get('https://lime-shop.com/ru_ru/catalog/men_view_all')

        # Ожидаем появления первого элемента на странице
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'CatalogProduct__content'))
        )

        # time.sleep(10)
        scroll_to_load(driver)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        data = get_LIME_goods(soup, driver)
        # for item in data:
        #     print(item)

        get_lime_photo_for_db(driver)

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    # ALL WE NEED
    try:
        driver.get('https://allweneed.ru/en/catalog/man')
        # time.sleep(2)
        scroll_to_load(driver)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        data = get_AWN_goods(soup)
        # for item in data:
        #     print(item)
        get_AWN_photo_for_db(driver, soup)


    except Exception as e:
        print(f"Произошла ошибка: {e}")

    # Zarina
    try:
        for i in range(1, 13):
            driver.get(f'https://zarina.ru/man/clothes/?page={i}')
            soup = BeautifulSoup(driver.page_source, 'lxml')
            time.sleep(2)
            data = get_ZRN_goods(soup)
            # for item in data:
            #     print(item)
            get_ZRN_photo_for_db(driver, soup)

    except Exception as e:
        print(f"Произошла ошибка: {e}")


    finally:
        # Закрываем браузер
        driver.quit()
        conn.close()


if __name__ == "__main__":
    main()
