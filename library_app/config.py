# config.py

class Config:
    SECRET_KEY = 'library_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
