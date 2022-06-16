from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from data.data import Base


class Key(Base):
    __tablename__ = 'keys'
    id = Column(Integer, primary_key=True)
    value = Column(String)
    name = Column(String)
    surname = Column(String)
    group = Column(String)
    school_id = Column(Integer)


class TeacherKey(Base):
    __tablename__ = 'teacher_keys'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    school_id = Column(Integer)
    value = Column(String)


class ApiKey(BaseModel):
    name: str
    surname: str
    group: str


class ApiTeacherKey(BaseModel):
    name: str
    surname: str
