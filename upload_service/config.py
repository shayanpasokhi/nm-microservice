import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///upload.db'
    DEBUG = os.environ.get('FLASK_DEBUG')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TMP_ROOT = '/tmp/tmp_share'
    MAX_FILE_SIZE = 10 * 1024 * 1024
