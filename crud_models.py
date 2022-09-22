import collections
from random import randint
from re import S
from typing import Optional

import psycopg2

from pydantic.dataclasses import dataclass
from db_models import DBHomework

from data.data import Sessions, symbols, DB_NAME, USERNAME, DB_HOST, DB_PASS
from fastapi.responses import JSONResponse
from fastapi import status
from abc import abstractmethod, ABC

from db_models import DBAdmin, DBTeacherKey, DBKey, DBGroup, DBStudent, DBSchool, DBTeacher, DBSubject, \
    DBClassesRelationship, DBScheduleClass, DBMark
from func.helpers import teaching_days_dates, check_date, get_title, get_day_index_from_date, get_current_time, \
    alert_on_telegram, get_seasons_info, get_current_season, eight_days
from logic.auth import get_password_hash
from contextlib import closing


@dataclass
class ApiBase:
    def __init__(self, email: str = None,
                 password: str = None,
                 old_password: str = None,
                 new_password: str = None,
                 type: str = None,
                 new_email: str = None,
                 value: str = None,
                 group_id: int = None,
                 subject_id: int = None,
                 teacher_id: int = None,
                 group: str = None,
                 day_number: int = None,
                 name: str = None,
                 surname: str = None,
                 city: str = None,
                 key: str = None,
                 school_id: int = None,
                 user_id: int = None,
                 lesson_number: int = None,
                 lesson_id: int = None,
                 id: int = None,
                 student_id: int = None,
                 date: str = None,
                 mark: int = None,
                 comment: str = None,
                 season: str = None,
                 class_id: int = None,
                 exec_time: int = None,
                 *args, **kwargs):
        self.email = email
        self.old_password = old_password
        self.new_password = new_password
        self.password = password
        self.type = type
        self.new_email = new_email
        self.value = value
        self.group_id = group_id
        self.subject_id = subject_id
        self.teacher_id = teacher_id
        self.group = group
        self.day_number = day_number
        self.name = name
        self.surname = surname
        self.city = city
        self.key = key
        self.school_id = school_id
        self.user_id = user_id
        self.lesson_number = lesson_number
        self.lesson_id = lesson_id
        self.id = id
        self.student_id = student_id
        self.date = date
        self.mark = mark
        self.comment = comment
        self.season = season
        self.class_id = class_id
        self.exec_time = exec_time

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
    id: Optional[int]
    date: Optional[str]
    mark: Optional[int]
    student_id: Optional[int]
    comment: Optional[str]
    season: Optional[int]
    class_id: Optional[int]
    exec_time: Optional[int]


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
                        school_id=School.school_name(Admin().get(body).school_id))
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
            keys = session.query(DBKey).filter_by(school_id=School.school_name(Admin().get(body).school_id)).all()
            return keys

    def get_student_keys_for_export(self, body: ApiBase):
        with Sessions() as session:
            keys_for_export = session.query(DBKey).filter_by(
                school_id=School.school_name(Admin().get(body).school_id)).all()
            return set([key.group for key in keys_for_export])

    @staticmethod
    def delete(id: int):
        with Sessions() as session:
            key = session.query(DBKey).filter_by(id=id).first()
            session.delete(key)
            session.commit()


