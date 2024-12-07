# python_project
Авторы: Коровина Полина и Филобок Екатерина

### Идея проекта:
Парсинг сайтов магазинов одежды для созданичя бд для стилистов, а так же ее визуализация


### UI пользователя 
На главной странице представлены актуальные тренды, а также самые выгодные предложения. Пользователь может перейти к поиску по категориям (женская/мужская одежда, обувь, аксессуары)


Пользователь может задать фильтры, чтобы сузить круг поиска, например, выбирает тип одежды, цену или стиль


При нажатии на товар отображается подробная информация: фото, описание, цена, текущие скидки, тренды, в которые он вписывается, и ссылка на товар на сайте магазина.



### Стек технологий


**Парсинг**:
- BeautifulSoup
- Selenium

**Обработка данных:**
- numpy
- sentence_transformers
- NLTK/SpaCy

**Хранение данных (PostgreSQL):**
- psycopg2
- SQLAlchemy


**Сайт:**
- Flask

### Ссылка на видеоотчёт
https://disk.yandex.ru/i/87hRYO_M4BfpAw

### Тесты
1. тест Endpoint_Tests проверяет доступен ли определённый маршрут и возвращает ли он правильный статус и содержимое

2. тест product_detail_test проверяет, что страница товара отображает корректную информацию о товаре, извлекаемую из базы данных

3. тест test_search проверяет работу поиска по каталогу
 
4. тест time_test проверяет что страницы home и catalog открываются быстрее 0.02 секунды

5. тест test_ui автоматически проверяет ппользоваательский интерфейс, а именно взаимодействие с кнопками, тут используется selenium
 
во всех тестах использован unittest

### Отчёт по сайту
**Сделано:**
На сайте реализована визуализация базы данных, на главной странице есть кнопка перехода к каталогу, а также 5 различных фотографий товаров в полный экран, которые меняются при каждом заходе на главную страницу, на эти фотографии можно нажать и перейти на страницу соответствующего товара.
На странице каталога есть кнопка, которая может вернуть пользователя на главную страницу, есть строка поиска. На одной странице отображаются по 16 товаров, внизу страницы есть кнопки перехода по страницам с различными товарами. На странице товара можно увидеть все фотографии связанные с ним, название и цену, также есть кнопка перехода на сайт магазина и кнопка, которая позволяет вернуться к каталогу. 
**Планируется сделать:**
Добавить фильтры по цене, типу и цвету одежды
Доработать поиск, чтобы он был не чувствителен к регистрам
Доработать переход со страницы товара обратно в каталог, чтобы пользователь возвращался на страницу, на которой был


### Роли в команде

Коровина Полина - работа над сайтом

Филобок Екатерина - парсинг и обработка данных (тг: https://t.me/kati4kaf)
