from Dairy.models.admin import Admin
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
