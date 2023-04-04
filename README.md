# praktikum_new_diplom

![example workflow](https://github.com/MaksimovVS/foodgram-project-react/actions/workflows/main.yml/badge.svg)
[Ссылка на сайт](http://51.250.98.43/)
[Админка](http://51.250.98.43/admin/) login: admin password: admin

## API для получения информации и обсуждения наиболее интересных произведений
### Стэк технологий:

    Python
    Django
    Django Rest Framework
    Postgres
    Docker
    Nginx

### Документация и возможности API:

К проекту подключен redoc. Для просмотра документации используйте эндпойнт redoc/

### Быстрый старт:

Склонируйте репозитрий на свой компьютер
Создайте .env файл в директории infra/, в котором должны содержаться следующие переменные:

```bash
DEBUG=0
DJANGO_SECRET_KEY=sefmioesjf89234uj3q2irnwjuifhwurwfknmsjefneushes
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
ALLOWED_HOST=127.0.0.1
```


Из папки infra/ соберите образ при помощи docker-compose 
```bash
sudo docker-compose up -d --build
```
Примените миграции
```bash
sudo docker exec back python manage.py migrate
```
Соберите статику
```bash
sudo docker exec back python manage.py collectstatic --no-input
```
Для доступа к админке создайте суперюзера 
```bash
sudo docker exec web python manage.py createsuperuser
```

### python developer:
[Vladimir Maksimov](https://github.com/MaksimovVS)
