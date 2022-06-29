from fastapi.responses import JSONResponse
from fastapi import status
from Dairy.data.data import Sessions
from Dairy.models.classes_rel import ApiClass, ClassesRelationship
from Dairy.models.school import School


def add_class_to_db(body: ApiClass, school_id: int):
    with Sessions() as session:
        cls = ClassesRelationship(group_id=body.group_id, subject_id=body.subject_id, teacher_id=body.teacher_id)
        school = session.query(School).filter_by(name=school_id).first()
        school.classes.append(cls)
        session.add(school)
        session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content='class created')
