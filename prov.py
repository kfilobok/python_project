import sqlite3

# Подключение к базе данных
# Укажите путь к вашей базе данных. Для SQLite это будет файл базы данных.
connection = sqlite3.connect("products.db")

# Создание курсора для выполнения запросов
cursor = connection.cursor()

# SQL-запрос для просмотра содержимого таблицы
query = "SELECT * FROM AWN;"  # Замените table_name на имя вашей таблицы

# Выполнение запроса
cursor.execute(query)

# Получение данных
rows = cursor.fetchall()

# Печать данных
for row in rows:
    print(row)

# Закрытие соединения
connection.close()
