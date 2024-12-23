import unittest
from app import app, get_db

class TestProductDetail(unittest.TestCase):
    def setUp(self):
        """Настройка тестового клиента Flask и контекста приложения"""
        self.app = app.test_client()
        self.app.testing = True

        # Устанавливаем контекст приложения
        self.app_context = app.app_context()
        self.app_context.push()

        # Подключаемся к базе данных
        self.db = get_db()


    def test_product_detail_page(self):
        # Выполняем GET-запрос к странице деталей товара
        response = self.app.get('/product/ZRN/483')

        # Проверяем, что ответ успешен
        self.assertEqual(response.status_code, 200)

        self.assertIn('Футболка relax fit'.encode('utf-8'), response.data)  # Название товара
        self.assertIn('1999'.encode('utf-8'), response.data)  # Цена товара
        self.assertIn('Черный'.encode('utf-8'), response.data)  # Цвет товара


if __name__ == '__main__':
    unittest.main()
