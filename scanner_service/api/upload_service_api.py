import requests, os

UPLOAD_API_URL = os.environ.get('UPLOAD_API_URL')

class UploadServiceApi:
    @staticmethod
    def check_file_user_id(key, data):
        try:
            headers = {'X-Internal-Auth': key}
            response = requests.post(f'{UPLOAD_API_URL}/upload/check_file_user_id', headers=headers, json=data, timeout=(3, 10))
            return response.json(), response.ok
        except Exception as e:
            return {'success': False, 'msg': 'An unexpected error occurred'}, False
