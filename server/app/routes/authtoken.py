from flask import Blueprint, request, jsonify, current_app
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.routes.users import get_users_db

bp = Blueprint('auth', __name__)

users_db = get_users_db()

@bp.route('', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = users_db.get(email)
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    if not check_password_hash(user['password'], password):
        return jsonify({'message': 'Incorrect password.'}), 401

    token = jwt.encode({
        'email': email,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token}), 200
