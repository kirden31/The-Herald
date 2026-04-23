![CI](https://github.com/kirden31/The-Herald/actions/workflows/ci.yml/badge.svg)
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.2-green)](https://www.django.org/)

# Новостной
![📰](herald/static_dev/img/fav/favicon-96x96.png)

**Новостной** — современный веб-агрегатор новостей, собирающий информацию из различных авторитетных источников по всему миру. Платформа предоставляет удобный поиск, персонализацию контента и безопасное хранение данных пользователей.

## 🌟 Ключевые особенности

- **🔍 Умный поиск** — поиск новостей по ключевым словам, категориям, дате и источнику
- **🌐 Мульти-источники** — интеграция с NewsAPI и The Guardian
- **🎯 Персонализация** — избранные категории, сохранение статей
- **🔒 Безопасность** — защита пользовательских данных, кастомная аутентификация
- **📱 Адаптивный дизайн** — современный интерфейс на Bootstrap 5
- **🌍 Мультиязычность** — поддержка интернационализации (i18n)

## 📋 Содержание

- [Быстрый старт](#-быстрый-старт)
- [Настройка](#-настройка)
- [Использование](#-использование)
- [API интеграции](#-api-интеграции)
- [Разработка](#-разработка)

## 🚀 Быстрый старт

### Необходимое ПО
- **Python 3.10-3.12** — [скачать](https://www.python.org/)
- **Git** — [скачать](https://git-scm.com/downloads)
- **Gettext** (для переводов) — [скачать](https://www.gnu.org/software/gettext/)

### Установка за 5 минут

```bash
# 1. Клонирование репозитория
git clone https://github.com/kirden31/The-Herald.git
cd The-Herald

# 2. Устанавливаем пакеты python
sudo apt install -y python3 python3-venv python3-pip build-essential gettext

# 3. Создание виртуального окружения
python3 -m venv .venv

# 4. Активация окружения
source .venv/bin/activate

# Запуск в PROD режиме

# 5. Установка зависимостей
pip install -r requirements/prod.txt

# 6. Настройка переменных окружения
# !!! ОБЯЗАТЕЛЬНО ЗАПОЛНИТЕ ПУСТЫЕ ПОЛЯ
cp template.env .env

cd herald
# 7. Применение миграций
python manage.py migrate
# 7.1. Компиляция статики
python manage.py collectstatic
# 7.2. Применение локализации
django-admin compilemessages

# 8. Создание суперпользователя
python manage.py createsuperuser

# 9. Тестовый запуск
python manage.py runserver 127.0.0.1:8000
```

Откройте браузер и перейдите по адресу: **http://127.0.0.1:8000/**

## ⚙️ Настройка

### Конфигурация .env файла

Создайте файл `.env` на основе `template.env`:

```env
# Базовые настройки Django для DEV режима
DJANGO_SECRET_KEY=not_so_secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*

# Кол-во попыток входа перед блокировкой
DJANGO_MAX_AUTH_ATTEMPTS=5

# Email отправителя
DEFAULT_FROM_EMAIL=<noreply@newshub.ru>

NEWS_API_KEYS=<ВАШИ API КЛЮЧИ С NewsAPI>
GUARDIAN_API_KEYS=<ВАШИ API КЛЮЧИ С The Guardian>
```
**Важно:** 
В `DJANGO_ALLOWED_HOSTS`, `NEWS_API_KEYS` и `GUARDIAN_API_KEYS` указывайте значения через _пробел_, **без запятых**!

### Настройки для разработки

`DEBUG` - необходимо поставить True

```bash
# Установка зависимостей для разработки
pip install -r requirements/dev.txt
```

### Команды разработки
- За подробностями обращайтесь к документации [Django](https://docs.djangoproject.com/en/6.0/)

```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск тестов
python manage.py test

# Сбор статических файлов
python manage.py collectstatic

# Создание дампа базы данных
python manage.py dumpdata <ПРИЛОЖЕНИЕ> > <ПУТЬ СОЗДАНИЯ>

# Загрузка тестовых данных
python manage.py loaddata fixtures/data.json
```

### Настройка переводов

```bash
# Создание файлов перевода
django-admin makemessages -l <КОД ЯЗЫКА>

# Редактирование файлов перевода
# Отредактируйте locale/<КОД ЯЗЫКА>/LC_MESSAGES/django.po

# Компиляция переводов
django-admin compilemessages
```

## 🎯 Использование

### Основные функции

1. **Главная страница**
   - Топ новости дня
   - Быстрый поиск
   - Фильтрация по категориям

2. **Поиск новостей**
   - Расширенная фильтрация
   - Сортировка по релевантности/дате/популярности

3. **Личный кабинет**
   - Управление профилем
   - Избранные новости
   - Любимые категории

4. **Избранное**
   - Сохранение понравившихся статей
   - Организация по категориям
   - Быстрый доступ к сохраненному

### API ключи

Для полноценной работы проекта необходимы API ключи:

1. **NewsAPI** — [получить ключ](https://newsapi.org/register)
2. **The Guardian** — [получить ключ](https://open-platform.theguardian.com/access/)

## 🔌 API интеграции

Проект поддерживает следующие API:

| API              | Назначение                                      |
|------------------|-------------------------------------------------|
| **NewsAPI**      | Основной поиск новостей, топ новости, источники |
| **The Guardian** | Поиск новостей с The Guardian                   |

---

**Следите за обновлениями ^w^**
