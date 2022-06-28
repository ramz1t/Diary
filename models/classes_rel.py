from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from data.data import Base


class ClassesRelationship(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer)
    subject_id = Column(Integer)
    teacher_id = Column(Integer)


class ApiClassesRelationship(BaseModel):
    group_id: int
    subject_id: int
    teacher_id: int
