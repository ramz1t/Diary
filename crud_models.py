from random import randint
from typing import Optional, Union

from pydantic import BaseModel

from Diary.data.data import Sessions, symbols
from fastapi.responses import JSONResponse
from fastapi import status
from abc import abstractmethod, ABC

from Diary.db_models import DBAdmin, DBTeacherKey, DBKey, DBGroup, DBStudent, DBSchool, DBTeacher, DBSubject, \
    DBClassesRelationship, DBScheduleClass
from Diary.logic.auth import get_password_hash
import re


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
    day_number: Optional[int]
    name: Optional[str]
    surname: Optional[str]
    city: Optional[str]
    key: Optional[str]
    school_id: Optional[int]
    user_id: Optional[int]
    lesson_number: Optional[int]
    lesson_id: Optional[int]


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
            name = ' '.join([name.capitalize() for name in body.name.split()])
            surname = ' '.join([surname.capitalize() for surname in body.surname.split()])
            key = DBKey(value=value, name=name, surname=surname, group=body.group,
                        school_id=School().school_name(Admin().get(body).school_id))
            session.add(key)
            session.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Key created successfully')

    def get_key(self, body: ApiBase):
        with Sessions() as session:
            key = session.query(DBKey).filter_by(value=body.key).first()
            return key

    def delete_key(self, body: ApiBase):
        with Sessions() as session:
            key = session.query(DBKey).filter_by(value=body.key).first()
            session.delete(key)
            session.commit()

    def get_student_keys(self, body: ApiBase):
        with Sessions() as session:
            keys = session.query(DBKey).filter_by(school_id=School().school_name(Admin().get(body).school_id)).all()
            return keys

    def get_student_keys_for_export(self, body: ApiBase):
        with Sessions() as session:
            keys_for_export = session.query(DBKey).filter_by(
                school_id=School().school_name(Admin().get(body).school_id)).all()
            return set([key.group for key in keys_for_export])


class TeacherKey(KeyBase):

    def add_key(self, body: ApiBase):
        with Sessions() as session:
            value = ''.join([symbols[randint(0, 61)] for _ in range(8)])
            key = DBTeacherKey(value=value, name=body.name.capitalize(), surname=body.surname.capitalize(),
                               school_id=School().school_name(Admin().get(body).school_id))
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
            keys = session.query(DBTeacherKey).filter_by(
                school_id=School().school_name(Admin().get(body).school_id)).all()
            return keys


class CRUDBase(ABC):

    @abstractmethod
    def create(self, body: ApiBase):
        raise NotImplementedError

    @abstractmethod
    def get(self, body: ApiBase):
        raise NotImplementedError

    @staticmethod
    def delete(id: int):
        raise NotImplementedError


class Admin(CRUDBase):

    def create(self, body: ApiBase):
        with Sessions() as session:
            if not session.query(DBAdmin).filter_by(email=body.email).first() is None:
                print('name already in use')
                return
            admin = DBAdmin(email=body.email, password=get_password_hash(body.password))
            session.add(admin)
            session.commit()
            print('admin created')

    def get(self, body: ApiBase):
        with Sessions() as session:
            return session.query(DBAdmin).filter_by(id=body.user_id).first()

    def delete(id: int):
        pass

    def link_school(self, body: ApiBase):
        with Sessions() as session:
            admin = self.get(body)
            if admin is None:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='school or profile not found')
            admin.school_id = body.school_id
            session.add(admin)
            session.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content=f'profile linked to school')

    def check_link(self, user_id) -> bool:
        with Sessions() as session:
            return session.query(DBAdmin).filter_by(id=user_id).first().school_id is not None


class Student(CRUDBase, StudentKey):

    def create(self, body: ApiBase):
        with Sessions() as session:
            key = self.get_key(body)
            group = session.query(DBGroup).filter_by(name=key.group).first()
            if key is None:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Wrong key')
            if not session.query(DBStudent).filter_by(email=body.email).first() is None:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Name already in use')
            student = DBStudent(email=body.email, password=get_password_hash(body.password), name=key.name,
                                surname=key.surname, school_id=key.school_id, group=key.group)
            group.students.append(student)
            session.add(group)
            session.commit()
            self.delete_key(body)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Student created')

    def get(self, body: ApiBase):
        pass

    @staticmethod
    def delete(id: int):
        pass


