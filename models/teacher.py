from sqlalchemy import Column, Integer, String, ForeignKey
from pydantic import BaseModel
from data.data import Base


class Teacher(Base):
    __tablename__ = 'teachers'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    email = Column(String)
    surname = Column(String)
    school_id = Column(Integer)
    school_db_id = Column(Integer, ForeignKey('schools.id'))
    # classes: relationship(Group)


class ApiTeacher(BaseModel):
    password: str
    email: str
    key: str
