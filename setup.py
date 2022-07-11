from Dairy.crud_models import ApiBase, Adapter

admin = ApiBase(email='2222', password='admin')
adapter = Adapter()
adapter.clss['admin']().create(admin)
