# This is project of admin panel travelling

## Schema database 

![alt text](schema.png)

---

**Стэк**:

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
[![SqlAlchemy](https://img.shields.io/badge/SqlAlchemy-%2307405e.svg?&style=for-the-badge&logo=SqlAlchemy&logoColor=white)](https://www.sqlalchemy.org/)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

---

## Как развернуть проект локально

Склонировать репозиторий:
```
git clone https://github.com/toth3m00n/admin-panel-travelling
```
Установить и активировать виртуальное окружение:
```
cd computer_club
python -m venv venv
source venv/bin/activate
(source venv/Scripts/activate - на Windows)
```
Установить необходимые зависимости:
```
pip install -r requirements.txt
```
Перейти в рабочую папку:
```
cd admin-panel-travelling
```

*Примечание:*
*Перед работой у вас должна быть создана база данных и файл .env*
*Пример файла `.env`:*
```
KEY=smth
DATABASE_URL=postgresql://[user[:password]@][netloc][:port][/dbname]
APP_SETTINGS=config.DevelopmentConfig
PASSWORD=your_db_password
```

Теперь можно запускать проект:
```
python manage.py runserver
```

Заполнить базу данных, если требуется. Данные для моего прилождения можно найти в [data for db](https://github.com/toth3m00n/admin-panel-travelling/blob/main/app/table/data_for_db.py) :
```
python table_fil.py
```
