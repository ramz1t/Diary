from Dairy.data.data import Sessions
from Dairy.db_models import DBAdmin, DBStudent, DBTeacher


def get_user_by_email(email: str, type: str):
    if type == 'admin':
        with Sessions() as session:
            return session.query(DBAdmin).filter_by(email=email).first()
    elif type == 'student':
        with Sessions() as session:
            return session.query(DBStudent).filter_by(email=email).first()
    elif type == 'teacher':
        with Sessions() as session:
            return session.query(DBTeacher).filter_by(email=email).first()