class Teacher(CRUDBase, TeacherKey):

    def create(self, body: ApiBase):
        with Sessions() as session:
            key = self.get_key(body)
            if key is None:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Wrong key')
            if not session.query(Teacher).filter_by(email=body.email).first() is None:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Name already in use')
            teacher = DBTeacher(email=body.email, password=get_password_hash(body.password), name=key.name,
                                surname=key.surname, school_id=key.school_id)
            school = session.query(DBSchool).filter_by(id=Admin().get(body).school_id).first()
            school.teachers.append(teacher)
            session.add(school)
            session.commit()
            self.delete_key(body)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Teacher created')

    def get(self, id: int):
        with Sessions() as session:
            teacher = session.query(DBTeacher).filter_by(id=id).first()
            return teacher.surname + ' ' + teacher.name

    @staticmethod
    def delete(id: int):
        pass

    def get_teachers(self, body: ApiBase):
        with Sessions() as session:
            school = session.query(DBSchool).filter_by(id=Admin().get(body).school_id).first()
            try:
                return school.teachers
            except AttributeError:
                return []


class Subject(CRUDBase):

    def create(self, body: ApiBase):
        with Sessions() as session:
            if session.query(DBSubject).filter_by(name=body.name).first() is not None:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Subject already in db')
            subject = DBSubject(name=body.name, type=body.type)
            school = session.query(DBSchool).filter_by(id=Admin().get(body).school_id).first()
            school.subjects.append(subject)
            session.add(school)
            session.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Subject added')

    def get(self, id: int):
        with Sessions() as session:
            return session.query(DBSubject).filter_by(id=id).first().name

    def get_subjects(self, body: ApiBase):
        with Sessions() as session:
            school = session.query(DBSchool).filter_by(id=Admin().get(body).school_id).first()
            try:
                return school.subjects
            except AttributeError:
                return []

    @staticmethod
    def delete(id: int):
        pass


class School(CRUDBase):

    def create(self, body: ApiBase):
        with Sessions() as session:
            if session.query(DBSchool).filter_by(name=body.name, city=body.city.capitalize()).first() is not None:
                print('school already in db')
                return
            school = DBSchool(name=body.name, city=body.city.capitalize())
            session.add(school)
            session.commit()
        print('school created')
        return

    def get(self, body: ApiBase):
        with Sessions() as session:
            return session.query(DBSchool).filter_by(id=Admin().get(body).school_id).first() is not None

    def school_name(self, school_id: int):
        with Sessions() as session:
            school = session.query(DBSchool).filter_by(id=school_id).first()
            if school is not None:
                return school.name
            return

    def get_city(self, id: int):
        with Sessions() as session:
            school = session.query(DBSchool).filter_by(id=id).first()
            if school is not None:
                return school.city
            return

    @staticmethod
    def delete(id: int):
        pass

    def find(self, body: ApiBase):
        with Sessions() as session:
            school = session.query(DBSchool).filter_by(name=body.name, city=body.city.capitalize()).first()
            school_info = ['No school found']
            if school is not None:
                school_info = [school.name, school.city, school.id]
            return school_info


class Group(CRUDBase):

    def create(self, body: ApiBase):
        with Sessions() as session:
            if not session.query(DBGroup).filter_by(name=body.name,
                                                    school_db_id=Admin().get(body).school_id).first() is None:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Group already exists')
            group = DBGroup(name=body.name)
            school = session.query(DBSchool).filter_by(id=Admin().get(body).school_id).first()
            school.groups.append(group)
            session.add(school)
            session.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Group created successfully')

    def get(self, id: int):
        with Sessions() as session:
            return session.query(DBGroup).filter_by(id=id).first()

    @staticmethod
    def delete(id: int):
        with Sessions() as session:
            group = session.query(DBGroup).filter_by(id=id).first()
            classes = session.query(DBClassesRelationship).filter_by(group_id=group.id).all()
            for cls in classes:
                Cls().delete(cls.id)
            session.delete(group)
            session.commit()

    def get_groups(self, body: ApiBase):
        with Sessions() as session:
            school = session.query(DBSchool).filter_by(id=Admin().get(body).school_id).first()
            try:
                groups = school.groups
                data = []
                for group in groups:
                    data.append({'id': group.id, 'name': group.name, 'student_count': len(group.students)})
                return data
            except AttributeError:
                return []

    def upgrade(self, body: ApiBase):
        with Sessions() as session:
            school = session.query(DBSchool).filter_by(id=Admin().get(body).school_id).first()
            for group in school.groups:
                for index, letter in enumerate(group.name, 0):
                    if letter.isalpha():
                        res = [group.name[:index], group.name[index:]]
                num = int(res[0]) + 1
                if num > 11:
                    self.delete(group.id)
                else:
                    group.name = ''.join((str(num), res[1]))
                    print(group.name)
                    session.add(group)
                    session.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content='upgraded')


