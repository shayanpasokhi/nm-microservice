import requests, os

AUTH_API_URL = os.environ.get('AUTH_API_URL')

class AuthServiceApi:
    @staticmethod
    def is_token_blacklisted(data):
        try:
            response = requests.get(f'{AUTH_API_URL}/auth/is_token_blacklisted', params=data, timeout=(3, 10))
            return response.json(), response.ok
        except Exception as e:
            return {'success': False, 'msg': 'An unexpected error occurred'}, False

    @staticmethod
    def current_user(token):
        try:
            headers = {'Authorization': token}
            response = requests.get(f'{AUTH_API_URL}/auth/current_user', headers=headers, timeout=(3, 10))
            return response.json(), response.ok
        except Exception as e:
            return {'success': False, 'msg': 'An unexpected error occurred'}, False
