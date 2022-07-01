from sqlalchemy import Column, Integer, String, ForeignKey
from pydantic import BaseModel
from data.data import Base


class Day(Base):
    __tablename__ = 'days'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    day_number = Column(Integer)
    #classes = relatisonship('ScheduleClass')


class ApiDay(BaseModel):
    group: str
    day_number: str


class ScheduleClass(Base):
    __tablename__ = 'scheduleclasses'
    id = Column(Integer, primary_key=True)
    class_number = Column(Integer)
    class_id = Column(Integer)


class ApiScheduleClass(BaseModel):
    class_number: int
    class_id: int
