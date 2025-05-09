import requests, os

SAMBA_API_URL = os.environ.get('SAMBA_API_URL')

class SambaServiceApi:
    @staticmethod
    def create_folder(data):
        try:
            response = requests.post(f'{SAMBA_API_URL}/create_folder', json=data, timeout=(3, 10))
            return response.json(), response.ok
        except Exception as e:
            return {'success': False, 'msg': 'An unexpected error occurred'}, False
