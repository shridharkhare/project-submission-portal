from flask import request, Blueprint, jsonify
from app.utils.auth_middleware import token_required
from werkzeug.security import generate_password_hash
from app.controllers.users_controller import create_user

bp = Blueprint('users', __name__)

# Dummy data
users_db = {}

@bp.route('', methods=['POST'])
def register():
    response = request.get_json()

    email, password, name, role = (response.get(key) for key in ('email', 'password', 'name', 'role'))
    branch = roll_no = year = semester = div = None

    if not email or not password or not role:
        return jsonify({'message': 'missing one or more info'}), 400


    data = {
        'email': email,
        'password': password,
        'name': name,
        'role': role,
        'branch': branch,
        'roll_no': roll_no,
        'year': year,
        'semester': semester,
        'div': div
    }

    data['password'] = generate_password_hash(data.pop('password'), method='pbkdf2:sha256')
    
    requests = create_user(data)

    if getattr(requests, 'error', False):
        return jsonify({'message': 'User already exists.'}), 400

    return jsonify({'message': 'User registered successfully.'}), 201
    

@bp.route('/me', methods=['GET'])
@token_required
def get_users(current_user):
    """Fetch users (protected route)"""
    # send dictionary of user in json
    current_user.pop('password')
    return jsonify(current_user), 200
