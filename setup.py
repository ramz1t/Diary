from Dairy.models.school import ApiSchool
from models.admin import ApiAdmin
from logic.admin import create_new_admin

admin = ApiAdmin(email='1534', password='admin')
create_new_admin(admin)
