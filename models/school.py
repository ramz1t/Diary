from sqlalchemy import Column, Integer, String, DateTime
from pydantic import BaseModel
from data.data import Base


class School(Base):
    __tablename__ = 'schools'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    #groups = relationship(groups)
    #subjects = relationship(subjects)


class ApiSchool(BaseModel):
    name: str
    city: str
