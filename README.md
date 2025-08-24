# Парсинга pep.
# Проект 19 спринта Яндекс Практикума. Python 

## Цель проекта

Автоматический парсинг документации Python (разделы What's New, PEP, список версий, страницы загрузки).

Сбор и структурирование информации для последующего анализа или сохранения.


## Автор проекта
[Думский Артём](https://github.com/Dumskii-Artem) в рамках обучения
на Яндекс.Практикум по программе Python-разработчик расширенный (когорта 57+)


## Технологический стек

### Язык и окружение

Python 3.x – основной язык разработки.

venv (или другое виртуальное окружение) – изоляция зависимостей.

### Библиотеки и инструменты

**requests + requests-cache** – HTTP-запросы и кеширование, чтобы уменьшить нагрузку и ускорить повторные запросы.

**BeautifulSoup4 (bs4) + lxml** – парсинг HTML-страниц и удобная навигация по DOM.

**tqdm** – прогресс-бары для отображения состояния парсинга.

**logging** – встроенный модуль логирования для фиксации ошибок и важных событий.

### Функциональные утилиты

Кастомные функции: fetch_soup(), find_tag(), get_response() – обёртки для загрузки и парсинга страниц.

Обработка ошибок сети с логированием недоступных или некорректных ссылок.

Поддержка параметров командной строки для вывода данных в файл или в консоль.

### Тестирование

**pytest** – модульное и интеграционное тестирование (tests/test_main.py).


## Установка программы и запуск скрипта

Клонировать репозиторий:
```
git clone git@github.com:Dumskii-Artem/bs4_parser_pep.git
```

Перейти в папку с Backend:
```
cd bs4_parser_pep
```
Cоздать виртуальное окружение для backend:
```
Ubuntu: python3 -m venv env
Windows: py -3.9 -m venv env
```
Активировать виртуальное окружение:
```
Ubuntu: source env/bin/activate
Windows: source ./env/Scripts/activate
    или ./env/Scripts/activate
```
Вот так написать:
```
Ubuntu: python3 -m pip install --upgrade pip
Windows: python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Теперь можно запустить скрипт
```
Ubuntu: python3 manage.py src/main.py -h
Windows: python manage.py src/main.py -h
```
в результате вы увидите справку по использованию скрипта.
```
python3 src/main.py -h
usage: main.py [-h] [-c] [-p] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша программы и чтение данных с сайта
  -p, --pretty          Вывод в формате PrettyTable
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```
### Примеры запуска 

```
python3 src/main.py pep -p -o file
python3 src/main.py whats-new -p -o pretty
```

## Запуск тестов
```
pytest
```

