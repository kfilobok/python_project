from flask import Flask, render_template, g, request
import sqlite3

# Константы
DATABASE = 'products.db'
PER_PAGE = 16  # Количество товаров на странице

# Инициализация
app = Flask(__name__)

# Подключение к базе данных
def get_db():
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

# Главная страница
@app.route('/')
def home():
    db = get_db()
    cursor = db.execute('SELECT * FROM products ORDER BY RANDOM() LIMIT 5')  # Выбираем 5 случайных товаров
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

# Страница каталога
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
