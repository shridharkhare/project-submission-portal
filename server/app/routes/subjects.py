from flask import Blueprint, jsonify, request

from app.controllers.subjects_controller import get_subjects_db

bp = Blueprint("subjects", __name__)


@bp.route("", methods=["GET"])
def get_subjects():
    """Get all subjects"""
    response = None
    branch = request.args.get("branch")
    semester = request.args.get("semester")

    #   Get all subjects from the database
    try:
        response = get_subjects_db(branch, semester)
    except Exception as e:
        print(e)
        return jsonify({"message": "Error getting subjects"}), 500

    return jsonify({"message": "Subjects fetched successfully", "data": response}), 200
