from flask import Blueprint, request, jsonify
from app.utils.auth_middleware import token_required
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('users', __name__)

# Dummy data
users_db = {}

@bp.route('', methods=['POST'])
def register():
    """User registration"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email in users_db:
        return jsonify({'message': 'User already exists.'}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    users_db[email] = {'email': email, 'password': hashed_password}

    return jsonify({'message': 'User registered successfully.'}), 201

@bp.route('', methods=['GET'])
@token_required
def get_users(current_user):
    """Fetch users (protected route)"""
    return jsonify({'users': list(users_db.keys())}), 200

# Export users_db
def get_users_db():
    return users_db