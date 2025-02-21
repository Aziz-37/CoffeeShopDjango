CoffeeShop Django
Описание
CoffeeShop — это тестовое приложение (REST API) для управления пользователями, товарами (продуктами), корзиной и заказами в сети кофеен. Пользователи могут просматривать каталог товаров, добавлять их в корзину и оформлять заказы, а администратор управляет всеми сущностями и получает уведомления.

Технологический стек:

Django 5.1 + Django REST Framework
PostgreSQL (реляционная база данных)
JWT (через djangorestframework-simplejwt)
Django Channels (для WebSocket-чата поддержки)
drf-yasg (Swagger / ReDoc документация)
Функциональность
Управление пользователями:

Регистрация нового пользователя.
Авторизация и получение/обновление токенов (JWT).
Роли: user, admin.
Очистка не верифицированных пользователей (через management command или Celery — по желанию).
Каталог:

Категории (Category): создание, просмотр, редактирование, удаление (доступно админам).
Товары (Product): CRUD-операции, сортировка, фильтр, поиск.
Корзина (Cart):

Добавление товара в корзину (POST).
Просмотр корзины (GET).
Удаление одного товара или очистка всей корзины (DELETE).
Заказы (Orders):

Создание заказа, просмотр списка (для админа — всех, для пользователя — только своих).
Уведомление по email (опционально).
WebSocket-чат (Support Chat):

Django Channels для реализации онлайн-чата поддержки.
Документация:

Swagger: /swagger/
ReDoc: /redoc/
Безопасность:

JWT (Bearer Token) — аутентификация.
Django ORM (защита от SQL injection).
Встроенный CSRF (для админки и Cookie-based запросов).
Запуск и установка
1. Клонирование проекта
bash
Copy
Edit
git clone https://github.com/Aziz-37/CoffeeShopDjango.git
cd CoffeeShopDjango
2. Виртуальное окружение (рекомендуется)
bash
Copy
Edit
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# или
.\.venv\Scripts\activate   # Windows
3. Установка зависимостей
bash
Copy
Edit
pip install -r requirements.txt
Убедитесь, что у вас установлен драйвер для PostgreSQL (например, psycopg2-binary).

4. Настройка базы данных
В файле CoffeeShop/settings.py в блоке DATABASES пропишите доступ к вашей PostgreSQL-базе:

python
Copy
Edit
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
Создайте базу coffee_db (через pgAdmin или psql):

sql
Copy
Edit
CREATE DATABASE coffee_db;
5. Применить миграции
bash
Copy
Edit
python manage.py migrate
6. Создать суперпользователя (админ)
bash
Copy
Edit
python manage.py createsuperuser
7. Запуск сервера
bash
Copy
Edit
python manage.py runserver
Откройте в браузере http://127.0.0.1:8000/admin/ чтобы зайти в админку Django.

8. (Опционально) Запуск с WebSockets (Channels)
Если вы хотите использовать WebSocket-чат:

bash
Copy
Edit
# Установите daphne (или uvicorn):
pip install daphne

# Запуск:
daphne CoffeeShop.asgi:application

# Теперь сервер слушает на 127.0.0.1:8000 и WebSocket-доступен на ws://127.0.0.1:8000/ws/support/
Маршруты (Основные эндпоинты)
Admin: http://127.0.0.1:8000/admin/ (Django админка)
Swagger: http://127.0.0.1:8000/swagger/
ReDoc: http://127.0.0.1:8000/redoc/
Auth (JWT)
POST /api/token/ — получить access и refresh токены.
json
Copy
Edit
{
  "username": "admin",
  "password": "admin123"
}
POST /api/token/refresh/ — обновить access, передав refresh.
Products & Categories
GET /api/products/ — список продуктов (фильтры, поиск, сортировка при желании).
POST /api/products/ — создать продукт (admin).
GET /api/categories/ — список категорий.
POST /api/categories/ — создать категорию (admin).
и т.д. (обычный ModelViewSet CRUD).
Cart
GET /api/cart/ — получить товары в корзине текущего пользователя.
POST /api/cart/ — добавить товар в корзину.
DELETE /api/cart/{id}/ — удалить позицию из корзины.
DELETE /api/cart/ — очистить корзину.
Orders
GET /api/orders/ — список заказов.
Админ видит все, пользователь — только свои.
POST /api/orders/ — создать заказ из своей корзины.
GET /api/orders/{id}/ — детали заказа.
PATCH/PUT/DELETE /api/orders/{id}/ — обновлять/удалять заказ (в зависимости от логики).
WebSocket Chat
ws://127.0.0.1:8000/ws/support/ — WebSocket-чат с поддержкой.
ER Диаграмма
Ниже условный пример (вставьте свою схему).

users_customuser: хранит пользователей, поля (id, username, email, role, is_verified...).
products_category, products_product: категории и товары (FK category -> product).
cart_cartitem: связь пользователь → товар (многие ко многим, через отдельную модель).
orders_order, orders_orderitem: заказ и позиции заказа.
Очистка не верифицированных пользователей
(Опционально) в users/management/commands/cleanup_unverified.py:

python
Copy
Edit
import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Удаляет не верифицированных пользователей старше 2 дней'

    def handle(self, *args, **options):
        cutoff = timezone.now() - datetime.timedelta(days=2)
        qs = CustomUser.objects.filter(is_verified=False, date_joined__lt=cutoff)
        count, _ = qs.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} unverified users"))
Запуск:

bash
Copy
Edit
python manage.py cleanup_unverified
Тесты
(Опционально) для каждого приложения можно сделать tests.py, например:

python
Copy
Edit
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='test', password='test123')

    def test_get_products_list(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        # ...
Дополнительно
Авторизация по JWT: при запросах к защищённым эндпоинтам (POST /api/products/ и т.п.) нужно передавать заголовок:
makefile
Copy
Edit
Authorization: Bearer <access_token>
Фильтры и поиск: Для примера /api/products/?search=latte&ordering=-price
Роль: можно хранить в поле CustomUser.role (user, admin), и проверять в вьюхах или через кастомные permissions.
