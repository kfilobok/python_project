from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import time

class TestUserLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5000/login")

    def tearDown(self):
        self.driver.quit()

    def test_user_login(self):
        """Тест авторизации пользователя"""
        driver = self.driver

        # Заполняем форму входа
        driver.find_element(By.ID, "email").send_keys("testuser2@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.XPATH, "//button[text()='Войти']").click()

        time.sleep(2)

        # Проверяем, что отображается приветственное сообщение
        self.assertIn("Привет, testuser!", driver.page_source)
