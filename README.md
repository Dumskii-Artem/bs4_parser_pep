# Парсинга pep.
# Проект 19 спринта Яндекс Практикума. Python 

## Автор проекта
[Думский Артём](https://github.com/Dumskii-Artem) в рамках обучения
на Яндекс.Практикум по программе Python-разработчик расширенный (когорта 57+)


## Использованные технологии

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)


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
  -c, --clear-cache     Очистка кеша
  -p, --pretty          Вывод в формате PrettyTable
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```

## Запуск тестов
```
pytest
```

