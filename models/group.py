from sqlalchemy import Column, Integer, String, ForeignKey
from pydantic import BaseModel
from data.data import Base
from sqlalchemy.orm import relationship


class Group(Base):
    __tablename__ = 'groups'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    school_id = Column(Integer)
    students = relationship("Student")
    school_db_id = Column(Integer, ForeignKey('schools.id'))
    #classes = relationship("Day")
    # tasks: relationship(Task)


class ApiGroup(BaseModel):
    name: str
