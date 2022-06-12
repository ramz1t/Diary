from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from data.data import Base
from sqlalchemy.orm import relationship


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    school_id = Column(Integer)
    #students = relationship("Student")
    # tasks: relationship(Task)


class ApiGroup(BaseModel):
    name: str
