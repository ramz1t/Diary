from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from data.data import Base
from sqlalchemy.orm import relationship


class School(Base):
    __tablename__ = 'schools'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    groups = relationship('Group')
    #subjects = relationship(subjects)


class ApiSchool(BaseModel):
    city: str
