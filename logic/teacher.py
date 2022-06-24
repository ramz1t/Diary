from Dairy.models.teacher import ApiTeacher, Teacher
from Dairy.data.data import Sessions
from fastapi.responses import JSONResponse
from fastapi import status
from Dairy.logic.auth import get_password_hash
from Dairy.logic.key import get_teacher_key, delete_teacher_key


def create_new_teacher(teacher: ApiTeacher):
    with Sessions() as session:
        key = get_teacher_key(teacher.key)
        if key is None:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Wrong key')
        if not session.query(Teacher).filter_by(email=teacher.email).first() is None:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Name already in use')
        teacher = Teacher(email=teacher.email, password=get_password_hash(teacher.password), name=key.name,
                          surname=key.surname, school_id=key.school_id)
        session.add(teacher)
        session.commit()
        delete_teacher_key(key.value)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content='Teacher created')
