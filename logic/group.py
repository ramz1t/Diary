from Dairy.models.group import Group, ApiGroup
from Dairy.data.data import Sessions
from fastapi.responses import JSONResponse
from fastapi import status


def add_new_group(group: ApiGroup):
    with Sessions() as session:
        if not session.query(Group).filter_by(name=group.name).first() is None:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Group already exists')
        group = Group(name=group.name)
        session.add(group)
        session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content='Group created successfully')
