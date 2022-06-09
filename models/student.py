from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from Dairy.data.data import Base


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    email = Column(String)
    school_id = Column(Integer)
    group = Column(String)
    # marks = relationship(Mark)


class ApiStudent(BaseModel):
    password: str
    email: str
    key: str
