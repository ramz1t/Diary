from Dairy.crud_models import ApiBase, CRUDAdapter

adapter = CRUDAdapter()

type = input('Choose model\n')
if type.lower() == 'admin':
    admin = ApiBase(email=input('email: '), password=input('password: '))
    adapter.clss['admin']().create(admin)
elif type.lower() == 'school':
    school = ApiBase(name=input('name: '), city=input('city: '))
    adapter.clss['school']().create(school)
else:
    print('incorrect model name')
