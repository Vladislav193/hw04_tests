# hw04_tests

[![CI](https://github.com/yandex-praktikum/hw04_tests/actions/workflows/python-app.yml/badge.svg?branch=master)](https://github.com/yandex-praktikum/hw04_tests/actions/workflows/python-app.yml)

Проект предназначен для тестирования сайта Yatube.

Технологии:

Django 2.2.19

Как запустить проект: 
Клонировать репозиторий и перейти в него в командной строке:

git clone <> 

Cоздать и активировать виртуальное окружение:

python3 -m venv env source env/bin/activate 

Установить зависимости из файла requirements.txt:

python3 -m pip install --upgrade pip pip install -r requirements.txt

Выполнить миграции:

python3 manage.py migrate 

Запустить pytest 
