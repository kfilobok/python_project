#Проверяют, доступен ли определённый маршрут и возвращает ли он правильный статус и содержимое

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
        self.assertIn(b'main page', response.data)

    def test_catalog_page(self):
        response = self.app.get('/catalog')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product Catalog', response.data)

if __name__ == '__main__':
    unittest.main()
