import datetime
import os
from contextlib import closing

import psycopg2
import requests
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt, JWTError
from starlette import status
from starlette.responses import JSONResponse
from datetime import date

from Diary.db_models import TelegramAuthorization
from Diary.func.db_user_find import get_user_by_email
from Diary.logic.auth import SECRET_KEY, ALGORITHM
# from Dairy.models.admin import ApiChangePassword, ApiChangeEmail
from Diary.data.data import Sessions, YEAR_END, YEAR_START, TODAY, DB_NAME, USERNAME, DB_HOST, DB_PASS

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
    while current_day < TODAY + datetime.timedelta(days=110):
        if current_day >= YEAR_START:
            for index in days_indexes:
                if index == current_day.weekday():
                    dates.append({'long': current_day.strftime("%Y-%m-%d"), 'short': current_day.strftime('%d')})
        current_day += datetime.timedelta(days=1)
    return dates


def get_day_index_from_date(date: str):
    date = make_datetime_from_str(date)
    return date.weekday()


def get_current_time():
    return datetime.datetime.now().strftime("%d/%m/%y %H:%M")


def check_telegram(student_id):
    with closing(psycopg2.connect(dbname=DB_NAME, user=USERNAME,
                                  password=DB_PASS, host=DB_HOST)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM users WHERE diary_id = %s', (student_id,))
            user = cursor.fetchone()
            if user is None:
                return False
    return user[4]


def check_permitions(student_id):
    with Sessions() as session:
        telegram_permitions = session.query(TelegramAuthorization).filter_by(diary_id=student_id).first()
        if telegram_permitions is None:
            session.add(TelegramAuthorization(diary_id=student_id, hw=False, mark=False))
            return False, False
        else:
            return telegram_permitions.mark, telegram_permitions.hw


def alert_on_telegram(student_id, data, type):
    # mark_permition, hw_permition = check_permitions(student_id)
    mark_permition, hw_permition = True, True
    if mark_permition or hw_permition:
        load_dotenv()
        bot_token = os.getenv('TELEGRAM_BOT_KEY')
        chat_id = check_telegram(student_id)
        message = f'⚠ Diary alert ⚠\n{data["body"]}\n<b>Time:</b> {data["time"]}\n<b>Class date:</b> {data["date"]}'
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=html'
        if (type == 'mark' and mark_permition) or (type == 'hw' and hw_permition):
            requests.get(url)
