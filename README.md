# Selfpub API

An API for Selfpub project that allow you to publics your books (allegedly).


## Populate the database


```
docker-compose run --rm api python manage.py generate_books
```


## Auth

Get token

```
POST api/v1/api-token-auth/
```

Body

```
{
    "username": "<email>",
    "password": "<password>",
}
```


## Main entites

[Authors](#authors)

[Genres](#genres)

[Books](#books)

[Comments](#comments)

## Authors

#### Methods
For authenticated users:
* GET


### List

```
GET api/authors/
```

### Response

```
{
    "count": 1001,
    "next": "http://0.0.0.0:8000/api/authors/?limit=100&offset=100",
    "previous": null,
    "results": [
        {
            "id": "7b19e560-1e80-4ebf-a208-c67a8ced6ed2",
            "full_name": "Самира Литвинова",
            "birth_year": 1969,
            "email": "caribbean1839@yandex.com",
            "books_count": 5,
            "genres": [
                "справочники"
            ]
        },
        {
            "id": "012dfb4a-848a-4097-b7e9-e3e52996806b",
            "full_name": "Марианна Поликарпова",
            "birth_year": 1994,
            "email": "pond2075@yahoo.com",
            "books_count": 5,
            "genres": [
                "искусство"
            ]
        },
        ...
    ]
}
```

### Single

#### Methods
For `id` owner:
* PUT
* PATCH
* DELETE

```
GET api/authors/<uuid:id>
```

### Response

```
{
    "id": "50e65218-232e-4587-973c-15626e20b964",
    "full_name": "Клара Анисимова",
    "birth_year": 2004,
    "email": "viewer2024@outlook.com",
    "books_count": 5,
    "genres": [
        "психология"
    ]
}
```

### PUT body

```
{
    "full_name": string
    "birth_year": integer
    "email": string
}
```

## Genres

#### Methods
For authenticated users:
* GET

### List

```
GET api/genres/
```

### Response

```
{
    "count": 14,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "6613c493-c52c-4fc6-9d52-49830ba097f7",
            "name": "поэзия",
            "books_count": 365
        },
        {
            "id": "2b46e43c-8dad-4d9d-9471-523785245acd",
            "name": "искусство",
            "books_count": 295
        },
        {
            "id": "56397737-ac6c-4330-8dc1-976d1c6d4d31",
            "name": "бизнес",
            "books_count": 391
        },
        ...
    ]
}
```

## Books

#### Methods
For authenticated users:
* GET
* POST

### List

```
GET api/books/
```

### Response

```
{
    "count": 5001,
    "next": "http://0.0.0.0:8000/api/books/?limit=100&offset=100",
    "previous": null,
    "results": [
        {
            "id": "4355fe12-7cf1-403f-9c1a-558798731bf2",
            "title": "Прекращай это!",
            "author": {
                "id": "7b19e560-1e80-4ebf-a208-c67a8ced6ed2",
                "full_name": "Самира Литвинова"
            },
            "year": 2012,
            "genre": "справочники",
            "pub_date": "2021-12-26T18:32:42.731483Z"
        },
        {
            "id": "7a61143d-37ac-4a50-b0a0-ef50da303951",
            "title": "Арестуйте обычных подозреваемых",
            "author": {
                "id": "3acb46a8-6fbc-4543-9cf5-47cf4f55b0b0",
                "full_name": "Авксентий Комиссаров"
            },
            "year": 2049,
            "genre": "нон-фикшен",
            "pub_date": "2021-12-26T18:32:42.731714Z"
        },
        ...
    ]
}
```

### Single

#### Methods
For authenticated users:
* GET

For `id` owner:
* PUT
* PATCH
* DELETE

```
GET api/books/<uuid:id>
```

### Response

```
{
    "id": "c4acecd7-4236-4222-8a13-03625a337e24",
    "title": "Я — король мира!",
    "author": {
        "id": "3acb46a8-6fbc-4543-9cf5-47cf4f55b0b0",
        "full_name": "Авксентий Комиссаров"
    },
    "year": 2010,
    "genre": "нон-фикшен",
    "pub_date": "2021-12-26T18:32:42.731808Z"
}
```

### POST, PUT body

```
{
    "title": string
    "year": integer
    "genre": string
}
```

## Comments

#### Methods
For authenticated users:
* GET
* POST


### List

```
GET api/books/<uuid:id>/comments/
```

### Response

```
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "8f3bde48-4748-4217-8b20-30fc0654e295",
            "author": {
                "id": "1b046077-0462-49ea-8c24-679594068d54",
                "full_name": "Руслана Маркелова"
            },
            "text": "Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение.",
            "created": "2021-12-26T18:32:42.915411Z"
        },
        {
            "id": "0e5ed38a-8711-4636-8ecf-4eb021b7995f",
            "author": {
                "id": "8de31d7b-0f6e-44d3-9aaf-d10205972853",
                "full_name": "Макар Полуяхтов"
            },
            "text": "Разработан и поддерживается компанией Ericsson.",
            "created": "2021-12-26T18:32:42.915433Z"
        },

```

### Single

#### Methods
For authenticated users:
* GET

For `id` owner:
* PUT
* PATCH
* DELETE

```
GET api/books/<uuid:id>/comments/<uuid:id>/
```

### Response

```
{
    "id": "88b569a9-1351-409e-a69d-8e0dda8e49e2",
    "author": {
        "id": "3115ff72-af56-4f9a-a2b7-3385cf05c7f7",
        "full_name": "Панкратий Бобров"
    },
    "text": "REPL — форма организации простой интерактивной среды программирования в рамках средств интерфейса командной строки.",
    "created": "2021-12-26T18:32:42.915477Z"
}
```

### POST, PUT body

```
{
    "text": string
}
```

## Caveats
1. Now the API doesn't allow users registration and password resetting (as time was running out 😬).
2. Some parts may not be consistent with the idiomatic Django solutions (as I haven't used this framework for a long time) and could be improves after more diligent documentation reading.