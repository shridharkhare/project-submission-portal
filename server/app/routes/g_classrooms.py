from flask import Blueprint, jsonify, request
from app.utils.auth_middleware import token_required

from app.controllers.users_controller import get_user
from app.controllers.g_classroom_controller import (
    get_student_g_classrooms,
    get_teacher_g_classrooms,
    get_admin_g_classrooms,
    create_g_classroom_db,
    delete_g_classroom_db,
)

from app.controllers.teams_controller import (
    create_team,
    get_my_team_by_gid,
    get_all_teams_by_gid,
    delete_team,
    update_team_request_db,
    get_team_requests_db,
)

from app.controllers.users_controller import get_student_status

from app.controllers.submission_controller import (
    get_all_submissions_by_g_id_db,
    get_submission_db,
    create_submission_db,
    delete_submission_db,
    update_submission_db,
)


bp = Blueprint("g_classrooms", __name__)

# Define your routes here


@bp.route("", methods=["GET"])
@token_required
def get_g_classrooms(current_user):
    """Fetch g_classrooms (protected route)"""

    user = get_user(current_user)
    response = None

    if user["role"] == "admin":
        response = get_admin_g_classrooms(user)
    if user["role"] == "student":
        response = get_student_g_classrooms(user)
    elif user["role"] == "teacher":
        response = get_teacher_g_classrooms(user)
    else:
        return jsonify({"message": "Invalid role"}), 400

    # Delete the id and uuid from the all dictionaries in the list
    if response:
        for g_classroom in response:
            g_classroom.pop("id", None)
            g_classroom.pop("uuid", None)

    # Sends the list of g_classrooms in json
    if response is None:
        return jsonify({"message": "No g_classrooms found"}), 404

    return jsonify(response), 200


@bp.route("", methods=["POST"])
@token_required
def create_g_classroom(current_user):
    """Create a g_classroom (protected route)"""
    data = request.get_json()
    
    response = None

    user = get_user(current_user)

    if current_user["role"] not in ["admin", "teacher"]:
        return jsonify({"message": "You are not authorized to create a class"}), 403

    if not data:
        return jsonify({"message": "Invalid data"}), 400

    response = create_g_classroom_db(user, data)
    if response is None:
        return jsonify({"message": "Class creation failed"}), 400

    return jsonify(response), 200


@bp.route("/<string:g_id>", methods=["DELETE"])
@token_required
def delete_g_classroom(current_user, g_id):
    """Delete a g_classroom (protected route)"""

    user = get_user(current_user)

    if current_user["role"] not in ["admin", "teacher"]:
        return jsonify({"message": "You are not authorized to delete a class"}), 403

    response = delete_g_classroom_db(user, g_id)

    if response is None:
        return jsonify({"message": "Class deletion failed"}), 400

    return jsonify({"message": "Class deleted successfully"}), 200


@bp.route("/<string:g_id>/teams", methods=["GET"])
@token_required
def get_teams_by_g_classroom(current_user, g_id):
    """Fetch all teams in a g_classroom (protected route)"""

    user = get_user(current_user)

    # Fetch team details based on role
    if current_user["role"] == "admin":
        response = get_all_teams_by_gid(user, g_id)
    elif current_user["role"] == "student":
        response = get_my_team_by_gid(user, g_id)
    elif current_user["role"] == "teacher":
        response = get_all_teams_by_gid(user, g_id)

    # Sends the team details in json
    if response is None:
        return jsonify({"message": "No teams found"}), 404

    return jsonify(response), 200


@bp.route("/<string:g_id>/teams", methods=["POST"])
@token_required
def create_team_by_g_classroom(current_user, g_id):
    """Create a team in a g_classroom"""

    user = get_user(current_user)

    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid data"}), 400

    response = create_team(user, data)
    if response is None:
        return jsonify({"message": "Team creation failed"}), 400

    # Sends the team details in json
    return jsonify(response), 201


