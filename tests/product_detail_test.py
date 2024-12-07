import unittest
from app import app, get_db

class TestProductDetail(unittest.TestCase):
    def setUp(self):
        """Настройка тестового клиента Flask и контекста приложения"""
        self.app = app.test_client()
        self.app.testing = True

        # Устанавливаем контекст
        self.app_context = app.app_context()
        self.app_context.push()

        # Подключаемся к базе данных и очищаем таблицу products
        self.db = get_db()
        self.db.execute("DELETE FROM products")
        self.db.commit()

    def tearDown(self):
        """Очистка после тестов"""
        # Удаляем все данные из таблицы products
        self.db.execute("DELETE FROM products")
        self.db.commit()

        # Завершаем контекст приложения
        self.app_context.pop()

    def test_product_detail_page(self):
        """Тест страницы деталей товара"""
        # Добавляем тестовые данные в таблицу products
        self.db.execute(
            "INSERT INTO products (id, name, price, photo) VALUES (?, ?, ?, ?)",
            (1, 'Product 1', 100.0, 'https://example.com/photo1.jpg')
        )
        self.db.commit()

        # Выполняем GET-запрос к странице деталей товара
        response = self.app.get('/product/1')

        # Проверяем, что ответ успешен
        self.assertEqual(response.status_code, 200)

        # Проверяем, что данные продукта отображаются на странице
        self.assertIn(b'Product 1', response.data)
        self.assertIn(b'100.0', response.data)  # Проверяем отображение цены

if __name__ == '__main__':
    unittest.main()
