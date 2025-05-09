import os
import threading
import docker
from flask import Blueprint, request, jsonify
from config import Config
from api.upload_service_api import UploadServiceApi
from api.report_service_api import ReportServiceApi
from schemas import ScanSchema
from marshmallow import ValidationError
from datetime import datetime, timezone

scanner_bp = Blueprint('scanner', __name__)
docker_client = docker.from_env()

@scanner_bp.route('/', methods=['POST'])
def scan():
    try:
        data = request.get_json()
        ScanSchema().load(data)
        _json, _status = UploadServiceApi.check_file_user_id(Config.SECRET_KEY, {'file_id': data['file_id'], 'user_id': data['user_id']})
        if not _status or not _json.get('success', False) or not _json.get('exists', False):
            return jsonify({'success': False, 'msg': 'File or User ID is invalid'}), 400
        abs_path = os.path.join(Config.TMP_ROOT, data['path'])
        if not os.path.isfile(abs_path):
            return jsonify({'success': False, 'msg': 'File path does not exist'}), 400
        report_data = []
        for scanner in Config.SCANNERS:
            __json, __status = ReportServiceApi.add(Config.SECRET_KEY, {'file_id': data['file_id'], 'scanner': scanner['name'], 'user_id': data['user_id']})
            if __status and __json.get('success', False) and __json.get('report_id', False):
                _data = {'report_id': __json['report_id'], 'file_id': data['file_id'], 'path': data['path'], 'scanner_info': scanner, 'user_id': data['user_id']}
                report_data.append(_data)
        if len(report_data) != 0:
            thread = threading.Thread(target=run_scan, args=(report_data,))
            thread.start()
            return jsonify({'success': True, 'msg': 'scan started', 'report_ids': [r['report_id'] for r in report_data]}), 202
        return jsonify({'success': False, 'msg': 'Failed to start scan'}), 400
    except ValidationError as err:
        return jsonify({'success': False, 'msg': err.messages}), 400
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500

def run_scan(reports):
    for report in reports:
        try:
            parent_dir = os.path.dirname(report['path'])
            volume_path = f"{Config.HOST_TMP_ROOT}/{parent_dir}"
            volumes = {
                volume_path: {'bind': '/scan', 'mode': 'ro'}
            }
            container = docker_client.containers.run(
                image=report['scanner_info']['image'],
                volumes=volumes,
                network_mode='none',
                remove=False,
                detach=True
            )
            container.wait()
            logs = container.logs().decode('utf-8').strip()
            container.remove()
            ReportServiceApi.update(Config.SECRET_KEY, {'report_id': report['report_id'], 'result': logs, 'scanned_at': str(datetime.now(timezone.utc))})
        except Exception as e:
            pass