class TeacherKey(KeyBase):

    def add_key(self, body: ApiBase):
        with Sessions() as session:
            value = ''.join([symbols[randint(0, 61)] for _ in range(8)])
            key = DBTeacherKey(value=value, name=body.name.capitalize(), surname=body.surname.capitalize(),
                               school_id=School.school_name(Admin().get(body).school_id))
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
                school_id=School.school_name(Admin().get(body).school_id)).all()
            return keys

    @staticmethod
    def delete(id: int):
        with Sessions() as session:
            key = session.query(DBTeacherKey).filter_by(id=id).first()
            session.delete(key)
            session.commit()


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

    @staticmethod
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
            if key is None:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Wrong key')
            group = session.query(DBGroup).filter_by(name=key.group).first()
            if not session.query(DBStudent).filter_by(email=body.email).first() is None:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT, content='Name already in use')
            password = get_password_hash(body.password)
            student = DBStudent(email=body.email, password=password, name=key.name,
                                surname=key.surname, school_id=key.school_id, group=key.group)
            group.students.append(student)
            session.add(group)
            session.commit()
            self.delete_key(body)

        with closing(psycopg2.connect(dbname=DB_NAME, user=USERNAME,
                                      password=DB_PASS, host=DB_HOST)) as conn:
            with conn.cursor() as cursor:
                login = body.email
                diary_id = self.get(ApiBase(email=body.email)).id
                cursor.execute(f'insert into users (login, password, diary_id) values (%s, %s, %s);',
                               (login, password, diary_id))
                conn.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='Student created')

    def get(self, body: ApiBase):
        with Sessions() as session:
            return session.query(DBStudent).filter_by(email=body.email).first()

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

    @staticmethod
    def get(id: int):
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
        with Sessions() as session:
            subject = session.query(DBSubject).filter_by(id=id).first()
            session.delete(subject)
            session.commit()


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

    @staticmethod
    def school_name(school_id: int):
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
        return JSONResponse(status_code=status.HTTP_200_OK, content='deleted')

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

    @staticmethod
    def for_teacher(teacher_id: int):
        with Sessions() as session:
            res = []
            classes_ids = [cls.id for cls in
                           session.query(DBClassesRelationship).filter_by(teacher_id=teacher_id).all()]
            for day_i in range(5):
                day_data = {'day_name': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'][day_i],
                            'lessons_count': 0, 'last_lesson_number': 0, 'lessons': []}
                for lesson_i in range(10):
                    lesson_found = False
                    for class_id in classes_ids:
                        cls = session.query(DBScheduleClass).filter_by(day_number=day_i,
                                                                       class_number=lesson_i,
                                                                       class_id=class_id).first()
                        if cls is not None:
                            lesson_found = True
                            day_data['lessons_count'] += 1
                            day_data['last_lesson_number'] = lesson_i + 1
                            db_cls = session.query(DBClassesRelationship).filter_by(id=class_id).first()
                            group_name = Group().get(db_cls.group_id).name
                            subject_name = Subject().get(db_cls.subject_id)
                            class_data = {'subject_name': subject_name, 'group_name': group_name,
                                          'group_id': db_cls.group_id, 'lesson_number': lesson_i + 1,
                                          'class_id': class_id}
                            day_data['lessons'].append(class_data)
                        if lesson_found:
                            break
                    if not lesson_found:
                        day_data['lessons'].append({'lesson_number': lesson_i + 1})
                        pass
                res.append(day_data)
            return res

    @staticmethod
    def get_classes_for_final_marks(teacher_id: int):
        with Sessions() as session:
            res = []
            classes_ids = session.query(DBClassesRelationship).filter_by(teacher_id=teacher_id).all()
            for cls in classes_ids:
                res.append({'id': cls.id, 'name': Group().get(cls.group_id).name,
                            'subject': Subject.get(cls.subject_id), 'group_id': cls.group_id})
            return res

    @staticmethod
    def get_teacher_classes_days(class_id: int):
        with Sessions() as session:
            res = []
            for day_i in range(5):
                classes = session.query(DBScheduleClass).filter_by(day_number=day_i, class_id=class_id).all()
                for cls in classes:
                    if cls is not None:
                        res.append(day_i)
            return res

    @staticmethod
    def get_one(id: int):
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
                    db_cls = Cls.get_one(cls.class_id)
                    name = Subject().get(db_cls.subject_id)
                    teacher = Teacher().get(db_cls.teacher_id)
                    day.append({'name': name.capitalize(), 'teacher': teacher.capitalize(), 'class_id': db_cls.id})
                data.append(day)
        return data


    @staticmethod
    def get_eight_teacher_working_days(class_id):
        with Sessions() as session:
            res = []
            for day_i in range(5):
                classes = session.query(DBScheduleClass).filter_by(day_number=day_i, class_id=class_id).all()
                for cls in classes:
                    if cls is not None:
                        res.append(day_i)
            return eight_days(res)
            



