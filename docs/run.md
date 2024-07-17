# Инструкция по запуску приложения

## Настройка базы данных

Поставить PostgreSQL, запустить сервер, открыть SQL Shell и прописать следующие команды для создания базы данных и пользователя с правами суперюзера:

```shell
CREATE DATABASE your_db_name;
CREATE USER your_db_user WITH PASSWORD 'your_password';
ALTER ROLE your_db_user WITH SUPERUSER;
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
```

Альтернативно: через GUI в pgAdmin 4 создать базу данных, пользователя и дать ему привелегию суперюзера.

## Настройка переменных среды через .env файл

В скачанном проекте в папке em_project необходимо добавить .env файл для хранения переменных окружения для настройки базы данных и SECRET_KEY Django проекта (задавать по аналогии: КЛЮЧ="значение"):

```shell
SECRET_KEY="Ключ Django проекта"
NAME="Название базы данных"
USER="Имя пользователя БД"
PASSWORD="Пароль"
HOST="Хост"
PORT="Порт"
```

## Установить зависимости (2 варианта)

- Установка зависимостей через [poetry](https://python-poetry.org/)

  ```shell
  poetry install
  poetry shell
  ```

- Установка зависимостей через pip:

  ```shell
  python -m venv venv
  venv\Scripts\activate
  pip install requirements.txt
  ```

## Заполнить базу данных тестовым набором данных
  
```shell
python manage.py populate_db
```

## Запустить проект на тестовом сервере

```shell
cd em_project
python manage.py server
```
