from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from data.data import Base


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)


class ApiAdmin(BaseModel):
    email: str
    password: str
