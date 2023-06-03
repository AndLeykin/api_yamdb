### Описание проекта:

API для сервиса отзывов и рейтингов произведений YamDB.
Написано на Python 3.9 с использованием фреймворков Django 3.2.16, Django Rest Framework 3.12.4.

### Авторы проекта:

Ирина Димаева, python backend разработчик.
Алексей Вишняков, python backend разработчик.
Андрей Лейкин, python backend разработчик.

### Установка и запуск:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AndLeykin/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
cd api_yamdb
```

```
python3 manage.py migrate
```

Создать суперпользователя:

```
python3 manage.py createsuperuser
```

Заполнить базу данных из csv-файлов:

```
python3 manage.py fill db
```
Опции заполнения:
```
--category
--genre
--user
--title
--genre_title
--review
```

Запустить проект:

```
python3 manage.py runserver
```

Зайти на страницу администратора:

```
http://127.0.0.1:8000/admin/
```

API-документация в формате redoc:

```
http://127.0.0.1:8000/redoc/
```

### Примеры запросов к API:

Получить код подтверждения:
```
POST http://127.0.0.1:8000/api/v1/auth/token/
```
Получение JWT-токена:
```
POST http://127.0.0.1:8000/api/v1/posts/
{
    "username": "string",
    "confirmation_code": "string"
}
```

Операции с категориями:
```
GET http://127.0.0.1:8000/api/v1/categories/
```
```
POST http://127.0.0.1:8000/api/v1/categories/
{
    "name": "string",
    "slug": "string"
}
```
```
DELETE http://127.0.0.1:8000/api/v1/categories/{slug}/
```

Операции с жанрами:
```
GET http://127.0.0.1:8000/api/v1/genres/
```
```
POST http://127.0.0.1:8000/api/v1/genres/
{
    "name": "string",
    "slug": "string"
}
```
```
DELETE http://127.0.0.1:8000/api/v1/genres/{slug}/
```

Операции с произведениями:
```
GET http://127.0.0.1:8000/api/v1/titles/
```
```
POST http://127.0.0.1:8000/api/v1/titles/
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```
```
PATCH http://127.0.0.1:8000/api/v1/titles/{titles_id}/
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```
```
DELETE http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

Операции с отзывами:
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
{
    "text": "string",
    "score": 1
}
```
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```
```
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
{
    "text": "string",
    "score": 1
}
```
```
DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

Операции с комментариями:
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
{
    "text": "string"
}
```
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
```
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
{
    "text": "string"
}
```
```
DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
Операции с пользователями:
```
GET http://127.0.0.1:8000/api/v1/users/
```
```
POST http://127.0.0.1:8000/api/v1/users/
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
```
GET http://127.0.0.1:8000/api/v1/users/{username}/
```
```
PATCH http://127.0.0.1:8000/api/v1/users/{username}/
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
```
DELETE http://127.0.0.1:8000/api/v1/users/{username}/
```
```
GET http://127.0.0.1:8000/api/v1/users/me/
```
```
PATCH http://127.0.0.1:8000/api/v1/users/me/
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string"
}
```