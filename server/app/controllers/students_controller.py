from flask import current_app
import csv


def get_students_db(div, branch, semester):
    supabase = current_app.supabase
    response = None

    # Get all students from the database
    try:
        response = (
            supabase.table("student")
            .select("student_id, name, email, roll_no")
            .match({"branch": branch, "semester": semester, "div": div})
            .execute()
        )
    except Exception as e:
        print(e)
        return None

    if response.count == 0:
        return None

    return response.data


def upload_students_data_db(file, data):
    supabase = current_app.supabase

    div, branch, semester, year = (
        data.get(k) for k in ("div", "branch", "semester", "year")
    )
    print("Div:", div)

    students_data = []

    try:
        # Read and decode the uploaded CSV
        reader = csv.DictReader(file.read().decode("utf-8").splitlines())

        for row in reader:
            student_id = row.get("student_id")
            name = row.get("name")
            email = row.get("email")

            if not student_id or not name or not email:
                continue  # skip invalid rows

            student_dict = {
                "student_id": student_id,
                "name": name,
                "email": email,
                "roll_no": student_id[-2:],  # last two digits of student_id
                "div": div,
                "branch": branch,
                "semester": semester,
                "year": year,
            }

            students_data.append(student_dict)

    except Exception as e:
        print("CSV Reading Error:", e)
        return None

    # Now upsert the prepared data into Supabase
    try:
        response = (
            supabase.table("student")
            .upsert(students_data, on_conflict=["student_id"])
            .execute()
        )
    except Exception as e:
        print("Supabase Error:", e)
        return None

    if response.count == 0:
        return None

    return response.data
