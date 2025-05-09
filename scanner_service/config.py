import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TMP_ROOT = '/tmp/tmp_share'
    SCANNERS = [
        {'id': 1, 'name': 'kaspersky', 'image': 'shayanpasokhi/free-kaspersky'},
        # {'id': 2, 'name': 'clamav', 'image': 'malice/clamav'}
    ]
