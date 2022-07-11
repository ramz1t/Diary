from random import randint
from typing import Optional, Union

from pydantic import BaseModel

from Dairy.data.data import Sessions, symbols
from fastapi.responses import JSONResponse
from fastapi import status
from abc import abstractmethod, ABC

from Dairy.db_models import DBAdmin, DBTeacherKey, DBKey, DBGroup, DBStudent, DBSchool, DBTeacher, DBSubject
from Dairy.logic.auth import get_password_hash


class ApiBase(BaseModel):
    email: Optional[str]
    password: Optional[str]
    old_password: Optional[str]
    new_password: Optional[str]
    type: Optional[str]
    new_email: Optional[str]
    value: Optional[str]
    group_id: Optional[int]
    subject_id: Optional[int]
    teacher_id: Optional[int]
    group: Optional[str]
    day_number: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    city: Optional[str]
    key: Optional[str]
    school_id: Optional[int]


class KeyBase(ABC):

    @abstractmethod
    def add_key(self, body: ApiBase):
        raise NotImplementedError

    @abstractmethod
    def get_key(self, body: ApiBase):
        raise NotImplementedError

    @abstractmethod
    def delete_key(self, body: ApiBase):
        raise NotImplementedError


class StudentKey(KeyBase):

    def add_key(self, body: ApiBase):
        with Sessions() as session:
            value = ''.join([symbols[randint(0, 61)] for _ in range(8)])
            key = DBKey(value=value, name=body.name, surname=body.surname, group=body.group,
                        school_id=body.school_id)
            session.add(key)
            session.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Key created successfully')

    def get_key(self, body: ApiBase):
        with Sessions() as session:
            key = session.query(DBKey).filter_by(value=body.value).first()
            return key

    def delete_key(self, body: ApiBase):
        with Sessions() as session:
            key = session.query(DBKey).filter_by(value=body.value).first()
            session.delete(key)
            session.commit()

    def get_student_keys(self, body: ApiBase):
        with Sessions() as session:
            keys = session.query(DBKey).filter_by(school_id=body.school_id).all()
            return keys

    def get_student_keys_for_export(self, body: ApiBase):
        with Sessions() as session:
            keys_for_export = session.query(DBKey).filter_by(school_id=body.school_id).all()
            return set([key.group for key in keys_for_export])


class TeacherKey(KeyBase):

    def add_key(self, body: ApiBase):
        with Sessions() as session:
            value = ''.join([symbols[randint(0, 61)] for _ in range(8)])
            key = DBTeacherKey(value=value, name=body.name, surname=body.surname,
                               school_id=body.school_id)
            session.add(key)
            session.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Key created successfully')

    def get_key(self, body: ApiBase):
        with Sessions() as session:
            key = session.query(DBTeacherKey).filter_by(value=body.value).first()
            return key

    def delete_key(self, body: ApiBase):
        with Sessions() as session:
            key = session.query(DBTeacherKey).filter_by(value=body.value).first()
            session.delete(key)
            session.commit()

    def get_teacher_keys(self, body: ApiBase):
        with Sessions() as session:
            keys = session.query(DBTeacherKey).filter_by(school_id=body.school_id).all()
            return keys


class CRUDBase(ABC):

    @abstractmethod
    def create(self, body: ApiBase):
        raise NotImplementedError

    @abstractmethod
    def get(self, body: ApiBase):
        raise NotImplementedError

    @abstractmethod
    def delete(self, body: ApiBase):
        raise NotImplementedError


class Admin(CRUDBase):

    def create(self, body: ApiBase):
        with Sessions() as session:
            if not session.query(Admin).filter_by(email=body.email).first() is None:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Name already in use')
            admin = DBAdmin(email=body.email, password=get_password_hash(body.password))
            session.add(admin)
            session.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Admin created')

    def get(self, body: ApiBase):
        pass

    def delete(self, body: ApiBase):
        return 'admin deleted' + body.email


class Student(CRUDBase, StudentKey):

    def create(self, body: ApiBase):
        with Sessions() as session:
            key = self.get_key(body)
            group = session.query(DBGroup).filter_by(name=body.group).first()
            if key is None:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Wrong key')
            if not session.query(DBStudent).filter_by(email=body.email).first() is None:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Name already in use')
            student = DBStudent(email=body.email, password=get_password_hash(body.password), name=body.name,
                                surname=body.surname, school_id=body.school_id, group=body.group)
            group.students.append(student)
            session.add(group)
            session.commit()
            self.delete_key(body)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Student created')

    def get(self, body: ApiBase):
        pass

    def delete(self, body: ApiBase):
        return 'student deleted'


class Teacher(CRUDBase, TeacherKey):

    def create(self, body: ApiBase):
        with Sessions() as session:
            key = self.get_key(body)
            if key is None:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Wrong key')
            if not session.query(Teacher).filter_by(email=body.email).first() is None:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Name already in use')
            teacher = DBTeacher(email=body.email, password=get_password_hash(body.password), name=body.name,
                                surname=body.surname, school_id=body.school_id)
            school = session.query(DBSchool).filter_by(name=body.school_id).first()
            school.teachers.append(teacher)
            session.add(school)
            session.commit()
            self.delete_key(body)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Teacher created')

    def get(self, body: ApiBase):
        pass

    def delete(self, body: ApiBase):
        return 'teacher deleted'


class Subject(CRUDBase):

    def create(self, body: ApiBase):
        with Sessions() as session:
            if session.query(DBSubject).filter_by(name=body.name).first() is not None:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Subject already in db')
            subject = DBSubject(name=body.name, type=body.type)
            school = session.query(DBSchool).filter_by(name=body.school_id).first()
            school.subjects.append(subject)
            session.add(school)
            session.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Subject added')

    def get(self, body: ApiBase):
        pass

    def get_subjects(self, body: ApiBase):
        with Sessions() as session:
            school = session.query(DBSchool).filter_by(name=body.school_id).first()
            try:
                return school.subjects
            except AttributeError:
                return []

    def delete(self, body: ApiBase):
        pass


class Adapter:

    _clss = {'student': Student,
             'admin': Admin,
             'teacher': Teacher,
             'subject': Subject,
             'studentkey': StudentKey,
             'teacherkey': TeacherKey}

    @property
    def clss(self):
        return self._clss