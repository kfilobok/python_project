import unittest
import time
from app import app

class TestPagePerformance(unittest.TestCase):
    def setUp(self):
        """Настройка тестового клиента Flask"""
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page_performance(self):
        """Тест производительности главной страницы"""
        start_time = time.time()
        response = self.app.get('/')
        end_time = time.time()

        # Измеряем время выполнения
        load_time = end_time - start_time
        print(f"Время загрузки главной страницы: {load_time:.4f} секунд")

        # Проверяем, что загрузка страницы занимает менее 1 секунды
        self.assertLess(load_time, 0.02, f"Загрузка главной страницы занимает слишком много времени: {load_time:.4f} секунд")

    def test_catalog_page_performance(self):
        """Тест производительности страницы каталога"""
        start_time = time.time()
        response = self.app.get('/catalog')
        end_time = time.time()

        # Измеряем время выполнения
        load_time = end_time - start_time
        print(f"Время загрузки страницы каталога: {load_time:.4f} секунд")

        # Проверяем, что загрузка страницы занимает менее 1.5 секунд
        self.assertLess(load_time, 0.02, f"Загрузка страницы каталога занимает слишком много времени: {load_time:.4f} секунд")


if __name__ == '__main__':
    unittest.main()
