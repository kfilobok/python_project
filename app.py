from flask import Flask, render_template, g, request, redirect, url_for, flash
import sqlite3
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
import bcrypt  # Для хэширования паролей

# Константы
DATABASE = 'products.db'
PER_PAGE = 16

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
    cursor = db.execute('SELECT * FROM products ORDER BY RANDOM() LIMIT 5')
    products = cursor.fetchall()

    featured_products = []
    for product in products:
        product_dict = dict(product)
        # Разделяем все ссылки
        photos = [photo.strip() for photo in product_dict['photo'].split(',')]
        # Берем первую ссылку высокого качества
        high_quality_photo = next((photo for photo in photos if is_high_quality(photo)), None)
        product_dict['photo'] = high_quality_photo
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
@app.route('/favorite/<int:product_id>', methods=['POST'])
@login_required
def add_to_favorites(product_id):
    db = get_db()
    cursor = db.execute(
        'SELECT * FROM favorites WHERE user_id = ? AND product_id = ?',
        (current_user.id, product_id)
    )
    if cursor.fetchone():
        return {"message": "Уже в избранном"}, 200

    db.execute(
        'INSERT INTO favorites (user_id, product_id) VALUES (?, ?)',
        (current_user.id, product_id)
    )
    db.commit()
    return {"message": "Добавлено в избранное"}, 200


# Удаление товара из избранного
@app.route('/favorite/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_favorites(product_id):
    db = get_db()
    db.execute(
        'DELETE FROM favorites WHERE user_id = ? AND product_id = ?',
        (current_user.id, product_id)
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
        SELECT products.*
        FROM products
        JOIN favorites ON products.id = favorites.product_id
        WHERE favorites.user_id = ?
        ''',
        (current_user.id,)
    )
    favorites = cursor.fetchall()

    processed_favorites = []
    for product in favorites:
        product_dict = dict(product)
        if product_dict['photo']:
            photos = [photo.strip() for photo in product_dict['photo'].split(',')]
            high_quality_photo = next((photo for photo in photos if is_high_quality(photo)), None)
            product_dict['photo'] = high_quality_photo
        processed_favorites.append(product_dict)

    return render_template('favorites.html', favorites=processed_favorites)


# Функция проверки высокого качества изображения
def is_high_quality(url):
    import re
    return bool(re.search(r'q=85', url) and re.search(r'w=1000', url))


@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    db = get_db()
    page = request.args.get('page', 1, type=int)
    query = request.form.get('query')

    if query:
        cursor = db.execute(
            '''
            SELECT * FROM products
            WHERE name LIKE ?
            LIMIT ? OFFSET ?
            ''',
            (f'%{query.strip()}%', PER_PAGE, (page - 1) * PER_PAGE)
        )
    else:
        cursor = db.execute(
            'SELECT * FROM products LIMIT ? OFFSET ?',
            (PER_PAGE, (page - 1) * PER_PAGE)
        )

    products = cursor.fetchall()

    # Обработка товаров
    processed_products = []
    for product in products:
        product_dict = dict(product)
        if product_dict['photo']:
            # Разделяем все ссылки
            photos = [photo.strip() for photo in product_dict['photo'].split(',')]
            # Берем первую ссылку высокого качества
            high_quality_photo = next((photo for photo in photos if is_high_quality(photo)), None)
            product_dict['photo'] = high_quality_photo
        processed_products.append(product_dict)

    total_products = db.execute(
        '''
        SELECT COUNT(*) FROM products
        WHERE name LIKE ?
        ''' if query else 'SELECT COUNT(*) FROM products',
        (f'%{query.strip()}%',) if query else ()
    ).fetchone()[0]
    total_pages = (total_products + PER_PAGE - 1) // PER_PAGE

    return render_template(
        'catalog.html',
        products=processed_products,
        query=query,
        page=page,
        total_pages=total_pages
    )


# Страница товара
def is_high_quality(url):
    import re
    return bool(re.search(r'q=85', url) and re.search(r'w=1000', url))


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()

    if product:
        product_dict = dict(product)
        if product_dict['photo']:
            # Разделяем все ссылки
            photos = [photo.strip() for photo in product_dict['photo'].split(',')]
            high_quality_photos = [photo for photo in photos if is_high_quality(photo)]
            product_dict['photos'] = high_quality_photos
        return render_template('product_detail.html', product=product_dict)
    else:
        return "Product not found", 404


# Запуск
if __name__ == '__main__':
    app.run(debug=True)
