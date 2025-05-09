import os
import subprocess
from flask import Flask, request, jsonify
from config import Config
from api.auth_service_api import AuthServiceApi
from schemas import CreateFolderSchema
from marshmallow import ValidationError

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/create_folder', methods=['POST'])
def create_folder():
    try:
        data = request.get_json()
        CreateFolderSchema().load(data)
        username = data['username']
        _json, _status = AuthServiceApi.current_user(Config.SECRET_KEY, {'username': username})
        if not _status or not _json.get('success', False) or not _json.get('exists', False):
            return jsonify({'success': False, 'msg': 'Username is invalid'}), 400
        path = os.path.join(Config.SAMBA_ROOT, username)
        try:
            subprocess.run(['mkdir', '-p', path], check=True)
            subprocess.run(['chmod', '700', path], check=True)
        except subprocess.CalledProcessError as e:
            return jsonify({'success': False, 'msg': 'Failed to create folder'}), 500
        return jsonify({'success': True, 'msg': 'folder created'}), 201
    except ValidationError as err:
        return jsonify({'success': False, 'msg': err.messages}), 400
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500

# @app.route('/transfer', methods=['POST'])
# def transfer():
#     data = request.get_json()
#     src = data['src']
#     username = data['username']
#     dest = f"{Config.SAMBA_ROOT}/{username}/{src.split('/')[-1]}"
#     subprocess.run(['cp', src, dest])
#     return jsonify({'msg': 'file transferred'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
