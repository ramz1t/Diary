from Dairy.models.student import ApiStudent, Student
from Dairy.data.data import Sessions
from fastapi.responses import JSONResponse
from fastapi import status
from Dairy.logic.auth import get_password_hash
from Dairy.logic.key import get_key


def create_new_student(student: ApiStudent):
    with Sessions() as session:
        key = get_key(student.key)
        if key is None:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Wrong key')
        if not session.query(Student).filter_by(email=student.email).first() is None:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Name already in use')
        student = Student(email=student.email, password=get_password_hash(student.password), name=key.name,
                          surname=key.surname, school_id=key.school_id, group=key.group)
        session.add(student)
        session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content='Student created')
