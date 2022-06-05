from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from data.data import Base


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    login = Column(String)
    school_id = Column(Integer)
    subject = Column(String)
    # classes: relationship(Group)


class Teacher(BaseModel):
    id: int
    name: str
    password: str
    login: str
    school_id: int
    subject: str
