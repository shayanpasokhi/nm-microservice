import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from models import File, db
from config import Config
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from werkzeug.utils import secure_filename
from schemas import CheckFileUserIdSchema
from marshmallow import ValidationError
from api.scanner_service_api import ScannerServiceApi
from api.auth_service_api import AuthServiceApi

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/', methods=['POST'])
def upload_file():
    try:
        user_id = ''
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity() or ''
        except Exception as e:
            return jsonify({'success': False, 'msg': 'Token is invalid'}), 400
        if user_id:
            token = request.headers.get('Authorization', None)
            _json, _status = AuthServiceApi.current_user(token)
            if not _status or not _json.get('success', False):
                return jsonify({'success': False, 'msg': 'User ID is invalid'}), 400
        if 'file' not in request.files:
            return jsonify({'success': False, 'msg': 'File is required'}), 400
        _file = request.files['file']
        org_filename = secure_filename(_file.filename)
        if org_filename == '':
            return jsonify({'success': False, 'msg': 'Filename is empty'}), 400
        _file.seek(0, os.SEEK_END)
        file_size = _file.tell()
        _file.seek(0)
        if file_size > Config.MAX_FILE_SIZE:
            return jsonify({'success': False, 'msg': 'File is too large'}), 400
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        dirname = f'{user_id}_{timestamp}_{unique_id}'
        _dir = os.path.join(Config.TMP_ROOT, dirname)
        os.makedirs(_dir, exist_ok=True)
        os.chmod(_dir, 0o755)
        uname = uuid.uuid4().hex
        path = os.path.join(_dir, uname)
        _file.save(path)
        os.chmod(path, 0o644)
        _path = os.path.join(dirname, uname)
        file = File(filename=org_filename, path=_path, user_id=user_id)
        db.session.add(file)
        db.session.commit()
        __json, __status = ScannerServiceApi.scan({'file_id': file.id, 'path': _path, 'user_id': user_id})
        if not __status or not __json.get('success', False):
            db.session.delete(file)
            db.session.commit()
            os.remove(path)
            return jsonify({'success': False, 'msg': 'Failed to upload file'}), 500
        return jsonify({'success': True, 'msg': 'File uploaded successfully', 'file_id': file.id, 'report_ids': __json['report_ids']}), 202
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500
    
@upload_bp.route('/check_file_user_id', methods=['POST'])
def check_file_user_id():
    try:
        if request.headers.get('X-Internal-Auth') != Config.SECRET_KEY:
            return jsonify({'success': False, 'msg': 'Unauthorized'}), 401
        data = request.get_json()
        CheckFileUserIdSchema().load(data)
        file_id = data['file_id']
        user_id = int(data['user_id']) if data['user_id'] else ''
        file = File.query.get(file_id)
        if file is not None and file.user_id == user_id:
            return jsonify({'success': True, 'exists': True}), 200
        return jsonify({'success': True, 'exists': False}), 200
    except ValidationError as err:
        return jsonify({'success': False, 'msg': err.messages}), 400
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500
