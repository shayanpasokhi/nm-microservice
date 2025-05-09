import os
import requests
import subprocess
import uuid
from flask import Blueprint, request, jsonify
from models import File, db
from config import Config
from api.scanner_service_api import ScannerServiceApi

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/', methods=['POST'])
def upload_file():
    try:
        f = request.files['file']
        user = request.form.get('user_id')
        _dir = f"{Config.TMP_ROOT}/{user}"
        subprocess.run(['mkdir', '-p', _dir])
        subprocess.run(['chmod', '777', _dir])
        uname = f"{uuid.uuid4().hex}"
        filename = f.filename
        path = os.path.join(Config.TMP_ROOT, user, uname)
        f.save(path)
        subprocess.run(['chmod', '777', path])
        _path = os.path.join(user, uname)
        file = File(filename=filename, path=_path, user_id=user)
        db.session.add(file)
        db.session.commit()
        scan_response = ScannerServiceApi.scan({'file_id': file.id, 'path': _path, 'user_id': user})
        if not scan_response['success']:
            db.session.delete(file)
            db.session.commit()
            subprocess.run(['rm', '-f', path])
            return jsonify({'success': False, 'msg': 'Failed to upload file'}), 500
        return jsonify({'success': True, 'msg': 'File uploaded successfully', 'file_id': file.id, 'report_ids': scan_response['report_ids']}), 202
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500
