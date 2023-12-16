from sqlalchemy import CheckConstraint

from app.database import db


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer(), primary_key=True)
    booking_id = db.Column(db.Integer(), db.ForeignKey('booking.id'))
    name = db.Column(db.Text(), nullable=False)
    surname = db.Column(db.Text(), nullable=False)
    sex = db.Column(db.Text(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    telephone = db.Column(db.Text(), unique=True)
    job = db.Column(db.Text())

    __table_args__ = (
        CheckConstraint("sex IN ('male', 'female')", name='sex_check'),
        CheckConstraint('age BETWEEN 1 AND 125', name='age_check'),
    )


class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer(), primary_key=True)
    room_number = db.Column(db.Integer(), nullable=False)
    class_id = db.Column(db.Integer(), db.ForeignKey('class.id'))
    check_in = db.Column(db.DateTime(timezone=True), nullable=False)
    check_out = db.Column(db.DateTime(timezone=True), nullable=False)
    price = db.Column(db.Numeric(10, 1))
    client = db.relationship('Client', backref='booking', uselist=False)

    __table_args__ = (
        CheckConstraint('check_in < check_out', name='valid_time'),
    )

