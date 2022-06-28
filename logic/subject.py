from Dairy.models.school import School
from Dairy.models.subject import Subject, ApiSubject
from Dairy.data.data import Sessions
from fastapi.responses import JSONResponse
from fastapi import status


def add_new_subject(subject: ApiSubject, school_id: int):
    with Sessions() as session:
        if session.query(Subject).filter_by(name=subject.name).first() is not None:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Subject already in db')
        subject = Subject(name=subject.name, type=subject.type)
        school = session.query(School).filter_by(name=school_id).first()
        school.subjects.append(subject)
        session.add(school)
        session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content='Subject added')


def get_subjects(school_id: int):
    with Sessions() as session:
        school = session.query(School).filter_by(name=school_id).first()
        try:
            return school.subjects
        except AttributeError:
            return []
