from sqlalchemy import CheckConstraint
from app.database import db


class Hotel(db.Model):
    __tablename__ = 'hotel'
    name = db.Column(db.Text(), primary_key=True)
    count_stars = db.Column(db.Numeric(2, 1), nullable=False)
    class_id = db.relationship('Class',  backref='hotel')
