import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestUserInterface(unittest.TestCase):
    def setUp(self):
        """Настройка браузера"""
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5000/catalog")

    def tearDown(self):
        """Закрытие браузера после тестов"""
        self.driver.quit()

    def test_navigation_to_home(self):
        """Тест перехода на главную страницу"""
        driver = self.driver

        # Найти кнопку перехода на главную страницу и нажать её
        home_button = driver.find_element(By.LINK_TEXT, "Back to Home")
        home_button.click()

        # Подождать загрузки страницы
        time.sleep(2)

        # Проверяем, что мы на главной странице
        self.assertIn("main page", driver.page_source)

    def test_navigation_to_product_page(self):
        """Тест перехода на страницу товара"""
        driver = self.driver

        # Найти ссылку на первый товар и нажать её
        product_link = driver.find_element(By.CSS_SELECTOR, ".product-link")
        product_link.click()

        # Подождать загрузки страницы
        time.sleep(2)

        # Проверяем, что мы на странице товара
        self.assertIn("Price:", driver.page_source)  # Проверяем, что на странице есть цена
        self.assertIn("Buy from Store", driver.page_source)  # Проверяем наличие кнопки покупки


if __name__ == '__main__':
    unittest.main()
