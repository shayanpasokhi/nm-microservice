import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///auth.db'
    DEBUG = os.environ.get('FLASK_DEBUG')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
