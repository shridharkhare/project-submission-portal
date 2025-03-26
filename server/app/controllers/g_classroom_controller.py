from flask import current_app


def get_student_g_classrooms(user):
    supabase = current_app.supabase
    branch = user['branch']
    semester = user['semester']
    div = user['div']

    try:
        response = supabase.table("g_classrooms").select("*").match({"branch": branch, "semester": semester, "div": div}).execute()
    except Exception as e:
        print(e)
    
    if response.count == 0:
        return None
    
    return response.data

def get_teacher_g_classrooms(user):
    supabase = current_app.supabase
    uuid = user['uuid']

    try:
        response = supabase.table("g_classrooms").select("*").match({"uuid": uuid}).execute()
    except Exception as e:
        print(e)

    if response.count == 0:
        return None
    
    return response.data

def get_admin_g_classrooms(user):
    supabase = current_app.supabase

    try:
        response = supabase.table("g_classrooms").select("*").execute()
    except Exception as e:
        print(e)

    if response.count == 0:
        return None
    
    return response.data

