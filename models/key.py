from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from data.data import Base


class Key(Base):
    __tablename__ = 'keys'
    id = Column(Integer, primary_key=True)
    value = Column(String)
    name = Column(String)
    surname = Column(String)
    group = Column(String)


class ApiKey(BaseModel):
    value: str
    name: str
    surname: str
    group: str
