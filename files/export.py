from crud_models import Admin, ApiBase, School
from data.data import Sessions
from db_models import DBKey, DBTeacherKey


def write_student_keys(group: str, admin_id: int):
    school_id = Admin().get(ApiBase(user_id=admin_id)).school_id
    with Sessions() as session:
        keys = session.query(DBKey).filter_by(group=group, school_id=school_id).all()
    with open(f'files/{group}.txt', 'w') as file:
        file.write(group + '\n')
        for key in keys:
            file.write(f'{key.value} - {key.surname} {key.name}\n')


def write_teacher_keys(admin_id: int):
    school_id = Admin().get(ApiBase(user_id=admin_id)).school_id
    school_name = School().school_name(school_id)
    with Sessions() as session:
        keys = session.query(DBTeacherKey).filter_by(school_id=school_id).all()
    with open('files/teachers.txt', 'w') as file:
        file.write(f'Teachers in {school_name}\n')
        for key in keys:
            file.write(f'{key.value} - {key.surname} {key.name}\n')
