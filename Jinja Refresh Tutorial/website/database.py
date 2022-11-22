from website import db
from flask_login import UserMixin

class Numbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable = False)
    username = db.Column(db.String(150), unique=True, nullable = False)
    password = db.Column(db.String(150), nullable = False)
    numbers = db.relationship('Numbers', backref='user')