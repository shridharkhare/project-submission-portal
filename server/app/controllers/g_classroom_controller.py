from flask import current_app

def create_g_classroom_db(user, req_data):
    supabase = current_app.supabase
    data = {}
    
    data['uuid'] = user['uuid']

    data['branch'] = req_data['branch']
    data['semester'] = req_data['semester']
    data['div'] = req_data['div']
    data['sub'] = req_data['sub']

    data['g_id'] = f"{data['branch']}_{data['div']}_{data['semester']}_{data['sub']}"

    try: 
        response = supabase.table("g_classroom").insert(data).execute()
    except Exception as e:
        print(e)
        return None
    
    if response.count == 0:
        return None
    
    return response.data

# Function to get g_classrooms for students
def get_student_g_classrooms(user):
    supabase = current_app.supabase
    branch = user['branch']
    semester = user['semester']
    div = user['div']

    try:
        response = supabase.table("g_classroom").select("*, uuid, user(uuid, name)").match({"branch": branch, "semester": semester, "div": div}).execute()
        if response.count == 0:
            return None
    except Exception as e:
        print(e)
    
    if response.count == 0:
        return None
    
    for classroom in response.data:
        classroom["teacher"] = classroom["user"]["name"]
        del classroom["user"]

    return response.data

# Function to get g_classrooms for teachers
def get_teacher_g_classrooms(user):
    supabase = current_app.supabase
    uuid = user['uuid']

    try:
        response = supabase.table("g_classroom").select("*").match({"uuid": uuid}).execute()
    except Exception as e:
        print(e)

    if response.count == 0:
        return None
    
    return response.data

# Function to get g_classrooms for admins (All classrooms available)
def get_admin_g_classrooms(user):
    supabase = current_app.supabase

    try:
        response = supabase.table("g_classroom").select("*").execute()
    except Exception as e:
        print(e)

    if response.count == 0:
        return None
    
    return response.data

def delete_g_classroom_db(user, g_id):
    supabase = current_app.supabase

    # Check if the user is owner of the classroom or is admin

    if user['role'] == 'admin':
        try:
            response = supabase.table("g_classroom").delete().match({"g_id": g_id}).execute()
        except Exception as e:
            print(e)
            return None
    elif user['role'] == 'teacher':
        try:
            response = supabase.table("g_classroom").delete().match({"g_id": g_id, "uuid": user['uuid']}).execute()
        except Exception as e:
            print(e)
            return None
    else:
        return None
    
    print(response)
    
    if response.count is None:
        return None
    
    return response.data