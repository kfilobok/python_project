import unittest
from app import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        # Создаём тестовый клиент
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Проверяем, есть ли фраза "Главная страница" на главной странице
        self.assertIn('Главная страница', response.data.decode('utf-8'))

    def test_catalog_page(self):
        response = self.app.get('/catalog')
        self.assertEqual(response.status_code, 200)
        # Проверяем, есть ли фраза "Каталог товаров" на странице каталога
        self.assertIn('Каталог товаров', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
