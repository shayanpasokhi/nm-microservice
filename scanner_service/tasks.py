import os
import shutil
import threading
import docker
import json
from flask import Blueprint, request, jsonify
from config import Config
from api.upload_service_api import UploadServiceApi
from api.report_service_api import ReportServiceApi
from schemas import ScanSchema
from marshmallow import ValidationError
from datetime import datetime, timezone
from helper import get_unique_path
from api.auth_service_api import AuthServiceApi

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
        if data['user_id']:
            token = request.headers.get('Authorization', None)
            __json, __status = AuthServiceApi.current_user(token)
            if not __status or not __json.get('success', False) or __json.get('username') != data['username']:
                return jsonify({'success': False, 'msg': 'User is invalid'}), 400
        abs_path = os.path.join(Config.TMP_ROOT, data['path'])
        if not os.path.isfile(abs_path):
            return jsonify({'success': False, 'msg': 'File path does not exist'}), 400
        report_data = []
        for scanner in Config.SCANNERS:
            ___json, ___status = ReportServiceApi.add(Config.SECRET_KEY, {'file_id': data['file_id'], 'scanner': scanner['name'], 'user_id': data['user_id']})
            if ___status and ___json.get('success', False) and ___json.get('report_id', False):
                _data = {'report_id': ___json['report_id'], 'file_id': data['file_id'], 'path': data['path'], 'scanner_info': scanner, 'user_id': data['user_id'], 'push_req': data['push_req'], 'filename': data['filename'], 'username': data['username']}
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
        container = None
        is_infected = True
        _data = {}
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
            result = json.loads(logs)
            if result.get('status', False) and 'result' in result:
                _data['version'] = result.get('version', '')
                _data['database'] = result.get('database', '')
                if len(result['result']) != 0:
                    is_infected = True
                    _data['info'] = result.get('result', [])[0].get('info', '')
                else:
                    is_infected = False
                    _data['info'] = ''
                ReportServiceApi.update(Config.SECRET_KEY, {'report_id': report['report_id'], 'result': json.dumps(_data), 'scanned_at': str(datetime.now(timezone.utc)), 'is_infected': is_infected})
        except Exception as e:
            pass
        finally:
            if container:
                try:
                    container.remove()
                except Exception:
                    pass
            try:
                abs_path = os.path.join(Config.TMP_ROOT, report['path'])
                if report.get('username') and report.get('filename') and report.get('push_req') and is_infected is False:
                    user_dir = os.path.join(Config.SAMBA_ROOT, report.get('username'))
                    os.makedirs(user_dir, exist_ok=True)
                    dest_path = get_unique_path(user_dir, report.get('filename'))
                    shutil.move(abs_path, dest_path)
                else:
                    if os.path.isfile(abs_path):
                        os.remove(abs_path)
                _parent_dir = os.path.join(Config.TMP_ROOT, os.path.dirname(abs_path))
                if os.path.isdir(_parent_dir):
                    shutil.rmtree(_parent_dir)
            except Exception:
                pass
