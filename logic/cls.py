from fastapi.responses import JSONResponse
from fastapi import status
from Dairy.data.data import Sessions
from Dairy.db_models import DBSchool
from Dairy.models.classes_rel import ApiClass, ClassesRelationship
from Dairy.models.group import Group
from Dairy.models.subject import Subject
from Dairy.models.teacher import Teacher


def add_class_to_db(body: ApiClass, school_id: int):
    with Sessions() as session:
        cls = ClassesRelationship(group_id=body.group_id, subject_id=body.subject_id, teacher_id=body.teacher_id)
        school = session.query(DBSchool).filter_by(name=school_id).first()
        school.classes.append(cls)
        session.add(school)
        session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content='class created')


def get_classes(school_id: int):
    with Sessions() as session:
        school = session.query(School).filter_by(name=school_id).first()
        classes = school.classes
        result = []
        for cls in classes:
            group = session.query(Group).filter_by(id=cls.group_id).first()
            subject = session.query(Subject).filter_by(id=cls.subject_id).first()
            teacher = session.query(Teacher).filter_by(id=cls.teacher_id).first()
            result.append({"id": cls.id,
                           "group": group.name,
                           "subject": subject.name,
                           "teacher": f'{teacher.surname} {teacher.name}'})
        return result
