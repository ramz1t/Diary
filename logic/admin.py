from models.admin import ApiAdmin, Admin
from data.data import Sessions
from fastapi.responses import JSONResponse
from fastapi import status
from logic.auth import get_password_hash
from logic.auth import verify_password


def create_new_admin(admin: ApiAdmin):
    with Sessions() as session:
        if not session.query(Admin).filter_by(email=admin.email).first() is None:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Name already in use')
        admin = Admin(email=admin.email, password=get_password_hash(admin.password))
        session.add(admin)
        session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content='Admin created')


def change_admin_password(email, old_password, new_password):
    with Sessions() as session:
        admin = session.query(Admin).filter_by(email=email).first()
        if not verify_password(plain_password=old_password, hashed_password=admin.password):
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Password missmatch')
        admin.password = get_password_hash(new_password)
        session.add(admin)
        session.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Successfully')
