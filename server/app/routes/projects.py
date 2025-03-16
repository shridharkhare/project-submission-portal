from flask import Blueprint, request, jsonify
from app.utils.auth_middleware import token_required

bp = Blueprint('projects', __name__)

# Dummy projects data
projects = {}

@bp.route('', methods=['GET'])
@token_required
def get_projects(current_user):
    """Get all projects"""
    return jsonify({'projects': projects}), 200
