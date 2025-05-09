import requests, os

AUTH_API_URL = os.environ.get('AUTH_API_URL')

class AuthServiceApi:        
    @staticmethod
    def current_user(key, data):
        try:
            headers = {'X-Internal-Auth': key}
            response = requests.post(f'{AUTH_API_URL}/auth/check_username', headers=headers, json=data, timeout=(3, 10))
            return response.json(), response.ok
        except Exception as e:
            return {'success': False, 'msg': 'An unexpected error occurred'}, False
