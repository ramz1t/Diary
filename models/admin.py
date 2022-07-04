from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from data.data import Base


class Admin(Base):
    __tablename__ = 'admins'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)


class ApiAdmin(BaseModel):
    email: str
    password: str


class ApiChangePassword(BaseModel):
    old_password: str
    new_password: str
    type: str


class ApiChangeEmail(BaseModel):
    type: str
    new_email: str
    email: str
