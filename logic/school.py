from fastapi.responses import JSONResponse
from fastapi import status

from Dairy.crud_models import ApiBase
from Dairy.data.data import Sessions
from Dairy.db_models import DBSchool


def add_new_school(school: ApiBase, school_id: int) -> JSONResponse:
    with Sessions() as session:
        if session.query(DBSchool).filter_by(name=school_id).first() is not None:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='School already created')
        school = DBSchool(name=school_id, city=school.city)
        session.add(school)
        session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content='School created')


def check_school_in_db(name: str) -> bool:
    with Sessions() as session:
        return session.query(DBSchool).filter_by(name=name).first() is not None
