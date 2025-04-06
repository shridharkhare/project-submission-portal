from flask import current_app, jsonify
from app.controllers.users_controller import get_student

# ############################# Functions to create team #############################


def get_max_team_no(user, g_id):
    supabase = current_app.supabase

    # Get the list of team_no where team_id is like g_id%
    try:
        response = (
            supabase.from_("team")
            .select("team_no")
            .like("team_id", f"{g_id}%")
            .execute()
        )
    except Exception as e:
        print(e)
        return None

    team_no_list = response.data

    if len(team_no_list) == 0:
        return 1
    team_no_list = [int(team["team_no"]) for team in team_no_list]
    team_no_list.sort()
    for i in range(1, len(team_no_list) + 1):
        if i not in team_no_list:
            return i
    return max(team_no_list) + 1


def request_students(roll_calls, leader, data):
    supabase = current_app.supabase

    sender_id = data["leader_id"]
    g_id = data["g_id"]
    team_id = data["team_id"]

    for i in roll_calls:
        receiver_id = (
            str(leader["branch"])
            + str(leader["div"])
            + str(leader["semester"])
            + str(i).zfill(2)
        )
        try:
            response = (
                supabase.table("team_req")
                .insert(
                    {
                        "sender_id": sender_id,
                        "receiver_id": receiver_id,
                        "g_id": g_id,
                        "team_id": team_id,
                    }
                )
                .execute()
            )
            # print(response)
        except Exception as e:
            print(e)
            return


def check_if_student_has_a_team(user, g_id):
    """Check if a student has a team in the database"""
    supabase = current_app.supabase

    student = get_student(user)

    try:
        response = (
            supabase.from_("student_team")
            .select("team_id")
            .like("team_id", f"{g_id}%")
            .eq("student_id", student["student_id"])
            .execute()
        )
    except Exception as e:
        print(e)
        return None

    if not response or not response.data:
        return False

    return True


def create_team(user, req_data):
    """Team creation in database"""

    supabase = current_app.supabase

    leader = get_student(user)

    # Check if the user already has a team
    if check_if_student_has_a_team(user, req_data["g_id"]):
        return None

    team_no = str(get_max_team_no(leader, req_data["g_id"])).zfill(2)

    leader_id = leader["student_id"] if leader else None

    roll_calls = req_data.get("roll_calls", [])

    team_id = f"{leader['branch']}_{leader['div']}_{leader['semester']}_{req_data['sub']}_T{team_no}"

    data = {
        "team_id": team_id,
        "leader_id": leader_id,
        "team_no": team_no,
        "topic": req_data["topic"],
        "no_members": 1,
        "g_id": req_data["g_id"],
        "div": leader["div"],
    }

    try:
        response = supabase.from_("team").insert(data).execute()
        print(response)
        add_student_to_team(leader_id, team_id)
        request_students(roll_calls, leader, data)
    except Exception as e:
        print(e)
        return None

    return response.data[0]


############################# Functions to fetch team details #############################


def get_team_id(student, g_id):
    """Fetch team_id for a given user and g_id"""
    supabase = current_app.supabase

    try:
        response = (
            supabase.from_("student_team")
            .select("team_id")
            .like("team_id", f"{g_id}%")
            .eq("student_id", student["student_id"])
            .execute()
        )
    except Exception as e:
        print(e)
        return None

    if not response or not response.data:
        return None

    return response.data[0]["team_id"]


def get_team_details(team_id):
    """Fetch team details for a given team_id"""
    supabase = current_app.supabase

    try:
        response = supabase.from_("team").select("*").eq("team_id", team_id).execute()
    except Exception as e:
        print(e)
        return None

    return response.data[0]


def get_team_members(team_id):
    """Fetch all team members for a given team_id"""
    supabase = current_app.supabase

    try:
        response = (
            supabase.from_("student_team")
            .select("student_id, student(name, roll_no, student_id)")
            .eq("team_id", team_id)
            .execute()
        )
    except Exception as e:
        print(e)
        return None

    if response and response.data:
        response.data[0].pop("student_id", None)

    members = []
    for item in response.data:
        # Get the student details from the "student" key, if it exists
        student = item.get("student")
        members.append(student)

    return {"members": members}


def get_my_team_by_gid(user, g_id):
    student = get_student(user)

    team_id = get_team_id(student, g_id)
    if not team_id:
        return None

    team_details = get_team_details(team_id)
    team_members = get_team_members(team_id)

    team_data = {**team_details, **team_members}

    return team_data


# ############################# Functions to fetch teams #############################


def get_all_teams_by_gid(user, g_id=None):
    supabase = current_app.supabase

    try:
        response = supabase.from_("team").select("*").match({"g_id": g_id}).execute()
    except Exception as e:
        print(e)
        return None

    return response.data


def get_all_teams_by_gid(user, g_id):
    supabase = current_app.supabase

    try:
        response = (
            supabase.from_("team")
            .select("*")
            .match({"g_id": g_id, "uuid": user["uuid"]})
            .execute()
        )
    except Exception as e:
        print(e)
        return None

    return response.get("data")


def add_student_to_team(student_id, team_id):
    supabase = current_app.supabase

    try:
        response = (
            supabase.from_("student_team")
            .insert({"student_id": student_id, "team_id": team_id})
            .execute()
        )
    except Exception as e:
        print(e)
        return None

    return response.data


def delete_team(user, team_id, g_id):
    """Delete a team from database"""
    supabase = current_app.supabase

    student = get_student(user)

    # Check if the user is the leader of the team
    team_details = get_team_details(team_id)

    if team_details["leader_id"] != student["student_id"]:
        return None
    try:
        # Delete the team from the database
        response = supabase.from_("team").delete().match({"team_id": team_id}).execute()
    except Exception as e:
        print(e)
        return None

    return response.data


def update_team_request_db(user, g_id, req_id, status):
    """Update a team request in the database"""
    supabase = current_app.supabase

    student = get_student(user)
    response = None

    if status == "approve":
        try:
            response = (
                supabase.from_("team_req")
                .update({"status": True})
                .eq("req_id", req_id)
                .execute()
            )
        except Exception as e:
            print(e)
            return None

        team_id = response.data[0]["team_id"]
        receiver_id = response.data[0]["receiver_id"]

        try:
            response = (
                supabase.from_("student_team")
                .insert({"student_id": receiver_id, "team_id": team_id})
                .execute()
            )
        except Exception as e:
            print(e)
            return None
    elif status == "reject":
        try:
            response = (
                supabase.from_("team_req")
                .update({"status": False})
                .eq("req_id", req_id)
                .execute()
            )
        except Exception as e:
            print(e)
            return None
    return response.data


def get_team_requests_db(user, g_id):
    """Fetch all team requests in a g_classroom (protected route)"""
    supabase = current_app.supabase

    student = get_student(user)

    try:
        response = (
            supabase.from_("team_req")
            .select("req_id, created_at, sender_id, g_id, team_id")
            .match({"receiver_id": student["student_id"], "g_id": g_id})
            .is_("status", "null")
            .order("created_at", desc=True)
            .execute()
        )
    except Exception as e:
        print(e)
        return None

    if not response or not response.data:
        return None
    
    team_details = get_team_details(response.data[0]["team_id"])

    response.data[0]["topic"] = team_details["topic"]

    if not response or not response.data:
        return None

    return response.data


def get_team_details_by_team_ids_db(team_ids):
    """Gets all team details in the database by team_ids."""
    supabase = current_app.supabase

    try:
        response = supabase.from_("teams").select("*").in_("id", team_ids).execute()
    except Exception as e:
        print(e)
        return None

    return response.data
