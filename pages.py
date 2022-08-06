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


class PageBase(ABC):
    USERTYPE = None

    @abstractmethod
    def export(self, body: ApiPage, request, current_user):
        raise NotImplementedError


class AddStudentKeyPage(PageBase):
    USERTYPE = 'admin'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        groups = clss['group'].get_groups(self, body)
        keys = clss['studentkey'].get_student_keys(self, body)
        data = {"request": request, "groups": groups, "keys": keys}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class ExportStudentKeysPage(PageBase):
    USERTYPE = 'admin'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        keys_for_export = clss['student'].get_student_keys_for_export(self, body)
        data = {"request": request, "keys_for_export": keys_for_export}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class AddGroupPage(PageBase):
    USERTYPE = 'admin'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        groups = clss['group'].get_groups(self, body)
        data = {"request": request, "groups": groups}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class AddTeacherKey(PageBase):
    USERTYPE = 'admin'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        keys = clss['teacherkey'].get_teacher_keys(self, body)
        data = {"request": request, "keys": keys}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class SchoolPage(PageBase):
    USERTYPE = 'admin'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        teachers = clss['teacher'].get_teachers(self, body)
        groups = clss['group'].get_groups(self, body)
        subjects = clss['subject'].get_subjects(self, body)
        classes = clss['cls'].get(self, body)
        availability = clss['school'].get(self, body)
        data = {"request": request, "number": clss['school']().school_name(clss['admin']().get(body).school_id),
                "availability": availability,
                "subjects": sorted(subjects, key=lambda x: x.name),
                "teachers": sorted(teachers, key=lambda x: x.surname), "groups": groups,
                "classes": classes}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class AddSubjectPage(PageBase):
    USERTYPE = 'admin'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        subjects = clss['subject'].get_subjects(self, body)
        data = {"request": request, "subjects": subjects}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class ManageGroups(PageBase):
    USERTYPE = 'admin'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        classes = clss['cls'].get(self, body)
        groups = clss['group'].get_groups(self, body)
        days_titles = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        data = {"request": request, "classes": sorted(classes, key=lambda x: x['subject']), "groups": groups,
                "days": days_titles}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class ExportTeacherKeys(PageBase):
    USERTYPE = 'admin'

    def export(self, body: ApiPage, request, current_user):
        if not verify_user_type(usertype=self.USERTYPE, request=request):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content='No access to this page with this account type')
        keys = clss['teacherkey'].get_teacher_keys(self, body)
        availability = len(keys) > 0
        data = {"request": request, "availability": availability}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class SchoolLinkPage(PageBase):
    USERTYPE = 'admin'

    def export(self, body: ApiPage, request, current_user):
        link = clss['admin'].check_link(self, body.user_id)
        data = {"request": request, 'link': link,
                "number": clss['school']().school_name(clss['admin']().get(body).school_id)}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class MyDairy(PageBase):
    USERTYPE = 'student'

    def export(self, body: ApiPage, request, current_user):
        school_city = clss['school'].get_city(self, id=clss['group'].get(self, id=current_user.group_id).school_db_id)
        try:
            weather = mgr.weather_at_place(school_city).weather.detailed_status
        except:
            weather = 'none'
        print(weather)
        data = {"request": request, "number": clss['school']().school_name(clss['admin']().get(body).school_id),
                'weather': weather}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


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
              'my_dairy': MyDairy}

    @property
    def pages(self):
        return self._pages
