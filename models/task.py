from sqlalchemy import Column, Integer, String, DateTime
from pydantic import BaseModel
from data.data import Base


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    body = Column(String)
    time = Column(DateTime(timezone=True))  # idk about timezone

    # group: relationship - back(Group)
    # teacher: relationship - back(Teacher)


class Task(BaseModel):
    id: int
    body: str
    # idk how i need to tell about time
