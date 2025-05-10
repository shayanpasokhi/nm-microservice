import requests, os

AUTH_API_URL = os.environ.get('AUTH_API_URL')

class AuthServiceApi:
    @staticmethod
    def current_user(token):
        try:
            headers = {'Authorization': token}
            response = requests.get(f'{AUTH_API_URL}/auth/current_user', headers=headers, timeout=(3, 10))
            return response.json(), response.ok
        except Exception as e:
            return {'success': False, 'msg': 'An unexpected error occurred'}, False
