# YaCut

## Описание

Проект, который позволяет укоротить любую нужную вам ссылку.
Ссылки станут не только короче, вы можете украсить их своим уникальным индентификатором,
если его никто не занял :).

Сокращатель ссылок - банально. В документации будем называть его укротитель.

"Укротитель" поддерживает не только пользовательский интерфейс браузера, но и работу с API,
по одноименному эндпоинту /api/  

### Функции "укротителя":

-   Укорачивает ссылку при помощи уникального идентификатора;
-   Если пользователь не желает украшать ссылку - проект сгенерирует ее самостоятельно;

## Применяемые технологии:

[![Python](https://img.shields.io/badge/Python-3.9-blue?style=flat-square&logo=Python&logoColor=3776AB&labelColor=d0d0d0)](https://www.python.org/)
[![FLask](https://img.shields.io/badge/Flask-2.0.2-blue?style=flat-square&labelColor=d0d0d0)](https://flask.palletsprojects.com/en/3.0.x/)

### Порядок действия для запуска "укротителя":

Клонировать репозиторий и перейти в папку в проектом:

```bash
git clone git@github.com:AlexandrVasilchuk/yacut.git
```

```bash
cd yacut
```

Создать и активировать виртуальное окружение:

```bash
python3 -m venv venv
```

-   Если у вас Linux/MacOS

    ```bash
    source venv/bin/activate
    ```

-   Если у вас windows

    ```bash
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

## Работа с "укротителя":

Запустить базу данных для "укротителя":

```bash
flask db init
```

Запустить "укротителя":

```bash
flask run
```

Перейти по ссылке: 

### Краткая документация по работе с API:

#### Как создать новую короткую ссылку?

    POST api/id/: 

    {
      "url": "string",
      "custom_id": "not_required_field" 
    }


    RESPONSE:

    {
      "url": "string",
      "short_link": "string"
    }

#### Как получить оригинальную ссылку по short_id?

    GET api/id//

    RESPONSE:

    {
      "url": "string"
    }

## Контакты

* * *

Автор:
[Васильчук Александр](https://github.com/AlexandrVasilchuk/)

#### Контакты:

![Gmail-badge](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)\
alexandrvsko@gmail.com\
![Telegram-badge](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)\
@vsko_ico