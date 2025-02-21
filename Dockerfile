# Используем официальный базовый образ Python
FROM python:3.11-slim

# Отключаем запись байткода и буферизацию вывода Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию контейнера
COPY . /app/

# Определяем команду запуска приложения
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "CoffeeShop.wsgi:application"]
