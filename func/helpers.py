import datetime
import os
from contextlib import closing
from logic.auth import create_access_token
from logic.auth import get_password_hash, verify_password
from models.token import TokenData
import psycopg2
import requests
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt, JWTError
from starlette import status
from starlette.responses import JSONResponse
from datetime import date, timedelta

from db_models import TelegramAuthorization
from func.db_user_find import get_user_by_email
from logic.auth import SECRET_KEY, ALGORITHM
from models.change import ApiChangePassword, ApiChangeEmail
from data.data import Sessions, YEAR_END, YEAR_START, TODAY, DB_NAME, USERNAME, DB_HOST, DB_PASS, SEASON_1, \
    SEASON_2, SEASON_3

def change_user_password(current_user, body: ApiChangePassword):
    with Sessions() as session:
        if not verify_password(body.new_pass, current_user.password):
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Wrong password')
        current_user.password = get_password_hash(body)
        session.add(current_user)
        session.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Password changed')


def change_user_email(current_user, body: ApiChangeEmail):
    with Sessions() as session:
        session.add(current_user)
        current_user.email = body.new_email
        session.add(current_user)
        session.commit()
        access_token_expires = timedelta(minutes=365 * 24 * 60)
        access_token = create_access_token(
            data={"sub": body.new_email, "type": body.type}, expires_delta=access_token_expires
        )
        response = JSONResponse(status_code=status.HTTP_200_OK, content='updated')
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=False)
    return response


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
    current_season = [SEASON_1, SEASON_2, SEASON_3][get_current_season() - 1]
    current_day = current_season[0] - datetime.timedelta(days=YEAR_START.weekday())
    while current_day < current_season[1]:
        if current_day > current_season[1]:
            break
        if current_day >= current_season[0]:
            for index in days_indexes:
                if index == current_day.weekday():
                    dates.append({'long': current_day.strftime("%Y-%m-%d"), 'short': current_day.strftime('%d')})
        current_day += datetime.timedelta(days=1)
    return dates


def eight_days(days_indexes):
    days_indexes = list(set(days_indexes))
    current_day = datetime.date.today()
    cd_index = current_day.weekday()
    dates = []
    start_index = -1
    for index in days_indexes:
        if index > cd_index:
            current_day = current_day - datetime.timedelta(cd_index) + datetime.timedelta(index)
            start_index = days_indexes.index(index)
            break
    k = 0
    if start_index == -1:
        start_index = 0
        current_day = current_day + datetime.timedelta(days=7 - current_day.weekday() + days_indexes[0])
    while k < 8:
        dates.append({'long': current_day.strftime('%Y-%m-%d'), 
                      'title': f"{current_day.strftime('%d.%m')}, {['Mon', 'Tue', 'Wed', 'Thu', 'Fri'][current_day.weekday()]}"})
        start_index += 1
        if start_index == len(days_indexes):
            start_index -= len(days_indexes)
            current_day += datetime.timedelta(days=7) - datetime.timedelta(current_day.weekday())
        current_day += datetime.timedelta(days=days_indexes[start_index]) - datetime.timedelta(current_day.weekday())
        if current_day > YEAR_END:
            break
        k += 1
    return dates


def get_day_index_from_date(date: str):
    date = make_datetime_from_str(date)
    return date.weekday()


def get_current_time():
    return datetime.datetime.now().strftime("%d/%m/%y %H:%M")


def get_current_season():
    today = datetime.date.today()
    if SEASON_1[0] <= today <= SEASON_1[1]:
        return 1
    elif SEASON_2[0] <= today <= SEASON_2[1]:
        return 2
    elif SEASON_3[0] <= today <= SEASON_3[1]:
        return 3


def check_telegram(student_id):
    with closing(psycopg2.connect(dbname=DB_NAME, user=USERNAME,
                                  password=DB_PASS, host=DB_HOST)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM users WHERE diary_id = %s', (student_id,))
            user = cursor.fetchone()
            if user is None:
                return False
    return user[4]


def check_permissions(student_id):
    with Sessions() as session:
        telegram_permissions = session.query(TelegramAuthorization).filter_by(diary_id=student_id).first()
        if telegram_permissions is None:
            session.add(TelegramAuthorization(diary_id=student_id, hw=False, mark=False))
            session.commit()
            return False, False
        else:
            return telegram_permissions.mark, telegram_permissions.hw


def alert_on_telegram(student_id: int, data: dict, alert_type: str):
    mark_permission, hw_permission = check_permissions(student_id)
    if mark_permission or hw_permission:
        load_dotenv()
        bot_token = os.getenv('TELEGRAM_BOT_KEY')
        chat_id = check_telegram(student_id)
        message = f'⚠ Diary alert ⚠\n{data["body"]}\n<b>Time:</b> {data["time"]}\n<b>Class date:</b> {data["date"]}\n<b>Comment: </b>{data["comment"]}'
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=html'
        if (alert_type == 'mark' and mark_permission) or (alert_type == 'hw' and hw_permission):
            requests.get(url)


def set_permissions(hw: bool, mark: bool, student_id: int):
    with Sessions() as session:
        permissions = session.query(TelegramAuthorization).filter_by(diary_id=student_id).first()
        permissions.hw, permissions.mark = hw, mark
        session.add(permissions)
        session.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content='permissions set')


def get_seasons_info():
    return {'current': get_current_season(),
            'dates': {
                1: f'{SEASON_1[0].strftime("%d.%m.%y")} - {SEASON_1[1].strftime("%d.%m.%y")}',
                2: f'{SEASON_2[0].strftime("%d.%m.%y")} - {SEASON_2[1].strftime("%d.%m.%y")}',
                3: f'{SEASON_3[0].strftime("%d.%m.%y")} - {SEASON_3[1].strftime("%d.%m.%y")}'
            }}
