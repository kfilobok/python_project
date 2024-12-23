import unittest
from app import app

class TestCatalogSearch(unittest.TestCase):
    def setUp(self):
        """Настройка тестового клиента Flask"""
        self.app = app.test_client()
        self.app.testing = True

    def test_search_results_found(self):
        """Тест поиска: результаты найдены"""
        response = self.app.post('/catalog', data={'query': 'Носки'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Носки'.encode('utf-8'), response.data)

    def test_search_no_results(self):
        """Тест поиска: результаты не найдены"""
        response = self.app.post('/catalog', data={'query': 'Несуществующий продукт'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Нет товаров, соответствующих вашему запросу.'.encode('utf-8'), response.data)
