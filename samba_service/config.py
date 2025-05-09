import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('FLASK_DEBUG')
    SAMBA_ROOT = '/mnt/samba_share'
