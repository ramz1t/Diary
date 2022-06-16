from fastapi.responses import JSONResponse
from fastapi import status
from Dairy.data.data import Sessions
from Dairy.models.key import Key, ApiKey
from random import randint
import string


symbols = string.digits + string.ascii_letters


def get_key(value: str):
    with Sessions() as session:
        key = session.query(Key).filter_by(value=value).first()
        return key


def add_new_key(key: ApiKey, school_id: int):
    with Sessions() as session:
        value = ''.join([symbols[randint(0, 61)] for _ in range(8)])
        key = Key(value=value, name=key.name, surname=key.surname,
                  group=key.group, school_id=school_id)
        session.add(key)
        session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content='Key created successfully')


def delete_key(value: str):
    with Sessions() as session:
        key = session.query(Key).filter_by(value=value).first()
        session.delete(key)
        session.commit()


def get_keys(school_id: int):
    with Sessions() as session:
        keys = session.query(Key).filter_by(school_id=school_id).all()
        return keys


def get_keys_for_export(school_id: int):
    with Sessions() as session:
        keys_for_export = session.query(Key).filter_by(school_id=school_id).all()
        return set([key.group for key in keys_for_export])
