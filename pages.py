import os
from abc import abstractmethod, ABC
from typing import Optional

from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from Diary.crud_models import CRUDAdapter
from Diary.data.data import Sessions
from Diary.func.helpers import verify_user_type
from pyowm import OWM

clss = CRUDAdapter().clss
templates = Jinja2Templates(directory="views/templates")
owm = OWM(os.getenv('OWM_KEY'))
mgr = owm.weather_manager()

class ApiPage(BaseModel):
    school_id: Optional[int]
    type: Optional[str]
    page: Optional[str]
    day_i: Optional[int]
    lesson_i: Optional[int]
    user_id: Optional[int]
    group_id: Optional[int]


class PageBase(ABC):
    USERTYPE = None
    FILE_NAME = None

    @abstractmethod
    def export(self, body: ApiPage, request, current_user):
        raise NotImplementedError


class AddStudentKeyPage(PageBase):
    USERTYPE = 'admin'
    FILE_NAME = 'add_student_key.html'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        groups = clss['group'].get_groups(self, body)
        keys = clss['studentkey'].get_student_keys(self, body)
        data = {"request": request, "groups": groups, "keys": keys}
        return templates.TemplateResponse(f'{self.USERTYPE}/{self.FILE_NAME}', data)


class ExportStudentKeysPage(PageBase):
    USERTYPE = 'admin'
    FILE_NAME = 'export_student_keys.html'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        keys_for_export = clss['student'].get_student_keys_for_export(self, body)
        data = {"request": request, "keys_for_export": keys_for_export}
        return templates.TemplateResponse(f'{self.USERTYPE}/{self.FILE_NAME}', data)


class AddGroupPage(PageBase):
    USERTYPE = 'admin'
    FILE_NAME = 'add_group.html'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        groups = clss['group'].get_groups(self, body)
        data = {"request": request, "groups": groups}
        return templates.TemplateResponse(f'{self.USERTYPE}/{self.FILE_NAME}', data)


class AddTeacherKey(PageBase):
    USERTYPE = 'admin'
    FILE_NAME = 'add_teacher_key.html'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        keys = clss['teacherkey'].get_teacher_keys(self, body)
        data = {"request": request, "keys": keys}
        return templates.TemplateResponse(f'{self.USERTYPE}/{self.FILE_NAME}', data)


class SchoolPage(PageBase):
    USERTYPE = 'admin'
    FILE_NAME = 'school.html'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        teachers = clss['teacher']().get_teachers(body)
        groups = clss['group']().get_groups(body)
        subjects = clss['subject']().get_subjects(body)
        classes = clss['cls']().get(body)
        availability = clss['school'].get(self, body)
        data = {"request": request, "number": clss['school'].school_name(clss['admin']().get(body).school_id),
                "availability": availability,
                "subjects": sorted(subjects, key=lambda x: x.name),
                "teachers": sorted(teachers, key=lambda x: x.surname), "groups": groups,
                "classes": classes}
        return templates.TemplateResponse(f'{self.USERTYPE}/{self.FILE_NAME}', data)


class AddSubjectPage(PageBase):
    USERTYPE = 'admin'
    FILE_NAME = 'add_subject.html'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        subjects = clss['subject'].get_subjects(self, body)
        data = {"request": request, "subjects": subjects}
        return templates.TemplateResponse(f'{self.USERTYPE}/{self.FILE_NAME}', data)


class ManageGroups(PageBase):
    USERTYPE = 'admin'
    FILE_NAME = 'manage_groups.html'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        classes = clss['cls']().get(body)
        groups = clss['group']().get_groups(body)
        days_titles = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        data = {"request": request, "classes": sorted(classes, key=lambda x: x['subject']), "groups": groups,
                "days": days_titles}
        return templates.TemplateResponse(f'{self.USERTYPE}/{self.FILE_NAME}', data)


