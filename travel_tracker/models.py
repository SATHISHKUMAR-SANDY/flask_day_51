from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(200))
    plans = db.relationship('TravelPlan', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class TravelPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(100))
    date = db.Column(db.String(50))
    reason = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
