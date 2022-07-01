from starlette import status
from starlette.responses import JSONResponse

from Dairy.func.db_user_find import get_user_by_email
from Dairy.logic.auth import verify_password, get_password_hash
from Dairy.logic.cls import get_classes
from Dairy.logic.group import get_groups
from Dairy.logic.key import get_student_keys, get_student_keys_for_export, get_teacher_keys
from Dairy.logic.school import check_school_in_db
from Dairy.logic.subject import get_subjects
from Dairy.logic.teacher import get_teachers
from Dairy.models.admin import ApiChangePassword
from Dairy.data.data import Sessions


def get_data_for_page(page: str, current_user, request):
    if page == 'add_student_key':
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
        teachers = get_teachers(current_user.email)
        groups = get_groups(current_user.email)
        subjects = get_subjects(current_user.email)
        classes = get_classes(current_user.email)
        availability = check_school_in_db(current_user.email)
        return {"request": request, "number": current_user.email, "availability": availability,
                "subjects": sorted(subjects, key=lambda x: x.name),
                "teachers": sorted(teachers, key=lambda x: x.surname), "groups": groups,
                "classes": classes}
    elif page == 'add_subject':
        subjects = get_subjects(current_user.email)
        return {"request": request, "subjects": subjects}
    elif page == 'manage_groups':
        classes = get_classes(current_user.email)
        groups = get_groups(current_user.email)
        days_titles = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        return {"request": request, "classes": sorted(classes, key=lambda x: x['subject']), "groups": groups,
                "days": days_titles}
    else:
        return {"request": request}


def change_user_password(email, body: ApiChangePassword):
    with Sessions() as session:
        user = get_user_by_email(email=email, type=body.type)
        if not verify_password(plain_password=body.old_password, hashed_password=user.password):
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Old password is not correct')
        user.password = get_password_hash(body.new_password)
        session.add(user)
        session.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Password changed')
