from Dairy.models.admin import ApiAdmin, Admin
from Dairy.data.data import Sessions
from Dairy.logic.auth import get_password_hash
from fastapi.responses import JSONResponse
from fastapi import status


def create_new_admin(admin: ApiAdmin):
    with Sessions() as session:
        if not session.query(Admin).filter_by(email=admin.email).first() is None:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Name already in use')
        admin = Admin(email=admin.email, password=get_password_hash(admin.password))
        session.add(admin)
        session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content='Admin created')
