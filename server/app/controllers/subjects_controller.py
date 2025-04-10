from flask import current_app, jsonify, request


def get_subjects_db(branch, semester):
    supabase = current_app.supabase
    response = None

    # Get all subjects from the database
    try:
        response = (
            supabase.table("subject")
            .select("subject_acronym, subject_name")
            .match({"branch": branch, "semester": semester})
            .execute()
        )
    except Exception as e:
        print(e)
        return None

    if response.count == 0:
        return None
    

    return response.data
