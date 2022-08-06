from fastapi import HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt, JWTError
from starlette import status
from starlette.responses import JSONResponse

from func.db_user_find import get_user_by_email
from logic.auth import verify_password, get_password_hash, SECRET_KEY, ALGORITHM

# from models.admin import ApiChangePassword, ApiChangeEmail
from data.data import Sessions


# def change_user_password(email, body: ApiChangePassword):
#     with Sessions() as session:
#         user = get_user_by_email(email=email, type=body.type)
#         if not verify_password(plain_password=body.old_password, hashed_password=user.password):
#             return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Old password is not correct')
#         user.password = get_password_hash(body.new_password)
#         session.add(user)
#         session.commit()
#         return JSONResponse(status_code=status.HTTP_201_CREATED, content='Password changed')
#
#
# def change_user_email(body: ApiChangeEmail):
#     with Sessions() as session:
#         user = get_user_by_email(email=body.email, type=body.type)
#         if user.email == body.email:
#             user.email = body.new_email
#             session.add(user)
#             session.commit()
#             return JSONResponse(status_code=status.HTTP_201_CREATED, content='Successfully')
#         else:
#             return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Old email is not correct')
from Diary.models.token import TokenData


def verify_user_type(usertype, request) -> bool:
    authorization: str = request.cookies.get("access_token")
    scheme, token = get_authorization_scheme_param(authorization)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    token_usertype = payload.get('type')
    return usertype == token_usertype
