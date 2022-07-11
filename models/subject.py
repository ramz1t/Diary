from sqlalchemy import Column, Integer, String, ForeignKey
from pydantic import BaseModel
from data.data import Base
from sqlalchemy.orm import relationship


class Subject(Base):
    __tablename__ = 'subjects'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    school_db_id = Column(Integer, ForeignKey('schools.id'))


class ApiSubject(BaseModel):
    name: str
    type: str
