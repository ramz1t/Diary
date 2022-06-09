from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from data.data import Base


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    email = Column(String)
    school_id = Column(Integer)
    # marks = relationship(Mark)


class ApiStudent(BaseModel):
    id: int
    name: str
    surname: str
    password: str
    email: str
    school_id: int
