# Описание.

Проект YaMDb собирает отзывы пользователей на произведения. 
Проект api_yamdb это rest api приложение для взаимодействия с базой данных отзывов на произведения.

### Стек использованных технологий:

* Python
* Django
* Django REST framework

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Sergei-Ryabev/api_yamdb.git
```

```
cd api_yamdb/
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры.
Запросы отправляются на эндпойнты c префиксом ```/api/v1```  например:
```http://127.0.0.1:8000```**/api/v1**```/titles/?genre```

## Регистрация нового пользователя

*POST /auth/signup/*

Request samples:

    {
    "email": "user@example.com",
    "username": "^w\\Z"
    }

Response samples (200_OK):

    {
    "email": "string",
    "username": "string"
    }

## Получение JWT-токена

*POST/auth/token/*

Request samples:

    {
    "username": "^w\\Z",
    "confirmation_code": "string"
    }

Response samples (200_OK):

    {
    "token": "string"
    }

## Получение списка всех категорий

QUERY PARAMETERS:
**search** *(string)* - Поиск по названию категории

*GET/categories/*

Response samples(200_OK):

    {
      "count": 0,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "name": "string",
          "slug": "^-$"
        }
      ]
    }

## Получение списка всех произведений

*GET/titles/*

QUERY PARAMETERS:
**category** *(string)* -фильтрует по полю slug категории
**genre** *(string)* - фильтрует по полю slug жанра
**name** *(string)* - фильтрует по названию произведения
**year** *(integer)* - фильтрует по году

Response samples (200_OK):

    {
      "count": 0,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": 0,
          "name": "string",
          "year": 0,
          "rating": 0,
          "description": "string",
          "genre": [
            {
              "name": "string",
              "slug": "^-$"
            }
          ],
          "category": {
            "name": "string",
            "slug": "^-$"
          }
        }
      ]
    }
        

Остальные примеры запросов и ответов для всех эндпоинтов можно посмотреть с помощью ReDoc после запуска проекта:

```
http://127.0.0.1:8000/redoc/
```
### import_csv
Импорт объектов из файлов .csv в БД:
```
python manage.py import_csv Название_Модели путь_к_файлу.csv
```

Например:
```
python manage.py import_csv Category static/data/category.csv
```

### Авторы:

* Sergei-Ryabev - https://github.com/Sergei-Ryabev
* Ilya Nizhelskiy (CTaPuH4)  - https://github.com/CTaPuH4
