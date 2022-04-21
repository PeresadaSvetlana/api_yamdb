###**YaMDb** - База с отзывами и оценками пользователей на музыкальные произведения, книги и фильмы. Совместный проект двух студенток Яндекс.Практикума.


**Технологии**

Python 3.7 Django 2.2.16


**Как запустить проект:**

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:PeresadaSvetlana/api_yamdb.git
```

```
cd api_yamdb/
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

**Некоторые примеры запросов к API.**

http://127.0.0.1:8000/api/v1/auth/signup/

http://127.0.0.1:8000/api/v1/genres/

http://127.0.0.1:8000/api/v1/titles/{titles_id}/

http://127.0.0.1:8000/api/v1/users/{username}/