class Book:

    @staticmethod
    def make_class(group_id: int, class_id: int):
        with Sessions() as session:
            res = {}
            group = session.query(DBGroup).filter_by(id=group_id).first()
            if group is not None:
                dates = teaching_days_dates(Cls.get_teacher_classes_days(class_id))
                subject = Subject().get(Cls.get_one(class_id).subject_id)
                res.update({'name': group.name, 'subject': subject, 'current_season': get_current_season(),
                            'students_count': 0, 'dates': dates, 'students': [],
                            'hw': []})
                try:
                    res['students_count'] = len(group.students)
                    students = sorted(group.students, key=lambda x: x.surname)
                    for number, student in enumerate(students):
                        marks, summ, count = Mark.get_student_marks(get_current_season(), class_id, student.id)
                        res['students'].append(
                            {'id': student.id, 'number': number + 1, 'name': student.name, 'surname': student.surname,
                             'marks': {'all': marks, 'summ': summ, 'count': count}})
                except KeyError:
                    pass
            else:
                res = {'no group with this id'}
        return res

    @staticmethod
    def make_day(date: str, current_user: DBStudent):
        day = {
            'has_classes': check_date(date),
            'title': get_title(date),
            'classes': [],
        }
        with Sessions() as session:
            group = session.query(DBGroup).filter_by(id=current_user.group_id).first()
            day_i = get_day_index_from_date(date)
            schedule_classes = session.query(DBScheduleClass).filter_by(group_id=group.id, day_number=day_i).all()
            schedule_classes = sorted(schedule_classes, key=lambda x: x.class_number)
            for cls in schedule_classes:
                db_cls = Cls.get_one(cls.class_id)
                number = cls.class_number + 1
                teacher = Teacher().get(db_cls.teacher_id)
                subject = Subject.get(db_cls.subject_id)
                hw = Homework().get(ApiBase(date=date, class_id=db_cls.id))
                mark = Mark().get(ApiBase(date=date, subject_id=db_cls.id, student_id=current_user.id))
                if mark is not None:
                    mark = mark.value
                else:
                    mark = ''
                mark_time = Mark.time(ApiBase(date=date, subject_id=db_cls.id, student_id=current_user.id))
                day['classes'].append(
                    {'number': number, 'teacher': teacher, 'subject': subject, 'hw': hw, 'mark': mark,
                     'mark_time': mark_time})
        return day

    @staticmethod
    def get_final(class_id: int):
        with Sessions() as session:
            cls = Cls.get_one(class_id)
            group = session.query(DBGroup).filter_by(id=cls.group_id).first()
            res = {'class_id': class_id, 'name': group.name, 'subject': Subject.get(cls.subject_id), 'students': []}
            students = group.students
            for number, student in enumerate(sorted(students, key=lambda x: x.surname)):
                season_1_final = Mark.get_final_mark(student.id, class_id, 1)
                season_2_final = Mark.get_final_mark(student.id, class_id, 2)
                season_3_final = Mark.get_final_mark(student.id, class_id, 3)
                season_4_final = Mark.get_final_mark(student.id, class_id, 4)
                season_1_avg, season_1_warning = Mark.get_student_avg_and_warning(student.id, class_id, 1)
                season_2_avg, season_2_warning = Mark.get_student_avg_and_warning(student.id, class_id, 2)
                season_3_avg, season_3_warning = Mark.get_student_avg_and_warning(student.id, class_id, 3)
                all_seasons = [season_1_avg, season_2_avg, season_3_avg]
                season_4_avg = sum(all_seasons) / (3 - all_seasons.count(0) if (3 - all_seasons.count(0)) > 0 else 1)
                student_data = {'id': student.id,
                                'number': number + 1,
                                'initials': f'{student.surname} {student.name}',
                                'season_1_final': season_1_final,
                                'season_1_avg': season_1_avg,
                                'season_2_final': season_2_final,
                                'season_2_avg': season_2_avg,
                                'season_3_final': season_3_final,
                                'season_3_avg': season_3_avg,
                                'season_4_final': season_4_final,
                                'season_4_avg': season_4_avg,
                                'season_1_warning': season_1_warning,
                                'season_2_warning': season_2_warning,
                                'season_3_warning': season_3_warning, }
                res['students'].append(student_data)
        return res

    @staticmethod
    def student_hw(student_id):
        with Sessions() as session:
            student: DBStudent = session.query(DBStudent).filter_by(id=student_id).first()
            group: DBGroup = Group().get(student.group_id)
            session.add(group)
            hw_query = group.homework.all()
            result: dict[DBHomework] = {}
            for dct in hw_query:
                result.setdefault(dct.class_date, []).append(dct)
            for index in result:
                hw_on_date = []
                for hw in result[index]:
                    subject = Subject.get(Cls.get_one(hw.class_id).subject_id)
                    hw_dict = {'body': hw.body, 'exec_time': hw.exec_time, 'made': hw.time, 'subject': subject}
                    hw_on_date.append(hw_dict)
                result[index] = hw_on_date
            result = collections.OrderedDict(sorted(result.items()))
            print(result)
            print(*result, sep='\n')
        return result


