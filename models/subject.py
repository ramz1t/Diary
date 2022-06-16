from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from data.data import Base
from sqlalchemy.orm import relationship


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)


class ApiSubject(BaseModel):
    name: str
    type: str
