from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from Dairy.data.data import Base


class Group(Base):
    __tablename__ = 'groups'
    name = Column(String, primary_key=True)
    # students: relationship(Student)
    # tasks: relationship(Task)
    # teacher: relationship - back(Teacher)


class ApiGroup(BaseModel):
    name: str
