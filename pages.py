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


class PagesAdapter:

    _pages = {'add_student_key': AddStudentKeyPage}

    @property
    def pages(self):
        return self._pages
