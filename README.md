# CoffeeShop Django

**Тестовое приложение** на Django для управления пользователями, товарами (продуктами), корзиной и заказами в сети кофеен. Пользователи могут просматривать каталог товаров, добавлять их в корзину и оформлять заказы, а администратор управляет категориями, товарами и пользователями. Также реализован чат поддержки (WebSocket), JWT-аутентификация, Swagger-документация, и (опционально) уведомления на почту.

---

## Функциональность

- **Пользователи (CustomUser)**:
  - Регистрация / аутентификация (JWT).
  - Поле `role` (значения: `user` или `admin`).
  - Поле `is_verified` (для подтверждённых / неподтверждённых аккаунтов).
  - Очистка не верифицированных пользователей через 2 дня (опционально).

- **Категории / Товары**:
  - Категории (`Category`) и Товары (`Product`).
  - CRUD-операции. Для админов — создание/редактирование, для пользователей — только чтение.
  - Поиск, фильтрация, сортировка, пагинация (через Django REST Framework).

- **Корзина (Cart)**:
  - Модель `CartItem` хранит `(user_id, product_id, quantity)`.
  - CRUD эндпоинты для добавления товаров в корзину, просмотра содержимого и удаления позиций.

- **Заказы (Order)**:
  - Модель `Order` (поля: `user_id`, `created_at`, `total_price`, `status`).
  - Модель `OrderItem` (ссылки на `order_id` и `product_id`, хранит `quantity`, `price`).
  - Создание заказа из корзины, просмотр. Админ видит все заказы, пользователь видит только свои.

- **WebSocket-чат (Support Chat)**:
  - Django Channels, маршрут `ws://127.0.0.1:8000/ws/support/`.
  - Позволяет пользователю общаться с поддержкой в реальном времени.

- **Swagger / ReDoc** (drf-yasg):
  - Swagger: `http://127.0.0.1:8000/swagger/`
  - ReDoc: `http://127.0.0.1:8000/redoc/`

---

## Технологии

```text
- Python 3.11
- Django 5.1
- Django REST Framework
- PostgreSQL (через psycopg2-binary)
- djangorestframework-simplejwt (JWT)
- Django Channels (websocket)
- drf-yasg (Swagger / ReDoc)

1. Клонировать репозиторий:
   git clone https://github.com/Aziz-37/CoffeeShopDjango.git
   cd CoffeeShopDjango

2. Создать виртуальное окружение (рекомендуется):
   python -m venv .venv
   # Активировать:
   # Windows:
   .\.venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate

3. Установить зависимости:
   pip install -r requirements.txt

4. Настроить базу (PostgreSQL):
   - Открыть CoffeeShop/settings.py
   - В секции DATABASES указать название БД, пользователя, пароль.
   Например:
       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.postgresql',
               'NAME': 'coffee_db',
               'USER': 'postgres',
               'PASSWORD': 'aziz123',
               'HOST': 'localhost',
               'PORT': '5432',
           }
       }
   - Создать базу coffee_db в PostgreSQL (через pgAdmin или psql).

5. Применить миграции:
   python manage.py migrate

6. Создать суперпользователя:
   python manage.py createsuperuser

7. Запустить сервер:
   python manage.py runserver
   # или (если нужен чат через Channels):
   # pip install daphne
   # daphne CoffeeShop.asgi:application

8. Открыть в браузере:
   http://127.0.0.1:8000/admin/  (админка)
   http://127.0.0.1:8000/swagger/
   http://127.0.0.1:8000/redoc/

ER Диаграмма (структура БД)
 ┌─────────────────────────┐      ┌─────────────────────────┐
 │       Category          │      │        Product          │
 │─────────────────────────│      │─────────────────────────│
 │ id (PK)                │1    *│ id (PK)                 │
 │ name                   ├──────┤ name                     │
 │ description            │      │ description              │
 └─────────────────────────┘      │ price                   │
                                  │ category_id (FK→Category)
                                  └─────────────────────────┘

 ┌─────────────────────────┐      ┌─────────────────────────┐
 │       CustomUser        │      │        CartItem         │
 │─────────────────────────│      │─────────────────────────│
 │ id (PK)                 │      │ id (PK)                 │
 │ username                │      │ user_id (FK→CustomUser) │
 │ email                   │1    *│ product_id (FK→Product) │
 │ password                ├──────┤ quantity                │
 │ role (user/admin)       │      └─────────────────────────┘
 │ is_verified (bool)      │
 └─────────────────────────┘

 ┌─────────────────────────┐      ┌─────────────────────────┐
 │         Order           │      │      OrderItem          │
 │─────────────────────────│      │─────────────────────────│
 │ id (PK)                 │      │ id (PK)                 │
 │ user_id (FK→CustomUser) │1    *│ order_id (FK→Order)     │
 │ created_at              ├──────┤ product_id (FK→Product) │
 │ total_price             │      │ quantity                │
 │ status                  │      │ price                   │
 └─────────────────────────┘      └─────────────────────────┘
Краткое описание
CustomUser: расширенная модель пользователя (роль, верификация).
Category ↔ Product: связь 1 ко многим (одна категория, много товаров).
CartItem: связь user ↔ product, хранит quantity.
Order: ссылка на user, хранит дату, сумму, статус.
OrderItem: внутри заказа, указывает какой товар и сколько штук.

JWT Аутентификация
POST /api/token/
  {
    "username": "...",
    "password": "..."
  }
# Ответ содержит "access" и "refresh" поля.

POST /api/token/refresh/
  {
    "refresh": "<refresh_token>"
  }
# Выдаёт новый "access".
Authorization: Bearer <access_token>

Пример эндпоинтов

1. /api/products/         # GET: список продуктов, POST: добавить продукт (admin)
2. /api/products/{id}/    # GET, PUT, PATCH, DELETE
3. /api/categories/       # CRUD аналогично
4. /api/cart/             # GET: корзина, POST: добавить товар
5. /api/cart/{id}/        # DELETE: удалить из корзины
6. /api/orders/           # GET (admin видит все, user видит свои), POST: создать заказ
7. /api/orders/{id}/      # GET, PATCH, DELETE
8. /api/token/            # Получить JWT-токен
9. /api/token/refresh/    # Обновить токен
Также можно ознакомиться с полным списком в:
/swagger/ (Swagger UI) или /redoc/ (ReDoc)

WebSocket-чат поддержки
Реализован с помощью Django Channels:
ws://127.0.0.1:8000/ws/support/

Можно протестировать через любой WebSocket клиент.


Очистка не верифицированных пользователей

В users/management/commands/delete_unverified_users.py объявлена функция:
  handle
которая удаляет пользователей, не подтвердивших регистрацию в течение 2 дней.