class Cls(CRUDBase):

    def create(self, body: ApiBase):
        with Sessions() as session:
            cls = DBClassesRelationship(group_id=body.group_id, subject_id=body.subject_id, teacher_id=body.teacher_id)
            school = session.query(DBSchool).filter_by(id=Admin().get(body).school_id).first()
            school.classes.append(cls)
            session.add(school)
            session.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='class created')

    def make_result(self, classes, session):
        result = []
        for cls in classes:
            print(cls.group_id)
            group = session.query(DBGroup).filter_by(id=cls.group_id).first()
            subject = session.query(DBSubject).filter_by(id=cls.subject_id).first()
            teacher = session.query(DBTeacher).filter_by(id=cls.teacher_id).first()
            result.append({"id": cls.id,
                           "group": group.name,
                           "subject": subject.name,
                           "teacher": f'{teacher.surname} {teacher.name}',
                           "subject_id": cls.subject_id})
        return result

    def get(self, body: ApiBase):
        with Sessions() as session:
            school = session.query(DBSchool).filter_by(id=Admin().get(body).school_id).first()
            classes = school.classes
            return self.make_result(classes, session)

    def for_schedule(self, body: ApiBase):
        with Sessions() as session:
            school = session.query(DBSchool).filter_by(id=Admin().get(body).school_id).first()
            classes = school.classes.filter_by(group_id=body.group_id).all()
            return self.make_result(classes, session)

    def get_one(self, id: int):
        with Sessions() as session:
            return session.query(DBClassesRelationship).filter_by(id=id).first()

    @staticmethod
    def delete(id: int):
        with Sessions() as session:
            cls = session.query(DBClassesRelationship).filter_by(id=id).first()
            session.delete(cls)
            session.commit()


class ScheduleClass(CRUDBase):

    def create(self, body: ApiBase):
        with Sessions() as session:
            if session.query(DBScheduleClass).filter_by(day_number=body.day_number, class_number=body.lesson_number,
                                                        group_id=body.group_id).first() is None:
                schedule_class = DBScheduleClass(day_number=body.day_number, class_number=body.lesson_number,
                                                 group_id=body.group_id, class_id=body.lesson_id)
            else:
                schedule_class = session.query(DBScheduleClass).filter_by(day_number=body.day_number,
                                                                          class_number=body.lesson_number,
                                                                          group_id=body.group_id).first()
                schedule_class.class_id = body.lesson_id
            session.add(schedule_class)
            session.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='added')

    def get(self, body: ApiBase):
        pass

    def delete(self, body: ApiBase):
        with Sessions() as session:
            schedule_class = session.query(DBScheduleClass).filter_by(day_number=body.day_number,
                                                                      class_number=body.lesson_number,
                                                                      group_id=body.group_id).first()
            session.delete(schedule_class)
            session.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content='deleted')

    def get_schedule(self, group_id: int):
        with Sessions() as session:
            group = session.query(DBGroup).filter_by(id=group_id).first()
            data = []
            for day_i in range(5):
                today_classes = group.classes.filter_by(day_number=day_i).all()
                day = []
                for lesson_i in range(len(set([cls.class_number for cls in today_classes]))):
                    cls = session.query(DBScheduleClass).filter_by(day_number=day_i, class_number=lesson_i,
                                                                   group_id=group_id).first()
                    db_cls = Cls().get_one(cls.class_id)
                    name = Subject().get(db_cls.subject_id)
                    teacher = Teacher().get(db_cls.teacher_id)
                    day.append({'name': name.capitalize(), 'teacher': teacher.capitalize(), 'class_id': db_cls.id})
                data.append(day)
        return data


class CRUDAdapter:
    _clss = {'student': Student,
             'admin': Admin,
             'teacher': Teacher,
             'subject': Subject,
             'studentkey': StudentKey,
             'teacherkey': TeacherKey,
             'school': School,
             'group': Group,
             'cls': Cls,
             'scheduleclass': ScheduleClass}

    @property
    def clss(self):
        return self._clss
