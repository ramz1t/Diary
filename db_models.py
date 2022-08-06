from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from data.data import Base


class DBKey(Base):
    __tablename__ = 'keys'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    value = Column(String)
    name = Column(String)
    surname = Column(String)
    group = Column(String)
    school_id = Column(Integer)


class DBTeacherKey(Base):
    __tablename__ = 'teacher_keys'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    school_id = Column(Integer)
    value = Column(String)


class DBAdmin(Base):
    __tablename__ = 'admins'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    school_id = Column(Integer)


class DBClassesRelationship(Base):
    __tablename__ = 'classes'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer)
    subject_id = Column(Integer)
    teacher_id = Column(Integer)
    school_db_id = Column(Integer, ForeignKey('schools.id'))


class DBScheduleClass(Base):
    __tablename__ = 'scheduleclasses'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    class_number = Column(Integer)
    day_number = Column(Integer)
    class_id = Column(Integer)
    group_id = Column(Integer, ForeignKey('groups.id'))


class DBGroup(Base):
    __tablename__ = 'groups'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    students = relationship("DBStudent")
    school_db_id = Column(Integer, ForeignKey('schools.id'))
    classes = relationship("DBScheduleClass", lazy='dynamic')
    # tasks: relationship(Task)


class DBSchool(Base):
    __tablename__ = 'schools'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    groups = relationship('DBGroup')
    subjects = relationship('DBSubject')
    teachers = relationship('DBTeacher')
    classes = relationship('DBClassesRelationship')


class DBStudent(Base):
    __tablename__ = 'students'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    email = Column(String)
    school_id = Column(Integer)
    group = Column(String)
    group_id = Column(Integer, ForeignKey("groups.id"))
    # marks = relationship(Mark)


class DBSubject(Base):
    __tablename__ = 'subjects'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    school_db_id = Column(Integer, ForeignKey('schools.id'))


class DBTeacher(Base):
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
