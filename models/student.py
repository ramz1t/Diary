from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from data.data import Base


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    login = Column(String)
    school_id = Column(Integer)
    # marks = relationship(Mark)


class ApiStudent(BaseModel):
    id: int
    name: str
    password: str
    login: str
    school_id: int
