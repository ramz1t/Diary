import datetime

from fastapi import HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt, JWTError
from starlette import status
from starlette.responses import JSONResponse
from datetime import date
from Diary.func.db_user_find import get_user_by_email
from Diary.logic.auth import SECRET_KEY, ALGORITHM
# from Dairy.models.admin import ApiChangePassword, ApiChangeEmail
from Diary.data.data import Sessions, YEAR_END, YEAR_START, TODAY

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


def make_datetime_from_str(date: str):
    date = list(map(int, date.split('-')))
    date_c = datetime.date(year=date[0], month=date[1], day=date[2])
    return date_c


def check_date(date: str):
    date = make_datetime_from_str(date)
    return YEAR_START <= date <= YEAR_END


def make_dates_for_week(date, type: str = None):
    if isinstance(date, str):
        date = make_datetime_from_str(date)
        if type == 'next':
            date += datetime.timedelta(days=7)
        elif type == 'back':
            date -= datetime.timedelta(days=7)
    today_i = date.weekday()
    start_day = date - datetime.timedelta(days=today_i)
    dates = []
    for i in range(5):
        date = start_day.strftime('%Y-%m-%d')
        day = start_day.strftime('%d')
        name = ['mon', 'tue', 'wed', 'thu', 'fri'][start_day.weekday()]
        dates.append({'date': date, 'day': day, 'name': name})
        start_day += datetime.timedelta(days=1)
    return dates


def get_title(date):
    date = make_datetime_from_str(date)
    month = \
        ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
         'December'][int(date.strftime('%m')) - 1]
    day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'][date.weekday()]
    num = date.strftime("%d")
    return f'{num if not num.startswith("0") else num[1]}th of {month}, {day}'


def teaching_days_dates(days_indexes):
    dates = []
    current_day = YEAR_START - datetime.timedelta(days=YEAR_START.weekday())
    while current_day < TODAY + datetime.timedelta(days=90):
        if current_day >= YEAR_START:
            for index in days_indexes:
                if index == current_day.weekday():
                    dates.append({'long': current_day.strftime("%Y-%m-%d"), 'short': current_day.strftime('%d')})
        current_day += datetime.timedelta(days=1)
    return dates


