from models.admin import ApiAdmin
from logic.admin import create_new_admin

admin = ApiAdmin(name='1534', password='admin', id=1)
create_new_admin(admin)
