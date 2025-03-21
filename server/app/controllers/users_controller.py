from flask import jsonify, current_app
from werkzeug.security import generate_password_hash

def create_user(data):
    """User creation in database"""
    supabase = current_app.supabase

    try: 
        response = supabase.table("users").insert(data).execute()
    except Exception as e:
        print(e)

    return response

def get_user(user):
    """Get user from database"""
    supabase = current_app.supabase
    email = user.get("email")

    try:
        response = supabase.table("users").select("*").match({"email": email}).execute()
    except Exception as e:
        print(e)
    
    if response.count == 0:
        return None
    
    return response.data[0]
