import datetime
from flask import Blueprint, request, jsonify
from models import ScanResult, db
from config import Config
from schemas import AddReportSchema, UpdateReportSchema
from marshmallow import ValidationError
from api.upload_service_api import UploadServiceApi

report_bp = Blueprint('report', __name__)

@report_bp.route('/<int:id>', methods=['GET'])
def generate_report(id):
    try:
        results = ScanResult.query.filter_by(id=id).first()
        return jsonify({'success': True, 'report_id': results.id, 'file_id': results.file_id, 'scanner': results.scanner, 'result': results.result, 'user_id': results.user_id, 'scanned_at': results.scanned_at, 'is_infected': results.is_infected})
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500

@report_bp.route('/add', methods=['POST'])
def add_report():
    try:
        if request.headers.get('X-Internal-Auth') != Config.SECRET_KEY:
            return jsonify({'success': False, 'msg': 'Unauthorized'}), 401
        data = request.get_json()
        AddReportSchema().load(data)
        _json, _status = UploadServiceApi.check_file_user_id(Config.SECRET_KEY, {'file_id': data['file_id'], 'user_id': data['user_id']})
        if not _status or not _json.get('success', False) or not _json.get('exists', False):
            return jsonify({'success': False, 'msg': 'File or User ID is invalid'}), 400
        scan = ScanResult(file_id=data['file_id'], scanner=data['scanner'], user_id=data['user_id'])
        db.session.add(scan)
        db.session.commit()
        return jsonify({'success': True, 'msg': 'Scan results added successfully', 'report_id': scan.id}), 201
    except ValidationError as err:
        return jsonify({'success': False, 'msg': err.messages}), 400
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500
    
@report_bp.route('/update', methods=['PUT'])
def update_report():
    try:
        if request.headers.get('X-Internal-Auth') != Config.SECRET_KEY:
            return jsonify({'success': False, 'msg': 'Unauthorized'}), 401
        data = request.get_json()
        UpdateReportSchema().load(data)
        scan = ScanResult.query.get(data['report_id'])
        if not scan:
            return jsonify({'success': False, 'msg': 'Report not found'}), 404
        scan.result = data['result']
        scan.scanned_at = datetime.datetime.fromisoformat(data['scanned_at'])
        scan.is_infected = data['is_infected']
        db.session.commit()
        return jsonify({'success': True, 'msg': 'Report updated successfully'}), 200
    except ValidationError as err:
        return jsonify({'success': False, 'msg': err.messages}), 400
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500

# @report_bp.route('/user/<int:user_id>', methods=['GET'])
# def user_reports(user_id):
#     results = ScanResult.query.filter_by(user_id=user_id).all()
#     return jsonify([{'file_id': r.file_id, 'scanner': r.scanner, 'result': r.result} for r in results])
