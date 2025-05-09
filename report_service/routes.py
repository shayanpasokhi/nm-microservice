import datetime
from flask import Blueprint, request, jsonify
from models import ScanResult, db

report_bp = Blueprint('report', __name__)

@report_bp.route('/<int:id>', methods=['GET'])
def generate_report(id):
    try:
        results = ScanResult.query.filter_by(id=id).first()
        return jsonify({'success': True, 'report_id': results.id, 'file_id': results.file_id, 'scanner': results.scanner, 'result': results.result, 'user_id': results.user_id, 'scanned_at': results.scanned_at})
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500

@report_bp.route('/add', methods=['POST'])
def add_report():
    try:
        data = request.get_json()
        scan = ScanResult(file_id=data['file_id'], scanner=data['scanner'], user_id=data['user_id'])
        db.session.add(scan)
        db.session.commit()
        return jsonify({'success': True, 'msg': 'Scan results added successfully', 'report_id': scan.id}), 201
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500
    
@report_bp.route('/update', methods=['PUT'])
def update_report():
    try:
        data = request.get_json()
        scan = ScanResult.query.get(data['report_id'])
        if not scan:
            return jsonify({'success': False, 'msg': 'Report not found'}), 404
        scan.result = data['result']
        scan.scanned_at = datetime.datetime.fromisoformat(data['scanned_at'])
        db.session.commit()
        return jsonify({'success': True, 'msg': 'Report updated successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500

# @report_bp.route('/user/<int:user_id>', methods=['GET'])
# def user_reports(user_id):
#     results = ScanResult.query.filter_by(user_id=user_id).all()
#     return jsonify([{'file_id': r.file_id, 'scanner': r.scanner, 'result': r.result} for r in results])
