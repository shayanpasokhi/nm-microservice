from flask import Blueprint, request, jsonify
import subprocess
import threading
import os
import requests
import docker
from config import Config
from api.report_service_api import ReportServiceApi
from datetime import datetime, timezone

scanner_bp = Blueprint('scanner', __name__)
docker_client = docker.from_env()

@scanner_bp.route('/', methods=['POST'])
def scan():
    try:
        data = request.get_json()
        report_data = []
        for scanner in Config.SCANNERS:
            report_response = ReportServiceApi.add({'file_id': data['file_id'], 'scanner': scanner['name'], 'user_id': data['user_id']})
            if report_response['success']:
                _data = {'report_id': report_response['report_id'], 'file_id': data['file_id'], 'path': data['path'], 'scanner': scanner, 'user_id': data['user_id']}
                report_data.append(_data)
        if len(report_data) != 0:
            thread = threading.Thread(target=run_scan, args=(report_data,))
            thread.start()
            return jsonify({'success': True, 'msg': 'scan started', 'report_ids': [r['report_id'] for r in report_data]}), 202
        return jsonify({'success': False, 'msg': 'Failed to start scan'}), 400
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500

def run_scan(reports):
    for report in reports:
        try:
            volume_path = f"{Config.TMP_ROOT}/{report['path']}"
            volumes = {
                volume_path: {'bind': '/scan', 'mode': 'ro'}
            }
            container = docker_client.containers.run(
                image=report['scanner']['image'],
                volumes=volumes,
                network_mode='none',
                remove=True,
                detach=True
            )
            container.wait()
            logs = container.logs().decode('utf-8').strip()
            ReportServiceApi.update({'report_id': report['report_id'], 'result': logs, 'scanned_at': str(datetime.now(timezone.utc))})
        except Exception as e:
            pass
