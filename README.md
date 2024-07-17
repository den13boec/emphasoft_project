# Приложение для бронирования комнат в отеле

Тестовое задание для компании Emphasoft - API на Django Rest Framework в связке с базой данных PostgreSQL.

## Реализованные требования

- Пользователи могут фильтровать и сортировать комнаты по цене, по количеству мест.
- Пользователи могут искать свободные комнаты в заданном временном интервале.
- Пользователи могут забронировать свободную комнату.
- Суперюзер может добавлять/удалять/редактировать комнаты и редактировать записи о бронях через админ панель Django.
- Брони могут быть отменены как самим юзером, так и суперюзером.
- Пользователи могут регистрироваться и авторизовываться.
- Чтобы забронировать комнату пользователи должны быть авторизованными. Просматривать комнаты можно без логина. Авторизованные пользователи могут посмотреть свои брони.

## Инструкция по запуску приложения

1. Поставить PostgreSQL, запустить сервер, открыть SQL Shell и прописать следующие команды для создания базы данных и пользователя с правами суперюзера:

   ```shell
   CREATE DATABASE your_db_name;
   CREATE USER your_db_user WITH PASSWORD 'your_password';
   ALTER ROLE your_db_user WITH SUPERUSER;
   GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
   ```

   Альтернативно: через GUI в pgAdmin 4 создать базу данных, пользователя и дать ему привелегию суперюзера.

2. В скачанном проекте в папке em_project необходимо добавить .env файл для хранения переменных окружения для настройки базы данных и SECRET_KEY Django проекта (задавать по аналогии: КЛЮЧ="значение"):

   ```shell
   SECRET_KEY="Ключ Django проекта"
   NAME="Название базы данных"
   USER="Имя пользователя БД"
   PASSWORD="Пароль"
   HOST="Хост"
   PORT="Порт"
   ```

3. Установить зависимости (2 варианта).

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

4. Заполнить базу данных тестовым набором данных
  
    ```shell
    python manage.py populate_db
    ```

5. Запустить проект на тестовом сервере

    ```shell
    cd em_project
    python manage.py server
    ```

## API Документация

https://den13boec.github.io/emphasoft_project/api/

> [!IMPORTANT]
> В описании методов API, везде где написано: `/auth/register/` имеется в виду `http://127.0.0.1:8000/api/auth/register/` и остальные URL по аналогии
