from flask import jsonify, current_app
from werkzeug.security import generate_password_hash

# Function to create a user in the database (Register)
def create_user(data):
    """User creation in database"""
    supabase = current_app.supabase

    response = None

    try: 
        response = supabase.table("user").insert(data).execute()
    except Exception as e:
        print(e)

    return response

# Function to get a user from the database based on email from the token
def get_user(user):
    """Get user from database"""
    supabase = current_app.supabase
    email = user.get("email")

    try:
        response = supabase.table("user").select("*").match({"email": email}).execute()
    except Exception as e:
        print(e)
    
    if response.count == 0:
        return None
    
    return response.data[0]

def get_student(user):
    """Get student from database"""
    supabase = current_app.supabase
    email = user.get("email")

    try:
        response = supabase.table("student").select("*").match({"email": email}).execute()
    except Exception as e:
        print(e)
    
    if response.count == 0:
        return None
    
    return response.data[0]
    
def get_student_status(user, roll, g_id):
    supabase = current_app.supabase
    student_id = f"{user['branch']}{user['div']}{user['semester']}{str(roll).zfill(2)}"

    try:
        response = (
            supabase.from_("student_team")
            .select("team_id")
            .eq("student_id", student_id)
            .like("team_id", f"{g_id}%")
            .execute()
        )
    except Exception as e:
        print(e)
        return None

    if not response or not response.data:
        return None
    
    return response.data[0]["team_id"]