class ExportTeacherKeys(PageBase):
    USERTYPE = 'admin'
    FILE_NAME = 'export_teacher_keys.html'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        keys = clss['teacherkey'].get_teacher_keys(self, body)
        availability = len(keys) > 0
        data = {"request": request, "availability": availability}
        return templates.TemplateResponse(f'{self.USERTYPE}/{self.FILE_NAME}', data)


class SchoolLinkPage(PageBase):
    USERTYPE = 'admin'
    FILE_NAME = 'school_link.html'

    def export(self, body: ApiPage, request, current_user):
        link = clss['admin'].check_link(self, body.user_id)
        data = {"request": request, 'link': link,
                "number": clss['school'].school_name(clss['admin']().get(body).school_id)}
        return templates.TemplateResponse(f'{self.USERTYPE}/{self.FILE_NAME}', data)


class MyDairy(PageBase):
    USERTYPE = 'student'
    FILE_NAME = 'my_diary.html'

    def export(self, body: ApiPage, request, current_user):
        school_city = clss['school'].get_city(self, id=clss['group'].get(self, id=current_user.group_id).school_db_id)
        try:
            weather = mgr.weather_at_place(school_city).weather.detailed_status
        except:
            weather = 'none'
        print(weather)
        data = {"request": request, "number": clss['school'].school_name(clss['admin']().get(body).school_id),
                'weather': weather}
        return templates.TemplateResponse(f'{self.USERTYPE}/{self.FILE_NAME}', data)


class TeacherClassesPage(PageBase):
    USERTYPE = 'teacher'
    FILE_NAME = 'classes.html'

    def export(self, body: ApiPage, request, current_user):
        classes = clss['cls'].for_teacher(current_user.id)
        data = {"request": request, 'classes_data': classes}
        return templates.TemplateResponse(f'{self.USERTYPE}/{self.FILE_NAME}', data)


class AdminInfoPage(PageBase):
    USERTYPE = 'admin'
    FILE_NAME = 'profile_info.html'

    def export(self, body: ApiPage, request, current_user):
        profile_info = {
            'email': current_user.email,
            'school': clss['school'].school_name(current_user.school_id)
        }
        data = {"request": request, 'info': profile_info}
        return templates.TemplateResponse(f'{self.USERTYPE}/{self.FILE_NAME}', data)


class TeacherInfoPage(PageBase):
    USERTYPE = 'teacher'
    FILE_NAME = 'profile_info.html'

    def export(self, body: ApiPage, request, current_user):
        profile_info = {
            'name': current_user.name,
            'surname': current_user.surname,
            'email': current_user.email,
            'school': clss['school'].school_name(current_user.school_db_id)
        }
        data = {"request": request, 'info': profile_info}
        return templates.TemplateResponse(f'{self.USERTYPE}/{self.FILE_NAME}', data)


class StudentInfoPage(PageBase):
    USERTYPE = 'student'
    FILE_NAME = 'profile_info.html'

    def export(self, body: ApiPage, request, current_user):
        profile_info = {
            'name': current_user.name,
            'surname': current_user.surname,
            'email': current_user.email,
            'school': current_user.school_id,
            'group': clss['group']().get(current_user.group_id).name
        }
        data = {"request": request, 'info': profile_info}
        return templates.TemplateResponse(f'{self.USERTYPE}/{self.FILE_NAME}', data)


class PagesAdapter:
    _pages = {'add_student_key': AddStudentKeyPage,
              'export_student_keys': ExportStudentKeysPage,
              'export_teacher_keys': ExportTeacherKeys,
              'add_group': AddGroupPage,
              'add_teacher_key': AddTeacherKey,
              'school': SchoolPage,
              'add_subject': AddSubjectPage,
              'manage_groups': ManageGroups,
              'school_link': SchoolLinkPage,
              'my_dairy': MyDairy,
              'classes': TeacherClassesPage,
              'admin_profile_info': AdminInfoPage,
              'teacher_profile_info': TeacherInfoPage,
              'student_profile_info': StudentInfoPage}

    @property
    def pages(self):
        return self._pages
