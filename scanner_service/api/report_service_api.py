import requests, os

REPORT_API_URL = os.environ.get('REPORT_API_URL')

class ReportServiceApi:
    @staticmethod
    def add(data):
        try:
            response = requests.post(REPORT_API_URL + '/report/add', json=data)
            return response.json()
        except Exception as e:
            return {'success': False, 'msg': 'An unexpected error occurred'}
        
    @staticmethod
    def update(data):
        try:
            response = requests.put(REPORT_API_URL + '/report/update', json=data)
            return response.json()
        except Exception as e:
            return {'success': False, 'msg': 'An unexpected error occurred'}
