from Dairy.models.admin import Admin
from Dairy.models.key import Key
from Dairy.models.student import Student
from Dairy.models.teacher import Teacher
from Dairy.data.data import Sessions


def get_user_by_email(email: str, type: str):
    if type == 'admin':
        with Sessions() as session:
            return session.query(Admin).filter_by(email=email).first()
    elif type == 'student':
        with Sessions() as session:
            return session.query(Student).filter_by(email=email).first()
    elif type == 'teacher':
        with Sessions() as session:
            return session.query(Teacher).filter_by(email=email).first()


def create_file(group: str, school_id: int):
    with Sessions() as session:
        keys = session.query(Key).filter_by(group=group, school_id=school_id).all()
    with open(f'files/{group}.txt', 'w') as file:
        file.write(group + '\n')
        for key in keys:
            file.write(f'{key.value} - {key.surname} {key.name}\n')