@bp.route("/<string:g_id>/teams/<string:team_id>", methods=["DELETE"])
@token_required
def delete_team_by_g_classroom(current_user, team_id, g_id):
    """Delete a team in a g_classroom"""

    user = get_user(current_user)

    response = delete_team(user, team_id, g_id)
    if response is None:
        return jsonify({"message": "Team deletion failed"}), 400

    # Sends the team details in json
    return jsonify("message: Team deleted successfully"), 200


@bp.route("/<string:g_id>/students/status", methods=["GET"])
@token_required
def check_student_in_team(current_user, g_id):
    """Check if a student is in a team in a g_classroom (protected route)"""
    roll = request.args["roll"]

    response = None

    if not roll:
        return jsonify({"message": "Roll number is required"}), 400

    user = get_user(current_user)

    response = get_student_status(user, roll, g_id)

    if response is None:
        return jsonify({"message": False}), 200
    else:
        return jsonify({"message": True}), 200


@bp.route("/<string:g_id>/teams/requests", methods=["GET"])
@token_required
def get_team_requests(current_user, g_id):
    """Fetch all team requests in a g_classroom (protected route)"""

    user = get_user(current_user)

    response = get_team_requests_db(user, g_id)

    if not response:
        return jsonify({"message": "No team requests found"}), 404

    return jsonify(response), 200


@bp.route("/<string:g_id>/teams/requests/<int:req_id>", methods=["PATCH"])
@token_required
def update_team_request(current_user, g_id, req_id):
    """Update a team request in a g_classroom (protected route)"""

    user = get_user(current_user)
    data = request.get_json()

    response = None
    status = data.get("status")

    response = update_team_request_db(user, g_id, req_id, status)

    if response is None:
        return jsonify({"message": "Team request update failed"}), 400

    if response:
        return jsonify({"message": "Team request updated"}), 200


@bp.route("/<string:g_id>/teams/<string:team_id>/submissions", methods=["GET"])
@token_required
def get_submissions_by_g_classroom(current_user, g_id, team_id):
    """Fetch all submissions in a g_classroom (protected route)"""

    user = get_user(current_user)

    response = get_submission_db(user, team_id)

    # Sends the submission details in json
    if not response:
        return jsonify({"message": "No submissions found"}), 404

    return jsonify(response), 200


@bp.route("/<string:g_id>/teams/<string:team_id>/submissions", methods=["POST", "PATCH"])
@token_required
def create_submission(current_user, g_id, team_id):
    """Create or update a submission in a g_classroom (protected route)"""

    user = get_user(current_user)

    data = request.get_json()

    response = None

    if not data:
        return jsonify({"message": "Invalid data"}), 400

    if request.method == "POST":
        response = create_submission_db(user, data, g_id, team_id)
        if response is None:
            return jsonify({"message": "Submission creation failed"}), 400
        return jsonify(response), 201

    elif request.method == "PATCH":
        response = update_submission_db(user, data, g_id, team_id)
        if response is None:
            return jsonify({"message": "Submission update failed"}), 400
        return jsonify(response), 200


@bp.route("/<string:g_id>/teams/<string:team_id>/submissions", methods=["DELETE"])
@token_required
def delete_submission(current_user, g_id, team_id):
    """Delete a submission in a g_classroom (protected route)"""

    user = get_user(current_user)

    response = delete_submission_db(user, team_id, g_id)
    if response is None:
        return jsonify({"message": "Submission deletion failed"}), 400

    # Sends the submission details in json
    return jsonify("message: Submission deleted successfully"), 200

@bp.route("/<string:g_id>/submissions", methods=["GET"])
@token_required
def get_submissions_by_g_classroom_for_teacher(current_user, g_id):
    """Fetch all submissions in a g_classroom"""

    user = get_user(current_user)

    # Fetch submission details based on role
    if current_user["role"] not in ["admin", "teacher"]:
        return jsonify({"message": "You are not authorized to view submissions"}), 403
    
    response = get_all_submissions_by_g_id_db(user, g_id)

    # Sends the submission details in json
    if not response:
        return jsonify({"message": "No submissions found"}), 404
    
    return jsonify(response), 200

