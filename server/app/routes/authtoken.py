from flask import Blueprint, request, jsonify, current_app, make_response
import jwt, datetime
from flask_cors import CORS
from werkzeug.security import check_password_hash
from app.controllers.users_controller import get_user

bp = Blueprint('authtoken', __name__)

CORS(bp, supports_credentials=True)

@bp.route('', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    password = data.pop('password')

    user = get_user(data)
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    if not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'iss': 'project-submission-backend',
        'uuid': user['uuid'],
        'email': user['email'],
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7),
    }, current_app.config['JWT_SECRET'], algorithm="HS256")

    response = make_response(jsonify({'message': 'Login successful'}))

    # Check for environment whether dev or prod
    secure_cookie = current_app.config.get("IS_PROD", False)

    # Set the token in the cookie
    response.set_cookie(
        key='access_token',
        value=token,
        httponly=True,           # Prevent JavaScript access (XSS protection)
        secure=secure_cookie,    # True in prod, False locally
        samesite='None' if secure_cookie else 'Lax',  # Protect against CSRF, None for Hosted and Lax for local
        max_age=60 * 60 * 24 * 7 , # Expiry time (7 days)
        path= '/',
    )

    return response, 200
