markdown
# Dating API

API платформы для знакомств на Django REST Framework.

## Возможности

- Регистрация и JWT-авторизация
- Профиль пользователя (ФИО, пол, возраст, город, увлечения, статус, приватность)
- Галерея фото с главным фото
- Лайки и дизлайки
- История просмотров профилей
- Приглашения на свидание
- Swagger-документация

## Установка

1. Клонировать репозиторий:
   git clone https://github.com/AnyaDlove/dating.app.git
   cd dating.app

2. Установить зависимости:
   pip install -r requirements.txt

3. Применить миграции:
   python manage.py migrate

4. Создать суперпользователя:
   python manage.py createsuperuser

5. Запустить сервер:
   python manage.py runserver

## Эндпоинты

- /admin/ — админка Django
- /api/docs/ — Swagger UI
- /api/register/ — регистрация
- /api/token/ — получение JWT-токена
- /api/me/ — свой профиль
- /api/users/ — список пользователей
- /api/photos/ — фото
- /api/likes/ — лайки
- /api/views/ — история просмотров
- /api/invitations/ — приглашения

## Технологии

- Python 3.14
- Django 6.1
- Django REST Framework
- Simple JWT
- drf-spectacular (Swagger)
- Pillow