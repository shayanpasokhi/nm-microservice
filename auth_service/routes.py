from flask import Blueprint, request, jsonify
from models import User, db, TokenBlocklist
from flask_jwt_extended import (
    create_access_token, get_jwt, jwt_required, get_jwt_identity
)
from datetime import timedelta
from api.samba_service_api import SambaServiceApi
from schemas import AuthSchema, CheckUsernameSchema
from marshmallow import ValidationError
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        AuthSchema().load(data)
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'success': False, 'msg': 'Username exists'}), 400
        user = User(username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        _json, _status = SambaServiceApi.create_folder({'username': user.username})
        if not _status or not _json.get('success', False):
            db.session.delete(user)
            db.session.commit()
            return jsonify({'success': False, 'msg': 'Failed to create user folder'}), 500
        return jsonify({'success': True, 'msg': 'User created'}), 201
    except ValidationError as err:
        return jsonify({'success': False, 'msg': err.messages}), 400
    except Exception as e:
        return jsonify({'success': False, 'msg': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        AuthSchema().load(data)
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(
                identity=str(user.id), expires_delta=timedelta(hours=24)
            )
            return jsonify({'success': True, 'access_token': access_token}), 200
        return jsonify({'success': False, 'msg': 'bad credentials'}), 401
    except ValidationError as err:
        return jsonify({'success': False, 'msg': err.messages}), 400
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        jti = get_jwt()['jti']
        db.session.add(TokenBlocklist(jti=jti))
        db.session.commit()
        return jsonify({'success': True, 'msg': 'logged out'}), 200
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500

@auth_bp.route('/current_user')
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return jsonify({'success': True, 'user_id': user.id, 'username': user.username})
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500

@auth_bp.route('/is_token_blacklisted', methods=['GET'])
def is_token_blacklisted():
    try:
        jti = request.args.get('jti')
        if jti is None:
            return jsonify({'success': False, 'msg': 'JTI is required'}), 400
        token = TokenBlocklist.query.filter_by(jti=jti).first()
        if token:
            return jsonify({'success': True, 'blacklisted': True}), 200
        else:
            return jsonify({'success': True, 'blacklisted': False}), 200
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500


@auth_bp.route('/check_username', methods=['POST'])
def check_username():
    try:
        if request.headers.get('X-Internal-Auth') != Config.SECRET_KEY:
            return jsonify({'success': False, 'msg': 'Unauthorized'}), 401
        data = request.get_json()
        CheckUsernameSchema().load(data)
        username = data['username']
        exists = User.query.filter_by(username=username).first() is not None
        return jsonify({'success': True, 'exists': exists}), 200
    except ValidationError as err:
        return jsonify({'success': False, 'msg': err.messages}), 400
    except Exception as e:
        return jsonify({'success': False, 'msg': 'An unexpected error occurred'}), 500
