from sqlalchemy import insert, distinct

from table.data_for_db import *

from app.hotel.models import *
from app.client.models import *
from app.class_type.models import *
from app.convenience.models import *
from app.database import db
from manage import app


def fil_database():
    # hotel
    for name in hotel_names:
        data_to_insert = {'name': name, 'count_stars': stars[randint(0, len(stars) - 1)]}
        db.session.add(Hotel(**data_to_insert))

    # class_type
    for name in class_names:
        for hotel in hotel_names:
            data_to_insert = {'name': name, 'hotel_name': hotel, 'price_per_night': hotel_price_on_class[hotel][name]}
            db.session.add(Class(**data_to_insert))

    # convenience
    for convenience in convenience_names:
        size = randint(10, 200)
        data_to_insert = {
            'size': size,
            'name': convenience
        }
        db.session.add(Convenience(**data_to_insert))

    # booking
    start_class_id = db.session.query(Class).first().id
    for booking_id in range(COUNT_CLIENTS):
        room_number = booking_id + 1
        class_id = randint(start_class_id, start_class_id + len(hotel_names) * len(class_names) - 1)
        index_for_check_in = randint(0, len(sessions) - 2)
        check_in = sessions[index_for_check_in][0]
        check_out = sessions[index_for_check_in][1]
        data_to_insert = {
            'room_number': room_number,
            'class_id': class_id,
            'check_in': check_in,
            'check_out': check_out,
        }
        db.session.add(Booking(**data_to_insert))

    # client
    start_booking_id = db.session.query(Booking).first().id
    for client_id in range(COUNT_CLIENTS):
        name = client_names[randint(0, len(client_names) - 1)]
        surname = client_surnames[randint(0, len(client_surnames) - 1)]
        age = client_age[randint(0, len(client_age) - 1)]
        telephone = client_telephone[client_id]
        job = client_jobs[randint(0, len(client_jobs) - 1)]
        booking_id = start_booking_id + client_id
        sex = client_sex[randint(0, len(client_sex) - 1)]

        data_to_insert = {
            'name': name,
            'surname': surname,
            'age': age,
            'telephone': telephone,
            'job': job,
            'booking_id': booking_id,
            'sex': sex
        }

        db.session.add(Client(**data_to_insert))

    classes = db.session.query(Class).all()

    # class_type-convenience
    for class_id in classes:
        id = class_id.id
        for convenience_name in convenience_names:
            amount = randint(0, 7)
            data_to_insert = {
                'class_id': id,
                'convenience_name': convenience_name,
                'amount': amount
            }
            db.session.add(ClassConvenience(**data_to_insert))

    db.session.commit()


with app.app_context():
    fil_database()
