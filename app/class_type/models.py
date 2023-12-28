from app.database import db


class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    hotel_name = db.Column(db.Text, db.ForeignKey('hotel.name'))
    price_per_night = db.Column(db.Numeric(6, 1), nullable=False)
    convenience = db.relationship("ClassConvenience", backref='class_type', cascade="all,delete")


class ClassConvenience(db.Model):
    __tablename__ = 'class_convenience'
    id = db.Column(db.Integer(), primary_key=True)
    convenience_name = db.Column(db.Text(), db.ForeignKey("convenience.name", ondelete='CASCADE'))
    class_id = db.Column(db.Integer(), db.ForeignKey("class.id"))
    amount = db.Column(db.Integer(), nullable=False)