class Mark(CRUDBase):

    def create(self, body: ApiBase):
        with Sessions() as session:
            mark = session.query(DBMark).filter_by(date=body.date, student_id=body.student_id,
                                                   class_id=body.subject_id).first()
            if mark is not None:
                mark.value = body.mark
                session.add(mark)
                session.commit()
                return JSONResponse(status_code=status.HTTP_200_OK, content='mark updated')
            mark = DBMark(date=body.date, value=body.mark, student_id=body.student_id, class_id=body.subject_id,
                          time=get_current_time(), comment=body.comment, season=body.season, final=False)
            session.add(mark)
            session.commit()
            data = {'time': mark.time, 'body': f'New mark, <b>{mark.value}</b>', 'date': mark.date,
                    'comment': mark.comment}
        alert_on_telegram(body.student_id, data, 'mark')
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='mark added successfully')

    @staticmethod
    def create_final_mark(body: ApiBase):
        with Sessions() as session:
            mark = session.query(DBMark).filter_by(student_id=body.student_id,
                                                   class_id=body.subject_id, final=True, season=body.season).first()
            if mark is not None:
                mark.value = body.mark
                session.add(mark)
                session.commit()
                return JSONResponse(status_code=status.HTTP_200_OK, content='mark updated')
            mark = DBMark(value=body.mark, student_id=body.student_id, class_id=body.subject_id,
                          time=get_current_time(), comment='', season=body.season, final=True)
            session.add(mark)
            session.commit()
            data = {'time': mark.time,
                    'body': f'New final mark, <b>{mark.value}</b>\nSeason: {mark.season if mark.season != 4 else "year"}',
                    'date': mark.date,
                    'comment': mark.comment}
        alert_on_telegram(body.student_id, data, 'mark')
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='mark added successfully')

    def get(self, body: ApiBase):
        with Sessions() as session:
            mark = session.query(DBMark).filter_by(student_id=body.student_id, date=body.date,
                                                   class_id=body.subject_id).first()
            return mark

    @staticmethod
    def delete(id: int):
        with Sessions() as session:
            mark = session.query(DBMark).filter_by(id=id).first()
            session.delete(mark)
            session.commit()
            return JSONResponse(status_code=status.HTTP_200_OK, content='mark deleted')

    @staticmethod
    def get_student_marks(season: int, subject_id: int, student_id: int):
        marks = {}
        summ = 0
        with Sessions() as session:
            marks_query = session.query(DBMark).filter_by(student_id=student_id, season=season,
                                                          class_id=subject_id).all()
            count = len(marks_query)
            for mark in marks_query:
                summ += mark.value
                marks.update({mark.date: {'value': mark.value, 'id': mark.id}})
        return marks, summ, count

    @staticmethod
    def time(body: ApiBase):
        with Sessions() as session:
            mark = session.query(DBMark).filter_by(student_id=body.student_id, date=body.date,
                                                   class_id=body.subject_id).first()
            return mark.time if mark is not None else ''

    def get_marks_list(self, student_id: int):
        seasons_info = get_seasons_info()
        data = {
            'current_season': seasons_info['current'],
            'seasons_dates': seasons_info['dates']
        }
        with Sessions() as session:
            marks_query = session.query(DBMark).filter_by(student_id=student_id)
            cls_ids = set([mark.class_id for mark in marks_query.all()])
            subjects = []
            for c_id in cls_ids:
                name = Subject.get(session.query(DBClassesRelationship).filter_by(id=c_id).first().subject_id)
                seasons = self.get_marks_by_seasons(student_id=student_id, class_id=c_id)
                final_mark = self.get_final_mark(student_id=student_id, class_id=c_id, season=4)
                subject = {'name': name, 'seasons': seasons, 'final': final_mark}
                subjects.append(subject)
        subjects = sorted(subjects, key=lambda x: x['name'])
        data.update({'subjects': subjects})
        return data

    @staticmethod
    def get_final_mark(student_id: int, class_id: int, season: int):
        with Sessions() as session:
            mark = session.query(DBMark).filter_by(student_id=student_id, class_id=class_id, final=True,
                                                   season=season).first()
            return mark.value if mark is not None else ''

    def get_marks_by_seasons(self, student_id: int, class_id: int):
        with Sessions() as session:
            data = {}
            for season in range(1, get_current_season() + 1):
                marks = session.query(DBMark).filter_by(final=False, season=season, student_id=student_id,
                                                        class_id=class_id).all()
                sum = 0
                k = 0
                for i in range(len(marks)):
                    sum += marks[i].value
                    k += 1
                    marks[i] = {'value': marks[i].value, 'comment': marks[i].comment, 'time': marks[i].time,
                                'date': marks[i].date}
                data.update({season: {'marks': marks, 'avg': "{:.2f}".format(sum / (1 if k == 0 else k)),
                                      'season_final': self.get_final_mark(student_id, class_id, season)}})
        return data

    @staticmethod
    def get_student_avg_and_warning(student_id: int, class_id: int, season: int):
        with Sessions() as session:
            marks = session.query(DBMark).filter_by(final=False, season=season, student_id=student_id,
                                                    class_id=class_id).all()
            sum = 0
            k = 0
            for mark in marks:
                sum += mark.value
                k += 1
        avg = float("{:.2f}".format(sum / (1 if k == 0 else k)))
        warning = ''
        if season <= get_current_season():
            if k < 3:
                warning = f'This student has only {k} marks\nMinimum required for attestation is 3'
            elif avg < 2.6:
                warning = f'Avg score {avg} is too low\nMinimum required for attestation is 2.6'
        return avg, warning


