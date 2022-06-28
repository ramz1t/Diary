from Dairy.models.group import Group, ApiGroup
from Dairy.data.data import Sessions
from Dairy.models.school import School
from fastapi.responses import JSONResponse
from fastapi import status


def add_new_group(group: ApiGroup, school_id: int):
    with Sessions() as session:
        if not session.query(Group).filter_by(name=group.name, school_id=school_id).first() is None:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Group already exists')
        group = Group(name=group.name, school_id=school_id)
        school = session.query(School).filter_by(name=school_id).first()
        school.groups.append(group)
        session.add(school)
        session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content='Group created successfully')


def get_groups(school_id: int):
    with Sessions() as session:
        school = session.query(School).filter_by(name=school_id).first()
        try:
            return school.groups
        except AttributeError:
            return []


def get_all_students_from_group(group: str):
    with Sessions() as session:
        group = session.query(Group).filter_by(name=group).first()
        return group.students
