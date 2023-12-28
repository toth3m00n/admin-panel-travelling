from sqlalchemy import distinct, and_

from app import Hotel, Class, Client, Booking
from app.database import db
from manage import app

with app.app_context():
    class_id = db.session.query(Class.id).filter(and_(Class.hotel_name == 'Рыбинск', Class.name == 'Стандарт')).scalar()
    print(class_id)
