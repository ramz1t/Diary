from Dairy.logic.group import get_groups
from Dairy.logic.key import get_student_keys, get_student_keys_for_export, get_teacher_keys
from Dairy.logic.school import check_school_in_db
from Dairy.models.admin import Admin
from Dairy.models.student import Student
from Dairy.models.teacher import Teacher
from Dairy.data.data import Sessions


def get_user_by_email(email: str, type: str):
    if type == 'admin':
        with Sessions() as session:
            return session.query(Admin).filter_by(email=email).first()
    elif type == 'student':
        with Sessions() as session:
            return session.query(Student).filter_by(email=email).first()
    elif type == 'teacher':
        with Sessions() as session:
            return session.query(Teacher).filter_by(email=email).first()


def get_data_for_page(page: str, current_user, request):
    if page == 'manage_groups':
        groups = get_groups(current_user.email)
        return {"request": request, "groups": sorted(groups)}
    elif page == 'add_student_key':
        groups = get_groups(current_user.email)
        keys = get_student_keys(current_user.email)
        return {"request": request, "groups": groups, "keys": keys}
    elif page == 'export_student_keys':
        keys_for_export = get_student_keys_for_export(current_user.email)
        return {"request": request, "keys_for_export": keys_for_export}
    elif page == 'add_group':
        groups = get_groups(current_user.email)
        return {"request": request, "groups": groups}
    elif page == 'add_teacher_key':
        keys = get_teacher_keys(current_user.email)
        return {"request": request, "keys": keys}
    elif page == 'school':
        availability = check_school_in_db(current_user.email)
        return {"request": request, "number": current_user.email, "availability": availability}
    elif page == 'change_password':
        return {"request": request}
    else:
        return {"request": request}
