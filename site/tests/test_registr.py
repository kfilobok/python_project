from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import time


class TestUserRegistration(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5000/register")

    def tearDown(self):
        self.driver.quit()

    def test_user_registration(self):
        """Тест регистрации нового пользователя"""
        driver = self.driver

        # Заполняем форму регистрации
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "email").send_keys("testuser2@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.XPATH, "//button[text()='Зарегистрироваться']").click()

        time.sleep(2)

        # Проверяем, что пользователь перенаправлен на страницу входа
        self.assertIn("Вход", driver.page_source)
