from flask import current_app, jsonify

from app.controllers.teams_controller import get_team_details, get_team_details_by_team_ids_db
from app.controllers.users_controller import get_student

def create_submission_db(user, req_data, g_id, team_id):
    """Creates a submission in the database."""

    supabase = current_app.supabase
    student = get_student(user)
    data = {}

    data["leader_id"] = student["student_id"]

    data["g_id"] = g_id
    data["team_id"] = team_id

    data["github_url"] = req_data["github_url"]
    data["ppt_url"] = req_data["ppt_url"]
    data["report_url"] = req_data["report_url"]

    try:
        response = supabase.from_("submission").insert(data).execute()
    except Exception as e:
        print(e)
        return None

    return response.data


def delete_submission_db(user, team_id):
    """Deletes a submission in the database."""

    supabase = current_app.supabase
    student = get_student(user)
    data = {}

    # Check if the user is the leader of the team
    team_details = get_team_details(team_id)

    if team_details["leader_id"] != student["student_id"]:
        return jsonify({"error": "You are not the leader of this team"}), 403

    try:
        response = (
            supabase.from_("submission").delete().match({"team_id": team_id}).execute()
        )
    except Exception as e:
        print(e)
        return None

    return response.data[0]


def update_submission_db(user, req_data, g_id, team_id):
    """Updates a submission in the database."""

    supabase = current_app.supabase
    student = get_student(user)
    data = {}

    # Check if the user is the leader of the team
    team_details = get_team_details(team_id)

    if team_details["leader_id"] != student["student_id"]:
        return jsonify({"error": "You are not the leader of this team"}), 403

    # Update only the fields present in req_data

    allowed_fields = {"github_url", "ppt_url", "report_url"}
    for field in allowed_fields:
        if field in req_data:
            data[field] = req_data[field]

    try:
        response = (
            supabase.from_("submission")
            .update(data)
            .match({"team_id": team_id})
            .execute()
        )
    except Exception as e:
        print(e)
        return None

    return response.data


def get_submission_db(user, team_id):
    """Gets a submission in the database."""
    supabase = current_app.supabase
    student = get_student(user)
    data = {}

    # Check if the user is the leader of the team
    team_details = get_team_details(team_id)

    if team_details["leader_id"] != student["student_id"]:
        return jsonify({"error": "You are not the leader of this team"}), 403

    try:
        response = (
            supabase.from_("submission").select("*").eq("team_id", team_id).execute()
        )
    except Exception as e:
        print(e)
        return None

    print(response)
    return response.data[0]


def get_all_submissions_by_g_id_db(user, g_id):
    """Gets all submissions in the database by g_id."""
    supabase = current_app.supabase

    try:
        response = supabase.from_("submission").select("*").eq("g_id", g_id).execute()
    except Exception as e:
        print(e)
        return None

    submissions = response.data
    team_ids = [submission["team_id"] for submission in submissions]

    response = get_team_details_by_team_ids_db(team_ids)
    if response is None:
        return None

    team_details = {team["id"]: team for team in response.data}

    submissions_with_team_details = [
        {**submission, "team_details": team_details[submission["team_id"]]}
        for submission in submissions
    ]

    return submissions_with_team_details



