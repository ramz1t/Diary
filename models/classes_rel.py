from sqlalchemy import Column, Integer, String, ForeignKey
from pydantic import BaseModel
from data.data import Base


class ClassesRelationship(Base):
    __tablename__ = 'classes'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer)
    subject_id = Column(Integer)
    teacher_id = Column(Integer)
    school_db_id = Column(Integer, ForeignKey('schools.id'))


class ApiClass(BaseModel):
    group_id: int
    subject_id: int
    teacher_id: int
