from sqlalchemy import distinct

from app import Hotel, Class, Client, Booking
from app.database import db
from manage import app

with app.app_context():
    uniq_booking = db.session.query(Booking).filter(Booking.id == 2).all()
    print(uniq_booking)
