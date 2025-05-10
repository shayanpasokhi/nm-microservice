import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('FLASK_DEBUG')
    TMP_ROOT = '/tmp/tmp_fscan'
    SAMBA_ROOT = '/mnt/samba_fscan'
    HOST_TMP_ROOT = '/tmp/tmp_fscan'
    SCANNERS = [
        {'id': 1, 'name': 'kaspersky', 'image': 'shayanpasokhi/free-kaspersky'}
    ]
