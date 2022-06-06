from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from data.data import Base


class Mark(Base):
    __tablename__ = 'marks'
    id = Column(Integer, primary_key=True)
    value = Column(Integer)
    # student: relationship-back(User)


class ApiMark(BaseModel):
    id: int
    value: int
