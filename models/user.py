import sqlite3
from db import db


# this is an API, not REST tho
class UserModel(db.Model):
    __tablename__ = 'users'

    # when saved to database, going to look for these three properties
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))  # limit of 80 characters
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()  # SQLAlchemy converts first row into user model obj

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()