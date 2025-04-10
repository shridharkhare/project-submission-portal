from flask import Blueprint, jsonify, request
import json
from app.utils.auth_middleware import token_required

from app.controllers.users_controller import get_user

from app.controllers.students_controller import (
    get_students_db,
    upload_students_data_db,
)

bp = Blueprint("students", __name__)

@bp.route("", methods=["GET"])
@token_required
def get_students(current_user):
    """Get all students (protected route)"""
    response = None
    
    user = get_user(current_user)
    div = request.args.get("div")
    branch = request.args.get("branch")
    semester = request.args.get("semester")

    if user["role"] == "student":
        return jsonify({"message": "You are not allowed to view this page"}), 400

    # Get all students from the database
    try:
        response = get_students_db(div, branch, semester)
    except Exception as e:
        print(e)
        return jsonify({"message": "Error getting students"}), 500

    return jsonify({"message": "Students fetched successfully", "data": response}), 200


@bp.route("", methods=["POST"])
@token_required
def upload_csv(current_user):
    """Upload a CSV file (protected route)"""
    
    file = request.files.get("file")


    user = get_user(current_user)
    # get the div, branch, semester and year from the form data 
    data = json.loads(request.form.get("metadata"))

    response = None

    if user["role"] == "student":
        return jsonify({"message": "You are not allowed to create a class"}), 400

    # Check if the request has a file
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400


    # Save the file in the database
    try:
        response = upload_students_data_db(file, data)
    except Exception as e:
        print(e)
        return jsonify({"message": "Error uploading file"}), 500
    
    if response is None or not response:
        return jsonify({"message": "Error uploading file"}), 500
    

    return jsonify({"message": "Class updated successfully"}), 200