from Diary.data.data import Sessions
from Diary.db_models import DBKey, DBTeacherKey


def write_student_keys(group: str, school_id: int):
    with Sessions() as session:
        keys = session.query(DBKey).filter_by(group=group, school_id=school_id).all()
    with open(f'files/{group}.txt', 'w') as file:
        file.write(group + '\n')
        for key in keys:
            file.write(f'{key.value} - {key.surname} {key.name}\n')


def write_teacher_keys(school_id: int):
    with Sessions() as session:
        keys = session.query(DBTeacherKey).filter_by(school_id=school_id).all()
    with open('files/teachers.txt', 'w') as file:
        file.write(f'Teachers in {school_id}\n')
        for key in keys:
            file.write(f'{key.value} - {key.surname} {key.name}\n')
