from flask import Flask, render_template, g, request, redirect, url_for, flash
import sqlite3
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
import bcrypt  # Для хэширования паролей

# Константы
DATABASE = 'products.db'
PER_PAGE = 64
VALID_TABLES = ['ZRN', 'AWN', 'LIME']

# Инициализация приложения
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Подключение к базе данных
def get_db():
    """Подключение к базе данных products.db."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Flask-Login: Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    if user:
        return User(user['id'], user['username'], user['email'], user['password_hash'])
    return None


# Модель пользователя
class User(UserMixin):
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash


# Функция для генерации хэша пароля
def generate_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


# Функция для проверки пароля
def check_password_hash(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))


# Главная страница
@app.route('/')
def home():
    db = get_db()
    featured_products = []

    for table in VALID_TABLES:
        cursor = db.execute(f'SELECT * FROM {table} ORDER BY RANDOM() LIMIT 5')
        products = cursor.fetchall()

        for product in products:
            product_dict = dict(product)
            if table == 'LIME':
                # Для LIME сохраняем всю работу с фотографиями
                photos = [photo.strip() for photo in product_dict['photo'].split(',')]
                high_quality_photo = next((photo for photo in photos if is_high_quality(photo)), None)
                product_dict['photo'] = high_quality_photo
            else:
                # Для остальных таблиц берём первую фотографию
                product_dict['photo'] = product_dict['photo'].split(',')[0].strip()

            product_dict['table_name'] = table  # Добавляем имя таблицы
            featured_products.append(product_dict)

    return render_template('home.html', featured_products=featured_products)


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Генерация хэша пароля
        password_hash = generate_password_hash(password)

        # Сохранение пользователя в базе данных
        db = get_db()
        db.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        db.commit()

        flash('Вы успешно зарегистрировались.')
        return redirect(url_for('login'))
    return render_template('register.html')


# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Поиск пользователя в базе данных
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        # Проверка пароля
        if user and check_password_hash(user['password_hash'], password):
            user_obj = User(user['id'], user['username'], user['email'], user['password_hash'])
            login_user(user_obj)
            flash('Вы успешно вошли в систему.')
            return redirect(url_for('home'))
        flash('Неправильный email или пароль.')
    return render_template('login.html')


# Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.')
    return redirect(url_for('home'))

# Добавление товара в избранное
@app.route('/favorite/<table_name>/<int:product_id>', methods=['POST'])
@login_required
def add_to_favorites(table_name, product_id):
    db = get_db()

    # Проверяем, если запись уже существует
    cursor = db.execute(
        'SELECT * FROM favorites WHERE user_id = ? AND product_id = ? AND table_name = ?',
        (current_user.id, product_id, table_name)
    )
    if cursor.fetchone():
        return {"message": "Уже в избранном"}, 200

    # Добавляем запись
    db.execute(
        'INSERT INTO favorites (user_id, product_id, table_name) VALUES (?, ?, ?)',
        (current_user.id, product_id, table_name)
    )
    db.commit()
    return {"message": "Добавлено в избранное"}, 200


# Удаление товара из избранного
@app.route('/favorite/<table_name>/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_favorites(table_name, product_id):
    db = get_db()

    # Удаляем запись
    db.execute(
        'DELETE FROM favorites WHERE user_id = ? AND product_id = ? AND table_name = ?',
        (current_user.id, product_id, table_name)
    )
    db.commit()
    return {"message": "Удалено из избранного"}, 200

# Страница с избранным
@app.route('/favorites')
@login_required
def favorites():
    db = get_db()
    cursor = db.execute(
        '''
        SELECT id, name, price, type, color, photo, link, 'ZRN' AS table_name 
        FROM ZRN
        WHERE id IN (SELECT product_id FROM favorites WHERE user_id = ? AND table_name = 'ZRN')
        UNION ALL
        SELECT id, name, price, type, color, photo, link, 'AWN' AS table_name 
        FROM AWN
        WHERE id IN (SELECT product_id FROM favorites WHERE user_id = ? AND table_name = 'AWN')
        UNION ALL
        SELECT id, name, price, type, color, photo, link, 'LIME' AS table_name 
        FROM LIME
        WHERE id IN (SELECT product_id FROM favorites WHERE user_id = ? AND table_name = 'LIME')
        ''',
        (current_user.id, current_user.id, current_user.id)
    )
    favorites = cursor.fetchall()

    processed_favorites = []
    for product in favorites:
        product_dict = dict(product)
        table_name = product_dict['table_name']

        if table_name == 'LIME':
            # Для LIME сохраняем всю работу с фотографиями
            if product_dict.get('photo'):
                photos = [photo.strip() for photo in product_dict['photo'].split(',')]
                high_quality_photo = next((photo for photo in photos if is_high_quality(photo)), None)
                product_dict['photo'] = high_quality_photo
        else:
            # Для остальных таблиц берём первую фотографию
            if product_dict.get('photo'):
                product_dict['photo'] = product_dict['photo'].split(',')[0].strip()

        processed_favorites.append(product_dict)

    return render_template('favorites.html', favorites=processed_favorites)


@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    db = get_db()
    page = request.args.get('page', 1, type=int)
    query = request.form.get('query') if request.method == 'POST' else request.args.get('query', '')
    sort = request.args.get('sort', 'asc')  # Значение по умолчанию: сортировка по возрастанию
    sort_enabled = request.args.get('sort_enabled', 'true') == 'true'  # По умолчанию сортировка включена

    # Лимиты и смещения для пагинации
    offset = (page - 1) * PER_PAGE

    # Основной запрос на выборку
    base_query = '''
        SELECT id, name, CAST(REPLACE(REPLACE(price, ' руб', ''), ',', '.') AS REAL) AS numeric_price,
               type, color, photo, link, 'ZRN' AS table_name FROM ZRN
        UNION ALL
        SELECT id, name, CAST(REPLACE(REPLACE(price, ' руб', ''), ',', '.') AS REAL) AS numeric_price,
               type, color, photo, link, 'AWN' AS table_name FROM AWN
        UNION ALL
        SELECT id, name, CAST(REPLACE(REPLACE(price, ' руб', ''), ',', '.') AS REAL) AS numeric_price,
               type, color, photo, link, 'LIME' AS table_name FROM LIME
    '''

    # Условие поиска
    if query:
        base_query = f'''
            SELECT * FROM (
                {base_query}
            ) WHERE name LIKE ? OR type LIKE ? OR color LIKE ?
        '''
        params = (f"%{query.strip()}%", f"%{query.strip()}%", f"%{query.strip()}%")
    else:
        # Без условия поиска
        params = ()

    # Добавление сортировки
    if sort_enabled:
        sort_order = 'ASC' if sort == 'asc' else 'DESC'
        base_query += f' ORDER BY numeric_price {sort_order}'
    base_query += ' LIMIT ? OFFSET ?'
    params += (PER_PAGE, offset)

    cursor = db.execute(base_query, params)
    products = cursor.fetchall()

    # Считаем общее количество товаров для пагинации
    total_query = '''
        SELECT COUNT(*) FROM (
            SELECT id FROM ZRN
            UNION ALL
            SELECT id FROM AWN
            UNION ALL
            SELECT id FROM LIME
        )
    '''
    if query:
        total_query = f'''
            SELECT COUNT(*) FROM (
                SELECT * FROM (
                    SELECT id, name, type, color FROM ZRN
                    UNION ALL
                    SELECT id, name, type, color FROM AWN
                    UNION ALL
                    SELECT id, name, type, color FROM LIME
                ) WHERE name LIKE ? OR type LIKE ? OR color LIKE ?
            )
        '''
        total_params = (f"%{query.strip()}%", f"%{query.strip()}%", f"%{query.strip()}%")
    else:
        total_params = ()

    total_products = db.execute(total_query, total_params).fetchone()[0]
    total_pages = (total_products + PER_PAGE - 1) // PER_PAGE

    # Проверяем товары в избранном
    if current_user.is_authenticated:
        favorite_query = '''
            SELECT product_id, table_name FROM favorites WHERE user_id = ?
        '''
        favorite_rows = db.execute(favorite_query, (current_user.id,)).fetchall()
        favorite_set = {(row['product_id'], row['table_name']) for row in favorite_rows}
    else:
        favorite_set = set()

    processed_products = []
    for product in products:
        product_dict = dict(product)
        # Обработка фотографий
        if product['table_name'] == 'LIME':
            # Для LIME берём первое фото высокого качества или первое доступное
            photos = [photo.strip() for photo in product_dict['photo'].split(',')]
            high_quality_photo = next((photo for photo in photos if is_high_quality(photo)), None)
            product_dict['photo'] = high_quality_photo or (photos[0] if photos else None)
        else:
            # Для остальных таблиц берём первое фото
            product_dict['photo'] = product_dict['photo'].split(',')[0].strip() if product_dict['photo'] else None

        product_dict['is_favorite'] = (product['id'], product['table_name']) in favorite_set
        processed_products.append(product_dict)

    # Если товаров нет, передаём флаг products_empty
    products_empty = len(processed_products) == 0

    return render_template(
        'catalog.html',
        products=processed_products,
        query=query,
        sort=sort,
        sort_enabled=sort_enabled,
        page=page,
        total_pages=total_pages,
        products_empty=products_empty  # Флаг для отображения сообщения
    )



@app.route('/product/<table_name>/<int:product_id>')
def product_detail(table_name, product_id):
    db = get_db()

    cursor = db.execute(f'SELECT * FROM {table_name} WHERE id = ?', (product_id,))
    product = cursor.fetchone()

    if not product:
        return "Product not found", 404

    product_dict = dict(product)

    if table_name == 'LIME':
        if product_dict['photo']:
            photos = [photo.strip() for photo in product_dict['photo'].split(',')]
            high_quality_photos = [photo for photo in photos if is_high_quality(photo)]
            product_dict['photos'] = high_quality_photos
    else:
        if product_dict['photo']:
            product_dict['photos'] = [photo.strip() for photo in product_dict['photo'].split(',')]

    # Проверяем, добавлен ли продукт в избранное
    product_dict['is_favorite'] = False
    if current_user.is_authenticated:
        favorite_check_query = '''
            SELECT 1 FROM favorites WHERE user_id = ? AND product_id = ? AND table_name = ?
        '''
        is_favorite = db.execute(favorite_check_query, (current_user.id, product_id, table_name)).fetchone()
        product_dict['is_favorite'] = is_favorite is not None

    # Передача параметров в шаблон
    return render_template(
        'product_detail.html',
        product=product_dict,
        table_name=table_name  # Передача table_name
    )


# Функция проверки высокого качества изображения
def is_high_quality(url):
    import re
    return bool(re.search(r'q=85', url) and re.search(r'w=1000', url))


# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
