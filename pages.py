from abc import abstractmethod, ABC
from pydantic import BaseModel
from starlette.templating import Jinja2Templates

from Dairy.crud_models import CRUDAdapter

clss = CRUDAdapter().clss
templates = Jinja2Templates(directory="views/templates")


class ApiPage(BaseModel):
    school_id: int
    type: str
    page: str


class PageBase(ABC):

    @abstractmethod
    def export(self, body: ApiPage, request):
        raise NotImplementedError


class AddStudentKeyPage(PageBase):

    def export(self, body: ApiPage, request):
        groups = clss['group'].get_groups(self, body)
        keys = clss['studentkey'].get_student_keys(self, body)
        data = {"request": request, "groups": groups, "keys": keys}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class ExportStudentKeysPage(PageBase):

    def export(self, body: ApiPage, request):
        keys_for_export = clss['student'].get_student_keys_for_export(self, body)
        data = {"request": request, "keys_for_export": keys_for_export}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class AddGroupPage(PageBase):

    def export(self, body: ApiPage, request):
        groups = clss['group'].get_groups(self, body)
        data = {"request": request, "groups": groups}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class AddTeacherKey(PageBase):

    def export(self, body: ApiPage, request):
        keys = clss['teacherkey'].get_teacher_keys(self, body)
        data = {"request": request, "keys": keys}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class SchoolPage(PageBase):

    def export(self, body: ApiPage, request):
        teachers = clss['teacher'].get_teachers(self, body)
        groups = clss['group'].get_groups(self, body)
        subjects = clss['subject'].get_subjects(self, body)
        classes = clss['cls'].get(self, body)
        availability = clss['school'].get(self, body)
        data = {"request": request, "number": body.school_id, "availability": availability,
                "subjects": sorted(subjects, key=lambda x: x.name),
                "teachers": sorted(teachers, key=lambda x: x.surname), "groups": groups,
                "classes": classes}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class AddSubjectPage(PageBase):

    def export(self, body: ApiPage, request):
        subjects = clss['subject'].get_subjects(self, body)
        data = {"request": request, "subjects": subjects}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class ManageGroups(PageBase):

    def export(self, body: ApiPage, request):
        classes = clss['cls'].get(self, body)
        groups = clss['group'].get_groups(self, body)
        days_titles = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        data = {"request": request, "classes": sorted(classes, key=lambda x: x['subject']), "groups": groups,
                "days": days_titles}
        return templates.TemplateResponse(f'{body.type}/{body.page}.html', data)


class PagesAdapter:

    _pages = {'add_student_key': AddStudentKeyPage,
              'export_student_keys': ExportStudentKeysPage,
              'add_group': AddGroupPage,
              'add_teacher_key': AddTeacherKey,
              'school': SchoolPage,
              'add_subject': AddSubjectPage,
              'manage_groups': ManageGroups}

    @property
    def pages(self):
        return self._pages
