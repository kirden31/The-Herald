# Новостной

[![pipeline status](https://gitlab.crja72.ru/django/2025/autumn/course/students/216206-yzavitova-course-1474/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2025/autumn/course/students/216206-yzavitova-course-1474/-/commits/main)

### Новостной - веб-ресурс для поиска новостей из разных источников со всего мира

## *Необходимое ПО и утилиты*
- #### [python 3.10-3.12](https://www.python.org/)
- #### [git](https://git-scm.com/downloads)
- #### [gettext](https://www.gnu.org/software/gettext/)

## Быстрый старт на Linux

### 1.
-  ### Создание/активация окружения
```bash
python3 -m venv venv
source venv/bin/activate
```
### 2.
-  ### Установка зависимостей для прода
```bash
pip install -r requirements/prod.txt
```
### 3.
-  ### Создание .env
```bash
cp template.env .env
```
### 4.
-  ### Переход в директорию herald
``` bash
cd herald
```
### 5.
-  ### Применение миграций
```bash
python3 manage.py migrate
```
### 6.
-  #### (*Опционально*) Создание/обновление переводов
```bash
django-admin makemessages -l >lang code<
```
-  ### Компиляция переводов
```bash
django-admin compilemessages
```
### 7.
-  #### (*Опционально*) Установка фикстур
```bash
python3 manage.py loaddata fixtures/data.json
```
### 8.
-  ### Создание суперпользователя
```bash
python3 manage.py createsuperuser
```
- Админка находится по адресу /admin
### 9.
-  ### Запуск сервера
```bash
python3 manage.py runserver
```
- Адрес по умолчанию http://127.0.0.1:8000/

### Если редактируете .env, то в DJANGO_ALLOWED_HOSTS пишите через пробел, без запятых