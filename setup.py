from Dairy.crud_models import ApiBase, CRUDAdapter

admin = ApiBase(email='2222', password='admin')
adapter = CRUDAdapter()
adapter.clss['admin']().create(admin)
