import requests, os

REPORT_API_URL = os.environ.get('REPORT_API_URL')

class ReportServiceApi:
    @staticmethod
    def add(key, data):
        try:
            headers = {'X-Internal-Auth': key}
            response = requests.post(REPORT_API_URL + '/report/add', headers=headers, json=data, timeout=(3, 10))
            return response.json(), response.ok
        except Exception as e:
            return {'success': False, 'msg': 'An unexpected error occurred'}, False
        
    @staticmethod
    def update(key, data):
        try:
            headers = {'X-Internal-Auth': key}
            response = requests.put(REPORT_API_URL + '/report/update', headers=headers, json=data, timeout=(3, 10))
            return response.json(), response.ok
        except Exception as e:
            return {'success': False, 'msg': 'An unexpected error occurred'}, False
