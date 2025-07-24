import os

class Config:
    SECRET_KEY = 'rsvp-secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///rsvp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
