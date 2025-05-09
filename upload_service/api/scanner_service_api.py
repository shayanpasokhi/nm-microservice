import requests, os

SCANNER_API_URL = os.environ.get('SCANNER_API_URL')

class ScannerServiceApi:
    @staticmethod
    def scan(data):
        try:
            response = requests.post(SCANNER_API_URL + '/scan', json=data, timeout=(3, 10))
            return response.json(), response.ok
        except Exception as e:
            return {'success': False, 'msg': 'An unexpected error occurred'}, False