class Homework(CRUDBase):

    def create(self, body: ApiBase):
        with Sessions() as session:
            print(body.class_id)
            group: DBGroup = Group().get(body.group_id)
            session.add(group)
            hw: DBHomework = group.homework.filter_by(db_group_id=body.group_id, class_date=body.date, class_id=body.class_id).first()
            if hw is not None:
                hw.time = get_current_time()
                hw.body = body.value
                hw.exec_time = body.exec_time
                session.add(hw)
                session.commit()    
                return JSONResponse(status_code=status.HTTP_200_OK, content='hw edited')
            hw = DBHomework(class_date=body.date, time=get_current_time(), body=body.value, exec_time=body.exec_time, 
                            class_id=body.class_id)
            group.homework.append(hw)
            session.add(group)
            session.commit()
            data = {'time': hw.time, 'body': f'New homework, <b>{hw.body}</b>', 'date': hw.time,
                    'comment': ''}
            [alert_on_telegram(student.id, data, 'hw') for student in group.students]
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='homework created')

    def get(self, body: ApiBase):
        with Sessions() as session:
            hw: DBHomework = session.query(DBHomework).filter_by(class_id=body.class_id, class_date=body.date).first()
            if hw is not None:
                return {'body': hw.body, 'exec_time': hw.exec_time, 'made': hw.time}
            else:
                return {'body': None, 'exec_time': None, 'made': None}

    def delete(id: int):
        with Sessions() as session:
            hw = session.query(DBHomework).filter_by(id=id).first()
            session.delete(hw)
            session.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content='hw deleted')

 
    @staticmethod
    def group_hw(class_id: int):
        with Sessions() as session:
            homework: list[DBHomework] = session.query(DBHomework).filter_by(class_id=class_id).all()
            homework = sorted(homework, key=lambda x: x.class_date, reverse=True)
        return homework


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
             'scheduleclass': ScheduleClass,
             'book': Book,
             'mark': Mark,
             'homework': Homework}

    @property
    def clss(self):
        return self._clss
