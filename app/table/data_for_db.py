import re
from datetime import datetime, timedelta
from random import randint

import exrex
import pytz

# drop table booking, class_type, class_convenience, client, convenience, hotel

# client
COUNT_CLIENTS = 50

client_names = (
    "Райан",
    "Абоба",
    "Ким пять с плюсом",
    "Гаечка",
    "Бубылда",
    "Ярик",
    "Полина",
    "Алиса",
    "Пятница",
    "Владимир",
    "Олег",
    "Колготочек",
    "Би",
    "X Æ A-12",
    "Дана",
    "Тикток",
    "Никита",
    "Мегафон",
    "Соня"
)

client_surnames = (
        "Абобов",
        "Таксимбаева",
        "Гослингова",
        "Самокат",
        "МТС",
        "Горин",
        "Милос",
        "Свитабобовна",
        "Дворникова",
        "Кудрин",
        "Бейтман",
        "Эссовна",
        "Ляпотун",
        "Путин",
        "Смолик",
        "Агеева",
        "Сигмов"
        )

client_sex = ('male', 'female')

client_age = [age for age in range(1, 120)]

valid_telephone = re.compile(r'[1-9]-\d{3}-\d{3}-\d{4}')
client_telephone = [exrex.getone(r'[1-9]-\d{3}-\d{3}-\d{4}') for _ in range(COUNT_CLIENTS)]

client_jobs = (
    'строитель',
    'программистка',
    'тиктокер',
    'стример',
    'вебкамщик',
    'врач',
    'наездник',
    'дворецкий',
    'юрист',
    'математик',
    'наркодиллер',
    'фея',
    'няня',
    'барабанщик',
    None
)

# hotel

hotel_names = (
    'Абу-даби',
    'Тикток хаус',
    'Тольятти',
    'Греция',
)

stars = (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5)

# class_type

class_names = ('Бизнес-класс', 'Супериор', 'Полулюкс', 'Стандарт', 'VIP')

hotel_price_on_class = {
    'Абу-даби': {
        'VIP': 35000,
        'Бизнес-класс': 20000,
        'Супериор': 15000,
        'Полулюкс': 10000,
        'Стандарт': 3000,
        },
    'Тикток хаус': {
        'VIP': 40000,
        'Бизнес-класс': 25000,
        'Супериор': 15000,
        'Полулюкс': 7500,
        'Стандарт': 4000,
        },
    'Тольятти': {
        'VIP': 35000,
        'Бизнес-класс': 25000,
        'Супериор': 9000,
        'Полулюкс': 7000,
        'Стандарт': 1500,
        },
    'Греция': {
        'VIP': 45000,
        'Бизнес-класс': 35000,
        'Супериор': 25000,
        'Полулюкс': 15000,
        'Стандарт': 13000,
        },
    }

# convenience

convenience_names = (
    'кондиционер',
    'стулья',
    'шкаф',
    'тумбочка',
    'холодильник',
    )

# booking

year = 2022
month = 1
hour = 14
day = 1
timezone = pytz.timezone('Europe/Istanbul')
sessions = [[None, None]] * (COUNT_CLIENTS + 1)
print(sessions)
prev_session_end = 1
current_date = timezone.localize(datetime(year, month, day, hour))

for i in range(COUNT_CLIENTS):
    duration = randint(1, 31)
    end_session = current_date + timedelta(days=duration)

    sessions[i] = [current_date, end_session]
    current_date = end_session

    print(sessions[i][0], sessions[i][1])
