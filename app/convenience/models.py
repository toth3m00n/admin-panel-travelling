from app.database import db


class Convenience(db.Model):
    __tablename__ = 'convenience'
    name = db.Column(db.Text(), primary_key=True)
    size = db.Column(db.Integer(), nullable=False)
    convenience = db.relationship("ClassConvenience", backref="convenience")
