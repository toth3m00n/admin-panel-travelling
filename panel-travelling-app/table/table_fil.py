from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from data_for_db import *

engine = create_engine("postgresql+psycopg2://postgres:123go@localhost:5432/admin_traveling")

metadata = MetaData()
metadata.reflect(bind=engine)

table_names = metadata.tables

Session = sessionmaker(engine)
with Session() as session:

    # hotel
    for name in hotel_names:
        data_to_insert = {'name': name, 'count_stars': stars[randint(0, len(stars) - 1)]}
        session.execute(table_names['hotel'].insert().values(data_to_insert))

    # class
    for name in class_names:
        for hotel in hotel_names:
            data_to_insert = {'name': name, 'hotel_name': hotel, 'price_per_night': hotel_price_on_class[hotel][name]}
            session.execute(table_names['class'].insert().values(data_to_insert))

    # convenience
    for convenience in convenience_names:
        size = randint(10, 200)
        data_to_insert = {
            'convenience_size': size,
            'name': convenience
        }
        session.execute(table_names['convenience'].insert().values(data_to_insert))

    # booking
    start_class_id = session.query(table_names['class']).first().id
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
        session.execute(table_names['booking'].insert().values(data_to_insert))

    # client
    start_booking_id = session.query(table_names['booking']).first().id
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

        session.execute(table_names['client'].insert().values(data_to_insert))

    # class-convenience
    for class_id in range(len(class_names)):
        for convenience_name in convenience_names:
            amount = randint(0, 7)
            data_to_insert = {
                'class_id': start_class_id + class_id,
                'convenience_name': convenience_name,
                'amount': amount
            }
            session.execute(table_names['class_convenience'].insert().values(data_to_insert))

    session.commit()


