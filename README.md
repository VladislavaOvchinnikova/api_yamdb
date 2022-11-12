### API_YaMDB
#### Проект YaMDb собирает отзывы пользователей на произведения. 
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

- [x] Позволяет делать запросы к моделям проекта: категории, жанры, произведения, отзывы и комментарии.

- [x] Поддерживает методы GET, POST, PATCH, DELETE.

- [x] Предоставляет данные в формате JSON.

#### Технологии
- Python 3.7
- Django==2.2.16
- djangorestframework==3.12.4
- djangorestframework-simplejwt==21.1

#### Как запустить проект
Клонировать репозиторий и перейти в него в командной строке:

```git clone https://github.com/VladislavaOvchinnikova/api_yamdb.git```

```cd api_yamdb```

Cоздать и активировать виртуальное окружение:

```python -m venv venv```

```source venv/Scripts/activate```

Установить зависимости из файла requirements.txt:

```python -m pip install --upgrade pip```

```pip install -r requirements.txt```

Выполнить миграции:

```python manage.py migrate```

Запустить проект:

```python manage.py runserver```

#### Примеры запросов

##### AUTH

```api/v1/auth/signup/``` (POST) - регистрация нового пользователя.

```api/v1/auth/token/``` (POST) - получение JWT-токена.

##### CATEGORIES

```api/v1/categories/``` (GET, POST) - получить список всех категорий или создать категорию.

```api/v1/categories/{slug}/``` (DELETE) - удалить категорию.

##### GENRES

```api/v1/genres/``` (GET, POST) - получить список всех жанров или создать жанр.

```api/v1/genres/{slug}/``` (DELETE) - удалить жанр.

##### TITLES

```api/v1/titles/``` (GET, POST) - получить список всех произведений или добавить новое произведение.

```api/v1/titles/{titles_id}/``` (GET, PATCH, DELETE) - получить, обновить или удалить информацию о произведении.

##### REVIEWS

```api/v1/titles/{titles_id}/reviews/``` (GET, POST) - получить список всех отзывов или оставить новый отзыв.

```api/v1/titles/{titles_id}/reviews/{review_id}/``` (GET, PATCH, DELETE) - получить, обновить или удалить отзыв об указанном произведении.

##### COMMENTS

```api/v1/titles/{title_id}/reviews/{review_id}/comments/``` (GET, POST) - получить список всех комментариев к отзыву или добавить новый комментарий для отзыва.

```api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/``` (GET, PATCH, DELETE) - получить, обновить или удалить комментарий к отзыву.

##### USERS

```api/v1/users/``` (GET, POST) - получить список всех пользователей или добавить нового пользователя.

```api/v1/users/{username}/``` (GET, PATCH, DELETE) - получить, обновить или удалить данные о конкретном пользователе.

```api/v1/users/me/``` (GET, PATCH) - получить или обновить данные своей учетной записи.
