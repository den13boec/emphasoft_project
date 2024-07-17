# Сборка проекта

## Поставить PostgreSQL, запустить сервер, открыть SQL Shell и прописать следующие команды

   ```shell
   CREATE DATABASE your_db_name;
   CREATE USER your_db_user WITH PASSWORD 'your_password';
   ALTER ROLE your_db_user WITH SUPERUSER;
   GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
   ```

Альтернативно: в pgAdmin 4 создать пользователя и дать ему привелегию суперюзера.

## В скачанном проекте в папке em_project необходимо добавить .env файл с настройками базы данных (задавать по аналогии: КЛЮЧ="значение")

- Ключ для Django (SECRET_KEY)
- Название базы данных (NAME)
- Имя пользователя БД (USER)
- Пароль (PASSWORD)
- Хост (HOST)
- Порт (PORT)

## Настроить зависимости

- Если вы используете менеджер версий python - [pyenv](https://github.com/pyenv/pyenv) или [pyenv-windows](https://github.com/pyenv-win/pyenv-win)

  ```shell
  pyenv local 3.11.3 # >= 3.11.x    
  ```

  - Установка зависимостей:

    ```shell
    python -m venv .venv
    source .venv/bin/activate
    ```

- Установка зависимостей пакетным менеджером [poetry](https://python-poetry.org/)

  ```shell
  poetry install
  ```

  - Установка зависимостей pip:

    ```shell
    pip install requirements.txt
    ```

  - Запуск проекта:

    ```shell
    cd em_project
    python manage.py server
    ```

- Опциональная генерация записей в базу данных
  
  ```shell
  python manage.py populate_db
  ```
