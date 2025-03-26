from flask import Blueprint, jsonify
from app.utils.auth_middleware import token_required
from app.controllers.users_controller import get_user
from app.controllers.g_classroom_controller import get_student_g_classrooms, get_teacher_g_classrooms, get_admin_g_classrooms

bp = Blueprint('g_classrooms', __name__)

# Define your routes here

@bp.route('', methods=['GET'])
@token_required
def get_g_classrooms(current_user):
    """Fetch g_classrooms (protected route)"""

    user = get_user(current_user)
    
    # Token must have a role key
    
    if user['role'] == 'admin':
        response = get_admin_g_classrooms(user)
    if user['role'] == 'student':
        response = get_student_g_classrooms(user)
    elif user['role'] == 'teacher':
        response = get_teacher_g_classrooms(user)
    else: 
        return jsonify({'message': 'Invalid role'}), 400
    
    # Delete the id and uuid from the all dictionaries in the list
    if response:
        for g_classroom in response:
            g_classroom.pop('id', None)
            g_classroom.pop('uuid', None)

    # Sends the list of g_classrooms in json
    if response is None:
        return jsonify({'message': 'No g_classrooms found'}), 404

    return jsonify(response), 200

@bp.route('', methods=['POST'])
@token_required
def create_g_classroom(current_user):
    """Create a g_classroom (protected route)"""
    response = None

    return jsonify(response), 200