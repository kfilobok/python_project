import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductCatalogFavoritesTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_favorites_display(self):
        driver = self.driver
        driver.get("http://localhost:5000/")  # Открыть главную страницу

        #Вход в систему
        login_button = driver.find_element(By.LINK_TEXT, "Войти")
        login_button.click()

        # Заполняем форму для входа
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")

        email_field.send_keys("testuser1@example.com")
        password_field.send_keys("1234")
        password_field.send_keys(Keys.RETURN)

        time.sleep(2)


        logout_button = driver.find_element(By.LINK_TEXT, "Выйти")
        self.assertTrue(logout_button.is_displayed(), "Кнопка 'Выйти' не отображается, вход не выполнен")

        # Переход в каталог товаров
        catalog_button = driver.find_element(By.LINK_TEXT, "Посмотреть весь каталог")
        catalog_button.click()
        time.sleep(2)

        # Добавление товара в избранное
        add_to_favorites_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-card .favorite-button"))
        )
        add_to_favorites_button.click()
        time.sleep(2)

        # Переход в раздел "Избранное"
        favorites_button = driver.find_element(By.LINK_TEXT, "Избранное")
        favorites_button.click()
        time.sleep(2)

        # Проверка наличия товара в разделе "Избранное"
        product_cards = driver.find_elements(By.CSS_SELECTOR, ".product-card")
        self.assertGreater(len(product_cards), 0, "В разделе 'Избранное' нет товаров")

        #  Проверка, что товар отображается с кнопкой удаления
        remove_button = driver.find_element(By.CSS_SELECTOR, ".product-card .remove-favorite-button")
        self.assertTrue(remove_button.is_displayed(), "Кнопка удаления из избранного не отображается")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
