# This is project of admin panel travelling

## Schema database 

![alt text](schema.png)
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
Перейти в рабочую папку и установить переменные окружения:
```
cd computer_club
export FLASK_APP=app
export FLASK_ENV=development (для режима разработки)
```
Заполнить базу данных:
```
python init_db.py
```
Теперь можно запускать проект:
```
flask run
```
*Примечание:*
*Перед работой у вас должна быть создана база данных, и в файле `.env` в корне репозитория необходимо прописать имя пользователя и пароль для подключения к базе.*
*Пример файла `.env`:*
```
DB_USERNAME=psql_user
DB_PASSWORD=psql1234
```