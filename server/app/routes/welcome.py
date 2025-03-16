from flask import Blueprint

bp = Blueprint('welcome', __name__)

@bp.route('', methods=['GET'])
def welcome():
    return "<h1>Welcome to Project Backend</h1>"