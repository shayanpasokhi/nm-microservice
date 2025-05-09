import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('FLASK_DEBUG')
    TMP_ROOT = '/tmp/tmp_share'
    HOST_TMP_ROOT = '/tmp/tmp_share'
    SCANNERS = [
        {'id': 1, 'name': 'kaspersky', 'image': 'shayanpasokhi/free-kaspersky'}
    ]
